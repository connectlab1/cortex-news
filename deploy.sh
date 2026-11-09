#!/bin/bash

# Interrompe o script imediatamente se ocorrer qualquer erro não tratado
set -e

# Força o Git a utilizar a chave SSH correta localizada em ~/.ssh/connectlab1
export GIT_SSH_COMMAND="ssh -i ~/.ssh/connectlab1 -o IdentitiesOnly=yes -F /dev/null"

# Cores ANSI para destaque no terminal
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
BLUE="\033[94m"
CYAN="\033[96m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${BLUE}${BOLD}==> Executando testes automatizados e QA (pytest)...${RESET}"
if ! pytest -q; then
    echo -e "${RED}==> ❌ Falha na suíte de testes unitários! O deploy foi abortado.${RESET}"
    exit 1
fi
echo -e "${GREEN}==> ✔ Suíte de testes unitários aprovada!${RESET}"

echo -e "${BLUE}${BOLD}==> Garantindo a URL remota correta do repositório (SSH)...${RESET}"
git remote set-url origin git@github.com:connectlab1/cortex-news.git

echo -e "${BLUE}${BOLD}==> Sincronizando com o repositório remoto (git pull com rebase)...${RESET}"
STASH_CREATED=false
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    git stash push -m "auto-stash-before-pull" >/dev/null 2>&1
    STASH_CREATED=true
fi

if ! git pull origin main --rebase; then
    echo -e "${RED}==> ❌ Falha no rebase remoto. Abortando deploy com segurança...${RESET}"
    git rebase --abort 2>/dev/null || true
    if [ "$STASH_CREATED" = true ]; then
        git stash pop >/dev/null 2>&1 || true
    fi
    exit 1
fi

if [ "$STASH_CREATED" = true ]; then
    git stash pop >/dev/null 2>&1 || true
fi

echo -e "${BLUE}${BOLD}==> Adicionando alterações ao controle de versão...${RESET}"
# Adiciona posts, dados, testes, documentação e estrutura essencial do projeto
git add _posts/ data/ src/ test/ assets/ _layouts/ _includes/ doc/ _config.yml index.html *.html README.md *.sh *.py *.json requirements.txt 2>/dev/null || git add .

if [ -n "$(git status --porcelain)" ]; then
    MSG="${1:-feat: atualização automática da pipeline ETL, testes e posts}"
    echo -e "${YELLOW}==> Criando commit: \"${MSG}\"${RESET}"
    git commit -m "$MSG"
else
    echo -e "${YELLOW}==> Nenhuma alteração pendente detectada para commit.${RESET}"
fi

echo -e "${BLUE}${BOLD}==> Enviando alterações para o GitHub (git push)...${RESET}"
git push origin main

echo -e "${GREEN}${BOLD}==> ✅ Deploy enviado com sucesso para git@github.com:connectlab1/cortex-news.git!${RESET}"
