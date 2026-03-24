import pollers.snmp_poller as snmp_poller

class BaseHost:
    
    def __init__(self, snmp = None):
        
        if not snmp:
            return None
        
        self.host_category : str = "Unknown"
        self.vendor : str = snmp.vendor_oid
        self.model : str = snmp.vendor_oid
        self.snmp = snmp

    def baseInfo_get_sysName(self) -> str:
        """
        """

        # Unknow vendor = No fallback to SSH, HTTP, etc.
        try:
            poller_snmp = snmp_poller.SNMPPoller()
            sys_name = poller_snmp.baseInfo_get_sysName(self.snmp)

        finally:
            return sys_name