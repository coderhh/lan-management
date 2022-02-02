from .. import db


class VlanBinding(db.Model):
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

    def __repr__(self):
        return '<binding: ip: {} mac: {} created_on: {} updated_on: {}'.format(self.ip_address, self.mac_address, self.created_on, self.updated_on)

    @staticmethod
    def check_binding(ip: str, mac: str) -> bool:
        # check whether ip or mac was already binded
        res = VlanBinding.query.filter(VlanBinding.ip_address == ip or VlanBinding.mac_address == mac).first()
        if res:
            return True
        else:
            return False

    @staticmethod
    def check_binding_id(ip: str, mac: str, id:str) -> bool:
        # check whether ip or mac was already binded
        res = VlanBinding.query.filter((VlanBinding.ip_address == ip or VlanBinding.mac_address == mac)).first()
        resd = res.query.filter(str(VlanBinding.id) != id)
        if resd:
            return True
        else:
            return False