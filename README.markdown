_abntex-utp_ — pacote L<sup><small>A</small></sup>T<sub>E</sub>X para as normas da UTP
=======================================================================================

Este é um pacote adaptando as definições do pacote
[ABNT<sub>E</sub>X](http://abntex.codigolivre.org.br/) para as normas da
UTP.

O que é L<sup><small>A</small></sup>T<sub>E</sub>X?
----------------------------------------------------

É uma ferrenta para escrita e editoração de documentos. Leia sobre. É bom
para você.

Como usar esse template?
------------------------

* Instale algum sistema TEX/LATEX: texlive, tetex, miktex, etc..
* Baixe este modelo
* Execute `make`
* Veja o pdf gerado
* Modifique o template para o seu trabalho
* Profit

Como instalar os pacotes de LATEX?
----------------------------------

Testei apenas em Linux, mas acredito que, usando o Miktex, seja possível
usar em Windows também.

Em [Mandriva Linux](http://www.mandriva.com/):

* Execute `urpmi texlive-latex make` 

Não testei, mas eis os meus palpites para Ubuntu e Debian:

* Instale `texlive-latex-base` e `texlive-latex-extra` (e, naturalmente,
  todas as dependências necessárias.)
* Instale `make`

Como baixar e usar o _abntex-utp_?
----------------------------------

Para baixar o _abntex-utp_, é necessário usar a ferramenta git
(referenciado como _o git_).

[git](http://git-scm.com/) é uma ferramenta de controle de versão.
Recomendo que continue mantendo seu trabalho usando esta ferramenta. Assim
como LATEX, também é bom para você.

Para instalar em Mandriva Linux:

* `urpmi git-core`

Em Ubuntu e Debian, instale `git-core`.

Em Windows, instale o [msysgit](http://code.google.com/p/msysgit/).

Depois de ter o git instalado, você deve baixar o projeto, executando:

> git clone http://github.com/bhdn/abntex-utp.git

Depois é só ir alterando `trabalho.tex` para ter o conteúdo do seu trabalho
e executando `make` para ter `trabalho.pdf`.

Como reportar problemas ou pedir modificações?
-----------------------------------------------

É só criar uma _issue_ [nesta página](http://github.com/bhdn/abntex-utp/issues)
do Github descrevendo o problema ou o pedido.
