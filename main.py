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
                            print(disc_eng.discover_services(disc_eng.get_subnets_from_user()))
                            pass

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