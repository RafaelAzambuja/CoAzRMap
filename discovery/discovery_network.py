import time
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from file_handler import ConfigFile
from discovery.discovery_icmp import poll_icmp_active_hosts
from discovery.discovery_snmp import SNMPMgmt
from discovery.discovery_ssh import test_ssh_on_host


class DiscoveryEngine:
    """ Network discovery engine responsible for:

    1. Collecting target subnets from the user
    2. Discovering alive hosts via ICMP
    3. Probing discovered hosts for services (SNMP, SSH, etc.)

    The engine performs ICMP scanning sequentially and service probing
    concurrently using a thread pool.
    """

    def __init__(self, cfg_file: ConfigFile):
        """ Initialize the discovery engine.

        Args:
            cfg_file (ConfigFile): Configuration file handler instance.
                Used to retrieve runtime options (e.g., max_threads).

        Notes:
            The number of worker threads is clamped between 1 and 128.
        """

        self.cfg = cfg_file
        self.max_threads = max(1, min(128, int(self.cfg.read_cfg_file("options", "max_threads"))))

    def _get_subnets_from_user(self) -> list[str]:
        
        """ Prompt the user to enter one or more IPv4 addresses and/or subnets.

        The user is repeatedly prompted until valid input is provided.
        Entries must be whitespace-separated and may be either:

        - IPv4 address (e.g., 192.168.1.10)
        - IPv4 subnet in CIDR notation (e.g., 192.168.1.0/24)

        Example:
            192.168.0.0/24 172.16.230.2 10.23.0.0/16

        Returns:
            list[str]: A list of validated IPv4 networks in CIDR notation.
                       Single IP addresses are normalized to /32 networks.

        Raises:
            No exceptions are propagated. Validation errors are caught
            and the user is prompted again.
        """

        while True:
            subnets_input = input(
                "ONLY IPv4 FOR NOW!! Enter subnets separated by space.\n"
                "Ex: 192.168.0.0/24 172.16.230.2 10.23.0.0/16:\n"
            ).strip()

            try:
                return self.validate_subnets(subnets_input)
            
            except ValueError as e:
                print(f"Error: {e}")

    def validate_subnets(self, ip_address_list: str) -> list[str]:
        
        """ Validate a whitespace-separated string of IPv4 addresses/subnets.

        Each entry may be:
            - A valid IPv4 address
            - A valid IPv4 network in CIDR notation (strict mode)

        Args:
            subnets (str): Whitespace-separated IPv4 addresses or subnets.

        Returns:
            list[str]: Normalized IPv4 networks in CIDR notation.
                       IPv4 addresses are converted to /32 networks.

        Raises:
            ValueError: If any entry is not a valid IPv4 address or subnet.
        """

        result: list[str] = []

        for entry in ip_address_list.split():
            try:
                ipaddress.IPv4Network(entry, strict=True)
                result.append(str(entry))

            except ValueError:
                raise ValueError(f"Invalid IPv4 address or subnet: {entry}")

        return result

    def discover(self, subnets: list[str]) -> dict[str, dict]:
        """ Execute full discovery process.

        Args:
            subnets (list[str]): List of validated IPv4 subnets in CIDR format.

        Returns:
            dict[str, dict]: Dictionary keyed by IP address containing
            discovered service information, for example:

            {
                "192.168.1.10": {
                    "icmp": True,
                    "snmp": {...} | None,
                    "ssh": {...} | None,
                    "http": {...} | None,
                }
            }

        Workflow:
            1. ICMP discovery phase
            2. Service probing phase (if hosts found)
        """

        hosts = self._icmp_phase(subnets)

        if not hosts:
            print("[INFO] No active hosts found.")
            return {}

        self._service_probe_phase(hosts)

        return hosts

    def _icmp_phase(self, subnets: list[str]) -> dict[str, dict]:
        """ Perform ICMP discovery on provided subnets.

        For each subnet:
            - Poll active hosts using ICMP
            - Register alive hosts in result structure

        Args:
            subnets (list[str]): List of IPv4 networks in CIDR notation.

        Returns:
            dict[str, dict]: Dictionary of alive hosts with initialized
            service states.
        """

        hosts: dict[str, dict] = {}
        start = time.perf_counter()

        for subnet in subnets:
            print(f"[INFO] ICMP - Polling active hosts in {subnet}")
            alive_hosts = poll_icmp_active_hosts(subnet, self.cfg)

            for ip in alive_hosts:
                hosts[ip] = {
                    "icmp": True,
                    "snmp": None,
                    "ssh": None,
                    "http": None,
                }

        elapsed = time.perf_counter() - start
        print(f"[DEBUG] Alive hosts in {subnet}: {alive_hosts}")
        print(f"[INFO] ICMP polling took {elapsed:.3f} seconds")

        return hosts

    def _probe_snmp(self, ip: str):
        print(f"[DEBUG] Trying SNMP on {ip}")
        snmp = SNMPMgmt(ip, self.cfg)

        if snmp.connect():
            print(f"[DEBUG] SNMP OK on {ip}")
            return snmp

        print(f"[DEBUG] SNMP FAILED on {ip}")
        return None

    def _service_probe_phase(self, hosts: dict[str, dict]) -> None:
        
        """ Probe discovered hosts for additional services.

        Currently probes:
            - SNMP
            - (SSH placeholder)
            - (HTTP placeholder)

        Service checks are executed concurrently using a thread pool.

        Args:
            hosts (dict[str, dict]): Mutable host dictionary that will
                be updated in-place with detected services.

        Notes:
            - Failures during probing are silently ignored.
            - Execution time is measured and logged.
        """

        print("[INFO] Probing services (SNMP / SSH / HTTP)")
        start = time.perf_counter()

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {}

            for ip in hosts.keys():

                if self.cfg.read_cfg_file("service", "snmp").lower() == "true":
                    futures[
                        executor.submit(self._probe_snmp, ip)
                    ] = ("snmp", ip)

                # Future extensions:
                # SSH
                # futures[
                #     executor.submit(test_ssh_on_host, ip, self.cfg)
                # ] = ("ssh", ip)

                # HTTP
                # futures[
                #     executor.submit(test_http_on_host, ip, self.cfg)
                # ] = ("http", ip)

            for future in as_completed(futures):
                service, ip = futures[future]

                try:
                    result = future.result()

                    if result:
                        hosts[ip][service] = result
                except Exception as e:
                    print(f"[ERROR] {service} probe failed on {ip}: {e}")

        elapsed = time.perf_counter() - start
        print(f"[INFO] Service probing took {elapsed:.3f} seconds")