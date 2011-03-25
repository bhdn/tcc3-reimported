import os
import logging
import csv

logger = logging.getLogger("tcc3.database")

class Database(object):

    def add(self, info, machine):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError

class DatabaseManager(object):

    target_class = Database

    def __init__(self, config):
        self.config = config

    def get_database(self, name):
        return self.target_class(name, self.config)

class CSVDatabase(Database):
    
    def __init__(self, name, config):
        self.name = name
        self.topdir = os.path.join(config.databases_dir, name)
        self.files = {}
        self._create_dirs()

    def _create_dirs(self):
        if not os.path.exists(self.topdir):
            logger.debug("creating directory %s" % (self.topdir))
            os.mkdir(self.topdir)

    def _base_path(self, machine):
        name = machine.replace("/", "_")
        return os.path.join(self.topdir, machine)

    def _open_base(self, machine, write=False):
        try:
            return self.files[machine]
        except KeyError:
            path = self._base_path(machine)
            mode = "r"
            if write:
                mode = "w"
            f = open(path, mode)
            if write:
                csv = csv.writer(f)
            else:
                csv = csv.reader(f)
            return f

    def add(self, info, machine):
        # just too lazy to implement something better now
        f = self._open_base(machine, write=True)
        line = ";".join(info) + "\n"
        f.write(line)
        # notice the file is not closed

    def __iter__(self):
        csv = self._open_base(machine)
        return iter(csv)

class CSVDatabaseManager(DatabaseManager):

    target_class = CSVDatabase

database_manager = Registry()
database_manager.register("csv", CSVDatabaseManager)

def get_database_manager(config):
    return databases.get_instance(config.database_type, config)
