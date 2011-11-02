#!/usr/bin/env python
import re
hosts = "n2", "n3", "n4", "n6", "seggie"

data_re = re.compile("Accuracy = [^%]+% \\((?P<correct>[\\d]+)/(?P<total>[\\d]+)\\) \\(classification\\)")

chart = {}

for testhost in hosts:
    for predicthost in hosts:
        for class_ in xrange(4):
            path = "output-test%s-train%s-%02d" % (testhost, predicthost,
                    class_)
            data = open(path).read()
            found = data_re.search(data)
            if not found:
                raise Exception, "didnt match!: %s" % (data)
            correct = int(found.group("correct"))
            total  = int(found.group("total"))
            print testhost, "vs", predicthost, correct, "/", total
            testdict = chart.setdefault(testhost, {})
            correctsum, totalsum = testdict.setdefault(predicthost, (0, 0))
            testdict[predicthost] = (correctsum + correct, totalsum + total)
print chart

print "\t",
for host in hosts:
    print host, "\t",
print "avg"
for testhost, predictions in chart.iteritems():
    print testhost, "\t",
    subtot = 0.0
    for predicthost in sorted(predictions):
        correct, total = predictions[predicthost]
        perc = (correct/float(total)) * 100.0
        subtot += perc
        print "%.2f%%\t" % (perc),
    avg = subtot / len(predictions)
    print "%.2f%%" % (avg)
