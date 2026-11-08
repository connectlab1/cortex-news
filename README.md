# ⚡ Cortex News

> **Pipeline ETL de Notícias & Blog Automatizado em Jekyll**

O **Cortex News** é um laboratório automatizado de engenharia de dados que realiza a coleta, limpeza, filtragem e conversão de feeds RSS de tecnologia em postagens otimizadas para um blog estático gerado em Jekyll.

---

## 🚀 Destaques do Projeto

* 🔄 **Pipeline ETL Robusto:** Coleta automatizada com tratamento de encoding (bytes crus) e parsing de datas UTC.  
* 🧹 **Sanitização de Dados:** Conversão de HTML para Markdown com remoção rigorosa de conteúdos institucionais e propaganda via `src/filters.py`.  
* 🛡️ **Persistência Atômica:** Histórico persistido em JSON (`data/historico.json`) com substituição atômica (`os.replace`) contra corrupção de dados.  
* 💻 **Modo de Desenvolvimento Isolado:** Scripts dedicados (`main-manual.py` e `main-automatico.py`) para testes locais seguros sem disparo de deploy acidental.

---

## 🛠️ Stack Tecnológica

* **Linguagens:** Python 3 (ETL e automações) \| Ruby 3.4 (Jekyll / Bundler)  
* **Sistema de Destino:** CachyOS / Arch Linux CLI  
* **Publicação:** GitHub Pages (com suporte a deploy local automatizado)

---

## 📖 Documentação Completa (Wiki)

Para guias detalhados de instalação, estrutura de pastas e solução de erros, acesse a nossa **Wiki**:

* 📘 [Visão Geral e Arquitetura do Projeto](https://github.com/connectlab1/cortex-news/wiki/Vis%C3%A3o-Geral)  
* 🛠️ [Guia de Instalação e Configuração do Ambiente](https://github.com/connectlab1/cortex-news/wiki/Instala%C3%A7%C3%A3o)  
* 💻 [Modo de Uso Local e Scripts Python](https://github.com/connectlab1/cortex-news/wiki/Uso-Local)  
* 🔧 [Manual de Resolução de Problemas (Troubleshooting)](https://github.com/connectlab1/cortex-news/wiki/Troubleshooting)

---

### ⚡ Quick Start Local

```sh
# 1. Instalar dependências
pip install -r requirements.txt
bundle install

# 2. Executar o pipeline local
python main-manual.py

# 3. Subir o servidor de desenvolvimento
bundle exec jekyll serve --baseurl ""
```

