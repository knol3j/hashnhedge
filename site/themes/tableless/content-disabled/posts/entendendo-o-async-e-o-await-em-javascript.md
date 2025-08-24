---
title: Entendendo o async e o await em JavaScript
authors: Wendell Adriel
type: post
date: 2016-04-12
excerpt: 'As funcionalidades async / await não conseguiram chegar para o ES6, mas isso não significa que elas não irão chegar ao JavaScript. Enquanto escrevo esse post, ela é uma proposta na fase 3 e está sendo trabalhada ativamente. As funcionalidades já estão no Edge e devem chegar a outros browsers assim que chegar na fase 4 - pavimentando seu caminho para inclusão na próxima edição da linguagem (veja também: Processo TC39).'
url: /entendendo-o-async-e-o-await-em-javascript/
titulo_personalizado:
  - 'Entenda um pouco sobre as funcionalidades <strong>async / await</strong>'
categories:
  - Artigos
  - Destaques
  - Javascript
  - Traduções
tags:
  - Adriel
  - async
  - babel
  - ES6
  - Javascript
  - traducoes
  - Wendell
  - Wendell Adriel

---
## Introdução

As funcionalidades `async` / `await` não conseguiram chegar para o ES6, mas isso não significa que elas não irão chegar ao JavaScript. Enquanto escrevo esse post, ela é uma proposta na <a href="https://github.com/tc39/ecma262/tree/82bebe057c9fca355cfbfeb36be8e42f18c61e94" target="_blank">fase 3</a> e está sendo trabalhada ativamente. As funcionalidades já estão no <a href="https://blogs.windows.com/msedgedev/2015/09/30/asynchronous-code-gets-easier-with-es2016-async-function-support-in-chakra-and-microsoft-edge/" target="_blank">Edge</a> e devem chegar a outros browsers assim que chegar na <a href="https://twitter.com/bterlson/status/692464374842290176" target="_blank">fase 4</a> &#8211; pavimentando seu caminho para inclusão na próxima edição da linguagem (veja também: <a href="https://tc39.github.io/process-document/" target="_blank">Processo TC39</a>). 

## Utilizando Promises

Vamos supor que tenhamos o código abaixo. Aqui eu estou encapsulando uma chamada `HTTP` em uma `Promise`. A promise executa o `body` caso haja sucesso e é rejeitada com um `err` caso contrário. Ela puxa o HTML de um artigo aleatório <a href="https://ponyfoo.com/" target="_blank">desse blog</a> toda vez que é executada. 

<pre class="lang-javascript">var request = require('request');

function getRandomPonyFooArticle () {
  return new Promise((resolve, reject) =&gt; {
    request('https://ponyfoo.com/articles/random', (err, res, body) =&gt; {
      if (err) {
        reject(err); return;
      }
      resolve(body);
    });
  });
}
</pre>

Uma utilização típica da promise mostrada anteriormente está no código abaixo. Nele nós construímos um encadeamento de promises transformando o HTML da página em Markdown de um subconjunto de seu DOM e então imprimimos de forma amigável no terminal utilizando um `console.log`. Sempre lembre de adicionar um `.catch` para suas promises. 

<pre class="lang-javascript">var hget = require('hget');
var marked = require('marked');
var Term = require('marked-terminal');

printRandomArticle();

function printRandomArticle () {
  getRandomPonyFooArticle()
    .then(html =&gt; hget(html, {
      markdown: true,
      root: 'main',
      ignore: '.at-subscribe,.mm-comments,.de-sidebar'
    }))
    .then(md =&gt; marked(md, {
      renderer: new Term()
    }))
    .then(txt =&gt; console.log(txt))
    .catch(reason =&gt; console.error(reason));
}
</pre>

Esse código foi “melhor que utilizar callbacks” quando se trata da sensação de como foi ler o código sequencialmente.

## Usando generators

