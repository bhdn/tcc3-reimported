import time
import collections
import logging

class Scheduler(object):

    def __init__(self, config, vmm, method, maindb):
        self.config = config
        self.vmm = vmm
        self.method = method
        self.maindb = maindb
        self.guests = config.guests.split()
        self.hosts = config.hosts.split()
        self.interval = int(config.sched_interval)
        self.windowsize = int(config.window_size)
        self.logger = logging.getLogger("tcc3.scheduler")

    def start(self):
        readings = {} # {guestname: deque of stats}
        while True:
            self.logger.debug("scheduler tick %r", readings)
            for guest, stats in self.vmm.collect_stats():
                if guest not in readings:
                    readings[guest] = collections.deque()
                readings[guest].append(stats)
                #FIXME ensure the number of fields is the same as used in
                # collector code
                print "not adding", stats, guest
                #self.maindb.add(stats, guest)
                if len(readings[guest]) >= self.windowsize:
                    assert len(readings[guest]) == self.windowsize
                    class_ = self.method.predict(guest, readings[guest])
                    readings[guest].popleft()
        #time.sleep(self.interval)
        time.sleep(1)
