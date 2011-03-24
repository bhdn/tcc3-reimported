import csv

class Database(object):

    def add(self, info, machine):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError

class TextDatabase(Database):
    
    def __init__(self, config):
        self.topdir = config
        self.file = None

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
        f = self._open_base(machine, write=True)
        line = ";".join(info) + "\n"
        f.write(line)
        # notice the file is not closed

    def __iter__(self):
        csv = self._open_base(machine)
        return iter(csv)

def get_database(config):
    # TODO use Registry
    return TextDatabase(config)
