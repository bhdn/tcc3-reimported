set encoding utf8
set term postscript eps color font 20
set output "load-simulator-n4.eps"
#set terminal png font Vera
set xlabel "Histórico de carga"
set ylabel "Uso de CPU"
plot "workloadsmaller.txt" using 1 title "Carga simulada", "steadysmaller.txt" using 1 title "Carga observada"
