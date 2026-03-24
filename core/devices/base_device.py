from ..pollers.snmp_poller import SNMPPoller

class BaseHost:
    
    def __init__(self, snmp = None, ssh = None):
        
        self.host_category : str = "Unknown"
        self.vendor : str = snmp.vendor_oid or None
        self.model : str = snmp.vendor_oid
        self.snmp = snmp
        self.ssh = ssh

    def baseInfo_get_sysName(self) -> str:
        """
        """

        # Unknow vendor = No fallback to SSH, HTTP, etc.
        try:
            poller_snmp = SNMPPoller(self.snmp)
            sys_name = poller_snmp.baseInfo_get_sysName()

        # except:
            # poller_ssh = ...
            # sys_name = poller_ssh.baseInfo_get_sysName(self.ssh)

        finally:
            return sys_name