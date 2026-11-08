from datetime import datetime
import hashlib
import os
import re
from .config import POSTS_DIR


def gerar_arquivo_jekyll(item):
  """Gera um arquivo Markdown (.md) estruturado para o Jekyll,

  utilizando o diretório centralizado configurado em config.py,
  garantindo slug único por hash de link e Front Matter seguro.
  """
  link = item.get("link", "").strip()

  # Validação de URL absoluta para evitar CTAs quebrados com links relativos
  if not link.startswith(("http://", "https://")):
    print(f"[Generator] Aviso: Link inválido ou relativo detectado ({link}). Post ignorado.")
    return

  os.makedirs(POSTS_DIR, exist_ok=True)

  data_obj = item["data_obj"]
  data_arquivo = data_obj.strftime("%Y-%m-%d")
  data_frontmatter = data_obj.strftime("%Y-%m-%d %H:%M:%S %z")

  titulo = item["titulo"]
  portal = item["portal"]

  # 1. Prevenção de colisão: Gera um hash curto baseado no link exclusivo da notícia
  hash_link = hashlib.md5(link.encode("utf-8")).hexdigest()[:6]

  # 2. Cria um slug limpo baseado no título (limitado a 40 caracteres)
  slug_base = "".join(
      c for c in titulo.lower() if c.isalnum() or c.isspace()
  ).replace(" ", "-")
  slug_limpo = re.sub(r"-+", "-", slug_base).strip("-")[:40]

  # Nome final do arquivo combinando data, slug e hash único anti-colisão
  nome_arquivo = f"{data_arquivo}-{slug_limpo}-{hash_link}.md"
  caminho_completo = os.path.join(POSTS_DIR, nome_arquivo)

  # Escapa aspas de forma segura para o YAML Front Matter
  titulo_yaml = titulo.replace('"', '\\"')
  portal_yaml = portal.replace('"', '\\"')

  # 3. Montagem do post Markdown seguindo os padrões de legibilidade e CTA
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

  # Escreve o arquivo no disco com codificação UTF-8 rígida
  try:
    with open(caminho_completo, "w", encoding="utf-8") as f:
      f.write(conteudo_markdown)
    print(f"[Generator] Post criado com sucesso: {nome_arquivo}")
  except IOError as e:
    print(f"[Generator] Erro ao criar o arquivo {nome_arquivo}: {e}")
