---
title: 12 plugins jQuery para começar bem o ano
authors: Davi Ferreira
type: post
date: 2011-02-17
excerpt: Confira uma lista de plugins jQuery, em sua maioria novidades, para acrescentar opções à sua caixa de ferramentas na hora de desenvolver uma interface web.
url: /12-plugins-jquery-para-comecar-bem-o-ano/
dsq_thread_id: 503040009
categories:
  - Javascript
  - Código
tags:
  - JQuery

---
O grande diferencial do jQuery é sua enorme biblioteca de plugins. Na lista abaixo, veremos plugins que cobrem desde upload de arquivos, passando por uma galeria de imagens diferente e indo até um emulador de livro/revista (aquele esquema de folhear, bastante famoso em aplicativos flash).

Procurei escolher plugins mais novos, desenvolvidos recentemente, mas nem todos seguem este padrão. Meu sonho é poder fazer, um dia, uma lista desse tipo apenas com plugins brasileiros. No entanto, ainda é escasso o conteúdo nacional desenvolvido para jQuery. Caso você tenha algum link de um plugin bacana, compartilhe nos comentários no final da página.

### CLEditor

<a href="https://premiumsoftware.net/cleditor/" target="_blank">https://premiumsoftware.net/cleditor/</a>

<img src="https://raw.githubusercontent.com/diegoeis/tableless-static-images/master/2011/02/cleditor.jpg" alt="CLEditor em ação" width="627" height="159" class="alignnone size-full wp-image-2947" srcset="uploads/2011/02/cleditor.jpg 627w, uploads/2011/02/cleditor-300x76.jpg 300w" sizes="(max-width: 627px) 100vw, 627px" />

No mundo dos editores rich text em javascript, o CKEditor (antigo FCK) e o TinyMCE são os mais famosos. Por serem muito completos, acabam sendo também extremamente pesados. O CLEditor é uma alternativa desenvolvida em jQuery, simples, mas &#8220;pesando&#8221; apenas 16KB. É claro que não vem acompanhado de módulo para upload de imagens e arquivos, inserção e configuração avançada de flash etc., mas nem sempre essas funcionalidades são necessárias.

### jQuery file upload

<a href="https://aquantum-demo.appspot.com/file-upload" target="_blank">https://aquantum-demo.appspot.com/file-upload</a>

Esse é um plugin bem interessante. Ele transforma um simples formulário de upload de arquivos em uma interface avançada com opção de envio de múltiplos arquivos ao mesmo tempo, barra de progresso, drag and drop e cancelamento do upload. Nos navegadores que já oferecem suporte, ele efetua o upload via XMLHttpRequest e pra navegadores sem suporte utiliza o bom e velho iframe oculto. A documentação é pobre, mas vale a pena dar uma fuçada. Outro ponto legal é que este plugin não utiliza flash na sua interface de upload.

### ezColumns

<a href="https://www.andresvidal.com/labs/ezcolumns.html" target="_blank">https://www.andresvidal.com/labs/ezcolumns.html</a>

Plugin mão na roda para sites que utilizam conteúdo em colunas e precisam que essas colunas possuam a mesma altura, porém, de forma dinâmica. O que o ezColumns faz é pegar todos os elementos filhos de um container e alinhar a altura de acordo a maior encontrada. Permite ainda definir o número de colunas e o template utilizado para englobar cada coluna.

### Embedded Help

<a href="https://embedded-help.net/" target="_blank">https://embedded-help.net/</a>

<img src="https://raw.githubusercontent.com/diegoeis/tableless-static-images/master/2011/02/help.jpg" alt="Embedded Help em ação" width="627" height="159" class="alignnone size-full wp-image-2950" srcset="uploads/2011/02/help.jpg 627w, uploads/2011/02/help-300x76.jpg 300w" sizes="(max-width: 627px) 100vw, 627px" />

Focado em usabilidade, este plugin oferece uma interface de ajuda dinâmica, em tempo real, a medida que o usuário precisa dela. Por exemplo, você pode exibir tooltips e até mesmo emular o movimento do mouse para indicar ao usuário o que ele deve fazer. O site é um pouco confuso, a documentação também (um problema para quase todos os plugins novos), mas este plugin é genial.

### Snippet

<a href="https://steamdev.com/snippet/" target="_blank">https://steamdev.com/snippet/</a>

Plugin simples para aplicar syntax highlighting em códigos de um artigo, texto etc. O plugin pode ser aplicado em qualquer elemento _<pre>_ e oferece suporte à diversas linguagens incluindo javascript, html/css, php e algumas opções avançadas de configuração como expandir/esconder códigos.

