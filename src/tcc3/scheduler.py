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
        self.nranges = int(config.cpu_usage_ranges)
        self.logger = logging.getLogger("tcc3.scheduler")

    def start(self):
        readings = {} # {guestname: deque of stats}
        canpredict = False
        while True:
            self.logger.debug("scheduler tick %r", readings)
            predictions = {} # guestname: predicted class_
            hostpredictions = {}
            hostsinfo = set(self.vmm.collect_stats())
            # collect information about hosts and predict cpu usage for
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
            time.sleep(1)
            if canpredict:
                self.logger.debug("predictions: %r", predictions)
                self.logger.debug("hostpredictions: %r", hostpredictions)
                # compute max cpu capacity for each host (in the same unity
                # used as in "class_"):
                maxcapacity = dict((hi.name, hi.maxcpus * (self.nranges - 1))
                                    for hi in hostsinfo)
                availcapacity = dict((hi.name,
                    (maxcapacity[hi.name] - hostpredictions[hi.name]))
                    for hi in hostsinfo)
                # used capacity as pointed by the predictions:
                # compute a list of the hosts that are most likely to
                # accomodate idle vms (those that already host many vms and are
                # able to keep even more, thus resulting in less vm-migrations
                # and more chance of being able to put idle hosts in
                # power-saving mode)
                sortcriteria = lambda hi: (len(hi.guests),
                        maxcapacity[hi.name], hi.freememory)
                tophosts = sorted(hostsinfo, key=sortcriteria, reverse=True)
                bottomhosts = list(reversed(tophosts)) # hosts that likely
                                                       # to be shut down
                migrations = [] # [(srchost, guest, dsthost), ...]
                migrated = set()
                weakhosts = []
                availmemory = dict((hi.name, hi.freememory)
                        for hi in hostsinfo)
                # first 'force' of migrations: try to put guests toghether
                # as most as possible by pulling those idle in hosts:
                for i, tophost in enumerate(tophosts):
                    if tophost in weakhosts:
                        # no need to go further, all hosts from now on are
                        # 'weak'
                        break
                    for j, bottomhost in enumerate(reversed(tophosts)):
                        if tophost == bottomhost:
                            continue
                        for guest in bottomhost.guests:
                            if guest in migrated:
                                continue
                            if (availmemory[tophost.name] > guest.memoryused
                                    and availcapacity[tophost.name] > predictions[guest.name]):
                                migrations.append((bottomhost, guest, tophost))
                                availmemory[tophost.name] -= guest.memoryused
                                availcapacity[tophost.name] -= predictions[guest.name]
                                availmemory[bottomhost.name] += guest.memoryused
                                availcapacity[bottomhost.name] += predictions[guest.name]
                                migrated.add(guest)
                                weakhosts.append(bottomhost)
                # second force: spread guests that are demanding more
                # resources from (overloaded) hosts and still trying to
                # preserve 'bottomhosts' from not going into power-save
                # mode
                sortcriteria = lambda guest: (predictions[guest.name],
                        guest.memoryused)
                for hostinfo in hostsinfo:
                    if availcapacity[hostinfo.name] < 0:
                        topguests = sorted(hostinfo.guests,
                                key=sortcriteria, reverse=True)
                        for guest in topguests:
                            # reversed(weakhosts) means 'those that were not considered
                            # the most unlikely to receive migrations'
                            for weakhost in reversed(weakhosts):
                                if (availmemory[weakhost.name] > guest.memoryused
                                        and availcapacity[weakhost.name] > predictions[guest.name]):
                                    migrations.append((hostinfo, guest, weakhost))
                                    availmemory[weakhost.name] -= guest.memoryused
                                    availcapacity[weakhost.name] -= predictions[guest.name]
                                    migrated.add(guest)
                self.logger.debug("migrations: %r", migrations)
                time.sleep(1)

