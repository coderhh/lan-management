from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from h3c import get_mac_ip_binding, get_all_firewall_rule, permit_ip, undo_permit_ip, bind_mac_ip, undo_bind_mac_ip
app = Flask(__name__)
CORS(app)

@app.route('/lan/api/v1.0/vlan/<string:vlan_id>', methods=['GET'])
def get_mac_ip_bind(vlan_id):
    """[summary]

    Args:
        vlan_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    vlan = get_vlan('vlan'+vlan_id)
    return jsonify(vlan)

def get_vlan(rule_num):
    vlanbindings = get_mac_ip_binding(rule_num)
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
    return vlan

@app.route('/lan/api/v1.0/vlan/add/', methods=['POST'])
def add_mac_ip_bind():
    bind = request.get_json()
    vlan_num = bind['vlan']
    ip_address = bind['ip_address']
    mac_address = bind['mac_address']
    
    bind_mac_ip(mac_address, vlan_num, ip_address)

    #vlan = get_vlan(vlan_num)
   
    return jsonify(bind)

@app.route('/lan/api/v1.0/vlan/delete/', methods=['POST'])
def delete_mac_ip_bind():
    bind = request.get_json()
    vlan_num = bind['vlan']
    ip_address = bind['ip_address']
    
    undo_bind_mac_ip(vlan_num, ip_address)   
    #vlan = get_vlan(vlan_num)
    return jsonify(bind)

@app.route('/lan/api/v1.0/firewall/', methods=['GET'])
def get_all_firewall_rules():
    rules = get_all_firewall_rule()

    results = []
    for rule in rules:
        results.append({"rule_num": rule.rule_num, "ip_address": rule.ip_address})
    
    return jsonify({"rules": results})

@app.route('/lan/api/v1.0/firewall/', methods=['POST'])
def add_new_firewall_rule():
    rule = request.get_json()
    rule_num = rule['rule_num']
    ip_address = rule['ip_address']
    permit_ip(rule_num, ip_address)

    return rule, 200

@app.route('/lan/api/v1.0/firewall/delete/<int:_rule_num>', methods=['DELETE'])
def remove_firewall_rule(_rule_num):
    undo_permit_ip(str(_rule_num))

    return   jsonify(_rule_num), 200