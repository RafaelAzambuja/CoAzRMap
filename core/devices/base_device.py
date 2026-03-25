from ..pollers.snmp_poller import SNMPPoller

class BaseHost:
    
    host_category = "Unknown"
    vendor = None
    model = None
    
    def __init__(self, ssh = None, snmp = None):
        
        self.snmp = snmp
        self.ssh = ssh
        self.host_category = self.host_category
        self.vendor = self.vendor
        self.model = self.model

        if snmp and not self.vendor:
            self.vendor = snmp.vendor_oid

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