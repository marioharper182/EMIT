__author__ = 'tonycastronova'

import os
import unittest
import utilities as utils
from tests.data import testmodel

class testExchangeItem(unittest.TestCase):


    def test_load_model(self):

        config = os.path.realpath('./configuration.ini')
        params = utils.parse_config(config)
        m = utils.load_model(params)

        #todo: make sure that this class is an instance of TestModel

        print 'done'