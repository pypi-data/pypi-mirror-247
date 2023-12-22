# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class SaleAvailableStockTestCase(ModuleTestCase):
    "Test Sale Available Stock module"
    module = 'sale_available_stock'


del ModuleTestCase
