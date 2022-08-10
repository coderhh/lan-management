#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   vlan.py
@Time    :   2022/08/10 10:12:49
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

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
        """_summary_

        Returns:
            _type_: _description_
        """
        msg = (f'<binding: ip: {self.ip_address} mac: {self.mac_address} '
               f'created_on: {self.created_on} updated_on: {self.updated_on}')
        return msg

    @staticmethod
    def check_binding(ip_addr: str, mac: str) -> bool:
        """_summary_

        Args:
            ip (str): _description_
            mac (str): _description_

        Returns:
            bool: _description_
        """
        # check whether ip or mac was already binded
        res = VlanBinding.query.filter(
            VlanBinding.ip_address == ip_addr
            or VlanBinding.mac_address == mac).first()
        return bool(res)

    @staticmethod
    def check_binding_id(ip_addr: str, mac: str, binding_id: str) -> bool:
        """_summary_

        Args:
            ip (str): _description_
            mac (str): _description_
            binding_id (str): _description_

        Returns:
            bool: _description_
        """
        # check whether ip or mac was already binded
        res = VlanBinding.query.filter(
            (VlanBinding.ip_address == ip_addr
             or VlanBinding.mac_address == mac)).first()
        resd = res.query.filter(str(VlanBinding.id) != binding_id)
        return bool(resd)
