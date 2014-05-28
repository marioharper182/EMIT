__author__ = 'tonycastronova'

import os
import unittest
import utilities as utils
from tests.data import testmodel

class testExchangeItem(unittest.TestCase):


    def test_load_model(self):

        config = os.path.realpath('./configuration.ini')

        m = utils.load_model(config)

        #todo: make sure that this class is an instance of TestModel

        print 'done'