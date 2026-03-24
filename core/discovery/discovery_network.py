import time
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.file_handler import ConfigFile
from discovery.discovery_icmp import poll_icmp_active_hosts
from discovery.discovery_snmp import SNMPMgmt
# from discovery.discovery_ssh import test_ssh_on_host


class DiscoveryEngine:
    """
    """

    def __init__(self, cfg_file : ConfigFile):
        """ 
        """

        self.max_threads = max(1, min(128, int(cfg_file.read_cfg_file("options", "max_threads", fallback="10"))))
        self.cfg_file = cfg_file

    def get_subnets(self, subnets_input = None) -> list[str]:
        
        """
        """

        while True:
            if not subnets_input:
                subnets_input = input(
                    "Enter subnets/addresses separated by space.\n"
                    "Ex: 192.168.0.0/24 172.16.230.2 10.23.0.0/16:\n"
                ).strip()

            try:
                return self._validate_subnets(subnets_input)
            
            except ValueError as e:
                print(f"Error: {e}")

    def _validate_subnets(self, ip_address_list: str) -> list[str]:
        """
        """

        # Time complexity: O(n log n)
        # start = time.perf_counter()
        ipv4_networks = []
        ipv6_networks = []

        for entry in ip_address_list.split():
            entry = entry.strip()
            if not entry:
                continue

            try:
                network = ipaddress.ip_network(entry, strict=True)
            except ValueError:
                try:
                    ip = ipaddress.ip_address(entry)
                    network = ipaddress.ip_network(f"{ip}/{ip.max_prefixlen}", strict=True)
                except ValueError:
                    raise ValueError(f"Invalid IPv4 or IPv6 address/subnet: {entry}")

            if network.version == 4:
                ipv4_networks.append(network)
            else:
                ipv6_networks.append(network)

        collapsed_v4 = list(ipaddress.collapse_addresses(ipv4_networks))
        collapsed_v6 = list(ipaddress.collapse_addresses(ipv6_networks))

        # elapsed = time.perf_counter() - start
        # print(f"[DEBUG] Subnet sorting took {elapsed:.3f} seconds")

        return [str(n) for n in (collapsed_v4 + collapsed_v6)]

    def discover_services(self, ip_addr_list : list[str]):

        hosts = self._icmp_phase(ip_addr_list)

        if not hosts:
            print("[INFO] No active hosts found.")
            return {}

        self._service_probe_phase(hosts)

        return hosts

    def _icmp_phase(self, subnets: list[str]) -> dict[str, dict]:

        hosts: dict[str, dict] = {}
        start = time.perf_counter()

        for subnet in subnets:
            print(f"[INFO] ICMP - Polling active hosts in {subnet}")
            alive_hosts = poll_icmp_active_hosts(subnet, self.cfg_file)

            for ip in alive_hosts:
                hosts[ip] = {
                    "icmp": True,
                    "snmp": None,
                    "ssh": None,
                    "http": None,
                }

        elapsed = time.perf_counter() - start
        #print(f"[DEBUG] Alive hosts in {subnet}: {alive_hosts}")
        print(f"[INFO] ICMP polling took {elapsed:.3f} seconds")

        return hosts

    def _probe_snmp(self, ip: str):
        print(f"[DEBUG] Trying SNMP on {ip}")
        snmp = SNMPMgmt(ip, self.cfg_file)

        if snmp.connect():
            print(f"[DEBUG] SNMP OK on {ip}")
            return snmp

        print(f"[DEBUG] SNMP FAILED on {ip}")
        return None

    def _service_probe_phase(self, hosts: dict[str, dict]) -> None:

        print("[INFO] Probing services (SNMP / SSH / HTTP)")
        start = time.perf_counter()

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {}

            for ip in hosts.keys():

                if self.cfg_file.read_cfg_file("service", "snmp"):
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
