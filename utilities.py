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
from odm2.api.ODMconnection import dbconnection, SessionFactory

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
    ignorecv = 'str'

def validate_config_ini(ini_path):

    try:

        cparser = ConfigParser.ConfigParser(None, multidict)

         # parse the ini
        cparser.read(ini_path)

        # get the ini sections from the parser
        parsed_sections = cparser.sections()

        # if no sections are found, than the file format must be incorrect
        if len(parsed_sections) == 0: raise Exception('Invalid model configuration file')

        # load lookup tables
        var = pickle.load(open('../data/var_cv.dat','rb'))
        unit = pickle.load(open('../data/units_cv.dat','rb'))

        # check to see if 'ignorecv' option has been provided
        ignorecv = False
        for p in parsed_sections:
            if p.split('^')[0] == 'options':
                if cparser.has_option(p,'ignorecv'):
                    ignorecv = int(cparser.get(p,'ignorecv'))
                    break


        # validate
        for section in parsed_sections:
            # get ini options
            options = cparser.options(section)

            if not ignorecv:
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

                    if not ignorecv:
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
                relpath = cparser.get(section,'filepath')
                basedir = os.path.realpath(os.path.dirname(ini_path))
                abspath = os.path.abspath(os.path.join(basedir,relpath))
                if not os.path.isfile(abspath):
                    raise Exception(abspath+' is not a valid file')

                #todo: check that software class name exists
                try:
                    classname = cparser.get(section,'classname')
                    filename = os.path.basename(abspath)
                    module = imp.load_source(filename, abspath)
                    m = getattr(module, classname)
                except:
                    print 'Configuration Parsing Error: '+classname+' is not a valid class name'

    except Exception, e:
        print '> [Configuration Parsing Error] '+str(e)
        return 0


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
        V = Variable()
        V.VariableNameCV(value=variable_name_cv)
        V.VariableDefinition(value='unknown')
        print '>  [WARNING] Variable not found in controlled vocabulary : '+variable_name_cv
        return V

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
        U = Unit()
        U.UnitName(value=unit_name)
        U.UnitTypeCV(value='unknown')
        U.UnitAbbreviation(value='unknown')
        print '>  [WARNING] Unit not found in controlled vocabulary : '+unit_name
        return U

def parse_config(ini):
    """
    parses metadata stored in *.ini file
    """

    isvalid = validate_config_ini(ini)
    if isvalid:
        #raise Exception('Configuration file is not valid!')

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

        # save the base path of the model
        config_params['basedir'] = basedir = os.path.realpath(os.path.dirname(ini))

        return config_params
    else:
        return None

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

def build_exchange_items(params):

    exchange_items = []
    oei = []
    iei = []

    # get all inputs and outputs
    eitems = params['input'] if 'input' in params else [] + params['output'] if 'output' in params else []

    itemid = 0

    # loop through each input/output and create an exchange item
    for io in eitems:
        variable = None
        unit = None
        elementset = []

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
                    # define initial dataset for element
                    dv = stlib.DataValues()

                    # create element
                    elem = stlib.Geometry()
                    elem.geom(element)
                    elem.type(element.geom_type)
                    elem.srs(srs)
                    elem.datavalues(dv)
                    elementset.append(elem)


        # increment item id
        itemid += 1
        id = iotype.upper()+str(itemid)

        # create exchange item
        ei = stlib.ExchangeItem(id,
                                name=variable.VariableNameCV(),
                                desc=variable.VariableDefinition(),
                                geometry=elementset,
                                unit= unit,
                                variable=variable,
                                type=iotype)

        # add to exchange item
        #for ds in datasets:
        #    ei.add_geometry(ds)

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
    relpath = software[0]['filepath']

    # load the model
    basedir = config_params['basedir']
    abspath = os.path.abspath(os.path.join(basedir,relpath))
    filename = os.path.basename(abspath)
    module = imp.load_source(filename, abspath)
    model_class = getattr(module, classname)

    # todo: Initialize model?
    instance = model_class(config_params)

    return (config_params['general'][0]['name'], instance)


def create_database_connections_from_file(ini):

    # database connections dictionary
    db_connections = {}

    # parse the dataabase connections file
    params = {}
    cparser = ConfigParser.ConfigParser(None, multidict)
    cparser.read(ini)
    sections = cparser.sections()

    # create a session for each database connection in the ini file
    for s in sections:
        # get the section key (minus the random number)
        #section = s.split('^')[0]

        # put ini args into a dictionary
        options = cparser.options(s)
        d = {}
        for option in options:
            d[option] = cparser.get(s,option)

        # build database connection
        connection_string = dbconnection.create_connection(d['engine'],d['address'],d['db'],d['user'],d['pwd'])

        # add connection string to dictionary (for backup/debugging)
        d['connection_string'] = connection_string

        # create a session
        try:
            session = SessionFactory(connection_string,None).get_session()
        except:
            session = None
            print 'Could not establish a connection with the database: '+connection_string

        # save this session in the db_connections object
        db_connections[d['name']] = {'session': session,
                                     'description':d['desc'],
                                     'args': d}
    return db_connections


def get_ts_from_link(session, links, target_model):
    """
    queries the data
    :param session: database session where the data is stored
    :param links: all links
    :param target_model:
    :return:
    """

    if session is None:
        print '>  [error] no default database has been specified'
        return 0

    mapping = {}
    timeseries = {}
    tname = target_model.get_name()
    for id,link_inst in links.iteritems():
        f,t = link_inst.get_link()
        if t[0].get_name() == tname:
            mapping[f[1].name()] = t[1].name()
            print '>  %s -> %s'%(f[1].name(), t[1].name())

        # get data and store in dict
    return timeseries

def save_model_results():
    pass

def unresolved_exchange_items():
    # make sure that all input items are satisfied
    # warn the user if output items are not being used or saved in database
    pass

def get_start_end(model_instance):
    """
    calculates the global start and end time for a model simulation
    :param model_instance: the class instance of the desired model
    :return: global start and end time for all exchange items
    """
    pass


# TODO: Move into wrapper?
def get_data_by_exchange_item(exchangeitemlist, variableName, unitName):
    """
    returns the exchange item associated with a given variable and unit
    :param exchangeitemlist: list of exchange items
    :param variableName: desired variable
    :param unitName: desired unit
    :return: exchange item associated with variable and unit
    """
    pass