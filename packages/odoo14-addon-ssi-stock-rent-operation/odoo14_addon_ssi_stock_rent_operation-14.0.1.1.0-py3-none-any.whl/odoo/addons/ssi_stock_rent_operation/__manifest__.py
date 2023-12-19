# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Donation Inventory Operation",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_stock",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "data/location_type_data.xml",
        "data/stock_location_data.xml",
        "data/ir_property_data.xml",
        "data/stock_picking_type_category_data.xml",
        "views/res_partner_views.xml",
        "views/customer_rent_out_views.xml",
        "views/customer_rent_in_views.xml",
        "views/supplier_rent_out_views.xml",
        "views/supplier_rent_in_views.xml",
    ],
    "demo": [],
}
