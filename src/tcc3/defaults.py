
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

svm-window-size = 5
libsvm-params = -s 0 -c 1 -b 1 -t 2 -h 0
libsvm-dir = thirdparty/libsvm/python/

svm-samples = 5000

svmlight-command = ../../libsvm/svm_learn -t 2

cpu-usage-ranges = 3
max-cpu-value = 100

[conf]
path-environment = TCC3_CONF
user-file = .tcc3.conf
system-file = /etc/tcc3/tcc3.conf
"""
