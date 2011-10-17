from tcc3.registry import Registry
import logging
import time
import libvirt # TODO load it only when needed

class VirtualMachineMonitor(object):

    def __init__(self, config):
        raise NotImplementedError

    def list_guests(self):
        raise NotImplementedError

    def migrate(self, guestname, srchost, dsthost):
        raise NotImplementedError

    def get_stats(self, guestname):
        raise NotImplementedError

class LibvirtVMM(VirtualMachineMonitor):

    def __init__(self, config):
        self.config = config
        self.hosts = config.hosts.split()
        self.guests = config.guests.split()
        self.scheme = config.libvirt_scheme.strip()
        self.urlsuffix = config.libvirt_url_suffix.strip()
        self.logger = logging.getLogger("tcc3.vmm.libvirt")
        self._previnfo = {}
        self._conns = {}

    def collect_stats(self):
        # use the same method of virtManager/domain.py to get the cpu usage
        # percentage (_sample_cpu_stats)
        # also http://people.redhat.com/~rjones/virt-top/faq.html#calccpu
        for host in self.hosts:
            url = self.scheme + host + self.urlsuffix
            try:
                conn = self._conns[host]
                conn.version() # is it still connected?
            except (KeyError, libvirt.libvirtError), e:
                self._conns[host] = conn = libvirt.open(url)
            for id in conn.listDomainsID():
                dom = conn.lookupByID(id)
                name = dom.name()
                info = dom.info()
                if info[0] in (libvirt.VIR_DOMAIN_CRASHED,
                        libvirt.VIR_DOMAIN_SHUTOFF):
                    self.logger.debug("ignoring guest %s as it is "
                            "either crashed or shutoff", name)
                    continue
                prevcpuabs, prevtimestamp = self._previnfo.get(name, (0, 0))
                cputime = info[4] - prevcpuabs
                cpuabs = info[4]
                guestcpus = info[3]
                now = time.time()
                elapsed = ((now - prevtimestamp) * 1000.0 * 1000.0 * 1000.0)
                pcentbase = (((cputime) * 100.0) / elapsed)
                pcentGuestCpu = pcentbase / guestcpus
                self._previnfo[name] = (cpuabs, now)
                yield name, int(pcentGuestCpu)

vmms = Registry()
vmms.register("libvirt", LibvirtVMM)

def get_vmm(config):
    return vmms.get_instance(config.vmm_type, config)
