
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

future-values = 10
svm-window-size = 15

libsvm-params = -t 2 -d 5 -c 10
libsvm-trained-dir = ./databases/libsvm-trained/
libsvm-dir = thirdparty/libsvm/python/

svm-samples = 10000
svm-test = 4000

svmlight-learn-command = ../../libsvm/svm_learn -t 2
svmlight-classify-command = ../../libsvm/svm_classify
svmlight-trained-dir = ./databases/svmlight-trained/
svmlight-test-dir = ./databases/svmlight-test/

cpu-usage-ranges = 4
max-cpu-value = 100

[conf]
path-environment = TCC3_CONF
user-file = .tcc3.conf
system-file = /etc/tcc3/tcc3.conf
"""
