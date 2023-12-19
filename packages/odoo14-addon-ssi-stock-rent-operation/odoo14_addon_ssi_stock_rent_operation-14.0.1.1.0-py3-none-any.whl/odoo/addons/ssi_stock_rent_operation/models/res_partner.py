# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner"]

    customer_rent_location_id = fields.Many2one(
        string="Customer Rent Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
    supplier_rent_location_id = fields.Many2one(
        string="Supplier Rent Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
