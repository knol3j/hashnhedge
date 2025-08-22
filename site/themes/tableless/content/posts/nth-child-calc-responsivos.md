---
title: nth-child() e calc() – Uma proposta para o abandono de frameworks de grids responsivos
authors: rogerio dias moreira
type: post
date: 2015-07-06
excerpt: Conheça mais sobre estas duas propriedades para a construção de layouts responsivos sem o utilizar frameworks de grids.
url: /nth-child-calc-responsivos/
categories:
  - Código
  - CSS
  - CSS3
  - HTML5
  - O Básico
  - Responsive Web Design (RWD)
  - Técnicas e Práticas
tags:
  - calc
  - CSS
  - CSS3
  - design responsivo
  - html5
  - nth-child

---
> Apesar da adoção do _Tableless_ para construção de layouts o conceito de tabela ainda persiste através de inúmeros _frameworks_ de _grids_ responsivos.

Além da semântica, o conceito _Tableless_ prega, sempre que possível, levar a responsabilidade do layout para o CSS. O problema dos _frameworks_ CSS focados em _grids_ é que a especificação do layout continua dentro do HTML, descrita através de classes CSS, ancoradas diretamente aos elementos HTML, e de forma intrusiva, ou seja, os elementos `<table>` antigamente utilizados foram substituídos por elementos `<div>` para a criação do layout.

![Exemplo de Grid Layout](https://raw.githubusercontent.com/diegoeis/tableless-static-images/master/2015/07/gridLayout.png)

Enquanto a especificação &#8220;<a href="https://www.w3.org/TR/css3-grid-layout/" target="_blank">CSS Grid Layout Module</a>&#8221; ainda está no forno, proponho uma alternativa simples aos _frameworks_ de _grids_ responsivos, através da dupla dinâmica _**nth-child()**_ e _**calc()**_ presentes no CSS3, e que são suportadas pelos navegadores modernos, inclusive o IE9 (veja mais opções de compatibilidade <a href="https://caniuse.com/#search=CALC" target="_blank">aqui</a> e <a href="https://caniuse.com/#search=nth-child" target="_blank">aqui</a>). Para um rápido entendimento destes recursos também confira estes artigos: <https://tableless.com.br/nth-child/> e <a href="https://www.maujor.com/tutorial/css3-funcao-css-calc.php" target="_blank">https://www.maujor.com/tutorial/css3-funcao-css-calc.php</a>

## Exemplo de formulário

Antes de partimos para o CSS, sempre que possível, precisamos usar elementos HTML5 semânticos, atributos WAI-ARIA, entre outros padrões de acessibilidade. Para este exemplo, o uso dos elementos de entradas de dados seguirão as técnicas preconizadas pelo eMAG 3.1 (ver <a href="https://emag.governoeletronico.gov.br/" target="_blank">https://emag.governoeletronico.gov.br/</a>).

Para cada elemento de entrada de dados presente na estrutura _form -> fieldset_ o seguinte padrão será seguido:

<pre><span style="line-height: 1.5;">&lt;label&gt;
    &lt;span&gt;XXX:&lt;/span&gt;
    &lt;input type="text" value=""&gt;
&lt;/label&gt;
</span></pre>

Agora podemos aplicar o seguinte CSS para todos os elementos `<label>` presentes neste padrão.

<pre>form fieldset &gt; label {
    display: block;
    float: left;
    width: calc(100% - 10px);
    height: 55px;
    margin-top: 10px;
    margin-right: 10px;
}
form fieldset label &gt; input {
    float: left;
}
label &gt; input {
    display: block;
    width: 100%;
}
</pre>

Por termos utilizado o _margin-right_ com 10px, este valor foi contabilizado na largura do _label_ (uso da função _calc_) com a finalidade de que sua margem não ultrapasse os limites do contêiner. Isto foi feito para que possamos alterar o layout de uma coluna para múltiplas colunas diretamente pelo CSS. Com este estilo, cada campo de entrada de dados aparecerá disposto como uma lista, e se adaptará a largura do contêiner.

![Exemplo de Código para Criação de Formulário](https://raw.githubusercontent.com/diegoeis/tableless-static-images/master/2015/07/RogerioDias-Artigo2-figura1.png)

O próximo passo é poder criar mais de uma &#8220;coluna&#8221;, para que o campo Código e Nome fiquem na mesma &#8220;linha&#8221; quando o tamanho da tela for grande. O campo Código terá uma largura fixa de 80px e o campo Nome preencherá o restante do espaço do contêiner descontando a largura do campo Código juntamente com a margem de 10px dos dois _labels_.

![Exemplo de Código para Criação de Formulário Responsivo](https://raw.githubusercontent.com/diegoeis/tableless-static-images/master/2015/07/RogerioDias-Artigo2-Figura3.png)

Com estes recursos podemos alterar o layout da página HTML diretamente pelo CSS sem que a estrutura do layout fique no próprio HTML. Além de criar colunas que se adaptam a largura do contêiner, é possível criar colunas com tamanhos fixos, evitando também o uso de classes CSS, que só é encorajado quando for realmente necessário.

O código fonte completo e a _Demo_ deste exemplo encontra-se em <a href="https://codepen.io/rogeriodegoiania/pen/GJQmzb" target="_blank">https://codepen.io/rogeriodegoiania/pen/GJQmzb</a>
