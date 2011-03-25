from tcc3 import database, collector

class TCC3Facade:

    def __init__(self, config):
        self.database = base.get_database(config.tcc3)
        self.collector = collector.get_collector(config, database)

    def collect(self, files, hostname):
        raise NotImplementedError
