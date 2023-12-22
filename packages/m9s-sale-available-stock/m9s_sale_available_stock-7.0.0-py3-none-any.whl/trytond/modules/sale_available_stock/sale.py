# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Or
from trytond.transaction import Transaction


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    available_stock_qty = fields.Function(
        fields.Float(
            'Available Quantity', digits='unit',
            states={
                'invisible': Or(
                    Eval('type') != 'line',
                    Eval('sale_state') == 'done'
                    ),
                }),
        'on_change_with_available_stock_qty')

    @fields.depends(
        '_parent_sale.warehouse', '_parent_sale.sale_date',
        'sale', 'product', 'type')
    def on_change_with_available_stock_qty(self, name=None):
        """
        Returns the available stock to process a sale
        """
        pool = Pool()
        Date = pool.get('ir.date')
        Product = pool.get('product.product')
        today = Date.today()

        # If a date is specified on sale, use that. If not, use the
        # current date.
        date = self.sale_date or today

        # If the sales person is taking an order for a date in the past
        # (which tryton allows), the stock cannot be of the past, but of
        # the current date.
        date = max(date, today)

        warehouse_id = self.warehouse and self.warehouse.id
        if self.type == 'line' and self.product and warehouse_id:
            with Transaction().set_context(
                    locations=[warehouse_id],       # sale warehouse
                    stock_skip_warehouse=True,      # quantity of storage only
                    stock_date_end=date,            # Stock as of sale date
                    stock_assign=True):             # Exclude Assigned
                product = Product(self.product.id)
                if date <= today:
                    return product.quantity
                else:
                    # For a sale in the future, it is more interesting to
                    # see the forecasted quantity rather than what is
                    # currently in the warehouse.
                    return product.forecast_quantity
