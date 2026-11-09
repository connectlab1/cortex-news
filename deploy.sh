#!/bin/bash

# Interrompe o script imediatamente se ocorrer qualquer erro não tratado
set -e

# Cores ANSI para destaque no terminal (Arch Linux / Linux CLI)
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
BLUE="\033[94m"
CYAN="\033[96m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${BLUE}${BOLD}==> Garantindo a URL remota correta do repositório (SSH)...${RESET}"
git remote set-url origin git@github.com:connectlab1/cortex-news.git

echo -e "${BLUE}${BOLD}==> Sincronizando com o repositório remoto primeiro (git pull com rebase)...${RESET}"
# Salva temporariamente qualquer alteração pendente em stash para evitar conflitos
STASH_CREATED=false
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    git stash push -m "auto-stash-before-pull" >/dev/null 2>&1
    STASH_CREATED=true
fi

# Executa o pull com rebase de forma segura antes de commitar localmente
if ! git pull origin main --rebase; then
    echo -e "${RED}==> Aviso: Falha no rebase remoto. Abortando com segurança...${RESET}"
    git rebase --abort 2>/dev/null || true
    if [ "$STASH_CREATED" = true ]; then
        git stash pop >/dev/null 2>&1 || true
    fi
    exit 1
fi

# Restaura o stash das alterações locais, se houver
if [ "$STASH_CREATED" = true ]; then
    git stash pop >/dev/null 2>&1 || true
fi

echo -e "${BLUE}${BOLD}==> Adicionando alterações, scripts e posts ao controle de versão...${RESET}"
# Adiciona posts, dados, includes, layouts e toda a estrutura essencial do projeto
git add _posts/ data/ src/ assets/ _layouts/ _includes/ _config.yml index.html *.html README.md *.sh *.py requirements.txt 2>/dev/null || git add .

# Verifica se há qualquer alteração pendente para commitar
if [ -n "$(git status --porcelain)" ]; then
    MSG="${1:-feat: atualização automática do blog, posts e estrutura}"
    echo -e "${YELLOW}==> Criando commit: \"${MSG}\"${RESET}"
    git commit -m "$MSG"
else
    echo -e "${YELLOW}==> Nenhuma alteração pendente detectada para commit.${RESET}"
fi

echo -e "${BLUE}${BOLD}==> Enviando alterações para o GitHub (git push)...${RESET}"
git push origin main

echo -e "${GREEN}${BOLD}==> ✅ Deploy enviado com sucesso para git@github.com:connectlab1/cortex-news.git!${RESET}"
