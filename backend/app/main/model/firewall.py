from .. import db
import datetime

class FirewallRule(db.Model):
    """
    Model for storing firewall rules
    """
    __tablename__ = 'firewall_rule'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(200), unique=True, nullable=False)
    vlan_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime,nullable=False)
    updated_on = db.Column(db.DateTime)

    def __init__(self, ip, vlan_id):
        self.ip_address = ip
        self.vlan_id = vlan_id
        self.created_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: rules: {}'.format(self.ip_address)

    @staticmethod
    def check_firewall_rule(ip: str) -> bool:
        # check whether ip address was already in the firewall rules
        res = FirewallRule.query.filter_by(ip_address=ip).first()
        if res:
            return True
        else:
            return False
