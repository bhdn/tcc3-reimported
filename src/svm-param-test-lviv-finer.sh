#!/bin/bash -ex
for C in 0.03125 0.0625 0.125 0.25 0.5 0.75 1 1.25 1.5 2; do
  for gamma in 0.03125 0.0625 0.125 0.25 0.5 0.75 1 1.25 1.5 1.75 2; do
    echo "***** C: $C, gamma: $gamma"
    rm -rf databases/
    for h in n2 n3 n4 n6 seggie; do
      ./tcc3-collect -o "tcc3.svm-params=-s 0 -t 2 -c $C -g $gamma" \
        -H $h vmstat-$h-partial.log
    done 
    wait
    for h in n2 n3 n4 n6 seggie; do
      ./tcc3-train -o "tcc3.svm-params=-s 0 -t 2 -c $C -g $gamma" \
        -H $h -v &
    done 
    wait
    for h in n2 n3 n4 n6 seggie; do
      echo "testing host $h"
      ./tcc3-test -o "tcc3.svm-params=-s 0 -t 2 -c $C -g $gamma" \
        -H $h &
    done 
    wait
  done
done
