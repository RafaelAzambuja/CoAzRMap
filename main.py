from core.menu import show_menu, show_mapping_menu, read_menu_input
from core.file_handler import ConfigFile
from discovery.discovery_network import DiscoveryEngine


if __name__ == "__main__":

    # VALIDATION
    cfg_file = ConfigFile()
    cfg_file.validate_config()

    # PROGRAM LOOP
    while True:
        show_menu()
        menu_option = read_menu_input()

        match menu_option:
            case '1':
                while True:
                    show_mapping_menu()
                    mapping_menu_option = read_menu_input()
                    match mapping_menu_option:
                        case '1':
                            disc_eng = DiscoveryEngine(cfg_file)
                            subnets = disc_eng.get_subnets()
                            hosts = disc_eng.discover_services(subnets)
                            print(f"total alive hosts: {len(hosts.items())}")
                            for host_ip, host_info in hosts.items():
                                snmp_object = host_info['snmp']
                                if snmp_object:
                                    print(f"Host IP: {host_ip}, Vendor OID: {snmp_object.vendor_oid}")
                                else:
                                    print(f"Host IP: {host_ip}, no snmp")
                        case '0':
                            print("Returning...")
                            break

                        case _:
                            print("Invalid option.")
                    # Map

            case '0':
                print("Exiting...")
                break

            case _:
                print("Invalid option.")
