---
layout: post
title: "AMD revela pistas dos novos Ryzen: 24 núcleos e desempenho muito maior?"
date: 2026-11-10 17:00:08 +0000
categories: [Canaltech]
link: "https://canaltech.com.br/hardware/amd-revela-pistas-dos-novos-ryzen-24-nucleos-e-desempenho-muito-maior/"
---

A AMD acabou de revelar todas as novidades dos seus gigantescos processadores EPYC Venice, com até 256 núcleos para servidores. Mas, se você não é dono de um data center, o que realmente importa são as **pistas que a fabricante deixou sobre a arquitetura Zen 6**, que também servirá de base para os próximos **chips Ryzen destinados aos computadores pessoais.**

Durante o AMD In Depth 2026, evento realizado em Las Vegas, nos Estados Unidos, o Canaltech acompanhou uma apresentação técnica de **Mike Clark, principal arquiteto da família Zen**, que detalhou mudanças importantes na organização dos núcleos, no sistema de cache e no processamento de instruções.

**As novidades indicam que os futuros Ryzen poderão chegar com até 24 núcleos, mais memória cache e ganhos expressivos de desempenho**, embora a AMD ainda não tenha confirmado as especificações dos modelos domésticos.

A seguir, reunimos cinco avanços da arquitetura que ajudam a entender o que esperar da próxima geração de processadores da marca.

## 1\. Próximos Ryzen podem chegar a 24 núcleos

Uma das novidades mais interessantes está na quantidade de núcleos que a AMD conseguiu colocar em cada complexo de processamento.

Na arquitetura Zen 5, utilizada pelos atuais Ryzen 9000, os complexos de núcleos (CCX) reúnem até oito núcleos. Com a Zen 6 convencional, esse número sobe para 12, um aumento de 50%.

Isso significa que, se a AMD mantiver a estratégia de utilizar dois _chiplets_ de processamento em seus Ryzen mais poderosos, **os futuros modelos poderão oferecer até 24 núcleos e 48 threads**, contra os atuais 16 núcleos e 32 threads.

A mudança poderá beneficiar especialmente aplicações profissionais que utilizam processamento paralelo, como **renderização 3D, compilação de programas, edição de vídeo e outras tarefas pesadas.**

Durante a apresentação, Clark explicou que a ampliação dos complexos foi pensada para permitir que mais tarefas compartilhem recursos internos do processador.

> "Aumentamos o número de núcleos no CCX para 12, permitindo que mais núcleos estejam disponíveis para as cargas de trabalho dentro do mesmo complexo", explicou o arquiteto.

Vale lembrar que a fabricante ainda não confirmou um Ryzen com 24 núcleos. O número é uma projeção baseada na nova organização dos chiplets, também mencionada em vazamentos anteriores.

## 2\. Mais memória cache pode melhorar o desempenho em jogos

