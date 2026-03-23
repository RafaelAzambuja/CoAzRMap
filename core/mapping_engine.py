import time
from discovery.discovery_network import DiscoveryEngine
from factory import create_device
from file_handler import ConfigFile, JsonFile


class MappingEngine:

    def __init__(self, cfg_file: ConfigFile):
        
        self.cfg = cfg_file
        self.discovery_engine = DiscoveryEngine(cfg_file)
        self.json_file = JsonFile(
            self.cfg.read_cfg_file("output", "json")
        )
        self.topology = {}

    def run_full_documentation(self) -> None:

        print("Note: Host documentation depends on SNMP.")

        ip_address_list = self.discovery_engine._get_subnets_from_user()
        if not ip_address_list:
            return

        hosts = self.discovery_engine.discover(ip_address_list)

        if not hosts:
            print("[INFO] No reachable hosts discovered.")
            return

        devices = self._create_devices(hosts)

        if not devices:
            print("[INFO] No SNMP-capable devices found.")
            return

        self._collect_base_information(devices)

        # Neighbor

        self.build_topology(devices)

    def _create_devices(self, hosts: dict) -> list:

        devices = []

        for ip, services in hosts.items():

            snmp_obj = services.get("snmp")

            if not snmp_obj:
                continue

            device = create_device(
                None,
                snmp_obj.vendor_oid,
                snmp_obj
            )

            if device:
                print(
                    f"[DEBUG] Created host: "
                    f"{device.snmp.agent_interface}, "
                    f"Vendor: {device.vendor}, "
                    f"Model: {device.model}"
                )
                devices.append(device)

        return devices

    def _collect_base_information(self, devices: list) -> None:

        print("[INFO] Collecting base device information...")

        start_time = time.perf_counter()

        self.json_file._create_json()

        for device in devices:

            if device.host_category != "Switch":
                continue

            print(f"[DEBUG] Polling {device.snmp.agent_interface}")

            device._build_data()

            self.json_file.add_to_category(
                device.host_category,
                device.data
            )

        elapsed = time.perf_counter() - start_time

        print(
            f"[INFO] Base info collected. "
            f"Elapsed time: {elapsed:.3f} seconds"
        )

    def build_topology(self, devices: list) -> None:

        print("[INFO] Collecting LLDP neighbor information...")
        start_time = time.perf_counter()

        json_data = self.json_file._load_data()
        switch_list = json_data.get("Switch", [])

        for device in devices:

            if device.host_category != "Switch":
                continue

            neighbors = device.lldp_get_remote_entry_list()

            if not neighbors:
                continue

            neighbor_list = []

            for local_port, remote_data in neighbors.items():
                neighbor_list.append({
                    "local_port": local_port,
                    "remote_host": remote_data.get("Remote Host"),
                    "remote_port": remote_data.get("Remote Port")
                })

            device.data["Neighbors"] = neighbor_list

            for sw in switch_list:
                if sw.get("Host SNMP Agent Interface") == device.snmp.agent_interface:
                    sw["Neighbors"] = neighbor_list
                    break

        json_data["Switch"] = switch_list
        
        self.json_file.save_all(json_data)

        elapsed = time.perf_counter() - start_time
        print(f"[INFO] LLDP info collected. Elapsed time: {elapsed:.3f} seconds")

    def _save_topology(self):
        json_data = self.json_file._load_data()
        json_data["Topology"] = self.topology
        self.json_file._save_data(json_data)