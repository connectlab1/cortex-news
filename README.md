# 🚀 Cortex News ETL Pipeline & Blog Jekyll

Um pipeline ETL (Extract, Transform, Load) automatizado em Python e Shell Script para Arch Linux, integrado a um site estático baseado em **Jekyll**. O sistema rastreia feeds RSS de portais de tecnologia, trata o conteúdo, converte para Markdown e publica automaticamente no repositório.

## 📌 Arquitetura e Fluxos de Trabalho

O projeto é dividido em dois ambientes estritamente independentes para garantir a segurança e a integridade entre operações manuais e execuções automatizadas em segundo plano:

### 🛠️ Ambiente Manual (`main.py` + `deploy.sh`)
* Executado sob demanda.
* Permite controle total do fluxo de extração e disparo manual do deploy.

### 🤖 Ambiente Automatizado (`main1.py` + `deploy1.sh`)
* Sistema totalmente automatizado operando em loop contínuo no terminal.
* Processa novos itens periodicamente, aplica intervalo de segurança (3s), emite alertas sonoros (`\a`) e visuais via ANSI no terminal, e dispara o `deploy1.sh` automaticamente.

## 📂 Estrutura do Projeto

```
.
├── assets/                 # Recursos estáticos do front-end
│   ├── css/
│   │   └── style.scss      # Estilos customizados (Sass)
│   └── js/
│       └── main.js         # Scripts JavaScript do site
├── data/
│   └── historico.json      # Registro persistente de links já processados (evita duplicatas)
├── _layouts/               # Templates HTML do Jekyll
│   ├── default.html        # Layout base da aplicação
│   └── post.html           # Template dos artigos de notícias
├── _posts/                 # Diretório de destino dos arquivos Markdown gerados
├── src/                    # Módulos Python da engine ETL
│   ├── cleaner.py          # Limpeza de HTML, conversão para MD e correções tipográficas
│   ├── config.py           # Configurações globais, URLs de RSS e parâmetros
│   ├── filters.py          # Filtros de regex e frases bloqueadas (blacklist)
│   ├── generator.py        # Geração dos arquivos .md com Front Matter do Jekyll
│   ├── history.py          # Leitura e escrita do histórico JSON
│   ├── processor.py        # Validação de qualidade, filtro por tamanho e ordenação
│   └── scraper.py          # Requisição HTTP e parser dos feeds RSS
├── _config.yml             # Configurações globais do Jekyll
├── index.html              # Página inicial do blog
├── deploy.sh               # Script de deploy Git manual
├── deploy1.sh              # Script de deploy Git automatizado (força remote SSH)
├── main.py                 # Ponto de entrada manual
├── main1.py                # Ponto de entrada automatizado (Loop + Deploy)
└── requirements.txt        # Dependências Python do projeto
```

## 🔒 Segurança e Autenticação

* **SSH Nativo:** O deploy utiliza a URL remota SSH (`git@github.com:connectlab1/cortex-news.git`).
* **Sem Exposição de Credenciais:** Nenhuma senha ou Personal Access Token (PAT) é mantido nos scripts ou enviada ao repositório.

## 🛠️ Como Executar

### 1. Instalação das Dependências

Instale os pacotes necessários listados em `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Execução Automatizada (Main Engine)

Para iniciar o robô contínuo com deploy automático:

```bash
python3 main1.py
```

### 3. Execução Manual

Para processar novas matérias pontualmente e decidir quando publicar:

```bash
python3 main.py
./deploy.sh
```

## 📝 Regras de Qualidade e Filtros

* **Filtro de Tamanho:** Artigos com menos de 40 palavras são descarta dos automaticamente.
* **Slugs Únicos:** Nomes de arquivos combinam título sanitizado (máx. 40 caracteres) e hash MD5 curto do link original para evitar colisões.
* **Limpeza Tipográfica:** Tratamento automático de pontuações, aspas e remoção de avisos de syndication.