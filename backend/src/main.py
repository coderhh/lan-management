from flask import Flask,jsonify
from .services.h3c import get_mac_ip_binding, get_all_firewall_rule
app = Flask(__name__)

@app.route('/lan/api/v1.0/vlan/<string:vlan_id>', methods=['GET'])
def get_mac_ip_bind(vlan_id):
    vlanbindings = get_mac_ip_binding(vlan_id)
    static_bind = []
    
    for bind in vlanbindings.static_bind:
        static_bind.append({"ip_address": bind.ip_address, 
                            "mask": bind.mask, 
                            "mac_address": bind.mac_address
                        })
        
    
    vlan = {
        "vlan_name": vlanbindings.vlan_name,
        "network": vlanbindings.network,
        "dns_list": vlanbindings.dns_list,
        "gateway_list": vlanbindings.gateway_list,
        "mask": vlanbindings.mask,
        "static_bind": static_bind
    }
    return jsonify(vlan)

@app.route('/lan/api/v1.0/firewall/', methods=['GET'])
def get_all_firewall_rules():
    rules = get_all_firewall_rule()

    results = []
    for rule in rules:
        results.append({"rule_num": rule.rule_num, "ip_address": rule.ip_address})
    
    return jsonify({"rules": results})