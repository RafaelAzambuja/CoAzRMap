import json

with open("output/map.json", 'r') as f:
      data = json.load(f)

for i in data.values():
    print(i)
    for j in i:
      print(j['Host System Name'])
# types = list(data.keys())  # List of the dictionary keys
# hosts = []

# host_macs = {}

# for item in data.get("Switch", []):
#     #print(f"{item["IP Addresses"]["IPv4"]["Address"]};{item["IP Addresses"]["IPv4"]["MAC Address"]}")
#     host_address = item["Host SNMP Agent Interface"]
#     for ipentry in item["IP Addresses"]["IPv4"]:
#         if ipentry["Address"] == "127.0.0.1" or ipentry["MAC Address"] == "00:00:00:00:00:00":
#             continue
#         host_macs[host_address] = {
#             "Address": ipentry["Address"],
#             "MAC": ipentry["MAC Address"]
#         }

# print(host_macs)

# for item in data.get("Switch", []):
#     for vid in item["VLANs"]:
#         print(vid["VID"])

# data = {
#   "10.10.0.11": [
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.12": [
#     {
#       "Local Port": "25",
#       "Neighbor IP": "10.10.0.16",
#       "Neighbor MAC": "1C:AF:F7:6C:5A:E1",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "25",
#       "Neighbor IP": "10.10.0.11",
#       "Neighbor MAC": "F0:7D:68:FF:1A:28",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.15",
#       "Neighbor MAC": "00:1E:58:99:30:96",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.19",
#       "Neighbor MAC": "00:1C:F0:8E:96:63",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.21",
#       "Neighbor MAC": "00:1E:58:99:30:9F",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "28",
#       "Neighbor IP": "10.10.0.22",
#       "Neighbor MAC": "00:1E:58:99:30:8E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "25",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "25",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "15",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "50",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "200"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "201"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "202"
#     },
#     {
#       "Local Port": "25",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "216"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "218"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "230"
#     }
#   ],
#   "10.10.0.13": [
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.15": [
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.16": [
#     {
#       "Local Port": "28",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "28",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "28",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "28",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "28",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "28",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "216"
#     }
#   ],
#   "10.10.0.19": [
#     {
#       "Local Port": "49",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "49",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "49",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "49",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "49",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.21": [
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.22": [
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "200"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "201"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "202"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "230"
#     }
#   ],
#   "10.10.0.23": [
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.24": [
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.25": [
#     {
#       "Local Port": "1",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "1",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "1",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "1",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "1",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.27": [
#     {
#       "Local Port": "24",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "24",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "24",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "24",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "24",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "24",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "24",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.28": [
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "200"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "201"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "202"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "230"
#     }
#   ],
#   "10.10.0.29": [],
#   "10.10.0.31": [
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.32": [
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.33": [],
#   "10.10.0.34": [
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     }
#   ],
#   "10.10.0.35": [
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "200"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "201"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "202"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "216"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "230"
#     }
#   ],
#   "10.10.0.36": [
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "200"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "216"
#     },
#     {
#       "Local Port": "52",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "230"
#     }
#   ],
#   "10.10.0.37": [
#     {
#       "Local Port": "76",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "200"
#     },
#     {
#       "Local Port": "76",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "201"
#     },
#     {
#       "Local Port": "76",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "202"
#     }
#   ],
#   "10.10.0.38": [],
#   "10.10.0.40": [
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "216"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "230"
#     }
#   ],
#   "10.10.0.41": [
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "48",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "230"
#     }
#   ],
#   "10.10.0.43": [],
#   "10.10.0.47": [],
#   "10.10.0.48": [],
#   "10.10.0.49": [
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.50",
#       "Neighbor MAC": "68:4F:64:D9:0D:6E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "200"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "201"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "202"
#     },
#     {
#       "Local Port": "26",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "230"
#     }
#   ],
#   "10.10.0.50": [
#     {
#       "Local Port": "23",
#       "Neighbor IP": "10.10.0.13",
#       "Neighbor MAC": "CC:B2:55:B2:A8:9E",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "23",
#       "Neighbor IP": "10.10.0.33",
#       "Neighbor MAC": "10:BD:18:87:94:3D",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "23",
#       "Neighbor IP": "10.10.0.36",
#       "Neighbor MAC": "58:0A:20:9A:8C:70",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "23",
#       "Neighbor IP": "10.10.0.35",
#       "Neighbor MAC": "58:0A:20:9A:83:54",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "23",
#       "Neighbor IP": "10.10.0.49",
#       "Neighbor MAC": "D0:67:26:FD:CC:68",
#       "VLAN": "1"
#     },
#     {
#       "Local Port": "23",
#       "Neighbor IP": "10.10.0.31",
#       "Neighbor MAC": "CC:B2:55:B2:74:DE",
#       "VLAN": "1"
#     }
#   ]
# }

