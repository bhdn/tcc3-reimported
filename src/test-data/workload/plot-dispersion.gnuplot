#set term postscript font 7 portrait
set encoding utf8
set term png
#set size 0.7,0.4
#set border lw 0.5
#

set ylabel "Tempo usado de CPU (%)"

set output "dispersion-n3.png"
plot "workload-n3.txt-full" u 1  notitle with dots

set output "dispersion-n2.png"
plot "workload-n2.txt-full" u 1 notitle with dots

set output "dispersion-n6.png"
plot "workload-n6.txt-full" u 1 notitle with dots

set output "dispersion-seggie.png"
plot "workload-seggie.txt-full" u 1 notitle with dots

set pointsize 0.5
set output "dispersion-4h-n4.png"
plot "workload-n4-4h.txt" u 1 notitle with points pt 4

set output "dispersion-n4.png"
plot "workload-n4.txt-full" u 1 notitle with dots
