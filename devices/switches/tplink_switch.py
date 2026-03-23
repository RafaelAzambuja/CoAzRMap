from .base_switch import Switch

class Tplink(Switch):
    vendor = "TP-Link"

class TL_SG5412F(Tplink):
    model = "TL-SG5412F"