__author__ = 'tonycastronova'

import unittest
from db.api import postgresdb

class test_postgres(unittest.TestCase):

    def setUp(self):
        # connect to the local db
        self.db = postgresdb('tonycastronova','water','localhost','odm2')


    def tearDown(self):
        # disconnect from db
        self.db.close()


    def test_all_timeseries_meta(self):
        data = self.db.get_all_ts_meta()

        for d in data:
            for k,v in d.iteritems():
                print k +': '+','.join([str(val) for val in v])


    def test_get_results_alc(self):
        ts = self.db.get_all_ts_alc()
        print 'done'
        #from sqlalchemy import create_engine
        #self.engine = create_engine(database='odm2',user='tonycastronova',password='water',host='localhost')
        #self.engine = create_engine("postgresql+psycopg2://tonycastronova:waterd@/odm2?host=localhost")
        #create_engine("postgresql+psycopg2://user:password@/dbname?host=/var/lib/postgresql"



        # connection = engine.connect()
        # result = connection.execute("select username from users")
        # for row in result:
        #     print "username:", row['username']
        # connection.close()


    def test_get_variables(self):
        vars = self.db.get_all_variables()
        print vars

    def test_get_simulation(self):
        sims = self.db.get_simulations()
        print 'done'