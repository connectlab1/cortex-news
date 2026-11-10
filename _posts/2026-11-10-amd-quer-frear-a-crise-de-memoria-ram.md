---
layout: post
title: "AMD quer frear a crise de memória RAM com tecnologia revolucionária"
date: 2026-11-10 17:00:00 +0000
categories: [Canaltech]
link: "https://canaltech.com.br/hardware/amd-quer-frear-a-crise-de-memoria-ram-com-tecnologia-revolucionaria/"
---

A novidade mais promissora que a AMD apresentou durante o lançamento dos novos processadores EPYC Venice, na última quarta-feira (4), em Las Vegas, não foram os chips em si, mas uma tecnologia de gerenciamento de memória chamada **MEXT Memory**. Desenvolvida para reduzir os custos dos servidores, a solução pode ter um impacto extremamente positivo no **combate à crise de memória RAM provocada pela demanda dos data centers de inteligência artificial.**

Quando a AMD começou a falar sobre uma tecnologia capaz de substituir metade da memória RAM de um servidor por armazenamento SSD, minha primeira reação foi de desconfiança. Afinal, soluções que prometem ampliar a memória utilizando o armazenamento interno existem há décadas, e nem sempre entregam os ganhos de desempenho esperados.

**Em testes apresentados pela fabricante durante o AMD In Depth 2026, a tecnologia conseguiu preservar 99% do desempenho original de um servidor utilizando apenas metade da memória DRAM.** Um resultado surpreendente e com potencial muito além do que apenas baratear servidores.

Em um momento de crise global de memória RAM, impulsionada pela demanda dos data centers de inteligência artificial, que já encarece celulares, notebooks e outros eletrônicos, a nova tecnologia da AMD pode aliviar a pressão sobre os preços atuais. Não é uma solução imediata nem uma garantia de que os eletrônicos ficarão mais baratos, mas a possibilidade é real.

Por trás da MEXT está a equipe de Gary Smerdon, vice-presidente corporativo de Desenvolvimento de Negócios da divisão de Computação e IA Empresarial da AMD. A proposta é combinar a memória DRAM convencional com SSDs NVMe, que são muito mais baratos, utilizando inteligência artificial para prever quais dados o processador precisará acessar e transferi-los antecipadamente para a memória mais rápida.

**É justamente essa capacidade de antecipação que diferencia a MEXT dos mecanismos tradicionais de memória virtual** e torna a proposta tão revolucionária.

## Como funciona a MEXT Memory da AMD?

A proposta da MEXT parte de um problema antigo da indústria: embora os SSDs sejam muito mais baratos que a memória RAM, eles também são consideravelmente mais lentos, o que impede sua utilização como substitutos diretos da DRAM em aplicações que exigem acesso rápido aos dados.

Segundo Smerdon, o armazenamento flash pode ser **50 vezes mais barato por bit e consumir 30 vezes menos energia por bit que a DRAM**, mas apresenta uma desvantagem importante: sua latência pode ser até 500 vezes maior.

> "Foi aí que surgiu a ideia: e se pudéssemos usar inteligência artificial para esconder essa latência e minimizar esse problema?", explicou o executivo.

A resposta encontrada pela equipe foi **utilizar modelos de IA que rodam em uma camada abaixo do sistema operacional** capazes de identificar quais informações estão sendo efetivamente utilizadas pelo processador e quais podem permanecer temporariamente armazenadas nos SSDs.

Quando determinados dados deixam de ser acessados com frequência, a MEXT transfere tudo da DRAM para o armazenamento flash. Antes que essas informações sejam necessárias novamente, a inteligência artificial tenta antecipar a demanda e devolvê-las à memória mais rápida.

> "Percebemos que poderíamos usar IA para monitorar o sistema e trazer essas páginas de volta para a DRAM de maneira proativa", afirmou Smerdon.

Na prática, o sistema faz com que uma parte do armazenamento flash funcione como uma extensão da memória RAM, sem exigir alterações nos aplicativos que utilizam essa capacidade adicional.

