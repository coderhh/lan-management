import datetime
from this import d
from typing import Dict, Tuple
from app.main import db
from app.main.model.firewall import FirewallRule
from app.main.util.dto import FirewallRuleDto

api = FirewallRuleDto.api
def get_all_rules():
    return FirewallRule.query.all()

def create_new_rule(data: Dict[str,str]) -> Tuple[Dict[str, str], int]:
    if not FirewallRule.check_firewall_rule(data['ip_address']):
        new_rule = FirewallRule(
            ip_address = data['ip_address'],
            rule_num = get_rule_num(),
            vlan_id = get_vlan_id(data['ip_address']),
            created_on = datetime.datetime.now()
        )
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
        delete_rule(rule)
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
    db.session.add(data)
    db.session.commit()
def delete_rule(data:FirewallRule):
    db.session.delete(data)
    db.session.commit()


# helper method
def get_rule_num():
    rule_nums = db.session.query(FirewallRule.rule_num).all()
    rule_nums_arr = []
    for i in rule_nums:
        rule_nums_arr.append(i[0])
    smallest_available_rule_num = firstMissingPositive(rule_nums_arr, len(rule_nums))
    return smallest_available_rule_num

def firstMissingPositive(arr, n):
    # Loop to traverse the whole array
    for i in range(n):
        # Loop to check boundary
        # condition and for swapping
        while (arr[i] >= 1 and arr[i] <= n
               and arr[i] != arr[arr[i] - 1]):
            temp = arr[i]
            arr[i] = arr[arr[i] - 1]
            arr[arr[i] - 1] = temp
    # Checking any element which
    # is not equal to i+1
    for i in range(n):
        if (arr[i] != i + 1):
            return i + 1
    # Nothing is present return last index
    return n + 1

def get_vlan_id(ip: str):
    vlan_id = str(ip).split('.')[2]
    return vlan_id