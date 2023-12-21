# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class PartyAddressTypeStrictTestCase(ModuleTestCase):
    "Test Party Address Type Strict module"
    module = 'party_address_type_strict'


del ModuleTestCase
