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

Em [Mandriva Linux](http://www.mandriva.com/):

* Execute `urpmi texlive-latex make` 

Não testei, mas eis os meus palpites para Ubuntu e Debian:

* Instale `texlive-latex-base` e `texlive-latex-extra` (e, naturalmente,
  todas as dependências necessárias.)
* Instale `make`

Para Windows:

* Instale o [MikTeX](http://miktex.org)
* Siga as instruções de download instalação do ABNTEX [nesta página](http://sourceforge.net/apps/mediawiki/abntex/index.php?title=Instala%C3%A7%C3%A3o).
* Fique atento para usar uma versão que seja igual ou superior à 0.9-beta2.

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

Em Windows, instale o [msysgit](http://code.google.com/p/msysgit/), baixe o arquivo
git-_algumacoisa_.exe e instale.

Depois de ter o git instalado, você deve baixar o projeto, executando:

> git clone http://github.com/bhdn/abntex-utp.git

Depois é só ir alterando `trabalho.tex` para ter o conteúdo do seu trabalho
e executando `make` para ter `trabalho.pdf`.

Para Windows, abra o arquivo `trabalho.tex` (o MikTeX deve associar esse tipo
com o TeXworks) e clique no ícone que parece um botão de play, mas tem descrição
"Typeset". Com isso deve ser suficiente para ter o PDF gerado. Recomendo usar o
Notepadd++ ou algum outro editor melhor que o TeXworks, especialmente se você
alterna o desenvolvimento entre Linux e Windows.

Como reportar problemas ou pedir modificações?
-----------------------------------------------

É só criar uma _issue_ [nesta página](http://github.com/bhdn/abntex-utp/issues)
do Github descrevendo o problema ou o pedido.
