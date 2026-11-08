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

echo -e "${BLUE}${BOLD}==> Adicionando alterações, scripts e posts ao controle de versão...${RESET}"
# Adiciona posts, dados e toda a estrutura essencial do projeto (layouts, assets, scripts, configs e docs)
git add _posts/ data/ src/ assets/ _layouts/ _config.yml index.html README.md deploy.sh main.py requirements.txt 2>/dev/null || git add .

# Verifica se há qualquer alteração pendente (posts novos ou edições de código/estrutura)
if [ -n "$(git status --porcelain)" ]; then
    MSG="${1:-feat: atualização automática do blog, posts e estrutura}"
    echo -e "${YELLOW}==> Criando commit: \"${MSG}\"${RESET}"
    git commit -m "$MSG"
else
    echo -e "${YELLOW}==> Nenhuma alteração pendente detectada para commit.${RESET}"
    exit 0
fi

echo -e "${BLUE}${BOLD}==> Sincronizando com o repositório remoto (git pull com rebase)...${RESET}"
# Utiliza rebase para manter o histórico linear e evitar telas interativas de merge
git pull origin main --rebase || {
    echo -e "${RED}==> Aviso: Conflito detectado no pull. Abortando rebase com segurança...${RESET}"
    git rebase --abort || true
    exit 1
}

echo -e "${BLUE}${BOLD}==> Enviando alterações para o GitHub (git push)...${RESET}"
git push origin main

echo -e "${GREEN}${BOLD}==> ✅ Deploy enviado com sucesso para git@github.com:connectlab1/cortex-news.git!${RESET}"
