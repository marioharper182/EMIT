from integration_framework.examples.swmm.bin import parse_swmm as ps
from integration_framework.wrappers import model_wrapper

__author__ = 'tonycastronova'



import os


class swmm_wrapper(model_wrapper.feed_forward_wrapper):

    def __init__(self):
        super(model_wrapper.feed_forward_wrapper,self).__init__()

    def data_directory(self):
        """
        returns the directory of the simulation input/output files
        """

        p1 =  os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../../../model_wrappers/swmm/sim_test')

        return os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             '../../../../../model_wrappers/swmm/sim_test'))

        #f = open(p2+'/sim.ini','r')

    def save(self):
        """
            returns a list of data objects that will be saved to the database

            This method is called by the coordinator when simulation is complete and data will be saved to the simulations database
        """

        #
        data = self.data_directory()
        parse = ps.SwmmExtract(data+'/sim.out')



wrapper = swmm_wrapper()
data = wrapper.data_directory()
print ps.list(data+'/sim.out')
print ps.listdetail(data+'/sim.out',type='subcatchment')
print ps.listvariables(data+'/sim.out')



#wrapper.save()
print 'done'