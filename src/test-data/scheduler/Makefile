# set tw=0
all:
	zcat scheduler-dummy-knn-4-one-day-six-hosts-stripped.log.gz | ../../parse-sched-log.py | grep host0 > stats-knn-oneday-host0
	zcat scheduler-dummy-knn-4-one-day-six-hosts-stripped.log.gz | ../../parse-sched-log.py | grep host1 > stats-knn-oneday-host1
	-zcat scheduler-dummy-knn-4-one-day-six-hosts-stripped.log.gz | ../../parse-sched-log.py | grep host2 > stats-knn-oneday-host2
	-zcat scheduler-dummy-knn-4-one-day-six-hosts-stripped.log.gz | ../../parse-sched-log.py | grep host3 > stats-knn-oneday-host3
	zcat scheduler-dummy-knn-4-one-day-six-hosts-stripped.log.gz | ../../parse-sched-log.py | grep used > stats-knn-oneday-used 
	zcat scheduler-dummy-svm-2-one-day-six-hosts.log.gz | ../../parse-sched-log.py | grep host0 > stats-svm-oneday-host0
	zcat scheduler-dummy-svm-2-one-day-six-hosts.log.gz | ../../parse-sched-log.py | grep host1 > stats-svm-oneday-host1
	-zcat scheduler-dummy-svm-2-one-day-six-hosts.log.gz | ../../parse-sched-log.py | grep host2 > stats-svm-oneday-host2
	-zcat scheduler-dummy-svm-2-one-day-six-hosts.log.gz | ../../parse-sched-log.py | grep host3 > stats-svm-oneday-host3
	zcat scheduler-dummy-svm-2-one-day-six-hosts.log.gz | ../../parse-sched-log.py | grep used > stats-svm-oneday-used
	:
	zcat scheduler-tendency-oneday-0.log.gz | ../../parse-sched-log.py | grep host0 > stats-tendency-oneday-host0
	zcat scheduler-tendency-oneday-0.log.gz | ../../parse-sched-log.py | grep host1 > stats-tendency-oneday-host1
	-zcat scheduler-tendency-oneday-0.log.gz | ../../parse-sched-log.py | grep host2 > stats-tendency-oneday-host2
	-zcat scheduler-tendency-oneday-0.log.gz | ../../parse-sched-log.py | grep host3 > stats-tendency-oneday-host3
	zcat scheduler-tendency-oneday-0.log.gz | ../../parse-sched-log.py | grep used > stats-tendency-oneday-used
	:
	zcat scheduler-real-svm-2.log.gz | ../../parse-sched-log-real.py | grep tcc159 > stats-svm-real-oneday-tcc159
	zcat scheduler-real-svm-2.log.gz | ../../parse-sched-log-real.py | grep tcc158 > stats-svm-real-oneday-tcc158
	zcat scheduler-real-svm-2.log.gz | ../../parse-sched-log-real.py | grep used > stats-svm-real-oneday-used
	:
	zcat scheduler-libvirt-svm-0-6-hosts-manual-stripped.log.gz | ../../parse-sched-log-real.py | grep tcc159 > stats-svm-manual-oneday-tcc159
	zcat scheduler-libvirt-svm-0-6-hosts-manual-stripped.log.gz | ../../parse-sched-log-real.py | grep tcc158 > stats-svm-manual-oneday-tcc158
	-zcat scheduler-libvirt-svm-0-6-hosts-manual-stripped.log.gz | ../../parse-sched-log-real.py | grep lviv > stats-svm-manual-oneday-lviv
	zcat scheduler-libvirt-svm-0-6-hosts-manual-stripped.log.gz | ../../parse-sched-log-real.py | grep used > stats-svm-manual-oneday-used
	touch $@
