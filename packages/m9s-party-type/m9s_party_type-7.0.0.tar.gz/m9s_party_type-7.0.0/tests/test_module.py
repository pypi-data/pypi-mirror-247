# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class PartyTypeTestCase(ModuleTestCase):
    "Test Party Type module"
    module = 'party_type'


del ModuleTestCase
