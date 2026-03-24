from base_device import BaseHost

class HPEBase(BaseHost):
    vendor = "HPE"

class HPE1920_48G(HPEBase):
    host_category = "Switch"
    model = "1920-48G"

    # def baseInfo_get_firmware(self):
    #     hh3cSysImageNameOID = ".1.3.6.1.4.1.25506.2.3.1.4.2.1.2"
    #     hh3cSysImageTypeOID = ".1.3.6.1.4.1.25506.2.3.1.4.2.1.5."
    #     hh3cSysImageNameList = self.snmpSettings.snmpwalk(self.ipMgmtAddress, hh3cSysImageNameOID)

    #     for entry in hh3cSysImageNameList:
    #         index = entry.split()[0].split('.')[-1]
    #         if self.snmpSettings.snmpget(self.ipMgmtAddress, hh3cSysImageTypeOID+index) == '1':
    #             return entry.split()[3:]
        
    #     return ""
    
    # def ipv4_get_info_list(self) -> list:
    #     """
    #     MAC == LLDPChassisId
    #     works even if lldp is disabled globally
    #     """

    #     ipAdEntAddr_oid = ".1.3.6.1.2.1.4.20.1.1"
    #     ipAdEntIfIndex_oid = ".1.3.6.1.2.1.4.20.1.2."
    #     ipAdEntNetMask_oid = ".1.3.6.1.2.1.4.20.1.3."

    #     ip_addr_list = self.snmp.snmpwalk(ipAdEntAddr_oid)

    #     ip_info_dict_list = []

    #     for entry in ip_addr_list:
    #         ip_addr = entry.split()[3]
    #         ip_net_mask = self.snmp.snmpget(ipAdEntNetMask_oid+ip_addr)[0]
    #         if_index = self.snmp.snmpget(ipAdEntIfIndex_oid+ip_addr)[0]
    #         if_descr = self.interface_get_name(if_index) # Remover depois
    #         if_phy_address = self.snmp.snmpgetnext(".1.0.8802.1.1.2.1.3.2")[0].replace(" ", ":").strip(':')

    #         ip_info_dict_list.append({"Address": ip_addr,
    #                                     "Netmask": ip_net_mask,
    #                                     "MAC Address": if_phy_address,
    #                                     "Interface Index": if_index,
    #                                     "Interface Description": if_descr # Remover depois
    #                                 })

    #     return ip_info_dict_list
