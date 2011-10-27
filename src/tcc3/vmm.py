from tcc3.registry import Registry
import logging
import time
import libvirt # TODO load it only when needed
from tcc3.util import system_command, CommandError

class VirtualMachineMonitor(object):

    def __init__(self, config):
        raise NotImplementedError

    def list_guests(self):
        raise NotImplementedError

    def migrate(self, guestname, srchost, dsthost):
        raise NotImplementedError

    def get_stats(self, guestname):
        raise NotImplementedError

class GuestInfo:

    def __init__(self, name):
        self.name = name
        self.cpuusage = None
        self.memoryused = None
        self.cpus = None

    def __repr__(self):
        return "<guest %r>" % (self.name)

class HostInfo:

    def __init__(self, name):
        self.name = name
        self.url = None
        self.freememory = None
        self.memory = None
        self.maxcpus = None
        self.guests = set()
    
    def __repr__(self):
        return "<host %r>" % (self.name)

class LibvirtVMM(VirtualMachineMonitor):

    def __init__(self, config):
        self.config = config
        self.hosts = config.hosts.split()
        self.guests = config.guests.split()
        self.scheme = config.libvirt_scheme.strip()
        self.urlsuffix = config.libvirt_url_suffix.strip()
        self.logger = logging.getLogger("tcc3.vmm.libvirt")
        self.cpucount = self._parse_ncpu_config(config.hosts_ncpus)
        self.memorycount = self._parse_ncpu_config(config.hosts_memory)
        self._previnfo = {}
        self._conns = {}

    def _parse_ncpu_config(self, rawvalue):
        config = {}
        for rawdef in rawvalue.split():
            try:
                name, rawcount = rawdef.split(":", 1)
                count = int(rawcount)
            except ValueError:
                self.logger.warn("invalid host-ncpus configuration: %r", rawdef)
                continue
            config[name] = count
        return config

    def _parse_memory(self, rawvalue):
        return self._parse_ncpu_config(self, rawvalue)

    def _host_url(self, host):
        return self.scheme + host + self.urlsuffix

    def _get_connection(self, host):
        url = self._host_url(host)
        try:
            conn = self._conns[host]
            conn.getVersion() # is it still connected?
        except (KeyError, libvirt.libvirtError), e:
            self.logger.debug("opening connection to %s", url)
            self._conns[host] = conn = libvirt.open(url)
        return conn

    def _invalidate_connections(self):
        self.logger.debug("invalidating libvirt connections")
        for conn in self._conns.values():
            try:
                conn.close()
            except libvirt.libvirtError:
                pass
        self._conns = {}

    def migrate(self, srchost, guest, dsthost):
        srcurl = self._host_url(srchost)
        dsturl = self._host_url(dsthost)
        migurl = "tcp://" + dsthost + ":49152"
        args = ["virsh", "-c", srcurl, "migrate", "--persistent", guest, dsturl,
                "--migrateuri", migurl]
        for i in xrange(10):
            self._invalidate_connections()
            try:
                system_command(args)
            except CommandError, e:
                # possibly related to a connection problem
                continue
            else:
                break

    def collect_stats(self):
        # use the same method of virtManager/domain.py to get the cpu usage
        # percentage (_sample_cpu_stats)
        # also http://people.redhat.com/~rjones/virt-top/faq.html#calccpu
        for host in self.hosts:
            conn = self._get_connection(host)
            hostinfo = HostInfo(host)
            for id in conn.listDomainsID():
                dom = conn.lookupByID(id)
                name = dom.name()
                info = dom.info()
                self.logger.info("state for machine %s: %s", name, info[0])
                if info[0] != libvirt.VIR_DOMAIN_RUNNING:
                    self.logger.debug("ignoring guest %s as it is "
                            "either crashed or shutoff", name)
                    self._invalidate_connections()
                    continue
                memory = info[2]
                prevcpuabs, prevtimestamp = self._previnfo.get(name, (0, 0))
                cputime = info[4] - prevcpuabs
                cpuabs = info[4]
                guestcpus = info[3]
                now = time.time()
                # FIXME ensure it is always >= 0.0 <= 100.0
                elapsed = ((now - prevtimestamp) * 1000.0 * 1000.0 * 1000.0)
                pcentbase = (((cputime) * 100.0) / elapsed)
                pcentGuestCpu = pcentbase / guestcpus
                self._previnfo[name] = (cpuabs, now)
                pcent = min(100, max(int(pcentGuestCpu), 0))
                self.logger.debug("host %s, info: %r, pcent: %d", name,
                        info, pcent)
                guestinfo = GuestInfo(name)
                guestinfo.cpuusage = pcent
                guestinfo.memoryused = memory
                guestinfo.cpus = dom.maxVcpus()
                hostinfo.guests.add(guestinfo)
            hostinfo.freememory = conn.getFreeMemory()
            # maxvcpus is not reliable, let's make it configurable for now,
            # fallback for 2cpus
            hostinfo.maxcpus = self.cpucount.get(hostinfo.name, 2)
            hostinfo.memory = self.memorycount.get(hostinfo.name, 1024*1024)
            yield hostinfo

    def close(self):
        self._invalidate_connections()

vmms = Registry()
vmms.register("libvirt", LibvirtVMM)

def get_vmm(config):
    return vmms.get_instance(config.vmm_type, config)