### xcolor

<a href="https://www.xarg.org/project/jquery-color-plugin-xcolor/" target="_blank">https://www.xarg.org/project/jquery-color-plugin-xcolor/</a>

O plugin xcolor adiciona inúmeras possibilidades para tratamento e manipulação de cores e, de quebra, também oferece um método para verificar a legibilidade de um texto. Entre suas funcionalidades estão:

  * métodos para extrair camadas (RGB) de uma cor;
  * a possibilidade de retornar o nome mais próximo de uma cor para CSS;
  * um parser de cores;
  * animação em gradiente.

### Quovolver

<a href="https://sandbox.sebnitu.com/jquery/quovolver/" target="_blank">https://sandbox.sebnitu.com/jquery/quovolver/</a>

Quovolver é um plugin simples, mas ideal para uma área muito comum em sites corporativos: depoimentos. Ele exibe, de forma elegante, um bloco de citações. Ele bem que podia ser um pouco mais flexível nas configurações, mas, por se tratar de um plugin, vamos dar um crédito extra e aguardar as novidades das próximas versões.

### Booklet

<a href="https://builtbywill.com/code/booklet/" target="_blank">https://builtbywill.com/code/booklet/</a>

Estamos quase acabando! Este é um dos plugins mais legais desta lista. O Booklet imita o movimento de folhear e é altamente personalizável. Cada página é representada por elementos filhos de um div. O plugin possui mais de 30 opções de parâmetros, entre elas o sentido das páginas, o cursor a ser utilizado e a opção de habilitar uma hashstring na URL para navegação. E o melhor de tudo é que é bem leve: 17KB na versão minified.

### MobilyMap

<a href="https://playground.mobily.pl/jquery/mobily-map.html" target="_blank">https://playground.mobily.pl/jquery/mobily-map.html</a>

<img src="https://raw.githubusercontent.com/diegoeis/tableless-static-images/master/2011/02/mobily.jpg" alt="MobilyMap em ação" width="627" height="159" class="alignnone size-full wp-image-2952" srcset="uploads/2011/02/mobily.jpg 627w, uploads/2011/02/mobily-300x76.jpg 300w" sizes="(max-width: 627px) 100vw, 627px" />

Outro plugin bastante interessante. O MobilyMap transforma qualquer imagem em uma interface à la GoogleMaps, com opção de arrastar, adicionar marcadores etc. Também é altamente personalizável. Os marcadores podem possuir tooltips contendo informações e links.

### Shadow Animation

<a href="https://www.bitstorm.org/jquery/shadow-animation/" target="_blank">https://www.bitstorm.org/jquery/shadow-animation/</a>

Como o próprio nome sugere, este plugin estende a funcionalidade do método animate() para aceitar também a propriedade CSS box-shadow. Os efeitos gerados são bem interessantes &#8211; é ideal para menus e para um destaque maior em imagens.

### CloudZoom

<a href="https://www.professorcloud.com/mainsite/cloud-zoom.htm" target="_blank">https://www.professorcloud.com/mainsite/cloud-zoom.htm</a>

E por falar em imagens, vamos encerrar nossa lista com dois plugins para elas. O primeiro é o CloudZoom, efeito muito utilizado em sites de e-commerce para ampliar a imagem de um produto sem abrir camadas e lightboxes. O zoom é feito ou na própria área da imagem, ou em uma área que não interfere muito no conteúdo. Possui opções de cores no zoom e legendas.

### Popeye

<a href="https://dev.herr-schuessler.de/jquery/popeye/" target="_blank">https://dev.herr-schuessler.de/jquery/popeye/</a>

<img src="https://raw.githubusercontent.com/diegoeis/tableless-static-images/master/2011/02/popeye.jpg" alt="Popeye em ação" width="627" height="159" class="alignnone size-full wp-image-2953" srcset="uploads/2011/02/popeye.jpg 627w, uploads/2011/02/popeye-300x76.jpg 300w" sizes="(max-width: 627px) 100vw, 627px" />

Por último, uma alternativa valiosa para todos os lightboxes e uma forma diferente de exibir fotos e galerias em sua página. O plugin Popeye exibe as galerias _inline_ em um artigo ou texto e suas opções de exibição procuram interferir o mínimo possível na leitura. As transições são muito bacanas e as opções de paginação e legenda também &#8220;saltam aos olhos&#8221;.