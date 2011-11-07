#!/usr/bin/env python
import sys
import re

count_re = re.compile("\*\*\*\*\* windowsize: (?P<window>[\d]+), futurevalue: (?P<future>[\d]+)")
total_re = re.compile("host (?P<host>n2|n3|n4|n6|seggie): (?P<perc>[^%]+)")

window = None
future = None
for line in sys.stdin:
    if line.startswith("*****"):
        match = count_re.search(line)
        window = int(match.group("window"))
        future = int(match.group("future"))
    else:
        match = total_re.match(line)
        if match:
            host = match.group("host")
            perc = float(match.group("perc"))
            print window, future, host, perc
