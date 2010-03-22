%.pdf: %.tex xunxos-utp.sty
	latex $<
	latex $<
	dvipdf $*.dvi

teste.pdf: teste.tex
	latex teste.tex
	latex teste.tex
	dvipdf teste.dvi

