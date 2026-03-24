from base_device import BaseHost

class CiscoBase(BaseHost):
    vendor = "Cisco"

class Cisco_SF300_24(CiscoBase):
    host_category = "Switch"
    model = "SF300-24"

class Cisco_SF300_48(CiscoBase):
    host_category = "Switch"
    model = "SF300-48"

class Cisco_SG300_28PP(CiscoBase):
    host_category = "Switch"
    model = "SG300-28PP"