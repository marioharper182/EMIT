__author__ = 'tonycastronova'

class multiplier(object):


    def __init__(self):
        """
        initialization that will occur when loaded into a configuration
        """

        self.results = None

        # build variables based on geometry
        # todo: create geom object type where a geom has a value that can change with time. POINT, times, values

    def save(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def get_data(self, links):
        """
        This is an abstract method that must be implemented
        links - all input links objects.  This is used to query the database

        usuwater

        usuwater
        usuwater



        """

    def run(self,exchangeitem):
        """
        This is an abstract method that must be implemented.
        input_ts => exchangeitem class object (see stdlib)
        """

        # get the geometries of the exchange item
        geoms = exchangeitem.get_geoms()

        # loop through geometry and perform calculation
        for geometry in geoms:
            # todo: some sort of automatic geometry mapping (utilites.py)




    def data_directory(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')


    """
    Remove "initialize" because its essentially a duplicate of __init__
    """

    def initialize(self):
        # TODO: This can be remove b/c it performs the same task as def __init__
        raise NotImplementedError('This is an abstract method that must be implemented!')






    """
    These are all loaded via INI config.  This info can be access via utilites.py or stdlib, so \
    they should be removed
    """

    def time_step(self):
        """
            ini configuration file
        """
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def outputs(self):
        """
            ini configuration file
        """
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def inputs(self):
        """
            ini configuration file
        """
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def simulation_start(self):
        """
            ini configuration file
        """
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def simulation_end(self):
        """
            ini configuration file
        """
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def name(self):
        """
            ini configuration file
        """
        raise NotImplementedError('This is an abstract method that must be implemented!')


