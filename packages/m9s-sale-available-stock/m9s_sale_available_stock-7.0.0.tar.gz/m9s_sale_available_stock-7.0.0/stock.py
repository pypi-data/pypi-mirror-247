# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction


class Move(metaclass=PoolMeta):
    __name__ = "stock.move"

    available_qty = fields.Function(
        fields.Float(
            'Available Quantity', digits='unit',
            ), 'on_change_with_available_qty')

    @fields.depends('product', 'planned_date', 'from_location')
    def on_change_with_available_qty(self, name=None):
        """
        Returns the available quantity
        """
        pool = Pool()
        Date = pool.get('ir.date')
        Product = pool.get('product.product')
        today = Date.today()

        if not (self.product and self.from_location):
            return

        warehouse = self.from_location.warehouse or self.to_location.warehouse
        if not warehouse:
            return
        location = warehouse.storage_location

        date = self.planned_date or today
        date = max(date, today)
        with Transaction().set_context(
                locations=[location.id],
                stock_date_end=date,
                stock_assign=True):
            product = Product(self.product.id)
            return product.quantity
