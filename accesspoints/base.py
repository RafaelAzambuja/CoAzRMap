#from common import convert_port_list, hex_to_oid
from snmpnetdoc import SNMPMgmt
from sshnetdoc import SSHMgmt

class AccessPoint:

    def __init__(self,
                 ssh : SSHMgmt | None = None,
                 snmp : SNMPMgmt | None = None):
        
        self.host_category = "Access Point"
        self.ssh = ssh
        self.snmp = snmp
        self.vendor = ""
        self.model = ""

    def _normalize_snmp_string(self, value: str) -> str:
        """

        """

        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        return value

    def baseInfo_get_sysDescr(self) -> str:
        """
        Get system description via SNMP GET (mib-2.system.sysDescr.0)

        :return: sysDescr.0 without surrounding quotes
        """

        sysDescr_oid = ".1.3.6.1.2.1.1.1.0"
        value = self.snmp.snmpget(sysDescr_oid)

        return self._normalize_snmp_string(value)
    
    def baseInfo_get_sysName(self) -> str:
        """
        """
        sysName_oid = ".1.3.6.1.2.1.1.5.0"
        value = self.snmp.snmpget(sysName_oid)
        
        return self._normalize_snmp_string(value)
    
    def baseInfo_get_sysLocation(self) -> str:
        sysLocation_oid = ".1.3.6.1.2.1.1.6.0"
        value = self.snmp.snmpget(sysLocation_oid)

        return self._normalize_snmp_string(value)