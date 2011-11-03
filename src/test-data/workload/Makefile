all: $(foreach name,$(wildcard *.txt.gz),$(subst .gz,,$(name)))
%.txt: %.txt.gz
	zcat $< | head -20160 > $@
