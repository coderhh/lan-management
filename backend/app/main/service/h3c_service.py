import getpass
import telnetlib
import os
import logging
import socket

L3SWICH_HOST = "172.16.10.253"
L3SWICH_USER = "admin"
L3SWICH_PASSWORD = "admin"

FIREWALL_HOST = "172.16.10.254"
FIREWALL_USER = "admin"
FIREWALL_PASSWORD = "admin"

logger= logging.getLogger(__name__)
def bind_mac_ip(mac, vlan, ip):
    """Bind mac with static ip address to access internal server on layer-3 switch"""
    tn = telnetlib.Telnet(L3SWICH_HOST)
    vlan = 'vlan'+vlan
    tn.read_until(b"login: ")
    tn.write(L3SWICH_USER.encode('ascii') + b"\n")
    if L3SWICH_PASSWORD:
        tn.read_until(b"Password: ")
        tn.write(L3SWICH_PASSWORD.encode('ascii') + b"\n")

    tn.write(b"sys\n")
    vlan_command = b"dhcp server ip-pool %s\n" % (vlan.encode('ascii'))
    tn.write(vlan_command)
    bind_command = b"static-bind ip-address %s mask 255.255.255.0 hardware-address %s\n" % (ip.encode('ascii'), mac.encode('ascii'))
    tn.write(bind_command)
    tn.write(b"sa f\n")
    tn.write(b"exit\n")
    tn.write(b"exit\n")
    tn.write(b"exit\n")

    print(tn.read_all().decode('ascii'))

def undo_bind_mac_ip(vlan,ip):
    """Remove mac and ip address binding from layer 3 switch"""
    tn = telnetlib.Telnet(L3SWICH_HOST)
    vlan = 'vlan'+vlan
    tn.read_until(b"login: ")
    tn.write(L3SWICH_USER.encode('ascii') + b"\n")
    if L3SWICH_PASSWORD:
        tn.read_until(b"Password: ")
        tn.write(L3SWICH_PASSWORD.encode('ascii') + b"\n")

    tn.write(b"sys\n")
    vlan_command = b"dhcp server ip-pool %s\n" % (vlan.encode('ascii'))
    tn.write(vlan_command)
    un_bind_command = b"undo static-bind ip-address %s\n" % (ip.encode('ascii'))
    tn.write(un_bind_command)
    tn.write(b"sa f\n")
    tn.write(b"exit\n")
    tn.write(b"exit\n")
    tn.write(b"exit\n")

    print(tn.read_all().decode('ascii'))

def get_mac_ip_binding(vlan):
    """Get mac and ip address binding info from layer 3 switch"""
    tn = telnetlib.Telnet(L3SWICH_HOST)
    tn.read_until(b"login: ")
    tn.write(L3SWICH_USER.encode('ascii') + b"\n")
    if L3SWICH_PASSWORD:
        tn.read_until(b"Password: ")
        tn.write(L3SWICH_PASSWORD.encode('ascii') + b"\n")

    tn.write(b"sys\n")
    vlan_command = b"dhcp server ip-pool %s\n" % (vlan.encode('ascii'))
    tn.write(vlan_command)
    tn.write(b"dis th\n")
    n = 1
    while n < 254:
        tn.write(b"\n")
        n = n + 1

    tn.write(b"exit\n")
    tn.write(b"exit\n")
    tn.write(b"exit\n")

    data = tn.read_all().decode('ascii')
    vlan = Vlan()
    vlan.static_bind = []
    for line in data.splitlines():
        line = line.strip()
        if line.startswith("static-bind"):
            vlan.static_bind.append(static_bind_parsor(line))
        elif line.startswith("gateway-list"):
            vlan.gateway_list = gateway_parsor(line)
        elif line.startswith("dns-list"):
            vlan.dns_list = dns_parsor(line)
        elif line.startswith("dhcp"):
            vlan.vlan_name = line.split(' ')[3]
        elif line.startswith("network"):
            vlan.network = line.split(' ')[1]
            vlan.mask = line.split(' ')[3]
        else:
            pass
    tn.close()
    return vlan

class Vlan:
    vlan_name = ""
    gateway_list = []
    network = ""
    mask = ""
    dns_list = []
    static_bind = []

class StaticBind:
    ip_address = ""
    mask = ""
    mac_address = ""

