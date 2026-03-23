from .base import Switch

class Cisco(Switch):
    vendor = "Cisco"

class Cisco_SF300_24(Cisco):
    model = "SF300-24"

class Cisco_SF300_48(Cisco):
    model = "SF300-48"

class Cisco_SG300_28PP(Cisco):
    model = "SG300-28PP"


