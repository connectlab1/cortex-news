from datetime import datetime, timezone
import html
import re
from email.utils import parsedate_to_datetime
import html2text
from .filters import limpar_texto_com_filtros


def limpar_html(texto_html: str) -> str:
    """Converte o HTML do RSS para Markdown limpo, aplicando a sanitização

    do módulo filters.py, removendo lixos residuais e efetuando ajustes tipográficos.
    """
    if not texto_html:
        return ""

    # 1. Decodifica entidades HTML (ex: &nbsp;, &amp;, &quot;)
    texto_decodificado = html.unescape(texto_html)

    # 2. Converte HTML para Markdown formatado
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.body_width = 0

    markdown = h.handle(texto_decodificado)

    # 3. Delegação estrita ao módulo filters.py (remove frases da blacklist, regexes de syndication e placeholders)
    texto_filtrado = limpar_texto_com_filtros(markdown)

    # 4. Remove marcações indesejadas de markdown residual (colchetes vazios ou asteriscos soltos)
    texto_filtrado = re.sub(r"\[\s*\]\([^)]+\)", "", texto_filtrado)
    texto_filtrado = re.sub(r"\*{2,}", "", texto_filtrado)
    texto_filtrado = re.sub(r"https?://\S+", "", texto_filtrado)

    # 5. Ajustes tipográficos: remove espaços residuais entre aspas de abertura e pontuações
    texto_final = re.sub(r'([“"‘’])\s+([_*\w])', r'\1\2', texto_filtrado)
    texto_final = re.sub(r"\s+([,\.\?!”\)])", r"\1", texto_final)

    # 6. Normaliza múltiplos saltos de linha em no máximo duas quebras (parágrafos limpos)
    texto_final = re.sub(r"\n{3,}", "\n\n", texto_final)

    return texto_final.strip()


def limpar_e_tratar_dados(dados_brutos):
    """Recebe os dados brutos vindos do scraper e executa a limpeza

    modularizada de HTML, formatação tipográfica e preservação de metadados.
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

        # Preserva o objeto data_obj criado na etapa de scraping ou aplica fallback seguro em UTC
        data_obj = item.get("data_obj")
        if not isinstance(data_obj, datetime):
            data_str = item.get("data_str", "")
            try:
                data_obj = parsedate_to_datetime(data_str) if data_str else datetime.now(timezone.utc)
            except Exception:
                data_obj = datetime.now(timezone.utc)

        # Garante que dados mínimos e válidos existam antes de repassar ao processor
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
