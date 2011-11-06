
CONFIG_DEFAULTS = """\
[tcc3]
log-format = $(levelname)s: $(message)s
database-type = csv
collector-type = vmstat
main-database-name = main
trained-database-name = trained
databases-dir = ./databases
libvirt-scheme = qemu+tcp://
libvirt-url-suffix = /system

ar-coefs = 10

vmm-type = libvirt
dummy-guests = n2:test-data/workload/workload-n2.txt:host0:131072:1
    n3:test-data/workload/workload-n3.txt:host0:131072:1
    n4:test-data/workload/workload-n4.txt:host0:131072:1
    n6:test-data/workload/workload-n6.txt:host0:131072:1
    seggie:test-data/workload/workload-seggie.txt:host0:131072:1
dummy-hosts = host0 host1
dummy-hosts-ncpus = host0:2 host1:2
dummy-hosts-memory = host0:3597132

sched-interval = 10
guests = tcc0 tcc1 tcc2 tcc3 tcc4 tcc5
hosts = tcc159 tcc158 lviv
hosts-ncpus = tcc159:4 tcc158:2 lviv:2
hosts-memory = tcc159:3597132 tcc158:4023472 lviv:4023472


skip-zeroes = 1
vmstat-fields = id
learning-method = svm
knn-number-neighbours = 10
knn-test = 10000
knn-train = 10000
future-values = 10
window-size = 10
s = 0
t = 2
C = 1.0
gamma = 0.79
degree = 4
cpu-usage-ranges = 4
svm-samples = 20000
svm-test = 70000

svm-params = -s %(s)s -t %(t)s -c %(C)s -g %(gamma)s
libsvm-learn-command = ../../libsvm/libsvm-3.1/svm-train
libsvm-classify-command = ../../libsvm/libsvm-3.1/svm-predict

svmlight-learn-command = ../../libsvm/svm_learn
svmlight-classify-command = ../../libsvm/svm_classify

svm-test-dir = ./databases/svmlight-test/
svm-trained-dir = ./databases/svmlight-trained/

max-cpu-value = 100

[conf]
path-environment = TCC3_CONF
user-file = .tcc3.conf
system-file = /etc/tcc3/tcc3.conf
"""
