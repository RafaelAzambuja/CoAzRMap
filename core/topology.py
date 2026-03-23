from collections import defaultdict
from main import get_hosts, create_hosts

def build_fdb_graph(cfg_file, json_data, local_macs):
    """
    Retorna:
    graph[switch_ip][port][vlan]["reachable_macs"] = { mac: remote_ip }
    """

    graph = {}

    for item in json_data.get("Switch", []):
        host_ip = item["Host SNMP Agent Interface"]

        host_objs = get_hosts(cfg_file, [host_ip])
        host_objs = create_hosts(host_objs)
        switch = host_objs[0]

        graph.setdefault(host_ip, {})

        for vlan in item["VLANs"]:
            vid = vlan["VID"]

            for possible_neighbor_ip, possible_neighbor_interface in local_macs.items():
                if host_ip == possible_neighbor_ip:
                    continue
                for interface_entry in possible_neighbor_interface:
                    mac = interface_entry["MAC"]
                    if not mac or mac == "00:00:00:00:00:00":
                        continue
                    if interface_entry["Address"] == "127.0.0.1":
                        continue

                    port = switch.find_host_port(vid, mac)
                    if not port:
                        continue

                    graph.setdefault(host_ip, {})
                    graph[host_ip].setdefault(port, {
                        "vlans": {}
                    })
                    graph[host_ip][port]["vlans"].setdefault(vid, {
                        "reachable_macs": {}
                    })

                    graph[host_ip][port]["vlans"][vid]["reachable_macs"][mac] = interface_entry["Address"]

    return graph

def build_mac_index(local_macs):
    mac_index = {}
    for switch_ip, entries in local_macs.items():
        for entry in entries:
            if entry["MAC"]:
                mac_index[entry["MAC"]] = switch_ip
    return mac_index

def switch_sees_mac(graph, switch_ip, target_mac):
    if switch_ip not in graph:
        return None

    for port, pdata in graph[switch_ip].items():
        for vlan, vdata in pdata["vlans"].items():
            if target_mac in vdata["reachable_macs"]:
                return port
    return None


def discover_neighbors(graph, local_macs):
    mac_index = build_mac_index(local_macs)
    topology = {}
    visited = set()

    for root in graph.keys():
        if root not in visited:
            _dfs_discover(
                root,
                graph,
                local_macs,
                mac_index,
                topology,
                visited
            )

    return topology

def _dfs_discover(
    current,
    graph,
    local_macs,
    mac_index,
    topology,
    visited
):
    visited.add(current)
    topology.setdefault(current, {"neighbors": {}})

    current_macs = {
        entry["MAC"]
        for entry in local_macs.get(current, [])
        if entry["MAC"]
    }

    for local_port, pdata in graph[current].items():
        for vlan, vdata in pdata["vlans"].items():
            for mac, remote_ip in vdata["reachable_macs"].items():

                # MAC não pertence a um switch conhecido
                if mac not in mac_index:
                    continue

                neighbor = mac_index[mac]

                # evitar laços triviais
                if neighbor == current:
                    continue

                # reciprocidade
                remote_port = switch_sees_mac(
                    graph,
                    neighbor,
                    next(iter(current_macs), None)
                )

                if not remote_port:
                    continue

                # registrar relação
                topology[current]["neighbors"][neighbor] = {
                    "local_port": local_port,
                    "remote_port": remote_port
                }

                # recursão
                if neighbor not in visited:
                    _dfs_discover(
                        neighbor,
                        graph,
                        local_macs,
                        mac_index,
                        topology,
                        visited
                    )