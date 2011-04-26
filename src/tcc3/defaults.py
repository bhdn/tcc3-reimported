
CONFIG_DEFAULTS = """\
[tcc3]
log-format = $(levelname)s: $(message)s
database-type = csv
collector-type = vmstat
main-database-name = main
trained-database-name = trained
databases-dir = ./databases

learning-method = svm-multiclass

knn-number-neighbours = 10

future-values = 6
svm-window-size = 30

t = 0
C = 0.02
gamma = 0.00005
degree = 5

params = -t %(t)s -c %(C)s -g %(gamma)s -d %(degree)s -v 5

libsvm-learn-command = ../../libsvm/libsvm-3.1/svm-train %(params)s
libsvm-classify-command = ../../libsvm/libsvm-3.1/svm-predict

svmlight-learn-command = ../../libsvm/svm_learn %(params)s
svmlight-classify-command = ../../libsvm/svm_classify

svm-samples = 10000
svm-test = 8000
svm-test-dir = ./databases/svmlight-test/
svm-trained-dir = ./databases/svmlight-trained/

cpu-usage-ranges = 3
max-cpu-value = 100

[conf]
path-environment = TCC3_CONF
user-file = .tcc3.conf
system-file = /etc/tcc3/tcc3.conf
"""
