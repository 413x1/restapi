# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request, Response
from odoo.exceptions import ValidationError


class Supplier(http.Controller):
    @http.route('/restapi/suppliers', type='json', auth="none", methods=['GET'])
    def list_suppliers(self, **kw):
        suppliers = request.env['restapi.suppliers'].sudo().read()
        supplier_data = []
        for supplier in suppliers:
            supplier_data.append({
                'id': supplier.id,
                'code': supplier.name
            })

        return supplier_data

    @http.route('/restapi/suppliers/<int:supplier_id>', type='json', auth="none", methods=['GET'])
    def detail_supplier(self, supplier_id,  **kw):
        try:
            supplier = request.env['restapi.suppliers'].sudo().show(supplier_id)
            supplier_data = {'id': supplier.id, 'name': supplier.name} if supplier else {}
            return supplier_data
        except Exception as e:
            return {'error': str(e)}

    @http.route('/restapi/suppliers', type='json', auth="none", methods=['POST'], csrf=False)
    def create_supplier(self, **kw):
        try:
            supplier_data = json.loads(request.httprequest.data)
            new_supplier = request.env['restapi.suppliers'].sudo().create(supplier_data)
            response_data = {'id': new_supplier.id, 'message': 'Supplier created successfully'}
            response = Response(json.dumps(response_data), status=201, content_type='application/json')
            return response
        except ValueError:
            return Response(json.dumps({'error': 'Invalid JSON data'}), status=400, content_type='application/json')
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=400, content_type='application/json')

        
class Material(http.Controller):
    @http.route('/restapi/materials/', type='json', auth="none", method=['GET'])
    def list_materials(self, **kw):
        materials = request.env['restapi.materials'].sudo().search([])
        material_data = []
        for material in materials:
            material_data.append({
                'id': material.id,
                'code': material.code,
                'name': material.name,
                'type': material.type,
                'buy_price': material.buy_price,
                'supplier_id': material.supplier_id.id if material.supplier_id else None,
            })
        
        if not material_data:
            return {}

        return material_data

    @http.route('/restapi/materials', type='json', auth="none", methods=['POST'], csrf=False)
    def create_material(self, **kw):
        try:
            material_data = json.loads(request.httprequest.data)
            new_material = request.env['restapi.materials'].sudo().validate_material_data(material_data).create_material(material_data)
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