"""Módulo centralizado para limpeza e conversão de HTML de feeds RSS

para Markdown limpo, estruturado e higienizado.
"""

from datetime import datetime, timezone
import html
import re
from email.utils import parsedate_to_datetime
import html2text
from .dictionary import aplicar_dicionario_termos
from .filters import limpar_texto_com_filtros


def limpar_html(texto_html: str) -> str:
    """Converte o HTML do RSS para Markdown limpo, organizando parágrafos,

    aplicando o dicionário externo de termos e os filtros de syndication.
    """
    if not texto_html:
        return ""

    # 1. Decodifica entidades HTML (ex: &nbsp;, &amp;, &quot;)
    texto_decodificado = html.unescape(texto_html)

    # 2. Converte HTML para Markdown formatado
    h = html2text.HTML2Text()
    h.ignore_links = False  # Preserva os links das matérias e referências
    h.ignore_images = True
    h.body_width = 0  # Desativa quebras artificiais de linha por largura

    markdown = h.handle(texto_decodificado)

    # 3. Formatação e separação de estrutura
    # Preserva quebras de linha em listas numeradas (ex: "1. Item; 2. Item;" -> "1. Item\n2. Item")
    markdown = re.sub(r";\s*(\d+\.\s+)", r";\n\1", markdown)

    # Garante que itens de lista com marcadores (ex: * Compre...) fiquem em novas linhas
    markdown = re.sub(r"([^\n])\s*\*\s+(Compre|Veja|Confira)", r"\1\n* \2", markdown)

    # Garante espaçamento adequado (linha dupla) antes de subtítulos (##)
    markdown = re.sub(r"([^\n])\n(#{1,6}\s+)", r"\1\n\n\2", markdown)

    # 4. Sanitização modular via filters.py (remove rodapés e lixos de RSS)
    texto_filtrado = limpar_texto_com_filtros(markdown)

    # 5. Aplicação do dicionário externo para correção de marcas e termos técnicos
    texto_filtrado = aplicar_dicionario_termos(texto_filtrado)

    # 6. Remove marcações residuais de markdown (colchetes vazios ou links soltos)
    texto_filtrado = re.sub(r"\[\s*\]\([^)]+\)", "", texto_filtrado)

    # 7. Normaliza múltiplos saltos de linha em no máximo duas quebras (parágrafos limpos)
    texto_final = re.sub(r"\n{3,}", "\n\n", texto_filtrado)

    # 8. Corrige espaços indesejados antes de pontuações (ex: "palavra , texto" -> "palavra, texto")
    texto_final = re.sub(r"\s+([,\.;!?])", r"\1", texto_final)

    return texto_final.strip()


def limpar_e_tratar_dados(dados_brutos):
    """Recebe a lista de dados brutos do scraper e executa a conversão,

    higienização e padronização dos metadados dos posts.
    """
    print("[2/4] Limpando e convertendo HTML com base no dicionário de filtros...")

    if not dados_brutos:
        print("[Cleaner] Nenhum dado bruto recebido para limpeza.")
        return []

    dados_limpos = []

    for item in dados_brutos:
        if not isinstance(item, dict):
            continue

        titulo = limpar_html(item.get("titulo", ""))
        descricao_md = limpar_html(item.get("descricao", ""))
        link = item.get("link", "").strip()
        portal = item.get("portal", "Desconhecido")

        # Preserva o objeto data_obj criado no scraping ou atribui fallback UTC
        data_obj = item.get("data_obj")
        if not isinstance(data_obj, datetime):
            data_str = item.get("data_str", "")
            try:
                data_obj = parsedate_to_datetime(data_str) if data_str else datetime.now(timezone.utc)
            except Exception:
                data_obj = datetime.now(timezone.utc)

        # Garante que apenas itens válidos com título e link sejam mantidos
        if titulo and link:
            dados_limpos.append({
                "portal": portal,
                "titulo": titulo,
                "link": link,
                "descricao": descricao_md,
                "data_obj": data_obj,
            })

    print(f"[Cleaner] {len(dados_limpos)} itens formatados e limpos com sucesso.")
    return dados_limpos
