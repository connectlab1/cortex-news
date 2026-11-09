---
layout: post
title: "Alerta para devs: Claude Code vaza senhas e chaves de API em massa no GitHub"
date: 2026-11-09 21:03:00 +0000
categories: [Canaltech]
link: "https://canaltech.com.br/seguranca/alerta-para-devs-claude-code-vaza-senhas-e-chaves-de-api-em-massa-no-github/"
---

Uma falha no Claude Code, ferramenta de inteligência artificial da Anthropic para auxiliar no desenvolvimento de software, **expôs milhares de senhas, tokens de API e credenciais** de servidores no GitHub. O problema está relacionado ao armazenamento de comandos autorizados pelos desenvolvedores em arquivos de configuração locais, que podem acabar enviados para repositórios públicos.

A descoberta foi feita por pesquisadores de segurança da empresa Apiiro, que identificaram **2.539 credenciais reais em 1.994 repositórios públicos**, com impacto sobre 63 organizações. Em 539 repositórios, os pesquisadores ainda identificaram commits coautorados pelo próprio Claude Code que incluíam arquivos com dados confidenciais. O levantamento abrange projetos acadêmicos, startups, agências de software e fornecedores de tecnologia.

A exposição ocorre por causa do **sistema de permissões do Claude Code** para executar comandos de terminal. Durante tarefas, como migrações de bancos de dados e diagnósticos, o assistente pode sugerir instruções que incluem senhas e outras informações confidenciais. Quando o desenvolvedor seleciona a opção "Yes, and don't ask again" (Sim, e não pergunte novamente), a ferramenta salva o comando autorizado em texto puro no arquivo.claude/settings.local.json, dentro da pasta do projeto.

Embora o Claude Code tente impedir o envio desse arquivo ao GitHub ao adicioná-lo ao.gitignore global do desenvolvedor, a **proteção não é aplicada ao arquivo.gitignore** do próprio projeto. Com isso, o documento pode acabar incluído no repositório quando a pasta é compartilhada, clonada ou configurada manualmente para usar o Git. A Apiiro encontrou 104.185 cópias públicas do arquivo, das quais 1.122 continham credenciais reais, totalizando 1.379 segredos distintos.

Esse número faz parte de um levantamento mais amplo da Apiiro, que chegou a 2.539 credenciais expostas. Além do arquivo.claude/settings.local.json, os pesquisadores encontraram dados confidenciais no histórico do Git, em arquivos compartilhados settings.json e em transcrições de conversas de outros agentes de IA.

O comportamento já havia sido reportado por usuários em chamados de suporte e issues no repositório do Claude Code **desde agosto de 2025**. No entanto, os relatos foram fechados automaticamente após 60 dias de inatividade, sem que medidas fossem implementadas. Após a divulgação do levantamento, o chefe do Claude Code na Anthropic se manifestou no fórum Hacker News e afirmou que a equipe **estuda formas de evitar novos vazamentos**, como o aprimoramento no modo automático e a inclusão de um scanner básico de segredos na ferramenta.

Entre e-mail, banco, lojas e streaming, criar uma senha forte para cada conta dá um trabalhão, e reaproveitá-las é um risco. O NordPass, gerenciador de senhas da NordVPN, está em oferta: o plano individual tem 53% de desconto + 3 meses extras, a R$ 4,90/mês, e o anual sai a partir de R$ 6,90/mês, com 33% de desconto. [_Aproveite e assine_](https://canalte.ch/op2/68th)!
---

## Quais dados foram expostos?

O levantamento identificou diferentes tipos de credenciais nos arquivos de configuração:

* **Tokens de API de serviços** : 398 registros;

* **Senhas de bancos de dados** : 379;

* **Chaves de API de modelos de IA** : 149;

* **Chaves de função de serviço do Supabase** : 122;

* **Chaves de API do Google** : 110;

* **Tokens de contas do Supabase** : 103;

* **Logins de servidores SSH** : 43;

* **Tokens do GitHub, GitLab e npm** : 42;

* **Chaves de nuvem da AWS:** 23;

* **Senhas de aplicativos e contas** : 9;

* **Chaves privadas** : 6.

Um dos pontos mais preocupantes é que 501 credenciais davam **acesso a bancos de dados de produção**. Entre os segredos encontrados no levantamento estavam sistemas de prontuários médicos, bancos em nuvem de produção e plataformas de pagamento.

Se você gostou do conteúdo, talvez também se interesse por conferir “[ _ChatGPT Codex e Claude Code: o que muda entre as IAs para programação?_](https://canaltech.com.br/apps/chatgpt-codex-e-claude-code-o-que-muda-entre-as-ias-para-programacao/)”.