Nós já exploramos os generators como uma forma de deixar o html disponível de uma maneira sintética e síncrona <a href="https://ponyfoo.com/articles/es6-generators-in-depth" target="_blank">no passado</a>. Mesmo que o código agora seja um pouco síncrono, existe um pouco de encapsulamento envolvido, e generators podem não ser a melhor maneira de chegar aos resultados que queremos, então vamos continuar utilizando Promises. 

<pre class="lang-javascript">function getRandomPonyFooArticle (gen) {
  var g = gen();
  request('https://ponyfoo.com/articles/random', (err, res, body) =&gt; {
    if (err) {
      g.throw(err); return;
    }
    g.next(body);
  });
}

getRandomPonyFooArticle(function* printRandomArticle () {
  var html = yield;
  var md = hget(html, {
    markdown: true,
    root: 'main',
    ignore: '.at-subscribe,.mm-comments,.de-sidebar'
  });
  var txt = marked(md, {
    renderer: new Term()
  });
  console.log(txt);
});
</pre>

> Lembre-se que você deve encapsular a chamada ao yield em um bloco try / catch para preservar o tratamento de erros que adicionamos quando usamos promises.

Nem precisamos falar que usar generators dessa maneira não permite que escalemos bem nossas aplicações. Além de envolver uma sintaxe não intuitiva nessa mistura, seu código iterador será altamente acoplado ao generator que está sendo consumido. Isso faz com que você terá de modificar ele toda vez que uma nova expressão de `await` for inserida no generator. A melhor alternativa é utilizar uma nova funcionalidade que está chegando: **Funções Assíncronas**. 

## Utilizando `async` / `await`

Quando as **Funções Assíncronas** finalmente chegarem, seremos capazes de pegar nossa implementação baseada em promises e tirar a vantagem do estilo de **“aparência síncrona”** dos generators. Outro benefício dessa abordagem é que não teremos que alterar o `getRandomPonyFooArticle`, enquanto ele retornar uma promise ele poderá ser aguardado. 

Perceba que o `await` só poderá ser utilizado em funções marcadas com a palavra chave `async`. Ele funciona similarmente aos generators, suspendendo a execução em seu contexto até que a promise seja entregue. Se a expressão esperada não for uma promise, ela é transformada em uma promise. 

<pre class="lang-javascript">read();

async function read () {
  var html = await getRandomPonyFooArticle();
  var md = hget(html, {
    markdown: true,
    root: 'main',
    ignore: '.at-subscribe,.mm-comments,.de-sidebar'
  });
  var txt = marked(md, {
    renderer: new Term()
  });
  console.log(txt);
}
</pre>

> Novamente &#8211; assim como os generators &#8211; lembre-se que você deverá encapsular o await em um bloco try / catch para que possamos capturar e tratar erros esperados das promises das funções assíncronas. 

Além disso, uma **Função Assíncrona** sempre irá retornar uma `Promise`. Essa promise é rejeitada em caso de exceções não tratadas ou é resolvida e enviada como retorno da função assíncrona caso contrário. Isso nos permite invocar uma Função assíncrona e misturar isso com uma continuação baseada em promises normalmente. O exemplo a seguir mostra como as duas maneiras podem ser combinadas. 

<pre class="lang-javascript">async function asyncFun () {
  var value = await Promise
    .resolve(1)
    .then(x =&gt; x * 3)
    .then(x =&gt; x + 5)
    .then(x =&gt; x / 2);
  return value;
}
asyncFun().then(x =&gt; console.log(`x: ${x}`));
// &lt;- &#039;x: 4&#039;
</pre>

Voltando ao nosso exemplo anterior, ele mostra que podemos usar o `return txt` da nossa função `async read` e permitir que os “consumidores” possam dar continuidade utilizando promises ou até mesmo uma outra **Função Assíncrona**. Dessa maneira, nossa função read deve se preocupar apenas com imprimir um markdown de forma legível no terminal de um artigo aleatório do Pony Foo. 

<pre class="lang-javascript">async function read () {
  var html = await getRandomPonyFooArticle();
  var md = hget(html, {
    markdown: true,
    root: 'main',
    ignore: '.at-subscribe,.mm-comments,.de-sidebar'
  });
  var txt = marked(md, {
    renderer: new Term()
  });
  return txt;
}
</pre>

