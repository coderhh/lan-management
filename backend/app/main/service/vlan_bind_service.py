from app.main import db
from sqlalchemy.exc import IntegrityError
import datetime
from typing import Dict, Tuple
from app.main.model.vlan import VlanBinding
from app.main.util.dto import VlanBindingDto
from app.main.service.h3c_service import get_bindings_from_lan,delete_binding_from_lan,create_new_binding_in_lan,update_vlan_binding_in_lan

api = VlanBindingDto.api
def get_all_bindings():
    bindings = VlanBinding.query.all()
    if bindings:
       return bindings
    else:
        api.logger.info('No binding found in local database, retriving from switch equipment.....')
        static_bindings = get_bindings_from_lan()
        if not isinstance(static_bindings, str):
            api.logger.info('Writing bindings data into database...')
            return bulk_create_new_bindings(static_bindings)
        else:
            response_object = {
                "error": static_bindings
            }
            return response_object, 500

def bulk_create_new_bindings(bindings):
    try:
        bindings_object = []
        mac_address = []
        for b in bindings:
            new_binding = VlanBinding(
                ip_address = b['ip_address'],
                mac_address = b['mac_address'],
                network_mask = b['mask'],
                vlan_id = get_vlan_id(b['ip_address']),
                created_on = datetime.datetime.now()
            )
            if new_binding.mac_address in mac_address:
                api.logger.warning(new_binding)
                filtered = filter(lambda score: score.mac_address == new_binding.mac_address, bindings_object)
                api.logger.warning(list(filtered))
            mac_address.append(new_binding.mac_address)
            bindings_object.append(new_binding)
        api.logger.info('Total bindings from L3 switch: {}'.format(len(bindings_object)))
        db.session.bulk_save_objects(bindings_object)
        db.session.commit()
        return VlanBinding.query.all()
    except Exception as e:
        api.logger.error(e)

def create_new_binding(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    if not VlanBinding.check_binding(data['ip_address'], data['mac_address']):
        new_binding = VlanBinding(
            ip_address = data['ip_address'],
            mac_address = data['mac_address'],
            network_mask = data['network_mask'],
            vlan_id = get_vlan_id(data['ip_address']),
            created_on = datetime.datetime.now()
        )
        res = create_new_binding_in_lan(new_binding.mac_address,str(new_binding.vlan_id), new_binding.ip_address)
        if not res:
            response_object = {
                'status': 'fail',
                'message': 'failed to save new binding in lan..'
            }
            return response_object, 500
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
        res = delete_binding_from_lan(str(binding.vlan_id), binding.ip_address)
        if not res:
            response_object = {
                'status': 'fail',
                'message': 'can not delete from lan'
            }
            return response_object, 500

        delete_binding_from_database(binding)
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
            new_ip_address = data['ip_address']
            new_mac_address = data['mac_address']
            new_vlan_id = get_vlan_id(data['ip_address'])

            res = update_vlan_binding_in_lan(binding.mac_address,str(binding.vlan_id), binding.ip_address, new_mac_address, new_vlan_id, new_ip_address)
            if not res:
                response_object = {
                    'status': 'fail',
                    'message': 'fail to update the bindings in lan',
                }
                return response_object, 500
            binding.ip_address = new_ip_address
            binding.mac_address = new_mac_address
            binding.network_mask = data['network_mask']
            binding.vlan_id = new_vlan_id
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
    try:
        api.logger.info('creating binding in database...')
        db.session.add(data)
        db.session.commit()
    except IntegrityError as e:
        api.logger.error(e)
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'ip or mac was already bound, please check.',
        }
        return response_object, 500

def delete_binding_from_database(data: VlanBinding):
    api.logger.info('deleting binding from database...')
    db.session.delete(data)
    db.session.commit()
