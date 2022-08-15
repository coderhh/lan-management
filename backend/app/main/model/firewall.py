#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   firewall.py
@Time    :   2022/08/10 10:02:24
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

from .. import db


class FirewallRule(db.Model):
    """
    Model for storing firewall rules
    """
    __tablename__ = 'firewall_rule'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_num = db.Column(db.Integer, unique=True, nullable=False)
    ip_address = db.Column(db.String(200), unique=True, nullable=False)
    vlan_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime)

    def __repr__(self):
        msg = (f'Rule: ip_address: {self.ip_address}'
               f'rule_num: {self.rule_num} vlan_id: {self.vlan_id}')
        return msg

    @staticmethod
    def check_firewall_rule(ip_addr: str) -> bool:
        """_summary_

        Args:
            ip (str): _description_

        Returns:
            bool: _description_
        """
        res = FirewallRule.query.filter_by(ip_address=ip_addr).first()
        return bool(res)
