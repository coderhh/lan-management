#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   firewall_rule_service.py
@Time    :   2022/08/10 11:27:09
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import datetime
from typing import Dict, Tuple

from app.main import db
from app.main.model.firewall import FirewallRule
from app.main.service.h3c_service import (create_new_rule_in_lan,
                                          delete_rule_from_lan,
                                          get_firewall_rules_from_lan)
from app.main.util.dto import FirewallRuleDto

api = FirewallRuleDto.api


def get_all_rules():
    """_summary_

    Returns:
        _type_: _description_
    """
    rules = FirewallRule.query.all()
    if rules:
        return rules
    else:
        api.logger.info(
            'No rules found in local database, retriving from firewall equipment.....'
        )
        rules = get_firewall_rules_from_lan()
        if not isinstance(rules, str):
            api.logger.info('Writing rules data into database...')
            return bulk_create_new_rules(rules)
        else:
            response_object = {"error": rules}
            return response_object, 500


def bulk_create_new_rules(rules):
    """_summary_

    Args:
        rules (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        rules_object = []
        for rule in rules:
            new_rule = FirewallRule(ip_address=rule['ip_address'],
                                    rule_num=rule['rule_num'],
                                    vlan_id=get_vlan_id(rule['ip_address']),
                                    created_on=datetime.datetime.now())
            rules_object.append(new_rule)
        api.logger.info('Total rules get from firewall: %s', len(rules_object))
        db.session.bulk_save_objects(rules_object)
        db.session.commit()
        return rules_object
    except RuntimeError as e_msg:
        api.logger.error(e_msg)


def create_new_rule(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """_summary_

    Args:
        data (Dict[str, str]): _description_

    Returns:
        Tuple[Dict[str, str], int]: _description_
    """
    if not FirewallRule.check_firewall_rule(data['ip_address']):
        new_rule = FirewallRule(ip_address=data['ip_address'],
                                rule_num=get_rule_num(),
                                vlan_id=get_vlan_id(data['ip_address']),
                                created_on=datetime.datetime.now())
        res = create_new_rule_in_lan(str(new_rule.rule_num),
                                     new_rule.ip_address)
        if not res:
            response_object = {
                'status': 'fail',
                'message': 'failed to save new rule in lan..'
            }
            return response_object, 500
        save_changes(new_rule)
        response_object = {
            'status': 'success',
            'message': 'Successfully Created.',
            'rule': str(new_rule)
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'ip already in firewall rule. Please check.',
        }
        return response_object, 409


def get_a_rule_by_rule_num(rule_num):
    """_summary_

    Args:
        rule_num (_type_): _description_

    Returns:
        _type_: _description_
    """
    return FirewallRule.query.filter_by(rule_num=rule_num).first()


def delete_a_rule(rule_num):
    """_summary_

    Args:
        rule_num (_type_): _description_

    Returns:
        _type_: _description_
    """
    rule = get_a_rule_by_rule_num(rule_num)
    if rule:
        res = delete_rule_from_lan(rule_num)
        if not res:
            response_object = {
                'status': 'fail',
                'message': 'can not delete from lan'
            }
            return response_object, 500
        delete_rule_from_database(rule)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Rule not exists.',
        }
        return response_object, 404


def delete_all_rules():
    """_summary_

    Returns:
        _type_: _description_
    """
    try:
        delete_sql = f'DELETE from {FirewallRule.__tablename__}'
        db.session.execute(delete_sql)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
        }
        return response_object, 200
    except RuntimeError as e_msg:
        api.logger.error(e_msg)
        response_object = {
            'status': 'fail',
            'message': 'can not delete from database'
        }
        return response_object, 500


def save_changes(data: FirewallRule):
    """_summary_

    Args:
        data (FirewallRule): _description_
    """
    api.logger.info('creating rule %s in database.', data.rule_num)
    db.session.add(data)
    db.session.commit()


def delete_rule_from_database(data: FirewallRule):
    """_summary_

    Args:
        data (FirewallRule): _description_
    """
    api.logger.info('deleting rule %s from database.', data.rule_num)
    db.session.delete(data)
    db.session.commit()


# helper method
def get_rule_num():
    """_summary_

    Returns:
        _type_: _description_
    """
    api.logger.info('getting rule nums...')
    rule_nums = db.session.query(FirewallRule.rule_num).all()
    rule_nums_arr = []
    for i in rule_nums:
        rule_nums_arr.append(i[0])
    smallest_available_rule_num = first_missing_positive(
        rule_nums_arr, len(rule_nums))
    return smallest_available_rule_num


def first_missing_positive(arr, num_rules):
    """_summary_

    Args:
        arr (_type_): _description_
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    api.logger.info('Total rules: %s.', num_rules)
    for i in range(1, num_rules):
        if i in arr:
            pass
        else:
            return i
    return num_rules + 1


def get_vlan_id(ip_addr: str):
    """_summary_

    Args:
        ip (str): _description_

    Returns:
        _type_: _description_
    """
    vlan_id = str(ip_addr).split('.')[2]
    return vlan_id
