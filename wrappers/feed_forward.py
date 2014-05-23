__author__ = 'tonycastronova'



class feed_forward_wrapper(object):
    def __init__(self):
        pass

    def data_directory(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def save(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def run(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

    def initialize(self):
        raise NotImplementedError('This is an abstract method that must be implemented!')

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

