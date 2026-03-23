
def show_menu():
    print("""
Option:
1 - Mapping
0 - Exit
""")


def show_mapping_menu():
    print("""
Option:
1 - Build IT Infrastructure Documentation
0 - Return
""")


def read_menu_input(prompt="Option: "):
    return input(prompt).strip()