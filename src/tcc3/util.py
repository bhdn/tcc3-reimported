import subprocess
from tcc3 import Error

class CommandError(Error):
    pass

def system_command(args, show=False):
    if show:
        stdout = subprocess.STDOUT
        stderr = None
    else:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT
    proc = subprocess.Popen(args, shell=False, stdout=stdout,
            stderr=stderr, bufsize=1024 * 1024 * 5)
    proc.wait()
    output = ""
    if show:
        output = proc.stdout.read()
    if proc.returncode != 0:
        cmdline = subprocess.list2cmdline(args)
        raise CommandError, "command failed: %s:\n%s" % (cmdline, output)
    return output, proc.returncode
