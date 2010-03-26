all: trabalho.pdf
%.pdf: %.tex xunxos-utp.sty biblio.bib Makefile
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<
