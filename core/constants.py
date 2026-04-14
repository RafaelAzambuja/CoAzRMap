# RFC/ISO
## MIB-2 System

SYS_OBJECT_ID_OID = "1.3.6.1.2.1.1.2.0"
SYS_NAME_OID = ".1.3.6.1.2.1.1.5.0"
SYS_LOCATION_OID = ".1.3.6.1.2.1.1.6.0"

## BRIDGE-MIB

BRIDGE_ADDRESS_OID = ".1.3.6.1.2.1.17.1.1.0"                # dot1dBaseBridgeAddress. Tells us base system MAC.

### Q-BRIDGE-MIB

VLAN_STATIC_ENTRY_OID = ".1.3.6.1.2.1.17.7.1.4.3.1.1"       # dot1qVlanStaticName. STATIC vlan list
VLAN_PORT_VID = "1.3.6.1.2.1.17.7.1.4.5.1.1"                # dot1qPvid
VLAN_UNTAGGED_PORTS = ".1.3.6.1.2.1.17.7.1.4.3.1.4"         # dot1qVlanStaticUntaggedPorts
VLAN_EGRESS_PORTS = ".1.3.6.1.2.1.17.7.1.4.3.1.2"           # dot1qVlanStaticEgressPorts

## INTERFACES

INTERFACE_TYPE_MAP = {
    '1': ("Other", "Other"),
    '6': ("ethernetCsmacd", "Port"),
    '24': ("softwareLoopback", "Loopback"),
    '53': ("propVirtual", "Proprietary"),
    '117': ("gigabitEthernet", "Port"),
    '131': ("tunnel", "Tunnel"),
    '135': ("l2vlan", "VLAN"),
    '136': ("l3ipvlan", "VLAN"),
    '161': ("LAG 802.3ad", "Link Aggregation"),
}

## LLDP

LLDP_CHASSIS_SUBTYPE_MAP = {
    '1': ("chassisComponent", "colon"),
    '2': ("interfaceAlias", "utf8"),
    '3': ("portComponent", "colon"),
    '4': ("macAddress", "colon"),
    '5': ("networkAddress", None),
    '6': ("interfaceName", None),
    '7': ("local", None),
}

LLDP_PORT_SUBTYPE_MAP = {
    '1': ("interfaceAlias", "utf8"),
    '2': ("portComponent", "colon"),
    '3': ("macAddress", "colon"),
    '4': ("networkAddress", None),
    '5': ("interfaceName", "utf8"),
    '6': ("agentCircuitId", "utf8"),
    '7': ("local", None),
}