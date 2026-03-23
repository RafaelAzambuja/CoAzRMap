from re import compile
from utils.common import convert_port_list, convert_hex_to_oid, convert_hex_to_utf8
from devices.base_device import Host_Device
from discovery.discovery_snmp import SNMPMgmt
from discovery.discovery_ssh import SSHMgmt

class Switch(Host_Device):
    """
    """


    def __init__(self,
                 ssh : SSHMgmt | None = None,
                 snmp : SNMPMgmt | None = None):
        
        """
        :param snmp: Instance of SNMPMgmt that contains IPv(4 | 6) address of the snmp agent and snmp commands.
        :param ssh: Instance of SSHMgmt.
        """

        self.host_category : str = "Switch"
        self.ssh = ssh
        self.snmp = snmp
        self.data = {
            "id": self.snmp.agent_interface,
            "date": "",
            "Base Info": {},
            "Services": {}
            }

        if self.snmp:
            self.data["Services"]["SNMP"] = {
                "Enabled": "true",
                "Version": self.snmp.version,
                #"Agent Address": self.snmp.agent_interface
            }

    

    def vlan_get_interface_pvid(self, instance) -> str:
        """
        
        """
        
        dot1qPvid_oid = "1.3.6.1.2.1.17.7.1.4.5.1.1."
        value = self.snmp.snmpget(dot1qPvid_oid+instance)

        return value[0] # Hopefully type is always INTEGER

    def vlan_get_name(self, instance) -> str:
        """
            Para dispositivos que possuem o grupo dot1qVlan (Q-BRIDGE-MIB)
        """

        vlanStaticName_oid = ".1.3.6.1.2.1.17.7.1.4.3.1.1."
        value = self.snmp.snmpget(vlanStaticName_oid+instance)

        if value[1] == "STRING":
            return self._normalize_snmp_string(value[0])

        if value[1] == "Hex-STRING":
            return convert_hex_to_utf8(value[0])

        return value[0]

    def vlan_get_static_list(self) -> list:
        """
            Check auto-vlan create
        """
        
        vlanStaticEntry_oid = ".1.3.6.1.2.1.17.7.1.4.3.1.1"
        vlan_entries = self.snmp.snmpwalk(vlanStaticEntry_oid)
        vlan_entry_list = []

        for vlan_entry in vlan_entries:
            vlan_vid = vlan_entry.split()[0].split('.')[13]
            vlan_name = self.vlan_get_name(vlan_vid)
            #vlan_name = self._normalize_snmp_string(" ".join(vlan_entry.split()[3:]))
            vlan_entry_dict = {"VID": vlan_vid,
                               "Name": vlan_name}
            vlan_entry_list.append(vlan_entry_dict)
        
        return vlan_entry_list

    def vlan_get_untagged(self, vid) -> dict:
        """
        Esta OID aparentemente não precisa de fix_port_list()
        """
        
        dot1qVlanStaticUntaggedPorts_oid = ".1.3.6.1.2.1.17.7.1.4.3.1.4."

        port_list = self.snmp.snmpget(dot1qVlanStaticUntaggedPorts_oid+vid)[0].split() # Hopefully type is always Hex-STRING
        port_list = convert_port_list(port_list)

        port_untagged_dict = {"VID": vid, "if Indexes": port_list}
        
        return port_untagged_dict
    
    def vlan_get_tagged(self, vid) -> dict:
        dot1qVlanStaticEgressPorts_oid = ".1.3.6.1.2.1.17.7.1.4.3.1.2."

        port_list = self.snmp.snmpget(dot1qVlanStaticEgressPorts_oid+vid)[0].split() # Hopefully type is always Hex-STRING
        port_list = convert_port_list(port_list)
		
        port_untagged_dict = self.vlan_get_untagged(vid)
        port_egress_dict = {"VID": vid, "if Indexes": port_list}

        for port_egress in reversed(port_egress_dict["if Indexes"]):
            if port_egress in port_untagged_dict["if Indexes"]:
                port_egress_dict["if Indexes"].remove(port_egress)
        
        return port_egress_dict
    
    def ipv4_get_info_list(self) -> list:
        """
        Deprecated. Should use .1.3.6.1.2.1.4.28
        Alterar para metodos get individuais
        """

        ipAdEntAddr_oid = ".1.3.6.1.2.1.4.20.1.1"
        ipAdEntIfIndex_oid = ".1.3.6.1.2.1.4.20.1.2."
        ipAdEntNetMask_oid = ".1.3.6.1.2.1.4.20.1.3."

        ip_addr_list = self.snmp.snmpwalk(ipAdEntAddr_oid)

        ip_info_dict_list = []

        for entry in ip_addr_list:
            ip_addr = entry.split()[3]
            ip_net_mask = self.snmp.snmpget(ipAdEntNetMask_oid+ip_addr)[0]
            if_index = self.snmp.snmpget(ipAdEntIfIndex_oid+ip_addr)[0]
            if_descr = self.interface_get_name(if_index) # Remover depois
            if_phy_address = self.interface_get_phyAddress(if_index)

            ip_info_dict_list.append({"Address": ip_addr,
                                      "Netmask": ip_net_mask,
                                      "MAC Address": if_phy_address,
                                      "Interface Index": if_index,
                                      "Interface Description": if_descr # Remover depois
                                    })
        
        return ip_info_dict_list

    #def ipv4_get_routes_list(self) -> list:

    #    {"Destiny": , "Netmask": \t\tNEXTHOP\t\tINTERFACE"}


        

    def find_host_port(self, vid, client_mac):
        dot1qTpFdbPort_oid = ".1.3.6.1.2.1.17.7.1.2.2.1.2."
        client_mac = convert_hex_to_oid(client_mac)
        portIndex = self.snmp.snmpget(dot1qTpFdbPort_oid+vid+client_mac)
        if portIndex:
            return portIndex[0]
        
        return ""



