__author__ = 'tonycastronova'

import sys, getopt
from coordinator import help as h
from utilities import *

"""
Purpose: This file contains the logic used to run coupled model simulations
"""

class Link(object):
    """
    stores info about the linkage between two components
    """
    def __init__(self):
        # TODO: this is not finished, just mocked up
        from_lc = None
        from_item = None

        to_lc = None
        to_item = None

        id = None


class Coordinator(object):
    def __init__(self):
        """
        globals
        """
        __models = {}
        pass


    def add_model(self, ini_path):
        """
        stores model component objects when added to a configuration
        """

        # parse the model configuration parameters
        params = parse_config(ini_path)

        # load model
        name,model = load_model(params)

        # save the model
        self.__models[name] = model


    def build_exchange_item(self, ini_path):

        pass


    def remove_model(self,linkablecomponent):
        """
        removes model component objects from the registry
        """
        pass

    def add_link(self,from_lc, to_lc):
        """
        adds a data link between two components
        """
        pass

    def get_links(self,lc):
        """
        returns all the links corresponding with a linkable component
        """
        pass

    def remove_link(self,id):
        """
        removes a link using the link id
        """

    def calculate_execution_order(self):
        """
        determines the order in which models will be executed
        """

    def transfer_data(self, link):
        """
        retrieves data exchange item from one component and passes it to the next
        """
        pass

    def get_global_start_end_times(self,linkablecomponents=[]):
        """
        determines the simulation start and end times from the linkablecomponent attributes
        """
        pass

    def run_simulation(self):
        """
        coordinates the simulation effort
        """
        pass



def main(argv):
    print '|-------------------------------------------------|'
    print '|      Welcome to the Utah State University       |'
    print '| Environmental Model InTegration (EMIT) Project! |'
    print '|-------------------------------------------------|'
    print '\nPlease enter a command or type "help" for a list of commands'

    arg = None
    while arg != 'exit':
        # create instance of coordinator
        coordinator = Coordinator()

        # get the users command
        arg = raw_input("> ").split(' ')

        if ''.join(arg).strip() != '':
            if arg[0] == 'help':
                if len(arg) == 1: print h.help()
                else: print h.help_function(arg[1])
            elif arg[0] == 'add' : coordinator.add_model(arg[1])
            elif arg[0] == 'info': print h.info()
            else:
                print '> [error] command not recognized.  Type "help" for a complete list of commands.'


    # try:
    #   opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    # except getopt.GetoptError:
    #   print 'test.py -i <inputfile> -o <outputfile>'
    #   sys.exit(2)
    # for opt, arg in opts:
    #   if opt == '-h':
    #      print 'test.py -i <inputfile> -o <outputfile>'
    #      sys.exit()
    #   elif opt in ("-i", "--ifile"):
    #      inputfile = arg
    #   elif opt in ("-o", "--ofile"):
    #      outputfile = arg
    # print 'Input file is "', inputfile
    # print 'Output file is "', outputfile

if __name__ == '__main__':
    main(sys.argv[1:])