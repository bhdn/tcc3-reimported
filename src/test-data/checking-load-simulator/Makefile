N = 500
output.pdf:	steadysmaller.txt workloadsmaller.txt plot.gnuplot
	gnuplot plot.gnuplot

steadysmaller.txt:
	head -$(N) > $@

smaller.txt:
	sed -u 1,1d workload-log.txt | head -$(N) | awk '{print $2}' > $@
