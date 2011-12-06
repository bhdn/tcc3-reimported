N = 500
load-simulator-n4.eps:	steadysmaller.txt workloadsmaller.txt plot.gnuplot
	gnuplot plot.gnuplot

steadysmaller.txt: steady.txt
	head -$(N) $< > $@

workloadsmaller.txt: workload-log.txt
	sed -u 1,1d $< | head -$(N) | awk '{print $$2}' > $@
