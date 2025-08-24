﻿---
title: Desenvolvimento web em camadas com API
authors: Luccas Marra do Amaral
type: post
image: https://i.imgur.com/yS6Tb6R.png
date: 2018-11-03
excerpt: Entenda mais sobre camadas na web e organize seu código
categories:
  - Front-end
  - Back-end
  - HTML
  - CSS
tags:
  - Desenvolvimento web
  - Desenvolvimento web em camadas
---

Muitos programadores web iniciam suas carreiras desenvolvendo websites e aplicações web como se fosse uma “brincadeira”, simplesmente pelo fato de serem fascinados por tecnologia e terem curiosidade no assunto. Entre noites em claro, buscas incessantes por respostas e muita persistência, são impactados pelo retorno “Success”, uma mensagem magnífica para quem após centenas de tentativas em milhares de linhas de código conseguiu atingir o resultado tão esperado. Mas, você organizou do jeito certo? Você não vai querer ler tudo novamente para realizar manutenções. 

Pensando nisso resolvi explicar de maneira rápida e didática as três camadas web e uma breve explicação sobre API. Esse conteúdo proporcionará que seu código fique mais organizado, além disso, você vai poder otimizar seu tempo conquistando melhores resultados, dessa forma, quando precisar fazer manutenção achará tudo o que precisar. 

### 1. HTML - Primeira Camada
Hypertext Markup Language, em português: Linguagem de Marcação de Hipertexto

É a linguagem base da internet criada para estruturar e organizar os conteúdos de sua página e foi desenvolvido para ser de fácil entendimento por todos, incluindo pessoas e máquinas. Utilize nomear seus arquivos de acordo com o conteúdo e que realmente exista neles, exemplo: Se a página mostra sobre projetos, que tal:  projetos.html



### 2. CSS - Segunda Camada

Cascading Style Sheets, em português Folha de Estilos em Cascata

Pelo nome já podemos identificar que é basicamente uma linguagem de regras de estilo que tem como objetivo alterar a forma visual do HTML, deixando sua página visualmente mais atrativa. Muitos utilizam o CSS diretamente no HTML. Porém, para melhorar a organização, deve ser a nossa segunda chamada. Além disso, ela deve estar dentro do HTML entre a tag HEAD, por exemplo:

```
<head>
	<link rel= stylesheet" href=”caminho-do-seu-arquivo.css">
</head>
```

Dica: Existem inúmeras estilizações que você pode aplicar ao seu HTML, pesquise um pouco no Google sobre CSS/CSS3 ou “Como estilizar minha página com CSS”, você encontrará uma gama de resultados que lhe ajudarão. Utilize suas estilizações a classes e ids de maneira que possa utilizá-los diversas vezes, otimizando seu código e reduzindo suas linhas.



### 3.JavaScript - Terceira Camada

É uma linguagem de interpretação que nos permite manipular elementos. Atualmente a maior parte das aplicações web usufruem dele para gerar interações dinâmicas com o cliente, como por exemplo ao clicar em um botão, a informação que antes estava oculta, agora pode aparecer sem precisar recarregar a página. E para você adicionar essa terceira camada ao nosso arquivo HTML utilize a tag:

```
<script src="caminho-do-seu-arquivo.js"></script>
```

Dica: Existem diversas bibliotecas, tais como Ajax e Jquery que nos possibilitam realizar ações de maneira mais fácil e nos conectar com a nossa quarta camada, a API.


### 4.API 
Acrônimo de Application Programming Interface, em português Interface de Programação de Aplicativos

Nada mais é que um “cérebro”. Responsável por gerar resultados para determinada requisição que pode ser desenvolvida em diversas linguagens. Na maioria das vezes possui comunicação a bancos de dados com o objetivo de responder prontamente as solicitações feitas. Como por exemplo quando realizamos um login, informamos nosso e-mail e senha para a API decidir se os dados estão corretos e você pode ou não acessar aquele conteúdo. 

Dica: Procure no google “Como realizar uma consulta MYSQL utilizando Ajax e PHP” e continue aprendendo. 



**Organizando as camadas e API**

![img](https://i.imgur.com/GU5KGDx.png)



**1 - Crie uma pasta para colocar seus arquivos, exemplo:  meu projeto**

**2 - Dentro dela crie as pastas: css, js, apis**

**3 - Dentro de cada pasta coloque o arquivo que se refere a explicação acima:**

Na pasta css, coloque o arquivo caminho-do-seu-arquivo.css. Na pasta js, coloque o arquivo caminho-do-seu-arquivo.js. Em apis, coloque o arquivo que será responsável por responder suas requisições.

*Desse jeito você poderá organizar de maneira simples sua aplicação web. Esse é um artigo introdutório e caso queira se aprofundar e saber mais sobre organização procure sobre MVC.*