__author__ = 'tonycastronova'

import os
import ConfigParser
import datetime
import cPickle as pickle
import stdlib as stlib
from shapely import wkt
from osgeo import ogr, osr
import imp
from stdlib import Variable, Unit

class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^'+str(self._unique)
        dict.__setitem__(self, key, val)

class ini_types():
    name = 'str'
    description = 'str'
    value = 'int'
    unit_type_cv = 'str'
    variable_name_cv = 'str'
    simulation_start = '%m/%d/%Y %H:%M:%S'
    simulation_end = '%m/%d/%Y %H:%M:%S'
    elementset = 'str'
    epsg_code = 'int'
    filepath = 'str'
    classname = 'str'

def validate_config_ini(ini_path):

    cparser = ConfigParser.ConfigParser(None, multidict)

     # parse the ini
    cparser.read(ini_path)

    # get the ini sections from the parser
    parsed_sections = cparser.sections()

    # load lookup tables
    var = pickle.load(open('../data/var_cv.dat','rb'))
    unit = pickle.load(open('../data/units_cv.dat','rb'))

    # validate
    for section in parsed_sections:
        # get ini options
        options = cparser.options(section)

        # validate units and variables parameters
        if section.split('_')[0] == 'output' or section.split('_')[0] == 'input':
            # check that variable and unit exist
            if 'variable_name_cv' not in options or 'unit_type_cv' not in options:
                raise Exception ('Inputs and Outputs must contain "variable_name_cv" and "unit_type_cv" parameters ')

        # check each option individually
        for option in options:
            val = cparser.get(section,option)

            # validate date format
            if option == 'simulation_start' or option == 'simulation_end':
                try:
                    datetime.datetime.strptime(val, getattr(ini_types, option))
                except ValueError:
                    raise ValueError("Incorrect data format, should be "+getattr(ini_types, option))
            else:
                # validate data type
                if not isinstance(val,type(getattr(ini_types, option))):
                    raise Exception(option+' is not of type '+getattr(ini_types, option))

                # check variable cv (i.e. lookup table)
                if option == 'variable_name_cv':
                    if val not in var:
                        raise Exception (val+' is not a valid controlled vocabulary term')

                # check unit type cv (i.e. lookup table)
                if option == 'unit_type_cv':
                    if val not in unit:
                        raise Exception (val+' is not a valid controlled vocabulary term')


        if section.split('^')[0] == 'software':
            # check that software filepath is valid
            path = cparser.get(section,'filepath')
            if not os.path.isfile(path):
                raise Exception(path+' is not a valid file')

            #todo: check that software class name exists
            try:
                classname = cparser.get(section,'classname')
                filename = os.path.basename(path)
                module = imp.load_source(filename, os.path.realpath(path))
                m = getattr(module, classname)
            except:
                raise Exception(classname+' is not a valid class name')


    return 1

def create_variable(variable_name_cv):
    """
    creates a variable object using the lookup table
    """
    var = pickle.load(open('../data/var_cv.dat','rb'))

    if variable_name_cv in var:
        V = Variable()
        V.VariableNameCV(value=variable_name_cv)
        V.VariableDefinition(value=var[variable_name_cv].strip())
        return V
    else:
        return None

def create_unit(unit_name):
    """
    creates a unit object using the lookup table
    """
    var = pickle.load(open('../data/units_cv.dat','rb'))

    if unit_name in var:
        U = Unit()
        U.UnitName(value=unit_name)
        U.UnitTypeCV(value=var[unit_name][0].strip())
        U.UnitAbbreviation(value=var[unit_name][1].strip())
        return U
    else:
        return None

