set encoding utf8
set term postscript eps color font 20

set ylabel "Uso de CPU de todas as tarefas"
set xlabel "Observações a cada ciclo do escalonador"

set output "stats-knn-oneday-host0.eps"
plot "stats-knn-oneday-host0" u 2 title "Demanda total de CPU para host0 (KNN)"

set output "stats-knn-oneday-host1.eps"
plot "stats-knn-oneday-host1" u 2 title "Demanda total de CPU para host1 (KNN)"

set output "stats-svm-oneday-host0.eps"
plot "stats-svm-oneday-host0" u 2 title "Demanda total de CPU para host0 (SVM)"

set output "stats-svm-oneday-host1.eps"
plot "stats-svm-oneday-host1" u 2 title "Demanda total de CPU para host1 (SVM)"

set output "stats-tendency-oneday-host0.eps"
plot "stats-tendency-oneday-host0" u 2 title "Demanda total de CPU para host0 (tendencia)"

set output "stats-tendency-oneday-host1.eps"
plot "stats-tendency-oneday-host1" u 2 title "Demanda total de CPU para host1 (tendencia)"

set output "stats-svm-real-oneday-tcc159.eps"
plot "stats-svm-real-oneday-tcc159" u 2 title "Demanda total de CPU para tcc158 (SVM)"

set output "stats-svm-real-oneday-tcc158.eps"
plot "stats-svm-real-oneday-tcc158" u 2 title "Demanda total de CPU para tcc159 (SVM)"

set output "stats-svm-manual-oneday-tcc159.eps"
plot "stats-svm-manual-oneday-tcc159" u 2 title "Demanda total de CPU para tcc158 (SVM)"

set output "stats-svm-manual-oneday-tcc158.eps"
plot "stats-svm-manual-oneday-tcc158" u 2 title "Demanda total de CPU para tcc159 (SVM)"

set yrange [0:3]

set ylabel "Número de hospedeiros utiilizados"
set xlabel "Observações a cada ciclo do escalonador"

set output "stats-knn-oneday-used.eps"
plot "stats-knn-oneday-used" u 2 title "Hospedeiros usados para KNN" \
	with impulses

set output "stats-svm-oneday-used.eps"
plot "stats-svm-oneday-used" u 2 title "Hospedeiros usados para SVM" \
	with impulses

set output "stats-tendency-oneday-used.eps"
plot "stats-tendency-oneday-used" u 2 title "Hospedeiros (baseado em tendencia)" \
	with impulses

set output "stats-svm-real-oneday-used.eps"
plot "stats-svm-real-oneday-used" u 2 title "Hospedeiros (SVM)" \
	with impulses

set output "stats-svm-manual-oneday-used.eps"
plot "stats-svm-manual-oneday-used" u 2 title "Hospedeiros (SVM)" \
	with impulses

set output "stats-svm-knn-oneday-used.eps"
plot "stats-svm-oneday-host1" u 2 title "Hospedeiros usados para SVM", \
     "stats-knn-oneday-host1" u 2 title "Hospedeiros usados para KNN"
