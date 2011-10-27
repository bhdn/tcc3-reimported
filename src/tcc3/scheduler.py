import time
import collections
import threading
import Queue
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
        self.nranges = int(config.cpu_usage_ranges)
        self.logger = logging.getLogger("tcc3.scheduler")
        self._statsource = Queue.Queue()
        self._finished = threading.Event()
        self._vmmlock = threading.Lock()

    def _collect_stats(self):
        try:
            last = 0
            while not self._finished.is_set():
                self.logger.debug("collector tick")
                self._vmmlock.acquire()
                try:
                    stats = list(self.vmm.collect_stats())
                finally:
                    self._vmmlock.release()
                self._statsource.put(stats)
                diff = time.time() - last
                waittime = max(self.interval - diff, 0)
                self._finished.wait(waittime)
                last = time.time()
        finally:
            self._finished.set()

    def _schedule(self):
        readings = {} # {guestname: deque of stats}
        canpredict = False
        while not self._finished.is_set():
            predictions = {} # guestname: predicted class_
            hostpredictions = {}
            # collect information about hosts and predict cpu usage for
            try:
                hostsinfo = self._statsource.get(timeout=1)
            except Queue.Empty:
                continue
            # guests:
            for hostinfo in hostsinfo:
                for guestinfo in hostinfo.guests:
                    if guestinfo.name not in readings:
                        readings[guestinfo.name] = collections.deque()
                    readings[guestinfo.name].append(guestinfo.cpuusage)
                    self.maindb.add((guestinfo.cpuusage,), guestinfo.name)
                    if len(readings[guestinfo.name]) >= self.windowsize:
                        assert len(readings[guestinfo.name]) == self.windowsize
                        class_ = self.method.predict(guestinfo.name,
                                readings[guestinfo.name])
                        predictions[guestinfo.name] = class_
                        hostpredictions[hostinfo.name] = \
                                hostpredictions.get(hostinfo.name, 0.0) \
                                + class_
                        readings[guestinfo.name].popleft()
                        canpredict = True
            if canpredict:
                self.logger.debug("predictions: %r", predictions)
                self.logger.debug("hostpredictions: %r", hostpredictions)
                # compute max cpu capacity for each host (in the same unity
                # used as in "class_"):
                maxcapacity = dict((hi.name, hi.maxcpus * (self.nranges - 1))
                                    for hi in hostsinfo)
                availcapacity = {}
                availcapacity.update(maxcapacity)
                availmemory = dict((hi.name, hi.memory)
                                    for hi in hostsinfo)
                self.logger.debug("maxcapacity: %r", maxcapacity)
                self.logger.debug("availcapacity: %r", availcapacity)
                # used capacity as pointed by the predictions:
                # compute a list of the hosts that are most likely to
                # accomodate idle vms (those that already host many vms and are
                # able to keep even more, thus resulting in less vm-migrations
                # and more chance of being able to put idle hosts in
                # power-saving mode)
                guestmap = {}
                for hi in hostsinfo:
                    for guest in hi.guests:
                        guestmap[guest] = hi
                # host name and guest names are used as sorting criteria to
                # ensure there will be no bouncing between a set of
                # machines that are identical (ie. one machine randomly
                # being consired first for the packing algorithm)
                hostscriteria = lambda hi: (maxcapacity[hi.name],
                        availmemory[hi.name], hi.name)
                tophosts = sorted(hostsinfo, key=hostscriteria, reverse=True)
                guestscriteria = lambda g: (predictions[g.name], g.memoryused, g.name)
                sortedguests = sorted(guestmap.keys(), key=guestscriteria)
                self.logger.debug("hosts: %r", tophosts)
                self.logger.debug("guests: %r", sortedguests)
                self.logger.debug("guestmap: %r", guestmap)
                migrations = [] # [(srchost, guest, dsthost), ...]
                for host in tophosts:
                    for guest in sortedguests[:]:
                        guesthost = guestmap[guest]
                        if (availcapacity[host.name] >= predictions[guest.name]
                                and availmemory[host.name] > guest.memoryused):
                            # good to migrate:
                            if guesthost != host:
                                migrations.append((guesthost, guest, host))
                                availcapacity[guesthost.name] += predictions[guest.name]
                                availmemory[guesthost.name] += guest.memoryused
                            availcapacity[host.name] -= predictions[guest.name]
                            availmemory[host.name] -= guest.memoryused
                            sortedguests.remove(guest)
                self.logger.info("migrations: %r", migrations)
                for srchost, guest, dsthost in migrations:
                    self.logger.info("migrating %s from %s to %s", guest.name,
                            srchost.name, dsthost.name)
                    self._vmmlock.acquire()
                    try:
                        self.vmm.migrate(srchost.name, guest.name, dsthost.name)
                    finally:
                        self._vmmlock.release()

    def start(self):
        try:
            t = threading.Thread(target=self._collect_stats)
            t.start()
            self._schedule()
        finally:
            self._finished.set()
            self.vmm.close()
