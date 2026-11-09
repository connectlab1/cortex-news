"""Módulo centralizado de processamento, validação de word count,

geração de slugs e persistência de posts no diretório _posts do Jekyll.
"""

from datetime import datetime, timezone
import os
import re
import unicodedata

from .config import MAX_SLUG_LENGTH, POSTS_DIR
from .history import carregar_historico, salvar_historico
from .rules import montar_front_matter, validar_regras_post


def gerar_slug(titulo: str) -> str:
    """Gera um slug limpo, URL-friendly e com limite de tamanho a partir do título."""
    if not titulo:
        return "post-sem-titulo"

    # Normaliza caracteres especiais e remove acentos
    nfkd_form = unicodedata.normalize("NFKD", titulo)
    texto_limpo = "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    # Converte para minúsculas e substitui caracteres não alfanuméricos por hífens
    slug = re.sub(r"[^a-z0-9]+", "-", texto_limpo.lower()).strip("-")

    # Corta no limite configurado, garantindo que não termine em hífen quebrado
    if len(slug) > MAX_SLUG_LENGTH:
        slug = slug[:MAX_SLUG_LENGTH].rsplit("-", 1)[0]

    return slug or "post"


def processar_e_salvar_posts(dados_limpos):
    """Processa os dados limpos aplicando as regras centrais de validação,

    evita duplicatas e salva os arquivos Markdown no formato padrão do Jekyll.
    """
    print("[3/4] Processando posts, validando regras e gerando arquivos Jekyll...")

    if not dados_limpos:
        print("[Processor] Nenhum dado limpo recebido para processamento.")
        return 0

    os.makedirs(POSTS_DIR, exist_ok=True)

    # Carrega histórico atômico (retorna lista de dicionários)
    historico_lista = carregar_historico()

    # Cria um conjunto (set) apenas com as strings dos links para busca rápida e segura
    historico_set = {item["link"] for item in historico_lista if isinstance(item, dict) and "link" in item}

    posts_salvos = 0
    novos_links_adicionados = []

    for item in dados_limpos:
        link = item.get("link")
        if not link or link in historico_set:
            continue

        titulo = item.get("titulo", "")
        descricao = item.get("descricao", "")
        portal = item.get("portal", "Tech")
        data_obj = item.get("data_obj", datetime.now(timezone.utc))

        # Validação centralizada através do módulo rules.py
        valido, mensagem_status = validar_regras_post(titulo, descricao, link)
        if not valido:
            print(f"[Processor] Ignorado: {titulo[:40]}... -> {mensagem_status}")
            continue

        # Gera slug e nome do arquivo Jekyll (YYYY-MM-DD-slug.md)
        slug = gerar_slug(titulo)
        data_str_jelly = data_obj.strftime("%Y-%m-%d")
        nome_arquivo = f"{data_str_jelly}-{slug}.md"
        caminho_arquivo = os.path.join(POSTS_DIR, nome_arquivo)

        # Evita sobreposição de arquivos com nomes idênticos no mesmo dia
        contador = 1
        base_nome, ext = os.path.splitext(nome_arquivo)
        while os.path.exists(caminho_arquivo):
            nome_arquivo = f"{base_nome}-{contador}{ext}"
            caminho_arquivo = os.path.join(POSTS_DIR, nome_arquivo)
            contador += 1

        # Formatação do Front Matter utilizando o modelo padrão de rules.py
        data_iso = data_obj.strftime("%Y-%m-%d %H:%M:%S %z")
        front_matter = montar_front_matter(titulo, data_iso, portal, link)
        conteudo_final = f"{front_matter}\n{descricao}\n"

        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo_final)

            historico_set.add(link)

            # Adiciona ao histórico o dicionário completo com o link e o nome do arquivo
            novos_links_adicionados.append({
                "link": link,
                "arquivo": nome_arquivo
            })

            posts_salvos += 1
            print(f"[Processor] Post salvo: {nome_arquivo}")
        except Exception as e:
            print(f"[Processor] Erro ao salvar o arquivo {nome_arquivo}: {e}")

    # Salva o histórico estruturado de forma atômica se houver novos itens
    if novos_links_adicionados:
        historico_atualizado = historico_lista + novos_links_adicionados
        salvar_historico(historico_atualizado)

    print(f"[Processor] Processamento concluído. {posts_salvos} novos posts gerados.")
    return posts_salvos
