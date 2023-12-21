# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class NewsletterTestCase(ModuleTestCase):
    "Test Newsletter module"
    module = 'newsletter'


del ModuleTestCase
