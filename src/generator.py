from datetime import datetime
import hashlib
import os
import re
import unicodedata
from .config import POSTS_DIR


def gerar_slug(titulo: str) -> str:
    """Gera um slug totalmente sanitizado, sem acentos e seguro para URLs do Jekyll.

    Exemplo: "Guia definitivo: Saiba qual versão do Gemini você realmente deve usar"
    Retorna: "guia-definitivo-saiba-qual-versao-do-gemini"
    """
    # 1. Converte para minúsculas e decompõe caracteres acentuados (NFKD)
    nfkd_form = unicodedata.normalize("NFKD", titulo.lower())
    slug_sem_acento = "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    # 2. Mantém apenas caracteres alfanuméricos simples e espaços
    slug_base = "".join(c for c in slug_sem_acento if c.isalnum() or c.isspace())

    # 3. Substitui espaços sequenciais por um único hífen e remove hífens nas extremidades
    slug_limpo = re.sub(r"\s+", "-", slug_base).strip("-")
    slug_limpo = re.sub(r"-+", "-", slug_limpo)

    # 4. Trunca mantendo o limite de tamanho sem cortar palavras/hífens no meio
    return slug_limpo[:40].rstrip("-")


def gerar_arquivo_jekyll(item):
    """Gera um arquivo Markdown (.md) padronizado para o Jekyll.

    Garante sanitização estrita de URLs (sem acentos nem códigos %XX)
    e previne colisões de nomes de arquivos.
    """
    link = item.get("link", "").strip()

    # Validação de URL absoluta para evitar links relativos quebrados
    if not link.startswith(("http://", "https://")):
        print(f"[Generator] Aviso: Link inválido ou relativo detectado ({link}). Post ignorado.")
        return

    os.makedirs(POSTS_DIR, exist_ok=True)

    data_obj = item["data_obj"]
    data_arquivo = data_obj.strftime("%Y-%m-%d")
    data_frontmatter = data_obj.strftime("%Y-%m-%d %H:%M:%S %z")

    titulo = item["titulo"]
    portal = item["portal"]

    # 1. Prevenção de colisão: Gera um hash curto de 6 caracteres baseado no link único da notícia
    hash_link = hashlib.md5(link.encode("utf-8")).hexdigest()[:6]

    # 2. Gera o slug totalmente sanitizado (sem acentos nem símbolos especiais)
    slug_limpo = gerar_slug(titulo)

    # Nome final do arquivo combinando data, slug limpo e hash único anti-colisão
    nome_arquivo = f"{data_arquivo}-{slug_limpo}-{hash_link}.md"
    caminho_completo = os.path.join(POSTS_DIR, nome_arquivo)

    # Escapa aspas duplas de forma segura para o YAML Front Matter
    titulo_yaml = titulo.replace('"', '\\"')
    portal_yaml = portal.replace('"', '\\"')

    # 3. Montagem do post Markdown seguindo os padrões do Jekyll
    conteudo_markdown = f"""---
layout: post
title: "{titulo_yaml}"
date: {data_frontmatter}
categories: [{portal_yaml}]
---

{item['descricao']}

---

> **Gostou do assunto?** Para conferir todos os detalhes, imagens originais e a discussão completa, acesse a matéria original.
>
> 👉 **[Ler artigo completo no {portal}]({link})**
"""

    # Escreve o arquivo no disco com codificação UTF-8 estrita
    try:
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(conteudo_markdown)
        print(f"[Generator] Post criado com sucesso: {nome_arquivo}")
    except IOError as e:
        print(f"[Generator] Erro ao criar o arquivo {nome_arquivo}: {e}")
