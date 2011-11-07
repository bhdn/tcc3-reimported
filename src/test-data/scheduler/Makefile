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
