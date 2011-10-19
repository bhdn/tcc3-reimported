from tcc3 import database, collector, method, vmm, scheduler

class TCC3Facade(object):

    def __init__(self, config):
        self.config = config
        self.dbmanager = database.get_database_manager(config.tcc3)
        self.mainname = config.tcc3.main_database_name
        self.trainedname = config.tcc3.trained_database_name
        self.maindb = self.dbmanager.get_database(self.mainname)
        self.traindb = self.dbmanager.get_database(self.trainedname)
        self.method = method.get_method(config.tcc3, self.maindb,
                self.traindb)
        self.collector = collector.get_collector(config.tcc3, self.maindb)
        self.vmm = vmm.get_vmm(config.tcc3)

    def collect(self, sourcedef, hostname):
        self.collector.collect(sourcedef, hostname)

    def dump_databases(self):
        def dbit(db):
            for name in db.list_machines():
                yield name, db.values(name)
        yield self.mainname, dbit(self.maindb)
        yield self.trainedname, dbit(self.traindb)

    def predict(self, values, hostname):
        return self.method.predict(hostname, values)

    def train(self, hostname):
        self.method.train(hostname)

    def test(self, hostname):
        return self.method.test(hostname)

    def schedule(self):
        sched = scheduler.Scheduler(self.config.tcc3, self.vmm, self.method,
                self.maindb)
        sched.start()
