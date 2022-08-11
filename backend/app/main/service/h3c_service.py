#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   h3c_service.py
@Time    :   2022/08/11 22:34:22
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import logging
import os
import telnetlib

from ..config import LANConfig

L3SWICH_HOST = LANConfig.L3SWICH_HOST
L3SWICH_USER = LANConfig.L3SWICH_USER
L3SWICH_PASSWORD = LANConfig.L3SWICH_PASSWORD

FIREWALL_HOST = LANConfig.FIREWALL_HOST
FIREWALL_USER = LANConfig.FIREWALL_USER
FIREWALL_PASSWORD = LANConfig.FIREWALL_PASSWORD

logger = logging.getLogger(__name__)


def create_new_binding_in_lan(mac, vlan, ip_addr):
    """Bind mac with static ip_addr address to access internal server on layer-3 switch"""
    try:
        if not check_connection(L3SWICH_HOST):
            logger.warning('L3 Switch is not reachable')
            return "L3 Switch is not reachable"
        t_n = telnetlib.Telnet(L3SWICH_HOST)
        vlan = 'vlan' + vlan
        t_n.read_until(b"login: ")
        t_n.write(L3SWICH_USER.encode('ascii') + b"\n")
        if L3SWICH_PASSWORD:
            t_n.read_until(b"Password: ")
            t_n.write(L3SWICH_PASSWORD.encode('ascii') + b"\n")

        t_n.write(b"sys\n")
        vlan_command = b"dhcp server ip_addr-pool %s\n" % (
            vlan.encode('ascii'))
        t_n.write(vlan_command)
        bind_cmd = b"static-bind ip_addr-address %s mask 255.255.255.0 hardware-address %s\n" % (
            ip_addr.encode('ascii'), mac.encode('ascii'))
        t_n.write(bind_cmd)
        t_n.write(b"sa f\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")

        logger.info(t_n.read_all().decode('ascii'))
        return True
    except RuntimeError as e_msg:
        logger.error(e_msg)
        return False


