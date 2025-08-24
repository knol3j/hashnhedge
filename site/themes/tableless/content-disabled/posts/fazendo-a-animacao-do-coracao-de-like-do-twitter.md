---
title: Fazendo a animação do coração de like do Twitter
authors: Diego Eis
type: post
date: 2016-01-12
excerpt: Fazendo a animação do coraçãozinho do Twitter.
url: /fazendo-a-animacao-do-coracao-de-like-do-twitter/
categories:
  - CSS
  - Técnicas e Práticas
tags:
  - CSS
  - heart
  - twitter

---
Quando o Twitter colocou uma animação no coração de Like na versão web, eu fiquei me perguntando como fazer aquela animação. De cara, parece ser bastante simples, e é. Mas é um detalhe que faz a diferença na interface para quem usa a rede social com frequência. Fiz uma versão mais simples. Segue abaixo:

<script async src="//jsfiddle.net/tableless/jk7zvh26/embed/html,css,result/"></script>

Antes de olhar o código deles pra pesquisar como foi feito, fiquei pensando em uma série de formas para fazer isso aí. Primeiro, pensei em ter várias imagens, e aí usar `keyframes` pra alterar esse background do elemento a cada X tempo de milésimos de segundos. Depois evolui o pensamento para fazer apenas uma imagem, com todos os &#8220;frames&#8221; da animação. Muito mais inteligente, claro&#8230; lembra dos Sprites&#8230; Pois é. Com essa imagem eu poderia simplesmente mover o background com um transition simples do CSS. A imagem em questão é essa aqui:

![](https://raw.githubusercontent.com/diegoeis/tableless-static-images/master/2016/01/web_heart_animation.png)

Quando utilizamos a propriedade `transition`, geralmente usamos os valores `linear`, `ease-in`, `ease-out` e etc&#8230; Essas funções definem como os valores intermediários de uma transição serão calculados. Eles pegam um valor inicial e calculam como a transição vai ocorrer até o valor final.


 ![][https://developer.mozilla.org/files/3426/cubic-bezier,ease-in.png]
 <br><br>
 ![][https://mdn.mozillademos.org/files/3429/cubic-bezier,ease.png]

Dá uma olhada nessa [tabela de referência][https://easings.net] de como as transições funcionam.

Há um valor que eu não conhecia até então, chamado `steps()`. A representação da transição do steps é assim:
  
![][https://mdn.mozillademos.org/files/3437/steps(4,end).png]

O `steps()`, ao contrário dos outros valores, não determina uma transição contínua, mas ele separa os valores intermediários em frames estáticos. Veja um exemplo básico abaixo. Um usando linear e outro usando steps().

Esse efeito seria o mesmo efeito que eu conseguiria se tivesse feito manualmente a primeira ideia de separar os frames da animação em várias imagens&#8230; Mas muito mais inteligente. Mas perceba que eu ainda faço a transição movendo a posição do background. O valor `left` do `background-position` começa no **** e termina no **-2800px**. Esse valor é exatamente a largura da imagem original que você quer fazer a animação. O coração do twitter é bem menor do que esse que eu estamos usando aqui no exemplo (embora a imagem seja a mesma). Aí é só mudar o tamanho usando o `background-size` e fazendo os devidos acertos.

O final, ficou assim:
<script async src="//jsfiddle.net/tableless/jk7zvh26/embed/html,css,result/"></script>