Outra mudança significativa da Zen 6 está na quantidade de memória cache L3 disponível para os núcleos. Nos [novos EPYC Venice](https://canaltech.com.br/hardware/amd-lanca-cpu-gigante-de-256-nucleos-para-deixar-nvidia-e-intel-preocupadas/), a versão convencional da arquitetura passa a reunir **48 MB de cache L3 por complexo de 12 núcleos**, contra 32 MB por complexo de oito núcleos na Zen 5.

Se essa configuração for mantida nos Ryzen da nova geração, um processador equipado com dois chiplets poderá chegar a 96 MB de cache L3, antes mesmo de considerar uma eventual implementação da tecnologia 3D V-Cache.

Essa memória é utilizada para armazenar informações frequentemente acessadas pelo processador, reduzindo a necessidade de buscar dados na RAM, que é mais lenta.

Em jogos, esse recurso pode ser especialmente importante porque ajuda a reduzir atrasos no processamento de informações, embora o ganho real dependa das características de cada título.

A AMD também mostrou mudanças na Zen 6c, versão otimizada para maior densidade de processamento. Nela, cada complexo passou de 16 para 32 núcleos, enquanto o cache L3 quadruplicou, saltando de 32 MB para 128 MB.

O avanço demonstra a capacidade da fabricante de ampliar a quantidade de cache compartilhado, mas não significa que os próximos Ryzen X3D necessariamente terão quatro vezes mais memória cache.

## 3\. Nova arquitetura entrega ganhos de até 31% em testes da AMD

Além de colocar mais núcleos nos processadores, a AMD trabalhou para aumentar a quantidade de instruções que cada núcleo consegue executar por ciclo de clock, métrica conhecida como IPC.

Nos benchmarks divulgados durante o evento, a Zen 6c apresentou um ganho médio de aproximadamente **20% em cargas corporativas e de servidores em nuvem**, chegando a 31% em aplicações relacionadas à inteligência artificial.

A AMD resume esses resultados como uma evolução média de aproximadamente 27% em IPC no conjunto de testes apresentado.

> "Há muitas cargas de trabalho diferentes. Algumas ficam abaixo de 20%, outras acima. Nenhum número sozinho consegue representar todas elas", explicou Clark ao comentar os resultados.

Os números são particularmente interessantes porque os testes foram realizados em frequências fixas, procurando demonstrar os avanços arquiteturais sem depender simplesmente de clocks mais elevados.

Entretanto, os benchmarks foram realizados com núcleos Zen 6c em aplicações de servidores e IA. Portanto, não é possível afirmar que os próximos Ryzen serão 27% ou 31% mais rápidos em jogos e programas domésticos.

O desempenho desses processadores dependerá das frequências, da quantidade de núcleos, dos limites de energia e da configuração final de cada modelo.

## 4\. Chips de 2 nm e melhorias de eficiência energética

Os novos EPYC Venice utilizam chiplets de processamento produzidos com o processo de fabricação N2, de 2 nanômetros, da TSMC.

Essa tecnologia permite à AMD trabalhar com uma quantidade maior de transistores e buscar melhorias na relação entre desempenho e consumo energético.

Além da evolução no processo de fabricação, a Zen 6 traz mudanças na previsão de desvios, no agendamento de instruções e na movimentação de dados entre os diferentes níveis de cache.

A arquitetura também incorpora uma janela de execução maior, com um buffer de reordenação de até 640 entradas, contra 448 na Zen 5c.

Essas alterações permitem que o processador mantenha mais operações em andamento, aproveitando melhor seus recursos internos e reduzindo determinados gargalos.

Outra novidade está nas instruções voltadas ao processamento matemático e à inteligência artificial. A Zen 6 oferece suporte completo a operações AVX-512 FP16, novas instruções para multiplicação de matrizes de bits e quatro pipelines VNNI INT8, o dobro da geração anterior.

Essas capacidades podem beneficiar programas de criação de conteúdo, aplicações científicas e determinadas tarefas de IA executadas diretamente na CPU.

Nos notebooks, os avanços arquiteturais também poderão contribuir para melhorar a autonomia, desde que acompanhados de um gerenciamento adequado de energia.

A AMD, entretanto, ainda não apresentou testes de consumo ou duração de bateria dos futuros Ryzen baseados na Zen 6.

## 5\. Quando os novos Ryzen Zen 6 chegam ao mercado?

Embora a arquitetura tenha estreado nos servidores, a AMD já deixou pistas sobre sua chegada aos computadores domésticos.

Como o Canaltech havia explicado anteriormente, [**a estreia da arquitetura Zen 6 aconteceu primeiro nos processadores EPYC, e não nos Ryzen**](https://canaltech.com.br/hardware/cpus-amd-zen-6-chegam-nos-proximos-dias-mas-nao-do-jeito-que-pensa/), invertendo a expectativa de quem acompanhava os lançamentos anteriores da empresa.

Em agosto, documentos técnicos da própria AMD também revelaram a existência das famílias Olympic Ridge e Medusa, relacionadas à próxima geração de processadores para PCs e notebooks.

Os registros indicam que a plataforma AM5 continuará fazendo parte dos planos da fabricante, embora a compatibilidade com placas-mãe específicas ainda dependa de atualizações e suporte dos fabricantes.

[**A AMD já identificou as famílias Olympic Ridge e Medusa como parte dos planos para os próximos Ryzen**](https://canaltech.com.br/hardware/amd-confirma-cpus-ryzen-olympic-ridge-e-medusa-zen-6-para-pcs-e-notebooks/), mas ainda não divulgou a configuração final, os preços ou a data exata de lançamento dos novos modelos.

A expectativa do mercado é de que os primeiros Ryzen Zen 6 domésticos apareçam em 2027.

Enquanto isso, a empresa continua ampliando a utilização da arquitetura em servidores. Um exemplo são [**os processadores EPYC Verano, que combinam até 192 núcleos com memória LPDDR5X**](https://canaltech.com.br/hardware/novas-cpus-amd-epyc-verano-apostam-em-lpddr5x-e-ate-192-nucleos/) para melhorar a eficiência energética dos data centers.

É importante observar que características específicas dos servidores, como os 16 canais de memória DDR5 e a enorme quantidade de núcleos da versão Zen 6c, não serão necessariamente reproduzidas nos processadores domésticos.

Ainda assim, os detalhes apresentados durante o AMD In Depth 2026 mostram que a próxima geração Ryzen poderá trazer uma das mudanças mais significativas na organização dos núcleos da AMD nos últimos anos.

Para os consumidores, a combinação de mais núcleos, cache ampliado, melhor desempenho por ciclo e fabricação mais avançada promete tornar a chegada da Zen 6 especialmente interessante.

_* O Canaltech viajou à Las Vegas a convite da AMD._
