all: trabalho.pdf exemplo.pdf apresentacao.pdf
trabalho.pdf: revisao.tex introducao.tex metodologia.tex consideracoes.tex \
	cronograma.tex \
	aprendizado.tex \
	definicoes.tex \
	img-met-contexto-0.pdf
img-%.pdf: img-%.eps
	epstopdf --outfile=$@ $<
img-%.eps: img-%.dia
	dia --export=$@ $<
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
