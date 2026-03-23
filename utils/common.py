import re


def normalize_snmp_string(value : str) -> str:
        """

        """
        if not value:
            return ""

        return value.strip('"')

def convert_port_list(port_list: list) -> list:
    res = ""
    offset = 1
    for j in port_list:
        res += str(bin(int(j, 16))[2:].zfill(8))+" "

    res = res.split()

    port_index_vlan = ""
    for j in res:
        for i in range(0, len(j)):
            if j[i] == '1':
                port_index_vlan += str(int(i) + offset)+" "
        offset += 8

    return port_index_vlan.split()

def fix_port_list(port_list):
	
    '''
        Instancias e portList seguem da forma:
        xx xx xx xx xx..., onde cada par de hexadecimais representa um grupo de oito porta no switch.
        e cada posição na hex-string é equivalente a um indice de interface. Convertendo para binário teria-se algo como:
        1011011011110111011101. Quando 1, a interface (porta) seria "positivo". Por exemplo, se este é o portList de interfaces que pertencem
        a vlan 10, todas as porta setadas em '1' pertencem a vlan 10.
        O problema é que cada grupo de 8 porta está invertido. Pegando o mesmo exemplo temos:
        10110110 11110111 01110110
        O primeiro campo equivale as porta de 1 à 8, porém na ordem inversa. O segundo campo às portas de 9 à 16, e assim pro diante.
        O problema é que a primeira posição, por exemplo, do priemiro campo equivale na verdade a porta 8, e a ultima posição, a porta 1.
    '''

    offset = 1
    res = ""

    for j in port_list:
        res += str(bin(int(j, 16))[2:].zfill(8))+" "
	
    port_index_vlan = ""
    res = res.split()

    for j in res:
        j = j[::-1]
        for i in range(0, len(j)):
            if j[i] == '1':
                port_index_vlan += str(int(i) + offset)+" "
        offset += 8
	
    return port_index_vlan.split()

def convert_hex_to_oid(hex_string) -> str:

    '''
		Converter MAC no formato XX:XX:XX:XX:XX:XX | xx:xx:xx:xx:xx:xx | xxxx-xxxx-xxxx | xx-xx-xx-xx-xx-xx para decimal no formato de OID.
	'''
    
    mac_regex = r'([0-9a-fA-F]{2})[:-]([0-9a-fA-F]{2})[:-]([0-9a-fA-F]{2})[:-]([0-9a-fA-F]{2})[:-]([0-9a-fA-F]{2})[:-]([0-9a-fA-F]{2})'

    match = re.match(mac_regex, hex_string)

    if match:
        parts = match.groups()
        decimal_parts = [str(int(part, 16)) for part in parts]
        mac_oid = '.'.join(decimal_parts)
        return "." + mac_oid
    else:
        raise ValueError("Formato de MAC Inválido.")

def convert_hex_to_utf8(hex_string: str) -> str:
    """
    """

    hex_string = hex_string.replace(" ", "").replace("\n", "")
    return bytes.fromhex(hex_string).decode("utf-8")