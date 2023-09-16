from odoo import  models, fields, exceptions, api


class Material(models.Model):
    _name = "restapi.materials"
    _description = "table materials"
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'item duplicate') 
    ]

    code = fields.Char('Material Code', required=True)
    name = fields.Char('Material Name', required=True)
    type = fields.Selection(
        selection=[
            ('fabric', 'Fabric'), ('jeans', 'Jeans'), ('cotton', 'Cotton')
        ],
        default='fabric'
    )
    buy_price = fields.Float(
        string='Material buy price',
        digits=(10, 2),
        required=True
    )
    supplier_id = fields.Many2one(
        comodel_name='restapi.suppliers',
        string='Related Material supplier',
        index=True, ondelete='cascade'
    )

    def validate_material_data(self, vals):
        if not vals.get('code') or not vals.get('name') or not vals.get('type') \
                or not vals.get('buy_price') or not vals.get('supplier_id'):
            raise exceptions.ValidationError("All fields (code, name, type, buy_price, supplier_id) are required.")

        if vals.get('buy_price') <= 100:
            raise exceptions.ValidationError("The 'buy_price' must be greater than 100.")

        supplier_id = vals.get('supplier_id')
        if not self.env['restapi.suppliers'].sudo().search([('id', '=', supplier_id)]):
            raise exceptions.ValidationError("Invalid 'supplier_id'.")
        
    def validate_material_update_data(self, vals):
        if 'code' in vals and not vals['code']:
            raise exceptions.ValidationError("Field 'code' cannot be empty.")
        
        if 'name' in vals and not vals['name']:
            raise exceptions.ValidationError("Field 'name' cannot be empty.")

        if 'buy_price' in vals and vals['buy_price'] <= 100:
            raise exceptions.ValidationError("The 'buy_price' must be greater than 100.")

        if 'supplier_id' in vals and not self.env['restapi.suppliers'].browse(vals['supplier_id']):
            raise exceptions.ValidationError("Invalid 'supplier_id'.")
    
    @api.model
    def create_material(self, vals):
        self.validate_material_data(vals)
        return self.create(vals)
    
    @api.model
    def partial_update_material(self, material_id, vals):
        self.validate_material_update_data(vals)
        material = self.search([('id', '=', material_id)], limit=1)
        if not material:
            raise exceptions.ValidationError("Material not found.")

        material.write(vals)
        return material

    def read(self, material_id):
        return self.browse(material_id)
    
    def show(self, material_id):
        return self.search([('id', '=', material_id)], limit=1)

    def delete(self, material_id):
        material = self.search([('id', '=', material_id)], limit=1)
        if material:
            material.unlink()
            return True
        return False
