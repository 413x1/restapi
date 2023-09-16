from odoo import http
from odoo.http import request, Response
import json


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