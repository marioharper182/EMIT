__author__ = 'tonycastronova'

import unittest

from integration_framework import utilities

class testUnit(unittest.TestCase):


    def test_set_unit(self):

        name = 'meters per second'
        unit = utilities.create_unit(name)
        self.assertTrue(unit.UnitName() == 'meters per second')
        self.assertTrue(unit.UnitTypeCV() == 'velocity')
        self.assertTrue(unit.UnitAbbreviation() == 'm/s')

        name = 'NotInCV'
        unit = utilities.create_unit(name)
        self.assertTrue(unit is None)