def update_vlan_binding_in_lan(update_dic):
    """_summary_

    Args:
        update_dic (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        if delete_binding_from_lan(update_dic["vlan_id"],
                                   update_dic["ip_address"]):
            return bool(
                create_new_binding_in_lan(update_dic["new_mac_address"],
                                          update_dic["new_vlan_id"],
                                          update_dic["new_ip_address"]))
        else:
            return False
    except RuntimeError as e_msg:
        logger.error(e_msg)
        return False


def delete_binding_from_lan(vlan, ip_addr):
    """Remove mac and ip_addr address binding from layer 3 switch"""
    try:
        if not check_connection(L3SWICH_HOST):
            logger.warning('L3 Switch is not reachable')
            return "L3 Switch is not reachable"
        t_n = telnetlib.Telnet(L3SWICH_HOST)
        vlan = 'vlan' + vlan
        t_n.read_until(b"login: ")
        t_n.write(L3SWICH_USER.encode('ascii') + b"\n")
        if L3SWICH_PASSWORD:
            t_n.read_until(b"Password: ")
            t_n.write(L3SWICH_PASSWORD.encode('ascii') + b"\n")

        t_n.write(b"sys\n")
        vlan_command = b"dhcp server ip_addr-pool %s\n" % (
            vlan.encode('ascii'))
        t_n.write(vlan_command)
        un_bind_command = b"undo static-bind ip_addr-address %s\n" % (
            ip_addr.encode('ascii'))
        t_n.write(un_bind_command)
        t_n.write(b"sa f\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        logger.info(t_n.read_all().decode('ascii'))
        return True
    except RuntimeError as e_msg:
        logger.error(e_msg)
        return False


def get_bindings_from_lan():
    """_summary_

    Returns:
        _type_: _description_
    """
    try:

        if not check_connection(L3SWICH_HOST):
            logger.warning('L3 Switch is not reachable')
            return "L3 Switch is not reachable"
        vlan10 = get_vlan('vlan10')
        vlan11 = get_vlan('vlan11')
        vlan13 = get_vlan('vlan13')
        static_bindings = [
            *vlan10.static_bind, *vlan11.static_bind, *vlan13.static_bind
        ]
        return static_bindings
    except RuntimeError as e_msg:
        logger.error(e_msg)
        return "internal error"


def get_vlan(vlan):
    """Get mac and ip_addr address binding info from layer 3 switch"""
    try:
        logger.info('getting data for %s', vlan)
        t_n = telnetlib.Telnet(L3SWICH_HOST)
        t_n.read_until(b"login: ")
        t_n.write(L3SWICH_USER.encode('ascii') + b"\n")
        if L3SWICH_PASSWORD:
            t_n.read_until(b"Password: ")
            t_n.write(L3SWICH_PASSWORD.encode('ascii') + b"\n")

        t_n.write(b"sys\n")
        vlan_command = b"dhcp server ip_addr-pool %s\n" % (
            vlan.encode('ascii'))
        t_n.write(vlan_command)
        t_n.write(b"dis th\n")
        n_n = 1
        while n_n < 254:
            t_n.write(b"\n")
            n_n = n_n + 1

        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")

        data = t_n.read_all().decode('ascii')
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
        t_n.close()
        return vlan
    except RuntimeError as e_msg:
        logger.error(e_msg)


class Vlan:
    """_summary_
    """
    vlan_name = ""
    gateway_list = []
    network = ""
    mask = ""
    dns_list = []
    static_bind = []


class StaticBind:
    """_summary_
    """
    ip_address = ""
    mask = ""
    mac_address = ""


def static_bind_parsor(line):
    """_summary_

    Args:
        line (_type_): _description_

    Returns:
        _type_: _description_
    """
    line_blocks = line.split(' ')
    static_bind = {
        'ip_address': line_blocks[2],
        'mac_address': line_blocks[6],
        'mask': line_blocks[4]
    }
    return static_bind


def gateway_parsor(line):
    """_summary_

    Args:
        line (_type_): _description_

    Returns:
        _type_: _description_
    """
    line_blocks = line.split(' ')
    gateway = line_blocks[1:]
    return gateway


def dns_parsor(line):
    """_summary_

    Args:
        line (_type_): _description_

    Returns:
        _type_: _description_
    """
    line_blocks = line.split(' ')
    dns = line_blocks[1:]
    return dns


def create_new_rule_in_lan(rule_num, ip_addr):
    """Permits certain ip_addr on firewall"""
    try:
        logger.info('creating rule %s in lan.', rule_num)
        if not check_connection(FIREWALL_HOST):
            logger.warning('Firewall is not reachable')
            return False
        t_n = telnetlib.Telnet(FIREWALL_HOST)
        t_n.read_until(b"login: ")
        t_n.write(FIREWALL_USER.encode('ascii') + b"\n")
        if FIREWALL_PASSWORD:
            t_n.read_until(b"Password: ")
            t_n.write(FIREWALL_PASSWORD.encode('ascii') + b"\n")

        permit_command = b"rule %s permit ip_addr source %s 0\n" % (
            rule_num.encode('ascii'), ip_addr.encode('ascii'))
        logger.info(permit_command)
        t_n.write(b"sys\n")
        t_n.write(b"acl advanced 3002\n")
        t_n.write(permit_command)
        t_n.write(b"sa f\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        logger.info(t_n.read_all().decode('ascii'))
        return True
    except RuntimeError as e_msg:
        logger.error(e_msg)
        return False


def delete_rule_from_lan(rule_num):
    """Un-permit ip_addr from firewall"""
    try:
        logger.info('deleting rule %s from lan.', rule_num)
        if not check_connection(FIREWALL_HOST):
            logger.warning('Firewall is not reachable')
            return False
        t_n = telnetlib.Telnet(FIREWALL_HOST)
        t_n.read_until(b"login: ")
        t_n.write(FIREWALL_USER.encode('ascii') + b"\n")
        if FIREWALL_PASSWORD:
            t_n.read_until(b"Password: ")
            t_n.write(FIREWALL_PASSWORD.encode('ascii') + b"\n")
        undo_command = b'undo rule %s\n' % (rule_num.encode('ascii'))
        t_n.write(b"sys\n")
        t_n.write(b"acl advanced 3002\n")
        t_n.write(undo_command)
        t_n.write(b"sa f\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        logger.info(t_n.read_all().decode('ascii'))
        return True
    except RuntimeError as e_msg:
        logger.error(e_msg)
        return False


def get_firewall_rules_from_lan():
    """_summary_

    Returns:
        _type_: _description_
    """
    rules = []
    try:
        if not check_connection(FIREWALL_HOST):
            logger.warning('Firewall is not reachable')
            return "Firewall is not reachable"
        logger.info('Connecting to firewall....')
        t_n = telnetlib.Telnet(FIREWALL_HOST)
        t_n.read_until(b"login: ")
        t_n.write(FIREWALL_USER.encode('ascii') + b"\n")
        if FIREWALL_PASSWORD:
            t_n.read_until(b"Password: ")
            t_n.write(FIREWALL_PASSWORD.encode('ascii') + b"\n")
        dis_command = (b'dis th\n')
        t_n.write(b"sys\n")
        t_n.write(b"acl advanced 3002\n")
        t_n.write(dis_command)
        n_n = 1
        while n_n < 254:
            t_n.write(b"\n")
            n_n = n_n + 1

        t_n.write(b"exit\n")
        t_n.write(b"exit\n")
        t_n.write(b"exit\n")

        data = t_n.read_all().decode('ascii')

        for line in data.splitlines():
            line = line.strip()
            if line.startswith("rule"):
                rules.append(permit_rule_parsor(line))
            else:
                pass
        t_n.close()
        return rules
    except RuntimeError as e_msg:
        logger.error(type(e_msg).__name__)


def permit_rule_parsor(line):
    """_summary_

    Args:
        line (_type_): _description_

    Returns:
        _type_: _description_
    """
    line_blocks = line.split(' ')
    rule = {"rule_num": line_blocks[1], "ip_address": line_blocks[5]}
    return rule


def check_connection(ip_addr):
    """_summary_

    Args:
        ip_addr (_type_): _description_

    Returns:
        _type_: _description_
    """
    host_up = True if os.system("ping -c 1 " + ip_addr) == 0 else False
    return host_up


if __name__ == "__main__":
    print("test! test! test!")
