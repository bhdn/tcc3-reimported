from tcc3 import database, collector

class TCC3Facade(object):

    def __init__(self, config):
        self.mainname = config.main_database_name
        self.learner = base.
        self.dbmanager = base.get_database_manager(config.tcc3)
        self.collector = collector.get_collector(config.tcc3, database)

    def collect(self, sourcedef, hostname):
        database = self.dbmanager.get_database(
        self.collector.collect(sourcedef, hostname)
