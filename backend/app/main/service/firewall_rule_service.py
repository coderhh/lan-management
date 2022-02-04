import datetime
from this import d
from typing import Dict, Tuple
from app.main import db
from app.main.model.firewall import FirewallRule
from app.main.util.dto import FirewallRuleDto
from app.main.service.h3c_service import get_firewall_rules_from_lan, delete_rule_from_lan, create_new_rule_in_lan

api = FirewallRuleDto.api
def get_all_rules():
    rules = FirewallRule.query.all()
    if rules:
        return rules
    else:
        api.logger.info('No rules found in local database, retriving from firewall equipment.....')
        rules = get_firewall_rules_from_lan()
        if not isinstance(rules, str):
            api.logger.info('Writing rules data into database...')
            return  bulk_create_new_rules(rules)
        else:
            response_object = {
                "error":rules
            }
            return response_object, 500

def bulk_create_new_rules(rules):
    try:
        rules_object = []
        for r in rules:
            new_rule = FirewallRule(
                ip_address = r['ip_address'],
                rule_num = r['rule_num'],
                vlan_id = get_vlan_id(r['ip_address']),
                created_on = datetime.datetime.now()
            )
            rules_object.append(new_rule)
        api.logger.info('Total rules get from firewall: {}'.format(len(rules_object)))
        db.session.bulk_save_objects(rules_object)
        db.session.commit()
        return rules_object
    except Exception as e:
        api.logger.error(e)

def create_new_rule(data: Dict[str,str]) -> Tuple[Dict[str, str], int]:
    if not FirewallRule.check_firewall_rule(data['ip_address']):
        new_rule = FirewallRule(
            ip_address = data['ip_address'],
            rule_num = get_rule_num(),
            vlan_id = get_vlan_id(data['ip_address']),
            created_on = datetime.datetime.now()
        )
        res = create_new_rule_in_lan(str(new_rule.rule_num), new_rule.ip_address)
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
    return FirewallRule.query.filter_by(rule_num=rule_num).first()

def delete_a_rule(rule_num):
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

def save_changes(data: FirewallRule):
    api.logger.info('creating rule {} in database.'.format(data.rule_num))
    db.session.add(data)
    db.session.commit()
def delete_rule_from_database(data:FirewallRule):
    api.logger.info('deleting rule {} from database.'.format(data.rule_num))
    db.session.delete(data)
    db.session.commit()


# helper method
def get_rule_num():
    api.logger.info('getting rule nums...')
    rule_nums = db.session.query(FirewallRule.rule_num).all()
    rule_nums_arr = []
    for i in rule_nums:
        rule_nums_arr.append(i[0])
    smallest_available_rule_num = firstMissingPositive(rule_nums_arr, len(rule_nums))
    return smallest_available_rule_num

def firstMissingPositive(arr, n):
    api.logger.info('Total rules: {}.'.format(n))
    for i in range(1,n):
        if i in arr:
            pass
        else:
            return i
    return n + 1

def get_vlan_id(ip: str):
    vlan_id = str(ip).split('.')[2]
    return vlan_id