def parse_config(ini):
    """
    parses metadata stored in *.ini file
    """

    isvalid = validate_config_ini(ini)
    if not isvalid:
        raise Exception('Configuration file is not valid!')

    config_params = {}
    cparser = ConfigParser.ConfigParser(None, multidict)
    cparser.read(ini)
    sections = cparser.sections()

    for s in sections:
        # get the section key (minus the random number)
        section = s.split('^')[0]

        # get the section options
        options = cparser.options(s)

        # save ini options as dictionary
        d = {}
        for option in options:
            d[option] = cparser.get(s,option)
        d['type'] = section


        if section not in config_params:
            config_params[section] = [d]
        else:
            config_params[section].append(d)

    return config_params

def read_shapefile(shp):
    """
    returns (shapely geometry, spatial reference system)
    """

    # open the shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(shp)

    layer = dataset.GetLayer()
    spatialRef = layer.GetSpatialRef()

    # from Geometry
    geoms = []
    for i in xrange(0,layer.GetFeatureCount()):
        feature = layer.GetNextFeature()
        geom = feature.GetGeometryRef()

        # convert into shapely geometry
        geom_wkt = geom.ExportToWkt()
        shapely_geom = wkt.loads(geom_wkt)

        geoms.append(shapely_geom)

    return geoms, spatialRef


def get_srs_from_epsg(code):
    """
    returns a spatial projection. code is an integer EPSG code, e.g. 2000
    """

    # validate the EPSG code
    codes = pickle.load(open('../data/epsg_codes.dat','rb'))
    if not str(code) in codes:
        raise Exception('Invalid EPSG code: %d'%code)

    # load spatial reference
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(int(code))
    return srs



def build_exchange_items(config_params):

    exchange_items = []
    oei = []
    iei = []

    #items = parse_config(ini)


    # get all inputs and outputs
    eitems = config_params['output'] + config_params['input']

    # loop through each input/output and create an exchange item
    for io in eitems:
        variable = None
        unit = None
        datasets = []
        #type = None
        iotype = stlib.ExchangeItemType.Output if io['type'].lower() == 'output' else stlib.ExchangeItemType.Input

        #if 'output' in io.keys(): type = stlib.ExchangeItemType.Output
        #else: type = stlib.ExchangeItemType.Input

        for key,value in io.iteritems():

            if key == 'variable_name_cv': variable = create_variable(value)
            elif key == 'unit_type_cv': unit = create_unit(value)
            elif key == 'elementset' :
                # check if the value is a path
                if os.path.dirname(value ) != '':
                    if not os.path.isfile(value):
                        raise Exception('Could not find file: %s'%value)

                    geom,srs = read_shapefile(value)


                # otherwise it must be a wkt
                else:
                    try:
                        value = value.strip('\'').strip('"')
                        geoms = wkt.loads(value)
                        geom = []
                        if 'Multi' in geoms.geometryType():
                                geom  = [g for g in geoms]
                        else:
                            geom = [geoms]

                    except: raise Exception('Could not load WKT string: %s.'%value)
                    srs = get_srs_from_epsg(io['epsg_code'])


                for element in geom:
                    # create element
                    elem = stlib.Element()
                    elem.geom(element)
                    elem.type(element.geom_type)
                    elem.srs(srs)

                    # define initial dataset for element
                    ds = stlib.DataValues(elem)

                    datasets.append(ds)


        # create exchange item
        ei = stlib.ExchangeItem(variable.VariableNameCV(),variable.VariableDefinition(),unit,variable,iotype)

        # add to exchange item
        for ds in datasets:
            ei.add_dataset(ds)

        exchange_items.append(ei)

    return exchange_items


def load_model(config_params):
    """
    Creates an instance of the model by loading the contents of the configuration ini file.
    returns (model name,model instance)
    """
    # parse module config
    #items = parse_config(ini)

    # get source attributes
    software = config_params['software']

    classname = software[0]['classname']
    filepath = os.path.realpath(software[0]['filepath'])

    # load the model
    model = imp.load_source(os.path.basename(filepath), filepath)
    model_class = getattr(model, classname)

    return (config_params['general'][0]['name'], model_class())