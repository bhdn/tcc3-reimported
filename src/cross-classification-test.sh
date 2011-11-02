#!/bin/bash -xe
for trainhost in n2 n3 n4 n6 seggie; do
	for testhost in n2 n3 n4 n6 seggie;do
		for i in {0..3}; do
			n=`printf "%02d" $i`
			../../libsvm/libsvm-3.1/svm-predict \
				./databases/svmlight-test/$testhost-$n \
				./databases/svmlight-trained/$trainhost-$n \
				/tmp/train-results-test$testhost-train$trainhost-$n |
			tee /tmp/output-test$testhost-train$trainhost-$n
done; done; done
