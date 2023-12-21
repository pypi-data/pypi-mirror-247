# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class ProductAttributeStrictTestCase(ModuleTestCase):
    "Test Product Attribute Strict module"
    module = 'product_attribute_strict'


del ModuleTestCase
