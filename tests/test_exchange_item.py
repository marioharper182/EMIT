__author__ = 'tonycastronova'

import os
import unittest
from stdlib import *
import utilities as utils
import datetime
from shapely.wkt import loads

class testExchangeItem(unittest.TestCase):

    def setUp(self):

        self.srscode = 2921

        self.item = ExchangeItem('e1','Test','Test Exchange Item')

    def tearDown(self):
        del self.item


    def test_create_exchange_item(self):

        item = self.item

        # -- Create Unit --#
        unit = utils.create_unit('cubic meters per second')

        # -- Create Variable --#
        variable = utils.create_variable('streamflow')

        # create dataset 1
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,10)]
        self.geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        dv = DataValues(elem,self.vals)
        item.add_dataset(dv)

        # create dataset 2
        self.vals = [(datetime.datetime(2014,2,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,10)]
        self.geometry = 'POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))'
        elem = Element()
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        elem.set_geom_from_wkt(self.geometry)
        dv = DataValues(elem,self.vals)
        item.add_dataset(dv)

        self.assertTrue(item.name() == 'Test')
        self.assertTrue(item.description() == 'Test Exchange Item')
        self.assertTrue(item.StartTime == datetime.datetime(2014,1,1,12,0,0))
        self.assertTrue(item.EndTime == datetime.datetime(2014,2,10,12,0,0))

    def test_add_dataset_seq(self):
        item = self.item

        # create dataset 1
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        dv = DataValues(elem,self.vals)
        item.add_dataset(dv)

        # create dataset 2
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))'
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        dv = DataValues(elem,self.vals)
        item.add_dataset(dv)

        datasets = item.get_dataset()
        ds1 = datasets[0]
        ds2 = datasets[1]
        self.assertTrue(len(datasets) == 2)
        self.assertTrue(ds2.element().geom().equals(loads('POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))')))
        self.assertTrue(ds1.element().geom().equals(loads('POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))')))



    def test_add_datasets_as_list(self):
        item = self.item

        # create dataset 1 & 2 together
        dvs = []
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        dv = DataValues(elem,self.vals)
        dvs.append(dv)

        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))'
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        dv = DataValues(elem,self.vals)
        dvs.append(dv)

        # add both datasets
        item.add_dataset(dvs)

        datasets = item.get_dataset()
        ds1 = datasets[0]
        ds2 = datasets[1]
        #self.assertTrue(len(datasets) == 2)
        self.assertTrue(ds2.element().geom().equals(loads('POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))')))
        self.assertTrue(ds1.element().geom().equals(loads('POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))')))

    def test_clear_datasets(self):
        item = self.item

        # create dataset 1
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        dv = DataValues(elem,self.vals)
        item.add_dataset(dv)


        item.clear_dataset()
        ds = item.get_dataset()
        self.assertTrue(len(ds) == 0)

    def test_set_dataset(self):
        item = self.item

        # create dataset 1 & 2 together
        dvs = []
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        dv = DataValues(elem,self.vals)
        dvs.append(dv)

        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))'
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        elem.srs(utils.get_srs_from_epsg(self.srscode))
        dv = DataValues(elem,self.vals)
        dvs.append(dv)

        # add both datasets
        item.set_dataset(dvs)

        datasets = item.get_dataset()
        ds1 = datasets[0]
        ds2 = datasets[1]
        self.assertTrue(len(datasets) == 2)
        self.assertTrue(ds2.element().geom().equals(loads('POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))')))
        self.assertTrue(ds1.element().geom().equals(loads('POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))')))




    def test_utilites_build_exchange_items(self):

        config = os.path.realpath('./configuration.ini')

        eitems = utils.build_exchange_items(config)

        print 'done'