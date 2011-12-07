set terminal postscript eps color font 20

set xlabel "Janela"
set ylabel "Futuro"

set view 108,74

set output "knn-n2.eps"
splot "knn-stats-n2" using 1:2:4 title "KNN n2"

set output "knn-n3.eps"
splot "knn-stats-n3" using 1:2:4 title "KNN n3"

set output "knn-n4.eps"
splot "knn-stats-n4" using 1:2:4 title "KNN n4"

set output "knn-n6.eps"
splot "knn-stats-n6" using 1:2:4 title "KNN n6"

set output "knn-seggie.eps"
splot "knn-stats-seggie" using 1:2:4 title "KNN seggie"

set xlabel "C"
set ylabel "$\sigma$"

set output "svm-n2.eps"
splot "svm-stats-n2" using 1:2:4 title "SVM n2"

set output "svm-n3.eps"
splot "svm-stats-n3" using 1:2:4 title "SVM n3"

set output "svm-n4.eps"
splot "svm-stats-n4" using 1:2:4 title "SVM n4"

set output "svm-n6.eps"
splot "svm-stats-n6" using 1:2:4 title "SVM n6"

set output "svm-seggie.eps"
splot "svm-stats-seggie" using 1:2:4 title "SVM seggie"

set output "svm-n2-finer.eps"
splot "svm-stats-finer-n2" using 1:2:4 title "SVM n2"

set output "svm-n3-finer.eps"
splot "svm-stats-finer-n3" using 1:2:4 title "SVM n3"

set output "svm-n4-finer.eps"
splot "svm-stats-finer-n4" using 1:2:4 title "SVM n4"

set output "svm-n6-finer.eps"
splot "svm-stats-finer-n6" using 1:2:4 title "SVM n6"

set output "svm-seggie-finer.eps"
splot "svm-stats-finer-seggie" using 1:2:4 title "SVM seggie"

set xlabel "Janela"
set ylabel "Futuro"

set output "svm-n2-window-future.eps"
splot "svm-stats-window-future-n2" using 1:2:4 title "SVM n2"

set output "svm-n3-window-future.eps"
splot "svm-stats-window-future-n3" using 1:2:4 title "SVM n3"

set output "svm-n4-window-future.eps"
splot "svm-stats-window-future-n4" using 1:2:4 title "SVM n4"

set output "svm-n6-window-future.eps"
splot "svm-stats-window-future-n6" using 1:2:4 title "SVM n6"

set output "svm-seggie-window-future.eps"
splot "svm-stats-window-future-seggie" using 1:2:4 title "SVM seggie"

set output "svm-vs-knn-n4.eps"
set view 63,115
splot "svm-stats-n4" using 1:2:4 title "SVM", "knn-stats-n4" using 1:2:4 title "k-NN"
