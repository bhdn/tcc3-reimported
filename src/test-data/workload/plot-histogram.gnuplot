# from:
# http://gnuplot-surprising.blogspot.com/2011/09/statistic-analysis-and-histogram.html
reset
n=100	#number of intervals
max=100	#max value
min=0	#min value
width=(max-min)/n	#interval width
#function used to map a value to the intervals
hist(x,width)=width*floor(x/width)+width/2.0
set encoding utf8
set term postscript eps color font 20
#set term png
#set size 0.7,0.7
set xrange [min:max]
set yrange [0:]
#to put an empty boundary around the
#data inside an autoscaled graph.
#set offset graph 0.05,0.05,0.05,0.0
set xtics min,(max-min)/5,max
#set boxwidth width*0.9
#set border lw 0.5
set style fill solid 0.5	#fillstyle
#set tics out nomirror
#count and plot
#

set ylabel "Frequência"
set xlabel "Valor coletado de uso de CPU (%)"

set output "histograma-n2.eps"
plot "workload-n2.txt-full" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb"green" notitle
set output "histograma-n3.eps"
plot "workload-n3.txt-full" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb"green" notitle
set output "histograma-n4.eps"
plot "workload-n4.txt-full" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb"green" notitle
set output "histograma-n6.eps"
plot "workload-n6.txt-full" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb"green" notitle
set output "histograma-seggie.eps"
plot "workload-seggie.txt-full" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb"green" notitle
