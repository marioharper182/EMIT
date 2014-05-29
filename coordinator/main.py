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
    def __init__(self, from_linkable_component, to_linkable_component, from_item, to_item):
        # TODO: this is not finished, just mocked up
        self.__from_lc = from_linkable_component
        self.__from_item = from_item

        self.__to_lc = to_linkable_component
        self.__to_item = to_item

    def get_link(self):
        return [self.__from_lc,self.__from_item], [self.__to_lc,self.__to_item]

class Model(object):
    """
    defines a model that has been loaded into a configuration
    """
    def __init__(self, id, name, instance, desc=None, input_exchange_items={}, output_exchange_items={}):
        self.__name = name
        self.__description = desc
        self.__iei = {}
        self.__oei = {}
        self.__id = id

        for iei in input_exchange_items:
            self.__iei[iei.name()] = iei

        for oei in output_exchange_items:
            self.__oei[oei.name()] = oei

        self.__inst = instance

    def get_input_exchange_items(self):
        return [j for i,j in self.__iei.items()]
    def get_output_exchange_items(self):
        return [j for i,j in self.__oei.items()]

    def get_input_exchange_item(self,value):
        ii = None

        for k,v in self.__iei.iteritems():
            if v.get_id() == value:
                ii = self.__iei[k]

        if ii is None:
            print '>  Could not find Input Exchange Item: '+value

        return ii

    def get_output_exchange_item(self,value):
        oi = None

        for k,v in self.__oei.iteritems():
            if v.get_id() == value:
                oi = self.__oei[k]

        if oi is None:
            print '>  Could not find Output Exchange Item: '+value

        return oi

    def get_description(self):
        return self.__description
    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id

class Coordinator(object):
    def __init__(self):
        """
        globals
        """
        self.__models = {}
        self.__links = {}
        self.__incr = 0

    def get_new_id(self):
        self.__incr += 1
        return self.__incr

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

            # generate a unique model id
            id = self.get_new_id()

            # create a model instance
            thisModel = Model('M'+str(id),name,
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

    def get_model_by_id(self,id):
        for m in self.__models:
            if self.__models[m].get_id() == id:
                return self.__models[m]
        return None


    def add_link(self,from_id, from_item_name, to_id, to_item_name):
        """
        adds a data link between two components
        """

        # check that from and to models exist in composition
        From = self.get_model_by_id(from_id)
        To = self.get_model_by_id(to_id)
        try:

            if self.get_model_by_id(from_id) is None: raise Exception(from_id+' does not exist in configuration')
            if self.get_model_by_id(to_id) is None: raise Exception(to_id+' does not exist in configuration')
        except Exception, e:
            print e
            return None


        if from_id not in self.__links:
            self.__links[from_id] = []

        # check that input and output exchange items exist
        ii = To.get_input_exchange_item(to_item_name)
        oi = From.get_output_exchange_item(from_item_name)

        if ii is not None and oi is not None:
            # create link
            self.__links[from_id].append({'to':to_id,
                                            'from_ei':oi,
                                            'to_ei':ii})
        else:
            print '>  Could Not Create Link :('

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

                print '   * desc: ' + model.get_description()
                print '   * id : '+ model.get_id()
                print '  '+(27+len(name))*'-'

                for item in model.get_input_exchange_items() + model.get_output_exchange_items():
                    print '   '+item.get_type().upper()
                    print '   * id: '+str(item.get_id())
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

            elif arg[0] == 'link':
                if len(arg) != 5: print h.help_function('link')
                else: coordinator.add_link(arg[1],arg[2],arg[3],arg[4])

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