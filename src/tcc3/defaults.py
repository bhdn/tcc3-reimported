
CONFIG_DEFAULTS = """\
[tcc3]
log-format = $(levelname)s: $(message)s
database-type = csv
collector-type = vmstat
main-database-name = main
trained-database-name = trained
databases-dir = ./databases

vmstat-fields = id
learning-method = svm
knn-number-neighbours = 10
future-values = 10
svm-window-size = 10
s = 0
t = 2
C = 1.525
gamma = 0.79
degree = 5
cpu-usage-ranges = 4
svm-samples = 5000
svm-test = 1000

params = -s %(s)s -t %(t)s -c %(C)s -g %(gamma)s -d %(degree)s

libsvm-learn-command = ../../libsvm/libsvm-3.1/svm-train %(params)s
libsvm-classify-command = ../../libsvm/libsvm-3.1/svm-predict

svmlight-learn-command = ../../libsvm/svm_learn %(params)s
svmlight-classify-command = ../../libsvm/svm_classify

svm-test-dir = ./databases/svmlight-test/
svm-trained-dir = ./databases/svmlight-trained/

max-cpu-value = 100

[conf]
path-environment = TCC3_CONF
user-file = .tcc3.conf
system-file = /etc/tcc3/tcc3.conf
"""
