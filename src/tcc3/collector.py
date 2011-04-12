from tcc3 import Error
from tcc3.registry import Registry

class CollectorError(Error):
    pass

class InvalidFormat(CollectorError):
    pass

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
        for n, line in enumerate(open(sourcedef)):
            if (line.startswith("procs ") or line.startswith(" r ")
                    or line.startswith("===")):
                continue
            fields = line.split()
            lineno = n + 1
            if len(fields) < 15:
                raise InvalidFormat, ("invalid number of fields in line %d"
                        % (lineno))
            rawidle = fields[14]
            try:
                idle = int(rawidle)
            except ValueError:
                raise InvalidFormat, ("invalid 'idle' value in line %d: %r" %
                        (lineno, rawidle))
            self.database.add((idle,), hostname)

collectors = Registry()
collectors.register("vmstat", VMStatCollector)

def get_collector(config, database):
    return collectors.get_instance(config.collector_type, config, database)
