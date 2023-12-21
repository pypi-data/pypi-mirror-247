# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class AccountTaxRuleZoneTestCase(ModuleTestCase):
    "Test Account Tax Rule Zone module"
    module = 'account_tax_rule_zone'


del ModuleTestCase
