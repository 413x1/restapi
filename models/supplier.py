from odoo import models, fields


class Supplier(models.Model):
    _name = "restapi.suppliers"
    _description = "table suppliers"

    name = fields.Char('Supplier Name', required=True)
    
    def read(self):
        return self.search([])

    def create(self, vals):
        new_supplier = super(Supplier, self).create(vals)
        return new_supplier

    def show(self, supplier_id):
        return self.search([('id', '=', supplier_id)], limit=1)

    def update(self, supplier_id, vals):
        supplier = self.search([('id', '=', supplier_id)], limit=1)
        if supplier:
            supplier.write(vals)
            return True
        return False

    def delete(self, supplier_id):
        supplier = self.search([('id', '=', supplier_id)], limit=1)
        if supplier:
            supplier.unlink()
            return True
        return False