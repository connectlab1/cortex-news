---
layout: post
title: "Driver da AMD pode desgastar SSD gravando 400 GB de lixo por dia"
date: 2026-11-09 12:35:02 +0000
categories: [Canaltech]
link: "https://canaltech.com.br/hardware/driver-da-amd-pode-desgastar-ssd-gravando-400-gb-de-lixo-por-dia/"
---

Donos de [placas de vídeo Radeon](https://canaltech.com.br/hardware/entenda-a-nomenclatura-das-placas-de-video-amd-radeon/): seu PC pode estar sofrendo de um problema silencioso fruto de um bug do driver de vídeo da AMD. O Time Vermelho confirmou o problema em suas versões recentes do driver Radeon Adrenalin, que faz com que **um processo do sistema grave dados continuamente no SSD do usuário, mesmo quando a máquina está completamente ociosa**. A correção oficial já foi confirmada e chega até o fim de novembro.

O problema foi apontado por diversos usuários nas redes sociais, que notaram uma **atividade anormal nos discos do sistema**. O vilão da história é o processo **atieclxx.exe** (vinculado ao AMD External Events Utility), serviço responsável por gerenciar atalhos do aplicativo e detecção de monitores. Em sistemas afetados, esse processo mantém uma **taxa constante de escrita que varia entre 0,3 MB/s e 1,5 MB/s,** com casos mais graves atingindo **até 5 MB/s sustentados**.

## O risco à vida útil e como contornar o problema

Embora valores na casa dos megabytes por segundo pareçam pequenos à primeira vista, o acúmulo em segundo plano é agressivo. Em um cenário extremo com gravação contínua a 5 MB/s, **o bug pode gerar cerca de 432 GB de dados gravados por dia, ultrapassando os 12 TB por mês apenas com lixo gerado pelo driver**. Embora nem todas as operações reflitam diretamente em gravações físicas no SSD, a atividade contínua consome ciclos desnecessários do drive e reduz a [sua vida útil (TBW)](https://canaltech.com.br/hardware/ssd-tem-prazo-de-validade-o-que-o-tbw-realmente-diz-sobre-isso/).

De acordo com representantes da AMD, em respostas aos usuários nas redes sociais, a falha parece acontecer por uma incompatibilidade entre o utilitário de eventos da placa e o driver de filtro PCIe da própria Microsoft. Enquanto o driver 26.11.1 não chega, os usuários podem checar se estão sendo afetados abrindo o Monitor de Recursos do Windows e conferindo a guia "Disco".

Caso o processo atieclxx.exe esteja gravando dados sem parar, a solução temporária mais recomendada é **desativar o serviço AMD External Events Utility nas Ferramentas Administrativas do Windows (services.msc)**. Vale notar que essa medida pode desativar temporariamente os atalhos de teclado do software Radeon, mas interrompe o desgaste desnecessário do armazenamento até a chegada do patch definitivo.

E falando em GPUs da AMD, a movimentação mais recente que temos acerca do assunto é um rumor apontando para o [atraso no lançamento da arquitetura RDNA 5+ para notebooks](https://canaltech.com.br/hardware/amd-deve-atrasar-nova-arquitetura-rdna-5-para-notebooks-veja-nova-previsao/), algo que ainda nem ao menos foi revelado oficialmente.
