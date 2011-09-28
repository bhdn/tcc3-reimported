from tcc3 import Error
from tcc3.registry import Registry

class CollectorError(Error):
    pass

class InvalidFormat(CollectorError):
    pass

class Collector:

    def collect(self, entries, machine):
        raise NotImplementedError

VMSTAT_FIELDS = " r  b   swpd   free   buff  cache   si   so    bi    bo in   cs us sy id wa"
VMSTAT_FIELDSMAP = dict((n, i) for i, n in enumerate(VMSTAT_FIELDS.split()))

class VMStatCollector(Collector):

    def __init__(self, config, database):
        fieldnames = config.vmstat_fields.split()
        self.collectfields = [VMSTAT_FIELDSMAP[n] for n in fieldnames]
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
            values = []
            # vmstat fields: id, r, bi, bo
            #for idx in (14, 0, 8, 9):
            import pdb; pdb.set_trace()
            for idx in self.collectfields:
                raw = fields[idx]
                try:
                    value = int(raw)
                except ValueError:
                    raise InvalidFormat, ("invalid 'idle' value in line %d: %r" %
                            (lineno, rawidle))
                values.append(value)
            self.database.add(values, hostname)

collectors = Registry()
collectors.register("vmstat", VMStatCollector)

def get_collector(config, database):
    return collectors.get_instance(config.collector_type, config, database)
