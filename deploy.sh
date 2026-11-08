#!/bin/bash

# Interrompe o script se qualquer comando falhar
set -e

echo "==> Adicionando arquivos ao Git..."
git add .

# Verifica se há alterações para commitar
if [ -n "$(git status --porcelain)" ]; then
    # Usa o argumento passado no terminal como mensagem, ou uma mensagem padrão
    MSG="${1:-atualizacao automatica: posts e layouts}"
    echo "==> Criando commit: \"$MSG\""
    git commit -m "$MSG"
else
    echo "==> Nenhuma alteração nova para commitar."
fi

echo "==> Sincronizando com o GitHub (git pull)..."
git pull origin main --no-rebase

echo "==> Enviando atualizações para o GitHub (git push)..."
git push origin main

echo "==> Concluído com sucesso!"
