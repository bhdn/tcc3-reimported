from tcc3.registry import Registry

class Collector:

    def __init__(self, config, database):
        self.database = database

    def collect(self, entries, machine):
        raise NotImplementedError

def get_collector(config, database):
    return Collector(config, database)
