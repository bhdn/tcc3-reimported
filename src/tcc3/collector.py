from tcc3.registry import Registry

class Collector:

    def collect(self, entries, machine):
        raise NotImplementedError

class VMStatCollector(Collector):

    def __init__(self, config, database):
        self.database = database

    def collect(self, sourcedef, hostname):
        """Parses vmstat output and adds into the database

        @sourcedef: the path of the file that has the vmstat output
        @hostname: the host whose data is related to
        """
        pass

collectors = Registry()
collectors.register("vmstat", VMStatCollector)

def get_collector(config, database):
    return collectors.get_instance(config.collector_type, config, database)
