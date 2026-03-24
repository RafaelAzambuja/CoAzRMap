from ..base_device import BaseHost

class TplinkBase(BaseHost):
    vendor = "TP-Link"

class TL_SG5412F(TplinkBase):
    host_category = "Switch"
    model = "TL-SG5412F"