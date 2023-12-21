# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class WebdavTestCase(ModuleTestCase):
    "Test Webdav module"
    module = 'webdav'


del ModuleTestCase
