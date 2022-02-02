from app.main import db
from sqlalchemy.exc import IntegrityError
import datetime
from typing import Dict, Tuple
from app.main.model.vlan import VlanBinding
from app.main.util.dto import VlanBindingDto

api = VlanBindingDto.api
def get_all_bindings():
    return VlanBinding.query.all()

def create_new_binding(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    if not VlanBinding.check_binding(data['ip_address'], data['mac_address']):
        new_binding = VlanBinding(
            ip_address = data['ip_address'],
            mac_address = data['mac_address'],
            network_mask = data['network_mask'],
            vlan_id = get_vlan_id(data['ip_address']),
            created_on = datetime.datetime.now()
        )
        save_changes(new_binding)
        response_object = {
            'status': 'success',
            'message': 'Successfully Created.',
            'rule': str(new_binding)
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'ip or mac already in vlan bindings. Please check.',
        }
        return response_object, 409

def get_a_binding_by_id(binding_id):
    return VlanBinding.query.filter_by(id=binding_id).first()

def delete_a_binding(binding_id):
    binding = get_a_binding_by_id(binding_id)
    if binding:
        delete_binding(binding)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Binding not exists.',
        }
        return response_object, 404

def update_a_binding(data: Dict[str, str], binding_id) -> Tuple[Dict[str, str], int]:
    binding = get_a_binding_by_id(binding_id)
    try:
        if binding:
            binding.ip_address = data['ip_address']
            binding.mac_address = data['mac_address']
            binding.network_mask = data['network_mask']
            binding.vlan_id = get_vlan_id(data['ip_address'])
            binding.updated_on = datetime.datetime.now()
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully updated.',
                'bind': str(binding)
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Vlan binding not exists.',
            }
            return response_object, 404
    except IntegrityError as e:
        api.logger.error(e)
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'ip or mac was already bound, please check.',
        }
        return response_object, 500



# helper method
def get_vlan_id(ip: str):
    vlan_id = str(ip).split('.')[2]
    return vlan_id

def save_changes(data: VlanBinding):
    db.session.add(data)
    db.session.commit()
def delete_binding(data: VlanBinding):
    db.session.delete(data)
    db.session.commit()
