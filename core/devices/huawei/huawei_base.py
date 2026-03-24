from base_device import BaseHost

class HuaweiBase(BaseHost):
    vendor = "Huawei"

    # def find_host_port(self, vid, client_mac):
    #     hwDynFdbPort_oid = ".1.3.6.1.2.1.17.7.1.2.2.1.2." # + .mac. + vlan_id.1.48(Vsi Table?)
    #     # hwDynMacAddrQueryIfIndex = ".1.3.6.1.4.1.2011.5.25.42.2.1.33.1.13"
    #     client_mac = convert_hex_to_oid(client_mac)
    #     portIndex = self.snmp.snmpget(hwDynFdbPort_oid+client_mac+vid+"1.48")
    #     if portIndex:
    #         return portIndex[0]
        
    #     return ""

class S5720_28X_LI_AC(HuaweiBase):
    host_category = "Switch"
    model = "S5720-28X-LI-AC"

    # def baseInfo_get_sys_image(self):
    #     hwSysImageVersion_oid = ".1.3.6.1.4.1.2011.5.25.19.1.4.2.1.5.1" # Multiple images? Get-Next?
    #     value = self.snmp.snmpget(hwSysImageVersion_oid)

    #     return self._normalize_snmp_string(value)
    
class S5720_52X_PWR_LI_AC(HuaweiBase):
    host_category = "Switch"
    model = "S5720-52X-PWR-LI-AC"