import telnetlib
import os
import logging
from ..config import LANConfig

L3SWICH_HOST = LANConfig.L3SWICH_HOST
L3SWICH_USER = LANConfig.L3SWICH_USER
L3SWICH_PASSWORD = LANConfig.L3SWICH_PASSWORD

FIREWALL_HOST = LANConfig.FIREWALL_HOST
FIREWALL_USER = LANConfig.FIREWALL_USER
FIREWALL_PASSWORD = LANConfig.FIREWALL_PASSWORD

logger= logging.getLogger(__name__)

def create_new_binding_in_lan(mac, vlan, ip):
    """Bind mac with static ip address to access internal server on layer-3 switch"""
    try:
        if not check_connection(L3SWICH_HOST):
            logger.warning('L3 Switch is not reachable')
            return "L3 Switch is not reachable"
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

        logger.info(tn.read_all().decode('ascii'))
        return True
    except Exception as e:
        logger.error(e)
        return False

def update_vlan_binding_in_lan(old_mac, old_vlan, old_ip, new_mac, new_vlan, new_ip):
    try:
        if delete_binding_from_lan(old_vlan, old_ip):
            if create_new_binding_in_lan(new_mac, new_vlan, new_ip):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        logger.error(e)
        return False

def delete_binding_from_lan(vlan,ip):
    """Remove mac and ip address binding from layer 3 switch"""
    try:
        if not check_connection(L3SWICH_HOST):
            logger.warning('L3 Switch is not reachable')
            return "L3 Switch is not reachable"
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
        logger.info(tn.read_all().decode('ascii'))
        return True
    except Exception as e:
        logger.error(e)
        return False

def get_bindings_from_lan():
    try:

        if not check_connection(L3SWICH_HOST):
            logger.warning('L3 Switch is not reachable')
            return "L3 Switch is not reachable"
        vlan10 = get_vlan('vlan10')
        vlan11 = get_vlan('vlan11')
        vlan13 = get_vlan('vlan13')
        static_bindings = [*vlan10.static_bind, *vlan11.static_bind, *vlan13.static_bind]
        return static_bindings
    except Exception as e:
        logger.error(e)
        return "internal error"

def get_vlan(vlan):
    """Get mac and ip address binding info from layer 3 switch"""
    try:
        logger.info('getting data for {}'.format(vlan))
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
    except Exception as e:
        logger.error(e)

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
    static_bind = {
        'ip_address': line_blocks[2],
        'mac_address': line_blocks[6],
        'mask' : line_blocks[4]
    }
    return static_bind

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
            logger.warning('Firewall is not reachable')
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
             logger.warning('Firewall is not reachable')
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
             logger.warning('Firewall is not reachable')
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
    HOST_UP  = True if os.system("ping -c 1 " + ip) == 0 else False
    return HOST_UP

if __name__ == "__main__":
    print("test! test! test!")