from tcc3 import database, collector, method

class TCC3Facade(object):

    def __init__(self, config):
        self.dbmanager = database.get_database_manager(config.tcc3)
        mainname = config.tcc3.main_database_name
        trainedname = config.tcc3.trained_database_name
        self.maindb = self.dbmanager.get_database(mainname)
        self.traindb = self.dbmanager.get_database(trainedname)
        self.method = method.get_method(config.tcc3)
        self.learner = self.method.get_learner(self.maindb)
        self.predictor = self.method.get_predictor(self.traindb)
        self.collector = collector.get_collector(config.tcc3, self.maindb)

    def collect(self, sourcedef, hostname):
        self.collector.collect(sourcedef, hostname)
