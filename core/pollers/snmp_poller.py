from ...utils.common import normalize_snmp_string
from ...discovery.discovery_snmp import SNMPMgmt

class SNMPPoller:

    def baseInfo_get_sysName(snmp_obj : SNMPMgmt) -> str:
        """
        Get system name via SNMP GET (mib-2.system.sysName.0)

        :return: sysName.0 without surrounding quotes, if object type is STRING
        """
        
        sysName_oid = ".1.3.6.1.2.1.1.5.0"
        value = snmp_obj.snmpget(sysName_oid)

        if value[1] == "STRING":
            return normalize_snmp_string(value[0])

        return value[0]