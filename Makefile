all: trabalho.pdf exemplo.pdf apresentacao.pdf
trabalho.pdf: revisao.tex introducao.tex metodologia.tex consideracoes.tex \
	cronograma.tex \
	aprendizado.tex \
	definicoes.tex \
	glossario.tex \
	relacionados.tex \
	img-met-contexto-0.pdf \
	img-met-contexto-1.pdf \
	img-host-guests1.pdf \
	img-host-guests2.pdf \
	img-host-guests3.pdf \
	img-host-guests4.pdf \
	img-vetor0.pdf \
	img-vetor-janela.pdf \
	img-diagrama-classes0.pdf \
	img-diagrama-classes1.pdf \
	img-diagrama-classes2.pdf \
	img-libvirt-contexto0.pdf \
	img-libvirt-contexto1.pdf
img-%.pdf: img-%.eps
	epstopdf --outfile=$@ $<
imgi-%.pdf: imgi-%.svg
	inkscape -D --export-dpi=90 --export-pdf=$@ $<
img-%.eps: img-%.dia
	dia --export=$@ $<
apresentacao.pdf: apresentacao.tex \
		img/img-smith2005cla.png \
		img/img-smith2005vir.png \
		img/fig-hiperplanos.png \
		img-met-contexto-1.pdf \
		img-vetor-janela.pdf \
		imgi-logos.pdf \
		imgi-amb0.pdf \
		imgi-amb1.pdf \
		imgi-amb-usocpu.pdf \
		imgi-amb-migracao.pdf \
		imgi-amb-projeto.pdf \
		img-vetor0.pdf
	pdflatex $<
	bibtex apresentacao
	pdflatex $<
	pdflatex $<
%.pdf: %.tex xunxos-utp.sty biblio.bib Makefile
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<

.PHONY: clean
clean:
	rm -f *.aux *.log *.lof *.loc *.lot *.qdr *.out *.blg *.bbl *.pdf