Então você poderá adicionar mais tarde um `await read()` em outra **Função Assíncrona**.

<pre class="lang-javascript">async function write () {
  var txt = await read();
  console.log(txt);
}
</pre>

Ou poderá simplesmente utilizar promises para dar continuação.

<pre class="lang-javascript">read().then(txt =&gt; console.log(txt));
</pre>

## Bifurcação no caminho

No fluxo assíncrono de código é comum executar duas ou mais tarefas concorrentemente. Enquanto as **Funções Assíncronas** facilitam a escrita de código assíncrono, elas também transformam elas mesmas em um código que é serial, ou seja, código que executa uma operação por vez. Uma função com múltiplos `await` irá ser suspensa uma vez em cada `await` até que a `Promise` chegue (antes de retomar a execução e mover para o próximo `await`, não diferente de como podemos ver com os generators e o `yield`). 

Para contornar isso você pode usar o `Promise.all` para criar uma única promise que você irá dar o `await` nela. O único problema é pegar o hábito de utilizar o `Promise.all` ao invés de deixar tudo ocorrer em série, como também pode diminuir a performance do seu código. 

O exemplo a seguir mostra como você pode utilizar o `await` em três diferentes promises que poderiam ser executadas concorrentemente. Dado que o `await` suspende a sua **Função Assíncrona** e que o `await Promise.all` resulta em um **array de results**, nós podemos desestruturar para puxar resultados individualmente do array. 

<pre class="lang-javascript">async function concurrent () {
  var [r1, r2, r3] = await Promise.all([p1, p2, p3]);
}
</pre>

Até um tempo atrás havia uma alternativa para o código acima: `await*`, onde você não precisava encapsular as promises com o `Promise.all`. O **Babel 5** ainda suporta essa sintaxe, mas ela foi tirada da documentação e também do **Babel 6**. 

<pre class="lang-javascript">async function concurrent () {
  var [r1, r2, r3] = await* [p1, p2, p3];
}
</pre>

Você ainda pode utilizar algo como `all = Promise.all.bind(Promise)` para obter uma alternativa ao `Promise.all`. Partindo desse ponto, você pode fazer o mesmo para o `Promise.race`, que não tinha um equivalente para `await*`. 

<pre class="lang-javascript">const all = Promise.all.bind(Promise);
async function concurrent () {
  var [r1, r2, r3] = await all([p1, p2, p3]);
}
</pre>

## Tratamento de Erros

Note que **erros são engolidos “silenciosamente” nas Funções Assíncronas** &#8211; assim como em `Promises` normais. A menos que você adicione blocos `try` / `catch` ao redor de chamadas `await`, exceções não capturadas &#8211; independentemente se ocorreram no corpo da sua **Função Assíncrona** ou enquanto estava suspensa durante o `await` &#8211; irão rejeitar a `Promise` retornada pela **Função Assíncrona**. 

Naturalmente isso pode ser visto como um ponto forte: você tem a capacidade de tirar proveito das convenções do uso do `try` / `catch`, algo que você era incapaz de realizar com o uso de `callbacks` &#8211; e de alguma forma utilizar com `Promises`. Nesse sentido, **Funções Assíncronas** são semelhantes aos generators, onde você também tinha a capacidade de tirar proveito do uso do `try` / `catch` graças à suspensão da execução da função tornando um fluxo assíncrono em um código síncrono. 

Além disso, você também é capaz de capturar exceções de fora da **Função Assíncrona**, simplesmente adicionando uma cláusula `.catch` à `Promise` que eles retornam. Enquanto isso é uma forma flexível de combinar o tratamento de erros utilizando `try` / `catch` com cláusulas `.catch` nas `Promises`, também pode levar a uma grande confusão e deixar com que erros fiquem sem tratamento. 

<pre class="lang-javascript">read()
  .then(txt =&gt; console.log(txt))
  .catch(reason =&gt; console.error(reason));
</pre>