**A ideia lembra a memória RAM virtual, um recurso que sistemas operacionais como Windows e Android utilizam há anos.** Em computadores, o Windows pode recorrer ao arquivo de paginação para armazenar temporariamente dados que não cabem na memória física. Já em celulares, fabricantes como Motorola e Samsung oferecem funcionalidades semelhantes, conhecidas como RAM Boost e RAM Plus.

A Motorola, por exemplo, costuma anunciar o RAM Boost somado à quantidade de memória física de seus smartphones, destacando uma capacidade total de memória que inclui o espaço reservado no armazenamento interno.

Entretanto, essa memória adicional não oferece a mesma velocidade da DRAM. Em [testes realizados pelo Canaltech com celulares equipados com RAM Boost](https://canaltech.com.br/smartphone/vale-a-pena-pagar-mais-por-celular-com-ram-boost-nos-fizemos-os-testes/), o recurso praticamente não trouxe diferenças perceptíveis na velocidade de abertura de aplicativos, carregamento de jogos ou navegação pelo sistema. Os ganhos ficaram restritos a situações específicas, como manter mais aplicativos abertos em segundo plano.

O grande **diferencial da MEXT estaria na utilização de inteligência artificial para antecipar o acesso aos dados,** em vez de depender apenas dos mecanismos tradicionais de gerenciamento da memória virtual. A intenção é diminuir o impacto da lentidão dos SSDs ao trazer as informações necessárias de volta à DRAM antes que o processador precise utilizá-las.

A tecnologia funciona por meio de um driver Linux e de um conjunto de modelos de inteligência artificial executados em segundo plano. Segundo a AMD, o **sistema consegue treinar seus modelos em menos de um segundo**, utilizando apenas um núcleo de processamento EPYC, sem precisar de uma GPU dedicada.

## AMD consegue manter 99% do desempenho usando metade da RAM

Nos testes apresentados pela AMD, a MEXT foi avaliada em diferentes cenários, incluindo aplicações de IA agêntica, bancos de dados, análise de informações e ferramentas utilizadas no desenvolvimento de semicondutores.

Em um teste com centenas de agentes de inteligência artificial, distribuídos entre diferentes cargas de trabalho, **a redução de 50% na quantidade de DRAM provocou uma perda de apenas 1% no desempenho médio**. Ao utilizar somente o agente que mais exigia memória, o desempenho ficou em 90% do original.

A AMD também apresentou resultados com a ferramenta Synopsys PrimeTime, utilizada no desenvolvimento de chips, na qual a redução pela metade da memória DRAM manteve 95% do desempenho.

Já em uma aplicação de análise de dados com Apache Spark, executada na nuvem Microsoft Azure, a fabricante novamente conseguiu preservar 99% do desempenho utilizando metade da DRAM convencional.

Os números são resultados de testes apresentados pela própria AMD e não significam que qualquer servidor poderá reduzir sua memória pela metade sem perdas relevantes de desempenho.

## Tecnologia pode ajudar a aliviar crise de memória RAM?

Além de diminuir o custo individual dos servidores, a MEXT também pode ter consequências para o mercado global de memória.

Isso porque os data centers utilizados por empresas de inteligência artificial são os responsáveis pela crise atual. Se uma parcela significativa dessas instalações conseguir reduzir a quantidade de memória convencional necessária, a tecnologia poderá diminuir a pressão sobre a demanda mundial pelo componente.

O problema é especialmente importante porque **a crise atual não afeta somente os preços da memória RAM, mas também a disponibilidade e os custos de outros componentes eletrônicos**.

Conforme o Canaltech explicou em uma reportagem sobre [por que até os processadores estão ficando mais caros em 2026](https://canaltech.com.br/hardware/por-que-processadores-estao-mais-caros-2026/), o crescimento da demanda por memória de alta largura de banda (HBM), utilizada em aceleradores de IA, tem levado fabricantes a priorizar componentes mais lucrativos destinados aos servidores.

Empresas como Samsung, SK hynix e Micron estão direcionando grande parte de sua capacidade produtiva para esse mercado, limitando a oferta de memórias convencionais destinadas a computadores e smartphones.

A situação é tão crítica que, segundo uma reportagem publicada pelo Canaltech em agosto, [as maiores fabricantes de memória já haviam comprometido sua capacidade de produção de DRAM e HBM para 2027](https://canaltech.com.br/hardware/memoria-ram-2027-capacidade-esgotada/), por meio de contratos antecipados com grandes clientes.

Essa disputa pelos componentes tem consequências diretas para os consumidores. Em dezembro de 2025, a Counterpoint Research projetava um aumento médio de **6,9% no preço global dos smartphones em 2026**. Na mesma época, a IDC trabalhava com cenários de alta de até 8% para celulares e computadores, enquanto a Gartner posteriormente estimou aumentos de 13% nos smartphones e 17% nos PCs.

Com o agravamento da crise, as projeções foram revisadas. Em setembro de 2026, a IDC passou a estimar uma elevação de **27,6% no preço médio global dos smartphones durante o ano**, refletindo não apenas o encarecimento dos componentes, mas também mudanças no perfil dos aparelhos comercializados.

A alta dos custos também pode prejudicar as especificações dos novos dispositivos. Para manter preços competitivos, fabricantes podem optar por oferecer menos RAM física, armazenamento mais limitado ou outras configurações inferiores às encontradas em gerações anteriores.

Em vez de aumentar a memória física, algumas marcas já passaram a destacar recursos de expansão virtual, como o RAM Boost, para compensar a redução de capacidade em determinados modelos.

O cenário tem efeitos diferentes ao longo da indústria. Enquanto fabricantes de dispositivos enfrentam dificuldades para absorver os novos custos, empresas fornecedoras de memória também podem registrar resultados financeiros expressivos.

Em julho, por exemplo, o Canaltech mostrou como [a crise da RAM ajudou a Samsung a registrar um lucro operacional recorde, superando marcas históricas de Apple e NVIDIA](https://canaltech.com.br/produtos/crise-da-ram-faz-samsung-bater-recorde-de-lucro-e-deixa-apple-e-nvidia-para-tras/).

**Em um cenário de adoção em larga escala, a MEXT poderia contribuir para aliviar a escassez de memória e, indiretamente, favorecer os preços de notebooks, celulares e outros eletrônicos.** Entretanto, esse efeito dependeria de fatores como capacidade de produção, comportamento dos fabricantes e crescimento da demanda por IA.

Também é importante considerar que a MEXT utiliza armazenamento flash, cuja oferta enfrenta pressões semelhantes às da DRAM. Assim, uma eventual migração de parte da demanda dos servidores de um componente para outro não garantiria, por si só, a normalização dos preços.

## MEXT já está em uso

A AMD já começou a colocar a proposta em prática dentro da própria empresa. Segundo Smerdon, uma implantação inicial em 145 servidores permitiu estimar uma economia próxima de US$ 5 milhões em compras de DRAM que deixaram de ser necessárias.

O executivo também afirmou que a economia de custos com memória chegou a 83% nessa implantação, demonstrando que a solução pode trazer vantagens financeiras expressivas para instalações que dependem de grandes quantidades de RAM.

A MEXT foi apresentada em conjunto com a sexta geração dos processadores AMD EPYC, conhecida pelo codinome Venice, mas também poderá ser utilizada em servidores EPYC de gerações anteriores e em ambientes de computação em nuvem compatíveis.

A empresa trabalha com parceiros para disponibilizar servidores preparados para receber a tecnologia e, posteriormente, sistemas comercializados com licenças MEXT e ferramentas de monitoramento pré-instaladas. Uma data definitiva para a disponibilidade comercial ampla ainda não foi detalhada.

_* O Canaltech viajou à Las Vegas, EUA, para cobrir o AMD in Depth à convite da AMD_
