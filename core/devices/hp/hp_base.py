from base_device import BaseHost

class HPBase(BaseHost):
    vendor = "HP"

class JL381A_1920S(HPBase):
    host_category = "Switch"
    model = "OfficeConnect Switch 1920S JL381A"