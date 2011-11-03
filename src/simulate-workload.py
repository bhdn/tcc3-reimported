#!/usr/bin/env python
import sys
import time
import signal

running = False

counter = 0

def handler(signum, frame):
    global running
    running = False

def work_for(usage=0.50, interval=10):
    global running
    global counter
    signal.signal(signal.SIGALRM, handler)
    cur = time.time()
    dur = interval * usage
    print "working for", dur
    if dur > 0.0:
        signal.setitimer(signal.ITIMER_REAL, dur)
        running = True
        while running:
            x = 0.001 + 323232.0
            counter += 1
    print "awake, counter:", counter
    now = time.time()
    time.sleep(max(interval - (now - cur), 0))

interval = float(sys.argv[1])

for line in open(sys.argv[2]):
    rawvalue = line.strip()
    if not rawvalue:
        continue
    value = float(rawvalue)
    print "current load:", value
    work_for(value / 100.0, interval)
    sys.stdout.flush()
