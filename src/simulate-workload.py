#!/usr/bin/env python
import sys
import time
import signal

running = False

def handler(signum, frame):
    global running
    running = False

def work_for(usage=0.50, interval=10)
    global running
    signal.signal(signal.SIGALRM, handler)
    cur = time.time()
    dur = interval * usage
    print "sleeping for", dur
    signal.setitimer(signal.ITIMER_REAL, dur)
    running = True
    while running:
        x = 0.001 + 323232.0
    print "awake!"
    now = time.time()
    time.sleep(max(interval - (now - cur), 0))

interval = float(sys.argv[1])

for rawvalue in open(sys.argv[2]):
    value = float(rawvalue.strip())
    print "current load:", value
    work_for(value, interval)