def static_bind_parsor(line):
    line_blocks = line.split(' ')
    staticBind = StaticBind()
    staticBind.ip_address = line_blocks[2]
    staticBind.mac_address = line_blocks[6]
    staticBind.mask = line_blocks[4]
    return staticBind

def gateway_parsor(line):
    line_blocks = line.split(' ')
    gateway = line_blocks[1:]
    return gateway

def dns_parsor(line):
    line_blocks = line.split(' ')
    dns = line_blocks[1:]
    return dns

def create_new_rule_in_lan(rule_num, ip):
    """Permits certain ip on firewall"""
    try:
        logger.info('creating rule {} in lan.'.format(rule_num))
        if not check_connection(FIREWALL_HOST):
            logger.info('Firewall is not reachable')
            return False
        tn = telnetlib.Telnet(FIREWALL_HOST)
        tn.read_until(b"login: ")
        tn.write(FIREWALL_USER.encode('ascii') + b"\n")
        if FIREWALL_PASSWORD:
            tn.read_until(b"Password: ")
            tn.write(FIREWALL_PASSWORD.encode('ascii') + b"\n")

        permit_command = b"rule %s permit ip source %s 0\n" % (rule_num.encode('ascii'), ip.encode('ascii'))
        logger.info(permit_command)
        tn.write(b"sys\n")
        tn.write(b"acl advanced 3002\n")
        tn.write(permit_command)
        tn.write(b"sa f\n")
        tn.write(b"exit\n")
        tn.write(b"exit\n")
        tn.write(b"exit\n")
        logger.info(tn.read_all().decode('ascii'))
        return True
    except Exception as e:
        logger.error(e)
        return False

def delete_rule_from_lan(rule_num):
    """Un-permit ip from firewall"""
    try:
        logger.info('deleting rule {} from lan.'.format(rule_num))
        if not check_connection(FIREWALL_HOST):
             logger.info('Firewall is not reachable')
             return False
        tn = telnetlib.Telnet(FIREWALL_HOST)
        tn.read_until(b"login: ")
        tn.write(FIREWALL_USER.encode('ascii') + b"\n")
        if FIREWALL_PASSWORD:
            tn.read_until(b"Password: ")
            tn.write(FIREWALL_PASSWORD.encode('ascii') + b"\n")
        undo_command = b'undo rule %s\n' % (rule_num.encode('ascii'))
        tn.write(b"sys\n")
        tn.write(b"acl advanced 3002\n")
        tn.write(undo_command)
        tn.write(b"sa f\n")
        tn.write(b"exit\n")
        tn.write(b"exit\n")
        tn.write(b"exit\n")
        logger.info(tn.read_all().decode('ascii'))
        return True
    except Exception as e:
        logger.error(e)
        return False

def get_firewall_rules_from_lan():
    rules = []
    try:
        if not check_connection(FIREWALL_HOST):
             logger.info('Firewall is not reachable')
             return "Firewall is not reachable"
        logger.info('Connecting to firewall....')
        tn = telnetlib.Telnet(FIREWALL_HOST)
        tn.read_until(b"login: ")
        tn.write(FIREWALL_USER.encode('ascii') + b"\n")
        if FIREWALL_PASSWORD:
            tn.read_until(b"Password: ")
            tn.write(FIREWALL_PASSWORD.encode('ascii') + b"\n")
        dis_command = (b'dis th\n')
        tn.write(b"sys\n")
        tn.write(b"acl advanced 3002\n")
        tn.write(dis_command)
        n = 1
        while n < 254:
            tn.write(b"\n")
            n = n + 1

        tn.write(b"exit\n")
        tn.write(b"exit\n")
        tn.write(b"exit\n")

        data = tn.read_all().decode('ascii')

        for line in data.splitlines():
            line = line.strip()
            if line.startswith("rule"):
                rules.append(permit_rule_parsor(line))
            else:
                pass
        tn.close()
        return rules
    except Exception as e:
        logger.error(type(e).__name__)

def permit_rule_parsor(line):
    line_blocks = line.split(' ')
    rule = { "rule_num": line_blocks[1], "ip_address": line_blocks[5]}
    return rule

def check_connection(ip):
    HOST_UP  = True if os.system("ping -c 1 " + ip) is 0 else False
    return HOST_UP

if __name__ == "__main__":
    print("test! test! test!")
    undo_bind_mac_ip("vlan11","192.168.11.8")
    bind_mac_ip("6c2b-5956-90c5","11","192.168.11.8")