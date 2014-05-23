__author__ = 'tonycastronova'

import unittest

from integration_framework import utilities



class testVariable(unittest.TestCase):


    def test_set_variable(self):

        name = 'streamflow'
        variable = utilities.create_variable(name)
        self.assertTrue(variable.VariableNameCV() == 'streamflow')
        self.assertTrue(variable.VariableDefinition() == 'The volume of water flowing past a fixed point.  Equivalent to discharge')

        name = 'NotInCV'
        variable = utilities.create_variable(name)
        self.assertTrue(variable is None)
