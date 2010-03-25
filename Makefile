estudo-caso.pdf: estudo-caso.tex xunxos-utp.sty biblio.bib Makefile
	pdflatex $<
	bibtex estudo-caso
	pdflatex $<
	pdflatex $<

teste.pdf: teste.tex
	latex teste.tex
	latex teste.tex
	dvipdf teste.dvi

