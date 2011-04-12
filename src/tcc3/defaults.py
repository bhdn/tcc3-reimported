
CONFIG_DEFAULTS = """\
[tcc3]
log-format = $(levelname)s: $(message)s
database-type = csv
collector-type = vmstat
main-database-name = main
trained-database-name = trained
databases-dir = ./databases
learning-method = svm

knn-number-neighbours = 10

libsvm-dir = thirdparty/libsvm/python/
svm-window-size = 5
svm-params = -s 0 -c 1 -b 1 -t 2 -h 0

cpu-usage-ranges = 3
max-cpu-value = 100

[conf]
path-environment = TCC3_CONF
user-file = .tcc3.conf
system-file = /etc/tcc3/tcc3.conf
"""
