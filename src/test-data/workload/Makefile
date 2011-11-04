all: $(foreach name,$(wildcard *.txt.gz),$(subst .gz,,$(name))) \
	$(foreach name,n2 n3 n4 n6 seggie,workload-$(name).txt-full) \
	workload-n4-4h.txt
workload-n4-4h.txt: workload-n4.txt-full
	sed 1,10000d $< | head -480 > $@
%.txt: %.txt.gz
	zcat $< | head -2880 > $@
vmstat-%-partial.log: ../mdv-bs-01/mdv-bs-01.tar.gz 
	tar xzf $< $@
workload-%.txt-full: vmstat-%-partial.log
	awk '{print 100-$$15}' $< > $@
