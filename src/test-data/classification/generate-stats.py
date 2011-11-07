#!/usr/bin/env python
import sys
import re

count_re = re.compile("\*\*\*\*\* windowsize: (?P<window>[\d]+), futurevalue: (?P<future>[\d]+)")
total_re = re.compile("INFO: (?P<host>[^:]+): total/correct: (?P<total>[\d]+)/(?P<correct>[\d]+)")

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
            total = int(match.group("total"))
            correct = int(match.group("correct"))
            print window, future, host, float(correct)/total*100.0
