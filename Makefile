all: trabalho.pdf exemplo.pdf apresentacao.pdf
trabalho.pdf: revisao.tex introducao.tex metodologia.tex consideracoes.tex cronograma.tex
apresentacao.pdf: apresentacao.tex
	pdflatex $<
%.pdf: %.tex xunxos-utp.sty biblio.bib Makefile
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<

.PHONY: clean
clean:
	rm -f *.aux *.log *.lof *.loc *.lot *.qdr *.out *.blg *.bbl *.pdf
