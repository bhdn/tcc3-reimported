from tcc3 import base, collector

class TCC3Facade:

    def __init__(self, config):
        self.base = base.get_base(config.tcc3)
        self.collector = collector.get_collector(config, base)

    def collect(self, files, hostname):
        raise NotImplementedError
