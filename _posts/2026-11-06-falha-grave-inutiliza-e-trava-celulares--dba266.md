---
layout: post
title: "Falha grave inutiliza e trava celulares Android em loop infinito"
date: 2026-11-06 16:05:00 +0000
categories: [Canaltech]
---

Os pesquisadores da Bitdefender descobriram uma vulnerabilidade no Android chamada GhostMap, que consegue**travar os celulares em um ciclo infinito de reinicializações**, conhecido como bootloop. O problema pode inutilizar o aparelho em poucos segundos, mesmo que o usuário não abra o aplicativo malicioso responsável pelo ataque.

Segundo o especialista Alecsandru Cătălin DAJ, da Bitdefender, a falha está no **processo de verificação dos aplicativos instalados**, realizado por um serviço do Android chamado system_server. Durante essa análise, o sistema tenta ler informações sobre a compressão dos arquivos ZIP que compõem os aplicativos. No entanto, determinados dados de compressão fazem o serviço parar de funcionar.

Quando isso acontece, o Android reinicia o system_server e tenta verificar os aplicativos novamente. Como encontra o mesmo arquivo problemático, o serviço trava outra vez e**dá início a um ciclo que impede o celular de concluir a inicialização**. Por isso, a instalação de um app malicioso já é suficiente para provocar o ataque, mesmo que ele nunca seja aberto. Durante o processo, o usuário não recebe nenhuma mensagem de erro ou aviso na tela que indique qual aplicativo causou o problema.

## Google ainda não corrigiu a falha GhostMap

A Bitdefender já comunicou a vulnerabilidade ao Google, mas a empresa inicialmente encerrou o chamado com o status “Won’t Fix (Not Reproducible)”. A justificativa foi que a equipe de segurança **não conseguiu reproduzir o erro**.

A empresa de segurança enviou um segundo relatório, dessa vez com um aplicativo de prova de conceito capaz de demonstrar o problema. Mesmo assim, o Google **recusou a solicitação novamente**, sob a justificativa de que a vulnerabilidade estava “fora do escopo de uma correção de atualização de segurança”.

Com essa classificação, a falha foi encaminhada para outra equipe do Google, responsável por analisar o caso e avaliar uma possível correção no sistema. Até o momento, porém, **não há confirmação de uma atualização** para resolver o problema.

Diante da falta de uma solução, a Bitdefender **decidiu divulgar a vulnerabilidade publicamente**. Com o alerta, porém, os criminosos podem tentar criar aplicativos maliciosos com aparência legítima e até enviá-los à Play Store para alcançar mais vítimas. No entanto, isso também poderá pressionar o Google por uma solução.

Até que a Google disponibilize uma correção, a recomendação é evitar a instalação de aplicativos de fontes desconhecidas ou suspeitas. Como a falha não depende de permissões especiais ou da abertura do app, o cuidado precisa começar no momento do download e da instalação.

Se você gostou do conteúdo, talvez também se interesse por conferir “_Como deixar o Android mais seguro | 9 dicas_”.

---

> **Gostou do assunto?** Para conferir todos os detalhes, imagens originais e a discussão completa, acesse a matéria original.
>
> 👉 **[Ler artigo completo no Canaltech](https://canaltech.com.br/apps/falha-grave-inutiliza-e-trava-celulares-android-em-loop-infinito/)**
