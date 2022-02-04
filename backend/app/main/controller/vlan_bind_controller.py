from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required
from app.main.service.vlan_bind_service import get_all_bindings, create_new_binding,get_a_binding_by_id,delete_a_binding, update_a_binding
from ..util.dto import VlanBindingDto
from typing import Dict, Tuple

api = VlanBindingDto.api
_vlan_binding = VlanBindingDto.vlan_binding

@api.route('/')
class VlanBindingList(Resource):
    @api.doc('list_of_vlan_binding')
    #@token_required
    @api.marshal_list_with(_vlan_binding, envelope='data')
    def get(self):
        """List all vlan bindings"""
        return get_all_bindings()

    @api.expect(_vlan_binding, validate=True)
    @api.response(201, 'Binding successfully created.')
    @api.doc('Create a new vlan binding')
    #@token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Vlan Bind """
        data = request.json
        return create_new_binding(data=data)

@api.route('/<binding_id>')
@api.param('binding_id', 'The Vlan binding identifier')
class VlanBinding(Resource):
    @api.response(404, 'Vlan binding not found.')
    @api.doc('Get a vlan binding')
    @api.marshal_with(_vlan_binding)
    #@token_required
    def get(self, binding_id):
        """Get a vlan binding given its identifier"""
        binding = get_a_binding_by_id(binding_id)
        if not binding:
            api.abort(404)
        else:
            return binding
    @api.doc('Delete a vlan binding')
    #@token_required
    def delete(self, binding_id) -> Tuple[Dict[str, str], int]:
        """Delete a vlan binding give its identifier"""
        return delete_a_binding(binding_id)

    @api.expect(_vlan_binding, validate=True)
    @api.response(200, 'Vlan binding successfully updated.')
    @api.doc('Update a vlan bindding')
    @token_required
    def put(self, binding_id) -> Tuple[Dict[str, str], int]:
        """Update a vlan binding """
        data = request.json
        return update_a_binding(data=data, binding_id=binding_id)






