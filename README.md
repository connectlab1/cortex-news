# 🚀 Cortex News ETL Pipeline & Blog Jekyll

Um pipeline ETL (Extract, Transform, Load) automatizado, modular, blindado e resiliente em Python e Shell Script para Arch Linux / Linux CLI, totalmente integrado a um site estático baseado em **Jekyll**. O sistema rastreia feeds RSS de portais de tecnologia brasileiros, aplica limpeza rigorosa de HTML e regras de syndication/blacklist, remove duplicatas persistentes via histórico atômico, converte para Markdown formatado com Front Matter e executa o deploy automatizado para o GitHub.

## 📌 Arquitetura e Pipeline ETL

O pipeline foi projetado seguindo o princípio de **Separação de Responsabilidades (SoC)**, onde cada módulo do diretório `src/` desempenha um papel estrito e isolado no ciclo de processamento.

```
+------------------+     +-----------------+     +-------------------+
|  src/scraper.py  | --> |  src/cleaner.py | --> | src/processor.py  |
| (Coleta RSS/UTC) |     |  (HTML2Text/MD) |     | (Qualidade/Duplic)|
+------------------+     +-----------------+     +-------------------+
                                                          |
                                                          v
+------------------+     +-----------------+     +-------------------+
|    deploy.sh     | <-- | src/history.py  | <-- | src/generator.py  |
|  (Git/Rebase)    |     | (Escrita Atômica|     | (Markdown Jekyll) |
+------------------+     +-----------------+     +-------------------+
```

### 🔄 Etapas Detalhadas do Pipeline

1. **Extração (`src/scraper.py`):**
   - Varre as fontes RSS brasileiras configuradas em `src/config.py`.
   - Utiliza bytes crus (`response.content`) com o `feedparser` para autodetectar a codificação de caracteres (evitando problemas de acentuação/`mojibake`).
   - Garante a extração de URLs absolutas (`http://` / `https://`) e padroniza datas em objetos `datetime` conscientes de timezone (UTC).

2. **Limpeza e Sanitização (`src/cleaner.py` + `src/filters.py`):**
   - Converte HTML bruto em Markdown legível via `html2text`.
   - Delegates rigorosamente todas as remoções de frases promocionais, avisos de syndication, placeholders e expressões regulares para o módulo dedicado **`src/filters.py`**.
   - Executa correções tipográficas (espaçamentos de aspas, pontuações e quebras de linha duplicadas).

3. **Processamento e Qualidade (`src/processor.py`):**
   - Importa o histórico persistido de links processados.
   - Remove duplicatas existentes no banco histórico e itens repetidos no próprio lote atual.
   - Aplica a regra de qualidade filtrando notícias com contagem real de palavras inferior ao parâmetro `MIN_PALAVRAS` (definido em `src/config.py`).
   - Atualiza a descrição limpa no dicionário e ordena cronologicamente do post mais antigo para o mais recente.

4. **Persistência Atômica (`src/history.py`):**
   - Evita corrupções de arquivo em caso de desligamento ou interrupções utilizando escrita atômica (`.tmp` + `os.replace`).
   - Deduplica, sanitiza e ordena alfabeticamente os links gravados em `data/historico.json`.

5. **Geração de Conteúdo (`src/generator.py`):**
   - Cria postagens em formato Markdown no diretório `_posts/`.
   - Adiciona o cabeçalho Front Matter do Jekyll (título, portal de origem, data formatada em ISO, layout).
   - Sanitiza o nome do arquivo combinando slug do título (máx. 40 chars) e hash MD5 curto da URL para evitar conflitos de sobreescrita.

6. **Orquestração e Deploy (`main.py` + `deploy.sh`):**
   - O `main.py` roda como um daemon persistente (loop de 1 hora) no terminal do Arch Linux com banners coloridos ANSI e alertas sonoros (``).
   - Valida a existência e aplica permissões de execução (`chmod +x`) em `deploy.sh`.
   - O `deploy.sh` versiona estritamente as pastas `_posts/` e `data/`, executa `git pull --rebase` (evitando telas interativas de merge em caso de concorrência remota) e envia os commits via SSH.

---

## 📂 Estrutura Completa do Projeto

```
.
├── assets/                 # Recursos estáticos do front-end
│   ├── css/
│   │   └── style.scss      # Estilos customizados (Sass)
│   └── js/
│       └── main.js         # Scripts JavaScript do site
├── data/
│   └── historico.json      # Registro persistente atômico de links já processados
├── _layouts/               # Templates HTML do Jekyll
│   ├── default.html        # Layout base da aplicação
│   └── post.html           # Template dos artigos de notícias
├── _posts/                 # Diretório de destino dos arquivos Markdown gerados
├── src/                    # Módulos Python da engine ETL
│   ├── cleaner.py          # Conversão HTML para Markdown e formatação tipográfica
│   ├── config.py           # Configurações globais, feeds RSS e parâmetros (timeouts, MIN_PALAVRAS)
│   ├── filters.py          # Centralizador de blacklists, regexes de syndication e frases proibidas
│   ├── generator.py        # Geração dos arquivos .md com Front Matter do Jekyll
│   ├── history.py          # Leitura e escrita atômica do histórico JSON (os.replace)
│   ├── processor.py        # Filtro de qualidade, contagem real de palavras e ordenação cronológica
│   └── scraper.py          # Requisição HTTP por bytes crus, validação de URLs e parser RSS
├── _config.yml             # Configurações globais do Jekyll
├── deploy.sh               # Script oficial de deploy Git automatizado (pull --rebase + push SSH)
├── index.html              # Página inicial do blog
├── main.py                 # Orquestrador contínuo do pipeline ETL (Loop 1h + Alertas ANSI)
├── README.md               # Documentação técnica do projeto
└── requirements.txt        # Dependências Python do projeto
```

---

## 🔒 Segurança, Resiliência e Integridade

* **Escrita Atômica em Disco:** Nenhuma alteração direta no `historico.json` sem antes validar o buffer em arquivo `.tmp`, garantindo 0% de risco de arquivo corrompido ou zerado.
* **Autenticação SSH:** Deploy para o GitHub utilizando autenticação por chave SSH (`git@github.com:connectlab1/cortex-news.git`).
* **Deploy sem Bloqueio de Terminal:** O script `deploy.sh` utiliza `git pull --rebase` e abortagem automática em caso de divergência grave (`git rebase --abort`), impedindo que o daemon trave aguardando input do usuário.
* **Sanitização de UTF-8:** Tratamento de feeds com encodings variados direto em nível de bytes.

---

## 🛠️ Como Instalar e Executar

### 1. Pré-requisitos e Dependências

Certifique-se de ter o Python 3.x instalado e instale os pacotes listados no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Executar o Robô de Produção (`main.py`)

Para iniciar o daemon ETL contínuo (executa imediatamente e depois aguarda em intervalos de 1 hora):

```bash
python3 main.py
```

### 3. Disparo Manual do Deploy (`deploy.sh`)

Se desejar versionar e enviar alterações pendentes manualmente para o GitHub:

```bash
./deploy.sh
```

---

## 📝 Regras de Qualidade e Boas Práticas

* **Isolamento do `filters.py`:** Toda e qualquer regra de filtragem textual (expressões regulares de syndication, frases institucionais, placeholders) é mantida exclusivamente no arquivo `src/filters.py`.
* **Slugificação MD5:** Todo post gerado possui slug sanitizado + hash da URL original, garantindo que matérias com títulos parecidos não sobrescrevam o mesmo arquivo `.md`.
* **Formatação Jekyll Front Matter:** Todo arquivo Markdown gerado é compatível com geradores de sites estáticos.
