from devices.switches.cisco_switch import *
from devices.switches.dell_switch import *
from devices.switches.dlink_switch import *
from devices.switches.hp_switch import *
from devices.switches.hpe_switch import *
from devices.switches.huawei_switch import *
from devices.switches.tplink_switch import *

# Usar introspecção?????

def create_device(ssh,
                  vendor_oid : str,
                  snmp):

    """
    """
	
    match vendor_oid:

        case "iso.3.6.1.4.1.9.6.1.82.24.1":
            return Cisco_SF300_24(ssh, snmp)

        case "iso.3.6.1.4.1.9.6.1.82.48.1":
            return Cisco_SF300_48(ssh, snmp)
        
        case "iso.3.6.1.4.1.9.6.1.83.28.2":
            return Cisco_SG300_28PP(ssh, snmp)

        case "iso.3.6.1.4.1.11.2.3.7.11.184":
            return JL381A_1920S(ssh, snmp)

        case "iso.3.6.1.4.1.171.10.63.6":
            return DES_3028(ssh, snmp)
        
        case "iso.3.6.1.4.1.171.10.63.7":
            return DES_3028P(ssh, snmp)
        
        case "iso.3.6.1.4.1.171.10.64.1":
            return DES_3526(ssh, snmp)
        
        case "iso.3.6.1.4.1.171.10.64.2":
            return DES_3550(ssh, snmp)

        case "iso.3.6.1.4.1.171.10.75.5.2":
            return DES_1210_28_B1(ssh, snmp)

        case "iso.3.6.1.4.1.171.10.75.18.1":
            return DES_1210_28_C1(ssh, snmp)

        case "iso.3.6.1.4.1.674.10895.3063":
            return N1524(ssh, snmp)

        case "iso.3.6.1.4.1.2011.2.23.406":
            return S5720_28X_LI_AC(ssh, snmp)

        case "iso.3.6.1.4.1.2011.2.23.444":
            return S5720_52X_PWR_LI_AC(ssh, snmp)

        case "iso.3.6.1.4.1.11863.1.1.9":
            return TL_SG5412F(ssh, snmp)

        case "iso.3.6.1.4.1.25506.11.1.169":
            return HPE1920_48G(ssh, snmp)
        
        case _:
            print(f"[INFO] Unknown vendor for host {snmp.agent_interface}: {vendor_oid}")
            return None
		#case _:
		#	raise ValueError(f"Unknown vendor: {vendor}. Unpredicdable behavior")