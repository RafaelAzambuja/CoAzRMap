import time
import json
from utils.file_handler import ConfigFile, JsonFile, CSVFile
from core.mapping_engine import MappingEngine
from discovery.discovery_network import DiscoveryEngine

# Graph = dict[str, dict[str, dict]]

# def get_device_macs(data : list) -> list:

#     local_macs = {}

#     for item in data.get("Switch", []):
#         local_ip = item["Host SNMP Agent Interface"]
#         local_macs.setdefault(local_ip, [])

#         for ipentry in item["IP Addresses"]["IPv4"]:
#             mac_address = ipentry.get("MAC Address")
#             ip_address = ipentry.get("Address")

#             if mac_address \
#                 and mac_address != "00:00:00:00:00:00" \
#                 and ip_address \
#                 and ip_address != "127.0.0.1":

#                 local_macs[local_ip].append({
#                         "Address": ip_address,
#                         "MAC": mac_address
#                     })

#     return local_macs


def show_menu():
    print("""
Option:
    1  - Mapping
    2  - Data treatment
    3  - Debug
    0  - Exit
""")

def mapping_menu():
    print("""
Option:
    1  - (FULL) Switch and AP documentation
    2  - Find Host L2 Uplink
    0  - Return
""")

def data_menu():
    print("""
Option:
    1  - Device list
    0  - Return
""")

def debug_menu():
    print("""
Option:
    1  - Check OID
    0  - Exit
""")

if __name__ == "__main__":

    while True:
        show_menu()
        opt = input("Option: ").strip()

        match opt:
            case '1':
                while True:
                    mapping_menu()
                    map_opt = input("Option: ").strip()

                    match map_opt:
                        case '1':
                            cfg_file = ConfigFile()
                            mapping_engine = MappingEngine(cfg_file)
                            mapping_engine.run_full_documentation()



                            # print(f"[INFO] Starting Local Neighbor Discovery")
                            # start_time = time.perf_counter()

                            # json_data = json_file._load_data()
                            # local_macs = get_device_macs(json_data)

                            # # LLDP
                            # # host.lldp_get_remote_entry_list()
                            # #   data[local_port_index] = {remote_chassis, remote_port_id}
                            # # 1. identificar tipo de remote_chassis
                            # # 2. 

                            # # FDB
                            # graph = build_fdb_graph(cfg_file, json_data, local_macs)

                            # topology = discover_neighbors(graph, local_macs)

                            # print(json.dumps(topology, indent=2))

                            # end_time = time.perf_counter()
                            # elapsed_time_neighbor = end_time - start_time
                            # print(f"[INFO] Neighbor info collected. Elapsed time: {elapsed_time_neighbor:.3f} seconds")
                            
                            # elapsed_time = elapsed_time_info + elapsed_time_neighbor
                            # print(f"[INFO] Done. Mapping took {elapsed_time:.3f} seconds")

                        case '2':
                            # To do
                            # validar e organizar
                            cfg_file = ConfigFile()
                            client_mac = input("MAC: ")
                            mapping_engine = MappingEngine(cfg_file)
                            #device_source_opt = input("M")


                        case '0':
                            print("Returning...")
                            break

                        case _:
                            print("Invalid Option")

            # case '2':
            #     while True:
            #         data_menu()
            #         data_opt = input("Option: ").strip()
            #         match data_opt:
            #             case '1':
            #                 json_data = json_file._load_data()
            #                 csv_file = CSVFile(cfg_file.read_cfg_file('output', 'csv'))
            #                 rows = [
            #                     {"Sys Address": device["Host SNMP Agent Interface"],
            #                      "Sys Vendor": device["Host Device Vendor"],
            #                      "Sys Model": device["Host Device Model"],
            #                      "Sys Name": device["Host System Name"],
            #                      "Sys Location": device["Host System Location"]}
            #                     for entry in json_data.values()
            #                     for device in entry
            #                     if "Host SNMP Agent Interface" in device \
            #                         and "Host Device Vendor" in device \
            #                         and "Host Device Model" in device \
            #                         and "Host System Name" in device \
            #                         and "Host System Location" in device
            #                 ]

            #                 csv_file._atomic_write(rows)

            #             case '0':
            #                 print("Returning...")
            #                 break

            #             case _:
            #                 print("Invalid Option")
                    
            case '3':
                while True:
                    debug_menu()
                    debug_opt = input("Option: ").strip()
                    match debug_opt:

                        case '1':
                            # cfg_file = ConfigFile()
                            # discovery_engine = DiscoveryEngine(cfg_file)
                            # ip_address_list = discovery_engine._get_subnets_from_user()

                            # if not ip_address_list:
                            #     return

                            # hosts = discovery_engine.discover(ip_address_list)

                            # if not hosts:
                            #     print("[INFO] No reachable hosts discovered.")
                            #     return

                            # devices = ._create_devices(hosts)

                            # if not devices:
                            #     print("[INFO] No SNMP-capable devices found.")
                            #     return
                            break
                        case '0':
                            print("Returning...")
                            break

                        case _:
                            print("Invalid Option")

            case '0':
                print("Exiting...")
                break
            case _:
                print("Invalid Option")