Nós devemos ter cuidado e educarmos a nós mesmos sobre as diferentes formas em que podemos encontrar, tratar, registrar e prevenir as exceções. 

## Utilizando `async` / `await` hoje

Uma das formas de se utilizar **Funções Assíncronas** em seu código hoje é através do **Babel**. Isso envolve uma série de módulos, mas você pode sempre criar um módulo que encapsula todos esses outros em um se você preferir. Eu incluí um `npm-run` como uma maneira útil de se manter tudo em pacotes instalados localmente. 

<pre class="lang-javascript">npm i -g npm-run
npm i -D \
  browserify \
  babelify \
  babel-preset-es2015 \
  babel-preset-stage-3 \
  babel-runtime \
  babel-plugin-transform-runtime

echo '{
  "presets": ["es2015", "stage-3"],
  "plugins": ["transform-runtime"]
}' &gt; .babelrc
</pre>

O exemplo a seguir irá compilar o arquivo `example.js` utilizando o **browserify** enquanto utiliza o **babelify** para habilitar o suporte às **Funções Assíncronas**. Você pode então enviar o script para o **node** ou **salvar em disco**. 

<pre class="lang-javascript">npm-run browserify -t babelify example.js | node
</pre>

## Leitura adicional

O rascunho das <a href="https://tc39.github.io/ecmascript-asyncawait/" target="_blank">especificações para Funções Assíncronas</a> é bem curto e deve ser uma leitura interessante se você quer aprender mais sobre essa funcionalidade que está por vir. 

Eu colei um pedaço de código abaixo com a finalidade de ajudar você a entender como **Funções Assíncronas** funcionam internamente. Mesmo que não possamos criar novas palavras chave, é importante em termos de compreensão saber o que está acontecendo atrás dar curtinas do `async` / `await`. 

> É útil saber que **Funções Assíncronas** internamente se aproveitam dos **generators** e das **promises**. 

O código a seguir mostra como uma declaração de uma **Função Assíncrona** pode ser transformada em uma função comum que retorna o resultado alimentando a `spawn` com um generator &#8211; onde nós iremos considerar o `await` como o equivalente sintático para `yield`. 

<pre class="lang-javascript">async function example (a, b, c) {
  example function body
}

function example (a, b, c) {
  return spawn(function* () {
    example function body
  }, this);
}
</pre>

Na `spawn`, uma promise é encapsulada em volta do código que irá percorrer o generator &#8211; composta do código do usuário &#8211; em série, repassando valores para o “generator” (corpo da **Função Assíncrona**). Com isso podemos observar que **Funções Assíncronas** são um `syntactic sugar` que utiliza generators e promises, isso faz com que seja importante você entender como cada uma dessas partes trabalham para que você possa ter um melhor entendimento em como você pode misturar, comparar e combinar diferentes tipos de fluxo de código assíncrono juntos. 

<pre class="lang-javascript">function spawn (genF, self) {
  return new Promise(function (resolve, reject) {
    var gen = genF.call(self);
    step(() =&gt; gen.next(undefined));
    function step (nextF) {
      var next;
      try {
        next = nextF();
      } catch(e) {
        // finished with failure, reject the promise
        reject(e);
        return;
      }
      if (next.done) {
        // finished with success, resolve the promise
        resolve(next.value);
        return;
      }
      // not finished, chain off the yielded promise and `step` again
      Promise.resolve(next.value).then(
        v =&gt; step(() =&gt; gen.next(v)),
        e =&gt; step(() =&gt; gen.throw(e))
      );
    }
  });
}
</pre>

> Os pedaços de códigos mostrados devem ajudá-lo a compreender como o algoritmo do `async` / `await` itera sobre uma sequência de generators (expressões `await`), encapsulando cada item na sequência em uma promise e então encadeando com a próxima sequência. Quando a sequência terminar ou uma das promises são rejeitadas ou a promise é retornada para a função que chamou o generator. 

Artigo traduzido e adaptado de: <a href="https://ponyfoo.com/articles/understanding-javascript-async-await" target="_blank">https://ponyfoo.com/articles/understanding-javascript-async-await</a>