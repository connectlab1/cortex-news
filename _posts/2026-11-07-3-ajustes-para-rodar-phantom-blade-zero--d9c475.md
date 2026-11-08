---
layout: post
title: "3 ajustes para rodar Phantom Blade Zero com o máximo desempenho no PC"
date: 2026-11-07 11:00:00 +0000
categories: [Canaltech]
---

Phantom Blade Zero está sendo jogado por centenas de milhares de PC gamers nesse exato momento, nas configurações gráficas e especificações de máquina mais variadas possíveis. O jogo foi feito na Unreal Engine 5 e, embora tenha seu peso por conta disso, e**le é bem otimizado em geral, mas sempre dá para deixar a experiência melhor**.

Depois de investir mais de 50 horas no game, percebi o que pesa e o que não pesa, quais efeitos é melhor ativar ou desativar, ou talvez mudar um preset inteiro, e trago aqui algumas dicas rápidas. Minha experiência foi em uma **RTX 5070**, com **Core Ultra 9 285K** e **32 GB de RAM**, rodando o game em **1440p, preset alto e com DLAA do DLSS ativado**.

## 1\. Realismo dos raios e seu peso

Ray Tracing é algo que pesa muito, e mais ainda o **Path Tracing**. Não é nem novidade dizer que, se você, por algum motivo, não é fã de upscaling de imagem ou não gosta nem de geração de quadros, nem cogite essas tecnologias de renderização avançada.

Caso opte por ativar o RT, saiba que **é necessário ativar também a reconstrução de raios**, essencial para deixar os efeitos sem ruídos e com uma qualidade de imagem melhor. Ao fazer isso, você **derruba o desempenho para o mesmo nível do Path Tracing**.

Em uma cena específica com muitos reflexos, onde é possível conseguir mais de **60 FPS em rasterização, ao ativar o Ray Tracing, o desempenho cai para 43 FPS**. Para reduzir os artefatos, temos que ativar a **reconstrução de raios e isso derruba a performance para 35 FPS**. Para efeito de comparação, o **Path Tracing** (que ativa a reconstrução de raios automaticamente) **causa perda de cerca de 10% nesse cenário**.

Claro que tudo isso é ajustável com o DLSS. Considerando os 30 FPS do jogo no alto e com Path Tracing, **ao ativar o upscaling para qualidade, conseguimos quase 50 FPS**. E ajustando o **Frame Generation para 2X** (não recomendo mais do que isso por causa dos artefatos), **passamos de 80 FPS**. O game fica bonito e muito fluido.

**Aqui fica uma observação importante** : cada cenário tem um peso diferente. Alguns se beneficiam mais do que outros com os raios, causando diferença considerável de desempenho.

## 2\. Em rasterização, a conversa é outra

Se você não tem GPU suficiente para Ray/Path Tracing, **Phantom Blade Zero entrega belos visuais em rasterização também** e ainda é consideravelmente mais leve. Meus testes foram no preset gráfico alto, e na mesma cena que escolhi, conseguimos cerca de **62 FPS em 1440p nativo**.

Ao subir todo o preset para **muito alto**, derrubamos o desempenho para algo **em torno de 48 a 50 FPS**. Ou seja, **perda de quase 15%**. **Um dos maiores vilões são os reflexos**, que causam uma **perda média de 6 FPS**. Ao deixar o preset no muito alto e os reflexos em alto, conseguimos 55 FPS nesse cenário, que é bem pesado.

Existem várias outras localizações em que, no preset muito alto, conseguimos mais de 60 FPS sem DLSS facilmente. **Com upscaling em qualidade, é possível conseguir mais do que 80 FPS ao renderizar em 960p e escalonar para 1440p** sem perdas na qualidade de imagem.

Ou seja, caso jogue Phantom Blade Zero em rasterização, escolha o preset alto e o upscaling em qualidade, seja qual for (DLSS, FSR ou XeSS). O game tem visuais belíssimos, mas **ele é muito focado na ação, então uma taxa alta de quadros é essencial**.

## 3\. Jogue sem outras aplicações abertas

Um dos maiores problemas de Phantom Blade Zero é o **consumo altíssimo de memória**. Em diversos momentos, **vi o game batendo 30 GB sem Chrome ou qualquer outra aplicação não essencial rodando ao fundo**.

Caso você esteja jogando com 16 GB de RAM, é muito provável que aconteçam stutterings ocasionais pela falta de memória. Para uma experiência com menos travamentos (já que engasgos acontecem por conta da UE5), deixe o mínimo de aplicações abertas.

---

> **Gostou do assunto?** Para conferir todos os detalhes, imagens originais e a discussão completa, acesse a matéria original.
>
> 👉 **[Ler artigo completo no Canaltech](https://canaltech.com.br/games/phantom-blade-zero-ajustes-para-rodar-maximo-desempenho-pc/)**
