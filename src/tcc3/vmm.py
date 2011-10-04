
class VirtualMachineMonitor(object):

    def __init__(self, config):
        pass

    def list_hosts(self):
        raise NotImplementedError

    def list_guests(self):
        raise NotImplementedError

    def migrate(self, guestname, srchost, dsthost):
        raise NotImplementedError

    def get_stats(self, guestname):
        raise NotImplementedError

class LibvirtVMM(VirtualMachineMonitor):

    pass

vmms = Registry()
vmms.register("libvirt", LibvirtVMM)

def get_vmm(config):
    return vmms.get_instance(config.vmm_type, config)
