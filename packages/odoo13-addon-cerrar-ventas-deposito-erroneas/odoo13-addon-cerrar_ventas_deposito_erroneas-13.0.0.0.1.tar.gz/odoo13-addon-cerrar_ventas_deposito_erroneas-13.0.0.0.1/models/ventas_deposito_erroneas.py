from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

LOCATION_ID_CUSTOMERS = 5
LOCATION_ID_DEPOSITO = 17
ROUTE_ID_DIRECTA = 3

class DerechosAutoriaWizard(models.TransientModel):
    """ Wizard: *** """
    _name = 'venta.dep.erroneas.wizard.descontrol'
    _description = "Wizard Cerrar Ventas Depósito Erróneas"

    def cerrar_ventas_dep_erroneas(self):
        _logger.debug(f"*********************-.-.-.-.-.-.- Hi! ")
        domain = [
            ('location_id', '=', LOCATION_ID_DEPOSITO),  # This is the id of the Location DS/Depósitos
            ('location_dest_id', '=', LOCATION_ID_CUSTOMERS), # This is the id of the Location Partner Locations/Customers
            ('state', '=', 'assigned'),
        ]
        transferencias = self.env['stock.picking'].search(domain)
        
        candidatas = transferencias.filtered(lambda transfer: transfer.sale_id.pricelist_id.route_id.id == ROUTE_ID_DIRECTA)

        for can in candidatas:
            _logger.debug(f"*********************-.-.-.-.-.-.- id transfer candidata: {can.id}")
            _logger.debug(f"*********************-.-.-.-.-.-.- pedido de venta origen de la transfer candidata: {can.origin}")
            _logger.debug(f"*********************-.-.-.-.-.-.- ids de las transfers de la sale order: {can.sale_id.picking_ids}")
            can.action_assign()
            for move_line in can.move_line_ids:
                move_line.qty_done = move_line.product_uom_qty
            can.button_validate()

        _logger.debug(f"*********************-.-.-.-.-.-.- total {len(candidatas)} ")