# for x,y in data.items():
#     print(x)
#     for j in y:
#         print(j)


# {
#   "10.10.0.11": {
#     "neighbors": {}
#   },
#   "10.10.0.15": {
#     "neighbors": {}
#   },
#   "10.10.0.12": {
#     "neighbors": {
#       "10.10.0.23": {
#         "local_port": "13",
#         "remote_port": "48"
#       }
#     }
#   },
#   "10.10.0.23": {
#     "neighbors": {
#       "10.10.0.12": {
#         "local_port": "48",
#         "remote_port": "13"
#       }
#     }
#   },
#   "10.10.0.19": {
#     "neighbors": {}
#   },
#   "10.10.0.16": {
#     "neighbors": {}
#   },
#   "10.10.0.21": {
#     "neighbors": {}
#   },
#   "10.10.0.22": {
#     "neighbors": {}
#   },
#   "10.10.0.25": {
#     "neighbors": {}
#   },
#   "10.10.0.27": {
#     "neighbors": {}
#   },
#   "10.10.0.24": {
#     "neighbors": {}
#   },
#   "10.10.0.13": {
#     "neighbors": {
#       "10.10.0.36": {
#         "local_port": "26",
#         "remote_port": "48"
#       },
#       "10.10.0.35": {
#         "local_port": "26",
#         "remote_port": "52"
#       },
#       "10.10.0.49": {
#         "local_port": "26",
#         "remote_port": "26"
#       },
#       "10.10.0.31": {
#         "local_port": "26",
#         "remote_port": "26"
#       }
#     }
#   },
#   "10.10.0.36": {
#     "neighbors": {
#       "10.10.0.31": {
#         "local_port": "52",
#         "remote_port": "26"
#       },
#       "10.10.0.13": {
#         "local_port": "48",
#         "remote_port": "26"
#       }
#     }
#   },
#   "10.10.0.31": {
#     "neighbors": {
#       "10.10.0.13": {
#         "local_port": "26",
#         "remote_port": "26"
#       },
#       "10.10.0.36": {
#         "local_port": "26",
#         "remote_port": "52"
#       },
#       "10.10.0.35": {
#         "local_port": "26",
#         "remote_port": "52"
#       },
#       "10.10.0.37": {
#         "local_port": "26",
#         "remote_port": "76"
#       },
#       "10.10.0.49": {
#         "local_port": "26",
#         "remote_port": "26"
#       },
#       "10.10.0.50": {
#         "local_port": "26",
#         "remote_port": "23"
#       }
#     }
#   },
#   "10.10.0.35": {
#     "neighbors": {
#       "10.10.0.31": {
#         "local_port": "52",
#         "remote_port": "26"
#       },
#       "10.10.0.13": {
#         "local_port": "52",
#         "remote_port": "26"
#       }
#     }
#   },
#   "10.10.0.37": {
#     "neighbors": {
#       "10.10.0.31": {
#         "local_port": "76",
#         "remote_port": "26"
#       }
#     }
#   },
#   "10.10.0.49": {
#     "neighbors": {
#       "10.10.0.13": {
#         "local_port": "26",
#         "remote_port": "26"
#       },
#       "10.10.0.50": {
#         "local_port": "26",
#         "remote_port": "23"
#       },
#       "10.10.0.31": {
#         "local_port": "26",
#         "remote_port": "26"
#       }
#     }
#   },
#   "10.10.0.50": {
#     "neighbors": {
#       "10.10.0.49": {
#         "local_port": "23",
#         "remote_port": "26"
#       },
#       "10.10.0.31": {
#         "local_port": "23",
#         "remote_port": "26"
#       }
#     }
#   },
#   "10.10.0.29": {
#     "neighbors": {}
#   },
#   "10.10.0.32": {
#     "neighbors": {
#       "10.10.0.40": {
#         "local_port": "48",
#         "remote_port": "48"
#       }
#     }
#   },
#   "10.10.0.40": {
#     "neighbors": {
#       "10.10.0.32": {
#         "local_port": "48",
#         "remote_port": "48"
#       },
#       "10.10.0.34": {
#         "local_port": "48",
#         "remote_port": "48"
#       }
#     }
#   },
#   "10.10.0.34": {
#     "neighbors": {
#       "10.10.0.40": {
#         "local_port": "48",
#         "remote_port": "48"
#       }
#     }
#   },
#   "10.10.0.33": {
#     "neighbors": {}
#   },
#   "10.10.0.47": {
#     "neighbors": {}
#   },
#   "10.10.0.48": {
#     "neighbors": {}
#   },
#   "10.10.0.28": {
#     "neighbors": {}
#   },
#   "10.10.0.43": {
#     "neighbors": {}
#   },
#   "10.10.0.38": {
#     "neighbors": {}
#   },
#   "10.10.0.41": {
#     "neighbors": {}
#   }
# }