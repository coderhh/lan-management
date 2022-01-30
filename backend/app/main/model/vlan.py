from ipaddress import ip_address
from .. import db
import datetime


class VlanBind(db.Model):
    """
     Model for storing vlan binding
    """
    __tablename__ = 'vlan_binding'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(100), unique=True, nullable=False)
    mac_address = db.Column(db.String(100), unique=True, nullable=False)
    network_mask = db.Column(db.String(100), nullable=False)
    vlan_id = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime)
    def __init__(self, ip, mac_address, mask, vlan_id):
        self.ip_address = ip
        self.mac_address = mac_address
        self.network_mask = mask
        self.vlan_id = vlan_id
        self.created_on = datetime.datetime.now()

    def __repr__(self):
        return '<binding: ip: {} mac: {}'.format(self.ip_address, self.mac_address)

    @staticmethod
    def check_binding(ip: str, mac: str) -> bool:
        # check whether ip or mac was already binded
        res = VlanBind.query.filter(VlanBind.ip_address == ip or VlanBind.mac_address == mac ).any()
        if res:
            return True
        else:
            return False
