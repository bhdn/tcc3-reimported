
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
svm-window-size = 20

t = 2
C = 2.0
gamma = 0.5

params = -t %(t)s -c %(C)s -g %(gamma)s

libsvm-learn-command = ../../libsvm/libsvm-3.1/svm-train %(params)s
libsvm-classify-command = ../../libsvm/libsvm-3.1/svm-predict

svmlight-learn-command = ../../libsvm/svm_learn %(params)s
svmlight-classify-command = ../../libsvm/svm_classify

svm-samples = 8000
svm-test = 4000
svm-test-dir = ./databases/svmlight-test/
svm-trained-dir = ./databases/svmlight-trained/

cpu-usage-ranges = 2
max-cpu-value = 100

[conf]
path-environment = TCC3_CONF
user-file = .tcc3.conf
system-file = /etc/tcc3/tcc3.conf
"""
