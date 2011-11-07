#!/bin/bash -ex
for N in {2..15} 30 40 50 75 100 150; do
	echo "***** N: $N"
	rm -rf databases/
	for h in n2 n3 n4 n6 seggie; do
		./tcc3-collect -o "tcc3.knn-number-neighbours=$N" \
			-H $h vmstat-$h-partial.log
	done 
	for h in n2 n3 n4 n6 seggie; do
		./tcc3-train -o "tcc3.knn-number-neighbours=$N" \
			-H $h -v &
	done 
	wait
	for h in n2 n3 n4 n6 seggie; do
		./tcc3-test -o "tcc3.knn-number-neighbours=$N" \
			-H $h &
	done 
	wait
done
