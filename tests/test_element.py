__author__ = 'tonycastronova'

import unittest

from stdlib import ElementType,Element


class testVariable(unittest.TestCase):


    def test_set_element(self):

        wkt_geometry = 'POINT (1.0 20.1)'

        elem = Element()
        self.assertTrue(elem.geom() == None)

        name,code = elem.srs()
        self.assertTrue(name == None)
        self.assertTrue(code == None)
        self.assertTrue(elem.elev() == None)
        self.assertTrue(elem.type() == None)

        elem.srs('NAD83(HARN) / Utah North (ft)','EPSG:2921')
        elem.set_geom_from_wkt(wkt_geometry)
        elem.type(ElementType.Point)

        name,code = elem.srs()
        self.assertTrue(code == 'EPSG:2921')
        self.assertTrue(elem.geom().geometryType() == 'Point')
        self.assertTrue(len(elem.geom().coords) == 1)
        self.assertTrue(elem.geom().coords[0][0] == 1.0)
        self.assertTrue(elem.geom().coords[0][1] == 20.1)



    def test_element_from_shp(self):
        pass