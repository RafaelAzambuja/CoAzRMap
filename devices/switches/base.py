from re import compile
from utils.common import convert_port_list, convert_hex_to_oid, convert_hex_to_utf8
from discovery.discovery_snmp import SNMPMgmt
from sshnetdoc import SSHMgmt

class Switch:
    """
    A class used to represent a generic L2 managed Switch

    ...

    Attributes
    ----------
    host_category : str
        used categorize and store the device information in a database
    vendor : str
        mapped value of sysObjectOID used to identify the switch's manufacterer/vendor, model and MIBs available
    model : str
        switch's model
    
    Methods
    -------
    """

    host_category : str = "Switch"
    vendor : str = "Unknown"
    model : str = "Unknown"

    def __init__(self,
                 ssh : SSHMgmt | None = None,
                 snmp : SNMPMgmt | None = None):
        
        """
        :param snmp: Instance of SNMPMgmt that contains IPv(4 | 6) address of the snmp agent and snmp commands.
        :param ssh: Instance of SSHMgmt.
        """
        
        self.ssh = ssh
        self.snmp = snmp
        self.data = {}

    def _build_data(self):
        """
        
        :param self: Description
        """


        lldp_chassis = self.lldp_get_local_chassis_info()

        self.data = {
            "Host System Name": self.baseInfo_get_sysName(),
            "Host System Location": self.baseInfo_get_sysLocation(),
            "Host SNMP Agent Interface": self.snmp.agent_interface,
            "Host System Description": self.baseInfo_get_sysDescr(),
            "Host Device Vendor": self.vendor,
            "Host Device Model": self.model,
            "LLDP Local Chassis ID": lldp_chassis["Local Chassis ID"],
            "LLDP Local Chassis ID Subtype": lldp_chassis["Local Chassis ID Subtype"],
            "VLANs": self.vlan_get_static_list(),
            "Interfaces": self.interface_get_list(),
            "IP Addresses": {
                "IPv4": self.ipv4_get_info_list(),
                "IPv6": "Empty"
            }
        }
    
        vlan_untagged_map = {}
        vlan_tagged_map = {}

        for vlan in self.data['VLANs']:
            vid = vlan["VID"]
            untagged = self.vlan_get_untagged(vid)
            tagged = self.vlan_get_tagged(vid)

            vlan_untagged_map[vid] = untagged["if Indexes"]
            vlan_tagged_map[vid] = tagged["if Indexes"]

        interfaces = self.data["Interfaces"]

        for iface in interfaces:
            iface_type = iface.get("Interface Type", {})
            if iface_type.get("Scope") != "Port":
                continue

            iface_index = iface.get("Interface ifIndex")

            iface["VLAN Untagged"] = []
            iface["VLAN Tagged"] = []

            for vid, ports in vlan_untagged_map.items():
                if iface_index in ports:
                    iface["VLAN Untagged"].append(vid)

            for vid, ports in vlan_tagged_map.items():
                if iface_index in ports:
                    iface["VLAN Tagged"].append(vid)

    def _normalize_snmp_string(self, value : str) -> str:
        """

        """
        if not value:
            return ""

        return value.strip('"')

    def baseInfo_get_sysDescr(self) -> str:
        """
        Get system description via SNMP GET (mib-2.system.sysDescr.0)

        :return: sysDescr.0 without surrounding quotes, if object type is STRING
        """

        sysDescr_oid = ".1.3.6.1.2.1.1.1.0"
        value = self.snmp.snmpget(sysDescr_oid)

        if value[1] == "STRING":
            return self._normalize_snmp_string(value[0])

        return value[0]
    
    def baseInfo_get_sysName(self) -> str:
        """
        Get system name via SNMP GET (mib-2.system.sysName.0)

        :return: sysName.0 without surrounding quotes, if object type is STRING
        """

        sysName_oid = ".1.3.6.1.2.1.1.5.0"
        value = self.snmp.snmpget(sysName_oid)

        if value[1] == "STRING":
            return self._normalize_snmp_string(value[0])

        return value[0]
    
    def baseInfo_get_sysLocation(self) -> str:
        """
        Get system location via SNMP GET (mib-2.system.sysLocation.0)

        :return: sysLocation.0 without surrounding quotes, if object type is STRING
        """

        sysLocation_oid = ".1.3.6.1.2.1.1.6.0"
        value = self.snmp.snmpget(sysLocation_oid)

        if value[1] == "STRING":
            return self._normalize_snmp_string(value[0])

        return value[0]
    
    def interface_get_name(self, instance) -> str:
        """
        Get interface textual name via SNMP GET (mib-2.ifMIB.ifName.instance)

        :return: If value is STRING: ifName.instance without surrounding quotes
        :return: If valeu is Hex-STRING: ifName.instance converted to UTF-8
        """

        ifName_oid = ".1.3.6.1.2.1.31.1.1.1.1."
        value = self.snmp.snmpget(ifName_oid+instance)

        if value[1] == "STRING":
            return self._normalize_snmp_string(value[0])

        if value[1] == "Hex-STRING":
            return convert_hex_to_utf8(value[0])

        return value[0]

    def _interface_identify_type(self, interface_type : str) -> dict:
        """
        Returns textual convention for IANAifType-MIB DEFINITIONS
        
        :param interface_type: ifType (mib-2.ifMIB.ifType.instance)
        """
        match interface_type:
            case '1': # Não definido. Geralmente implica em interface CPU.
                return {"Descr": "Other", "Scope": "Other"}
            case '6': # ethernetCsmacd (RFC 3635). Deveria ser padrão para interfaces tipo ethernet
                return {"Descr": "ethernetCsmacd", "Scope": "Port"}
            case '24': # softwareLoopback
                return {"Descr": "softwareLoopback", "Scope": "Loopback"}
            case '53': # Proprietary Virtual/Internal
                return {"Descr": "propVirtual", "Scope": "Proprietary"}
            case '117': # gigabitEthernet. Obsoleto. Deveria retornar ethernetCsmacd
                return {"Descr": "gigabitEthernet", "Scope": "Port"}
            case '131': # tunnel
                return {"Descr": "tunnel", "Scope": "Tunnel"}
            case '135': # l2vlan 802.1Q
                return {"Descr": "l2vlan", "Scope": "VLAN"}
            case '136': # l3ipvlan. vlan utilizando IP
                return {"Descr": "l3ipvlan", "Scope": "VLAN"}
            case '161': # IEEE 802.3ad Link Aggregate
                return {"Descr": "LAG 802.3ad", "Scope": "Link Aggregation"}
            case _:
                return {"Descr": interface_type, "Scope": "Unknown"}

    def interface_get_type(self, instance) -> dict:
        """
        Get interface enumerated value for IANAifType-MIB DEFINITIONS via SNMP GET (mib-2.ifMIB.ifType.instance)

        :return:
        """

        ifType_oid = ".1.3.6.1.2.1.2.2.1.3."
        value = self.snmp.snmpget(ifType_oid+instance)

        return value[0] # Hopefully type is always INTEGER

    def interface_get_phyAddress(self, instance) -> str:
        """

        """

        ifPhyAddress_oid = ".1.3.6.1.2.1.2.2.1.6."
        value = self.snmp.snmpget(ifPhyAddress_oid+instance)

        return value[0].replace(" ", ":").strip(':') # Hopefully type is always Hex-STRING

    def interface_get_alias(self, instance) -> str:
        """

        """

        ifAlias_oid = ".1.3.6.1.2.1.31.1.1.1.18."
        value = self.snmp.snmpget(ifAlias_oid+instance)

        if value[1] == "STRING":
            return self._normalize_snmp_string(value[0])

        if value[1] == "Hex-STRING":
            return convert_hex_to_utf8(value[0])

        return value[0]

    def interface_get_list(self) -> list:
        ifType_oid = ".1.3.6.1.2.1.2.2.1.3"
        interface_type_list = self.snmp.snmpwalk(ifType_oid)
        interface_list = []

        for interface in interface_type_list:
            if_type = interface.split()[3]
            if_type = self._interface_identify_type(if_type)

            if_index = interface.split()[0].split('.')[-1]

            if_dict = {
                "Interface ifIndex": if_index,
                "Interface Description": self.interface_get_name(if_index),
                "Interface Alias": self.interface_get_alias(if_index),
                "Interface Type": if_type,
                "Interface Physical Address": self.interface_get_phyAddress(if_index)
            }

            interface_list.append(if_dict)
        
        return interface_list

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

    def _lldp_normalize_chassis_id_subtype(self, local_chassis : tuple, chassis_id_subtype : tuple) -> dict:
        match chassis_id_subtype[0]:
            case '1': # entPhysicalAlias (stack member?)

                if local_chassis[1] == "STRING":
                    local_chassis = self._normalize_snmp_string(local_chassis[0])
                if local_chassis[1] == "Hex-STRING":
                    local_chassis = local_chassis[0].replace(" ", ":").strip('"')
                return { "Local Chassis ID": local_chassis, "Local Chassis ID Subtype": "chassisComponent" }
            
            case '2': # ifAlias

                if local_chassis[1] == "STRING":
                    local_chassis = self._normalize_snmp_string(local_chassis[0])
                if local_chassis[1] == "Hex-STRING":
                    local_chassis = local_chassis[0].replace(" ", ":").strip('"')
                return { "Local Chassis ID": local_chassis, "Local Chassis ID Subtype": "interfaceAlias" }
            
            case '3': # entPhysicalAlias (port)

                if local_chassis[1] == "STRING":
                    local_chassis = self._normalize_snmp_string(local_chassis[0])
                if local_chassis[1] == "Hex-STRING":
                    local_chassis = local_chassis[0].replace(" ", ":").strip('"')
                return { "Local Chassis ID": local_chassis, "Local Chassis ID Subtype": "portComponent" }
            
            case '4': # unicast source address

                if local_chassis[1] == "STRING":
                    local_chassis = self._normalize_snmp_string(local_chassis[0])
                if local_chassis[1] == "Hex-STRING":
                    local_chassis = local_chassis[0].replace(" ", ":").strip('"')
                return { "Local Chassis ID": local_chassis, "Local Chassis ID Subtype": "macAddress" }
            
            case '5': # network address

                if local_chassis[1] == "STRING":
                    local_chassis = self._normalize_snmp_string(local_chassis[0])
                if local_chassis[1] == "Hex-STRING":
                    local_chassis = local_chassis[0].replace(" ", ":").strip('"')
                return { "Local Chassis ID": local_chassis, "Local Chassis ID Subtype": "networkAddress" }
            
            case '6': # ifName

                if local_chassis[1] == "STRING":
                    local_chassis = self._normalize_snmp_string(local_chassis[0])
                if local_chassis[1] == "Hex-STRING":
                    local_chassis = local_chassis[0].replace(" ", ":").strip('"')
                return { "Local Chassis ID": local_chassis, "Local Chassis ID Subtype": "interfaceName" }
            
            case '7': # Locally Assigned

                if local_chassis[1] == "STRING":
                    local_chassis = self._normalize_snmp_string(local_chassis[0])
                if local_chassis[1] == "Hex-STRING":
                    local_chassis = local_chassis[0].replace(" ", ":").strip('"')
                return { "Local Chassis ID": local_chassis, "Local Chassis ID Subtype": "local" }
            
            case _:
                return { "Local Chassis ID": local_chassis[0], "Local Chassis ID Subtype": "Unknown Subtype" }

    def lldp_get_local_chassis_info(self) -> dict:
        lldpLocChassisId_oid = ".1.0.8802.1.1.2.1.3.2.0"
        lldpLocChassisIdSubtype_oid = ".1.0.8802.1.1.2.1.3.1.0"

        local_chassis = self.snmp.snmpget(lldpLocChassisId_oid)
        local_chassis_id_subtype = self.snmp.snmpget(lldpLocChassisIdSubtype_oid)

        if local_chassis[1] and local_chassis_id_subtype[1]:
            local_chassis_id_info = self._lldp_normalize_chassis_id_subtype(local_chassis, local_chassis_id_subtype[0])
            return local_chassis_id_info
        
        return {"Local Chassis ID": "Unknown", "Local Chassis ID Subtype": "Unknown"}
            
    def lldp_get_remote_chassis_info(self) -> dict:
        lldpRemChassisId_oid = ".1.0.8802.1.1.2.1.4.1.1.5."
        lldpRemChassisIdSubtype_oid = ".1.0.8802.1.1.2.1.4.1.1.4."

        remote_chassis = self.snmp.snmpget(lldpRemChassisId_oid)
        remote_chassis_id_subtype = self.snmp.snmpget(lldpRemChassisIdSubtype_oid)

        if remote_chassis[1] and remote_chassis_id_subtype[1]:
            remote_chassis_id_info = self._lldp_normalize_chassis_id_subtype(remote_chassis, remote_chassis_id_subtype[0])
            return remote_chassis_id_info
    
    def _lldp_identify_port_subtype(self, port_subtype):
        match port_subtype:
            case '1':
                return "interfaceAlias"
            case '2':
                return "portComponent"
            case '3':
                return "macAddress"
            case '4':
                return "networkAddress"
            case '5':
                return "interfaceName"
            case '6':
                return "agentCircuitId"
            case '7':
                return "local"
            case _:
                return "Unknown port subtype"
    
    def lldp_get_remote_port_id(self, instance):
        lldpRemPortId_oid = ".1.0.8802.1.1.2.1.4.1.1.7."
        value = self.snmp.snmpget(lldpRemPortId_oid+instance)
        if not value:
            return ""

        return self._normalize_snmp_string(value[0])

    def lldp_get_remote_port_id_subtype(self, instance):
        lldpRemPortIdSubtype_oid = ".1.0.8802.1.1.2.1.4.1.1.6."
        value = self.snmp.snmpget(lldpRemPortIdSubtype_oid+instance)
        if not value:
            return ""

        return self._lldp_identify_port_subtype(value[0])

    def lldp_get_local_port_id(self, index):
        lldpLocPortId_oid = ".1.0.8802.1.1.2.1.3.7.1.3."
        value = self.snmp.snmpget(lldpLocPortId_oid+index)
        if not value:
            return ""
        
        return self._normalize_snmp_string(value[0])

    def lldp_get_remote_entry_list(self) -> list:
        lldpRemChassisId_oid = ".1.0.8802.1.1.2.1.4.1.1.5"
        # 1.0.8802.1.1.2.1.4.1.1.5.timeMark.locPort.lldpRemIndex
        lldp_rem_entry_list = self.snmp.snmpwalk(lldpRemChassisId_oid)

        regex = compile(
            r"iso\.0\.8802\.1\.1\.2\.1\.4\.1\.1\.5\.(\d+)\.(\d+)\.(\d+)\s*=\s*(.*)"
        )

        validos = {}
        if not lldp_rem_entry_list:
            return ""
        for lldp_rem_entry in lldp_rem_entry_list:
            m = regex.match(lldp_rem_entry)
            if not m:
                continue

            time_mark = int(m.group(1))
            local_port = int(m.group(2))
            rem_index = int(m.group(3))

            chave = (local_port, rem_index)

            # Mantém apenas o maior timemark para cada chave
            if chave not in validos or time_mark > validos[chave]:
                validos[chave] = time_mark

        # "timeMark.localPort.remIndex"

        data = {}
        for (local_port, rem_index), time_mark in validos.items():
            data[local_port] = {
                "Remote Host": self._normalize_snmp_string(self.snmp.snmpget(".1.0.8802.1.1.2.1.4.1.1.5."+f"{time_mark}.{local_port}.{rem_index}")[0]),
                "Remote Port": self._normalize_snmp_string(self.snmp.snmpget(".1.0.8802.1.1.2.1.4.1.1.7."+f"{time_mark}.{local_port}.{rem_index}")[0])
            }

        return data

        # return [
        #     f"{time_mark}.{local_port}.{rem_index}"
        #     for (local_port, rem_index), time_mark in validos.items()
        # ]

    # def lldp_get_info_list(self) -> list:

    #     return {"LLDP Chassis ID": self.lldp_get_chassis_id(),
    #             #"LLDP Global Enabled": self.lldp_get_global_status() # implementar?
    #             "Local Port": 
    #             {
    #                 "LLDP Local Port ID": self
    #             },
    #             }

    # Outros

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