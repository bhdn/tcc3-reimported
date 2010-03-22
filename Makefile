estudo-caso.pdf: estudo-caso.tex xunxos-utp.sty biblio.bib Makefile
	latex $<
	bibtex estudo-caso
	latex $<
	latex $<
	dvipdf estudo-caso.dvi

teste.pdf: teste.tex
	latex teste.tex
	latex teste.tex
	dvipdf teste.dvi

