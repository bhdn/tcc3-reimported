import subprocess
from tcc3 import Error

class CommandError(Error):
    pass

def system_command(args):
    proc = subprocess.Popen(args, shell=False)
    proc.wait()
    if proc.returncode != 0:
        cmdline = subprocess.list2cmdline(args)
        output = proc.stdout.read()
        raise CommandError, "command failed: %s:\n%s" % (cmdline, output)
    return output, returncode
