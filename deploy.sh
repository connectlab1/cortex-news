#!/bin/bash

# Interrompe o script imediatamente se ocorrer qualquer erro
set -e

echo "==> Adicionando alterações ao controle de versão..."
git add .

# Verifica se há arquivos modificados ou novos posts para commitar
if [ -n "$(git status --porcelain)" ]; then
    # Usa a mensagem passada por argumento ou uma padrão descritiva
    MSG="${1:-feat: atualização automática de posts e layouts}"
    echo "==> Criando commit: \"$MSG\""
    git commit -m "$MSG"
else
    echo "==> Nenhuma alteração nova detectada para commit."
fi

echo "==> Sincronizando com o repositório remoto (git pull)..."
git pull origin main --no-rebase

echo "==> Enviando alterações para o GitHub (git push)..."
git push origin main

echo "==> Deploy enviado com sucesso! O GitHub Actions já está processando a publicação do site."
