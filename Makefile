estudo-caso.pdf: estudo-caso.tex xunxos-utp.sty
	latex $<
	latex $<
	dvipdf estudo-caso.dvi

teste.pdf: teste.tex
	latex teste.tex
	latex teste.tex
	dvipdf teste.dvi

