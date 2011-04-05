import os
import logging
import csv

from tcc3.registry import Registry

logger = logging.getLogger("tcc3.database")

def list_valid_names(dir):
    for name in os.listdir(dir):
        if not name.startswith(".") or name.endswith("~"):
            yield name

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
        self.topdir = config.databases_dir

    def list_databases(self):
        raise NotImplementedError

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
            os.makedirs(self.topdir)

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
                mode = "a"
            f = open(path, mode)
            if write:
                obj = f
            else:
                obj = csv.reader(f)
            self.files[machine] = obj
            return obj

    def add(self, info, machine):
        # just too lazy to implement something better now
        f = self._open_base(machine, write=True)
        line = ";".join(str(x) for x in info) + "\n"
        f.write(line)
        # notice the file is not closed

    def values(self, machine):
        csv = self._open_base(machine)
        return iter(csv)

    def list_machines(self):
        return list_valid_names(self.topdir)

class CSVDatabaseManager(DatabaseManager):

    target_class = CSVDatabase

    def list_databases(self):
        return list_valid_names(self.topdir)

database_managers = Registry()
database_managers.register("csv", CSVDatabaseManager)

def get_database_manager(config):
    return database_managers.get_instance(config.database_type, config)
