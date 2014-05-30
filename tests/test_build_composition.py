__author__ = 'tonycastronova'

import unittest

from stdlib import *
from coordinator import main

class test_build_composition(unittest.TestCase):

    def setUp(self):
        self.sim = main.Coordinator()

    def test_add_model(self):

        # model file
        mdl = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'

        # load a model
        self.sim.add_model(mdl)

        # check that the model exists
        self.assertTrue(self.sim.__mod)





    def test_remove_model(self):
        pass

    def test_add_link(self):
        pass