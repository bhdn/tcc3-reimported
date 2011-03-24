from tcc3.registry import Registry

class Collector:

    def __init__(self, config, base):
        self.base = base

    def collect(self, entries, machine):
        raise NotImplementedError

def get_collector(config, base):
    return Collector(config, base)
