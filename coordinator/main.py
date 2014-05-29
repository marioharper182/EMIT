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

class Model(object):
    """
    defines a model that has been loaded into a configuration
    """
    def __init__(self, name, instance, desc=None, input_exchange_items={}, output_exchange_items={}):
        self.__name = name
        self.__description = desc
        self.__iei = {}
        self.__oei = {}

        for iei in input_exchange_items:
            self.__iei[iei.name()] = iei

        for oei in output_exchange_items:
            self.__oei[oei.name()] = oei

        self.__inst = instance

    def get_input_exhange_items(self):
        return [j for i,j in self.__iei.items()]
    def get_output_exhange_items(self):
        return [j for i,j in self.__oei.items()]
    def get_description(self):
        return self.__description
    def get_name(self):
        return self.__name

class Coordinator(object):
    def __init__(self):
        """
        globals
        """
        self.__models = {}
        pass


    def add_model(self, ini_path):
        """
        stores model component objects when added to a configuration
        """

        # parse the model configuration parameters
        params = parse_config(ini_path)

        if params is not None:
            # load model
            name,model_inst = load_model(params)

            # make sure this model doesnt already exist
            if name in self.__models:
                print 'Model named '+name+' already exists in configuration'
                return None

            # build exchange items
            ei = build_exchange_items(params)

            # organize input and output items
            iei = [item for item in ei if item.get_type() == 'input']
            oei = [item for item in ei if item.get_type() == 'output']

            # create a model instance
            thisModel = Model(name,
                              model_inst,
                              params['general'][0]['description'],
                              iei,
                              oei)

            # save the model
            self.__models[name] = thisModel




    def remove_model(self,linkablecomponent):
        """
        removes model component objects from the registry
        """

        if linkablecomponent in self.__models:
            # remove the model
            self.__models.pop(linkablecomponent,None)

            #todo: remove all associated links


    def build_exchange_item(self, ini_path):

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

    def get_configuration_details(self,arg):

        if len(self.__models.keys()) == 0:
            print '> Could not complete request. No models found in configuration.'
            return

        # print model info
        if arg.strip() == 'models' or arg.strip() == 'summary':

            # loop through all known models
            for name,model in self.__models.iteritems():



                # print exchange items
                print '  '+(27+len(name))*'-'
                print '  |' + ((33-len(name))/2)*' ' +'Model: '+name + ((33-len(name))/2)*' '+'|'
                print '  '+(27+len(name))*'-'

                print '   * ' + model.get_description()
                print '  '+(27+len(name))*'-'

                for item in model.get_input_exhange_items() + model.get_output_exhange_items():
                    print '   '+item.get_type().upper()
                    print '   * name: '+item.name()
                    print '   * description: '+item.description()
                    print '   * unit: '+item.unit().UnitName()
                    print '   * variable: '+item.variable().VariableNameCV()
                    print '  '+(27+len(name))*'-'
                print ''



        # print link info
        if arg.strip() == 'links' or arg.strip() == 'summary':
            pass

            # print links



def main(argv):
    print '|-------------------------------------------------|'
    print '|      Welcome to the Utah State University       |'
    print '| Environmental Model InTegration (EMIT) Project! |'
    print '|-------------------------------------------------|'
    print '\nPlease enter a command or type "help" for a list of commands'

    arg = None

    # create instance of coordinator
    coordinator = Coordinator()

    while arg != 'exit':

        # get the users command
        arg = raw_input("> ").split(' ')

        if ''.join(arg).strip() != '':
            if arg[0] == 'help':
                if len(arg) == 1: print h.help()
                else: print h.help_function(arg[1])

            elif arg[0] == 'add' :
                if len(arg) == 1: print h.help_function('add')
                else: coordinator.add_model(arg[1])

            elif arg[0] == 'remove':
                if len(arg) == 1: print h.help_function('remove')
                else: coordinator.remove_model(arg[1])

            elif arg[0] == 'showme':
                if len(arg) == 1: print h.help_function('showme')
                else: coordinator.get_configuration_details(arg[1])


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