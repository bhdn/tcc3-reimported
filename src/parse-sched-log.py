#!/usr/bin/env python
import re
import sys

# DEBUG: guestmap: {<guest 'seggie'>: <host 'host0'>, <guest 'n4'>: <host 'host0'>, <guest 'n2'>: <host 'host0'>, <guest 'n6'>: <host 'host0'>, <guest 'n3'>: <host 'host0'>}

is_re = re.compile("DEBUG: (?P<guest>[^ ]+) is (?P<perc>[^%]+)%")
pair_re = re.compile("<guest '(?P<guest>[^']+)'>: <host '(?P<host>[^']+)'>")

first = None
all = []
cur = {}
if len(sys.argv) > 1:
    f = open(sys.argv[1])
else:
    f = sys.stdin
for line in f:
    match = is_re.search(line)
    if match:
        guest = match.group("guest")
        perc = float(match.group("perc"))
        if first is None:
            first = guest
        elif guest == first:
            all.append(cur)
            cur = {}
        cur[guest] = perc
    found = pair_re.findall(line)
    if found:
        usage = {}
        used = set()
        for guest, host in found:
            used.add(host)
            if guest in cur:
                if host in usage:
                    usage[host] += cur[guest]
                else:
                    usage[host] = cur[guest]
        for host, perc in usage.iteritems():
            print host, perc
        print "used", len(used)
