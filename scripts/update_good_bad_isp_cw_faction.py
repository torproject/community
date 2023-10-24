import json
import requests

resp = requests.get("https://onionoo.torproject.org/details",
                    timeout=10)
onionoo_data = resp.json()

asn_cw = {}

for relay in onionoo_data['relays']:
    if relay["running"]:
        asn = relay["as"]
        if asn not in asn_cw:
            asn_cw[asn] = 0
        asn_cw[asn] += relay["consensus_weight_fraction"] * 100


with open("databags/good-bad-isps.json", "r") as file:
    isp_list = json.load(file)

for country in isp_list.copy():
    for index, isp in enumerate(isp_list[country]):
        if isp["asn"] in asn_cw:
            cw_fraction = f"{round(asn_cw[isp['asn']], 2)}%"
        else:
            cw_fraction = ""
        isp_list[country][index]["cw_fraction"] = cw_fraction

with open("databags/good-bad-isps.json", "w") as file:
    json.dump(isp_list, file)
