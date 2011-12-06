all: trabalho.pdf exemplo.pdf apresentacao.pdf
trabalho.pdf: revisao.tex introducao.tex metodologia.tex consideracoes.tex \
	resultados.tex \
	aprendizado.tex \
	definicoes.tex \
	glossario.tex \
	relacionados.tex \
	anexos.tex \
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
	img-libvirt-contexto1.pdf \
	src/test-data/workload/histograma-n2.pdf \
	src/test-data/workload/histograma-n3.pdf \
	src/test-data/workload/histograma-n4.pdf \
	src/test-data/workload/histograma-n6.pdf \
	src/test-data/workload/histograma-seggie.pdf \
	src/test-data/workload/dispersion-n2.png \
	src/test-data/workload/dispersion-n3.png \
	src/test-data/workload/dispersion-n4.png \
	src/test-data/workload/dispersion-n6.png \
	src/test-data/workload/dispersion-seggie.png \
	src/test-data/workload/dispersion-4h-n4.png \
	src/test-data/classification/knn-n2.pdf \
	src/test-data/classification/knn-n3.pdf \
	src/test-data/classification/knn-n4.pdf \
	src/test-data/classification/knn-n6.pdf \
	src/test-data/classification/knn-seggie.pdf \
	src/test-data/classification/svm-n2.pdf \
	src/test-data/classification/svm-n3.pdf \
	src/test-data/classification/svm-n4.pdf \
	src/test-data/classification/svm-n6.pdf \
	src/test-data/classification/svm-seggie.pdf \
	src/test-data/classification/svm-n2-finer.pdf \
	src/test-data/classification/svm-n3-finer.pdf \
	src/test-data/classification/svm-n4-finer.pdf \
	src/test-data/classification/svm-n6-finer.pdf \
	src/test-data/classification/svm-seggie-finer.pdf \
	src/test-data/classification/svm-seggie.pdf \
	src/test-data/classification/svm-n2-window-future.pdf \
	src/test-data/classification/svm-n3-window-future.pdf \
	src/test-data/classification/svm-n4-window-future.pdf \
	src/test-data/classification/svm-n6-window-future.pdf \
	src/test-data/classification/svm-seggie-window-future.pdf \
	src/test-data/scheduler/stats-knn-oneday-used.pdf \
	src/test-data/scheduler/stats-svm-oneday-host0.pdf \
	src/test-data/scheduler/stats-knn-oneday-host0.pdf \
	src/test-data/scheduler/stats-svm-oneday-host1.pdf \
	src/test-data/scheduler/stats-knn-oneday-host1.pdf \
	src/test-data/scheduler/stats-tendency-oneday-host0.pdf \
	src/test-data/scheduler/stats-tendency-oneday-used.pdf \
	src/test-data/scheduler/stats-svm-real-oneday-tcc159.pdf \
	src/test-data/scheduler/stats-svm-real-oneday-used.pdf \
	src/test-data/scheduler/stats-svm-manual-oneday-tcc159.pdf \
	src/test-data/scheduler/stats-svm-manual-oneday-tcc158.pdf \
	src/test-data/scheduler/stats-svm-manual-oneday-used.pdf \
	src/test-data/checking-load-simulator/load-simulator-n4.pdf

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

src/test-data/%.pdf: src/test-data/%.eps
	epstopdf --outfile=$@ $<

src/test-data/workload/workload-%.eps: src/test-data/workload/plot-histogram.gnuplot
	cd src/test-data/workload; gnuplot $(<F)

src/test-data/workload/dispersion-%.png: src/test-data/workload/plot-dispersion.gnuplot
	cd src/test-data/workload; gnuplot $(<F)

src/test-data/classification/%.eps: src/test-data/classification/plot-stats.gnuplot
	cd $(<D); gnuplot $(<F)

src/test-data/scheduler/%.eps: src/test-data/scheduler/plot.gnuplot
	cd $(<D); gnuplot $(<F)
src/test-data/checking-load-simulator/%.eps: src/test-data/checking-load-simulator/plot.gnuplot
	cd $(<D); gnuplot $(<F)

.PHONY: clean
clean:
	rm -f *.aux *.log *.lof *.loc *.lot *.qdr *.out *.blg *.bbl *.pdf