###

    # def baseInfo_get_stack_list(self) -> list:
    #     ianaPhysicalClassOID = ".1.3.6.1.2.1.47.1.1.1.1.5"
    #     entPhysicalDescrOID = "1.3.6.1.2.1.47.1.1.1.1.2."
    #     stackRawList = self.snmpSettings.snmpwalk(self.ipMgmtAddress, ianaPhysicalClassOID)
    #     stackList = []

    #     for entry in stackRawList:
    #         parts = entry.split()
    #         index = parts[0].split('.')[-1]
    #         entityType = parts[3]
    #         if entityType == '3':
    #             stackList.append({"Index": index, "Description": self.snmpSettings.snmpget(self.ipMgmtAddress, entPhysicalDescrOID+index).strip('"')})

    #     return stackList


    # def interface_is_physical(self, instance) -> bool:
    #     ianaPhysicalClassOID = ".1.3.6.1.2.1.47.1.1.1.1.5"
    #     entAliasMappingOID = ".1.3.6.1.2.1.47.1.3.2.1.2"
    #     entToIfIndexList = self.snmpSettings.snmpwalk(self.ipMgmtAddress, entAliasMappingOID)
    #     for entry in entToIfIndexList:
    #         if entry.split()[3].split('.')[-1] == instance:
    #             entityClass = self.snmpSettings.snmpget(self.ipMgmtAddress, ianaPhysicalClassOID+'.'+entry.split()[0].split('.')[-2])
    #             if entityClass == '10':
    #                 return True
        
    #     return False

    # def interface_get_l2_list(self) -> list:
    #     ifNameOID = ".1.3.6.1.2.1.31.1.1.1.1"
    #     ifRawList = self.snmpSettings.snmpwalk(self.ipMgmtAddress, ifNameOID)
    #     ifList = []

    #     for entry in ifRawList:
    #         parts = entry.split()
    #         index = parts[0].split('.')[-1]
    #         ifType = self.interface_get_type(index)
    #         #if self.interface_is_physical(index):
    #         #    ifList.append({"Index": index, "Name": parts[3].strip('"'), "Type": self.interface_get_type(index)})
    #         if ifType["Scope"] == "Port":
    #             ifList.append({"Index": index,
    #                            "Name": parts[3].strip('"'),
    #                            "Alias": self.interface_get_alias(index),
    #                            "Type": ifType["Descr"],
    #                            #"Physical": self.interface_is_physical(index),
    #                            "MAC Address": self.interface_get_phy_address(index)})
            
    #     return ifList