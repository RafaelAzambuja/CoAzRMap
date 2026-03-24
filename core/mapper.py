from core.file_handler import ConfigFile
from discovery.discovery_network import DiscoveryEngine


class MapEngine:
    
    def __init__(self, cfg_file : ConfigFile):
        self.cfg_file = cfg_file
        self.discovery_engine = DiscoveryEngine(self.cfg_file)
    
    def run_documentation(self):
        
        # Workflow:
        # 1. Obtain IP Address list
        # 2. Obtain dict of available services

        ip_address_list = self.discovery_engine.get_subnets()
        service_dict = self.discovery_engine.discover_services(ip_address_list)

        return service_dict