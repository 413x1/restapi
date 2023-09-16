# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class Material(http.Controller):
    @http.route('/restapi/materials/', type='json', auth="none", method=['GET'])
    def list_materials(self, **kw):
        search_query = []
        if kw.get('type', None):
            search_query.append(('type', '=', kw.pop('type')))

        materials = request.env['restapi.materials'].sudo().search(search_query)
        material_data = []
        for material in materials:
            material_data.append({
                'id': material.id,
                'code': material.code,
                'name': material.name,
                'type': material.type,
                'buy_price': material.buy_price,
                'supplier_id': material.supplier_id.id,
            })

        if not material_data:
            return {}

        return material_data

    @http.route('/restapi/materials', type='json', auth="none", methods=['POST'], csrf=False)
    def create_material(self, **kw):
        try:
            material_data = json.loads(request.httprequest.data)
            new_material = request.env['restapi.materials'].sudo().create_material(material_data)
            response_data = {'id': new_material.id, 'message': 'Material created successfully'}
            
            return response_data
        
        except ValueError:
            return {'error': 'Invalid JSON data'}
        
        except Exception as e:
            return {'error': str(e)}

    @http.route('/restapi/materials/<int:material_id>', type='json', auth="none", methods=['GET'], csrf=False)
    def detail_material(self, material_id, **kw):
        try:
            material_data = request.env['restapi.materials'].sudo().show(material_id)
            
            material = {
                'id': material_data.id,
                'code': material_data.code,
                'name': material_data.name,
                'type': material_data.type,
                'buy_price': material_data.buy_price,
                'supplier_id': material_data.supplier_id,
            }
            response_data = {'message': 'Material updated successfully', 'data': material}
            return response_data

        except ValueError:
            return {'error': 'Invalid JSON data'}

        except Exception as e:
            return {'error': str(e)}

    @http.route('/restapi/materials/<int:material_id>', type='json', auth="none", methods=['PUT', 'PATCH'], csrf=False)
    def partial_update_material(self, material_id, **kw):
        try:
            material_data = json.loads(request.httprequest.data)
            
            # Partial update with validation
            updated_material = request.env['restapi.materials'].sudo().partial_update_material(material_id, material_data)
            
            material = {
                'id': updated_material.id,
                'code': updated_material.code,
                'name': updated_material.name,
                'type': updated_material.type,
                'buy_price': updated_material.buy_price,
                'supplier_id': updated_material.supplier_id,
            }

            response_data = {'message': 'Material updated successfully', 'data': material}
            return response_data

        except ValueError:
            return {'error': 'Invalid JSON data'}

        except ValidationError as e:
            return {'error': str(e)}

        except Exception as e:
            return {'error': str(e)}

    @http.route('/restapi/materials/<int:material_id>', type='json', auth="none", methods=['DELETE'], csrf=False)    
    def delete_material(self, material_id, **kw):
        try:
            deleted = request.env['restapi.materials'].sudo().delete(material_id)
            if deleted:
                return {'message': 'Material deleted successfully'}
            return {'error': 'Not found'}

        except Exception as e:
            return {'error': str(e)}
