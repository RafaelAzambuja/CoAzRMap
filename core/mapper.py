from core.file_handler import ConfigFile
from core.devices.factory import create_device
from .discovery.discovery_network import DiscoveryEngine


class MapEngine:
    
    def __init__(self, cfg_file : ConfigFile):
        self.cfg_file = cfg_file
        self.discovery_engine = DiscoveryEngine(self.cfg_file)
    
    def run_documentation(self):
        
        # Workflow:
        # 1. Obtain IP Address list
        # 2. Obtain dict of hosts and available services
        # 3. Create host objects, based on available services.

        ip_address_list = self.discovery_engine.get_subnets()
        host_service_dict = self.discovery_engine.discover_services(ip_address_list)

        hosts = create_device(host_service_dict)

        return hosts
    
  