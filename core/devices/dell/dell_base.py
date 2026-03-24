from ..base_device import BaseHost

class DellBase(BaseHost):
    vendor = "Dell"

class N1524(DellBase):
    host_category = "Switch"
    model = "N1524"