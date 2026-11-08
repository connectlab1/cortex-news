#!/bin/bash

# Interrompe o script imediatamente se ocorrer qualquer erro
set -e

# Cores ANSI para destaque no terminal (Arch Linux / Bash)
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
BLUE="\033[94m"
CYAN="\033[96m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${BLUE}${BOLD}==> Garantindo a URL remota correta do repositório (SSH)...${RESET}"
git remote set-url origin git@github.com:connectlab1/cortex-news.git

echo -e "${BLUE}${BOLD}==> Adicionando alterações ao controle de versão...${RESET}"
git add .

# Verifica se há arquivos modificados ou novos posts para commitar
if [ -n "$(git status --porcelain)" ]; then
    MSG="${1:-feat: atualização automática de posts e layouts}"
    echo -e "${YELLOW}==> Criando commit: \"${MSG}\"${RESET}"
    git commit -m "$MSG"
else
    echo -e "${YELLOW}==> Nenhuma alteração nova detectada para commit.${RESET}"
fi

echo -e "${BLUE}${BOLD}==> Sincronizando com o repositório remoto (git pull)...${RESET}"
git pull origin main --no-rebase

echo -e "${BLUE}${BOLD}==> Enviando alterações para o GitHub (git push)...${RESET}"
git push origin main

echo -e "${GREEN}${BOLD}==> ✅ Deploy enviado com sucesso para git@github.com:connectlab1/cortex-news.git!${RESET}"
