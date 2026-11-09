"""Módulo centralizado para coleta, extração e normalização de dados

dos feeds RSS configurados no projeto.
"""

from datetime import datetime, timezone
import feedparser
import requests
from .config import HEADERS, REQUEST_TIMEOUT, RSS_FEEDS


def _extrair_data_entrada(entry):
    """Extrai e converte de forma segura a data de publicação da entrada RSS

    utilizando as tuplas normalizadas do feedparser ou gerando fallback em UTC.
    """
    for campo_parsed in ("published_parsed", "updated_parsed", "expired_parsed"):
        struct_time = entry.get(campo_parsed)
        if struct_time:
            try:
                # Converte struct_time em datetime consciente de UTC
                return datetime(*struct_time[:6], tzinfo=timezone.utc)
            except Exception:
                continue

    # Fallback seguro em UTC caso a conversão direta falhe
    return datetime.now(timezone.utc)


def buscar_feeds():
    """Varre os feeds RSS configurados centralmente no config.py,

    tratando falhas de rede individualmente, normalizando datas via feedparser,
    garantindo links absolutos e autodetectando o encoding por bytes crus.
    """
    print("[1/4] Coletando dados dos feeds RSS...")
    dados_brutos = []

    for portal, url in RSS_FEEDS.items():
        try:
            # Requisição HTTP com timeout e cabeçalhos centralizados
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            # Passa os bytes crus (response.content) para o feedparser autodetectar a codificação de caracteres
            feed = feedparser.parse(response.content)

            if not feed.entries:
                print(f"[Scraper] Aviso: Nenhuma entrada encontrada no feed de {portal}.")
                continue

            if feed.get("bozo", 0) == 1:
                print(f"[Scraper] Nota: Feed de {portal} possui alertas de formatação XML (bozo), prosseguindo...")

            contador_portal = 0
            for entry in feed.entries:
                titulo = entry.get("title", "").strip()
                link = entry.get("link", "").strip()

                # Validação estrita para aceitar apenas URLs absolutas válidas
                if not link.startswith(("http://", "https://")):
                    print(f"[Scraper] Link relativo ou inválido descartado em {portal}: {link}")
                    continue

                # Captura o sumário ou o conteúdo completo disponível na tag de conteúdo do feed
                descricao = entry.get("summary", "").strip()
                if not descricao and "content" in entry:
                    content_list = entry["content"]
                    if isinstance(content_list, list) and len(content_list) > 0:
                        descricao = content_list[0].get("value", "").strip()

                # Extrai e padroniza a data em objeto datetime consciente (UTC)
                data_obj = _extrair_data_entrada(entry)

                if titulo and link:
                    dados_brutos.append({
                        "portal": portal,
                        "titulo": titulo,
                        "link": link,
                        "descricao": descricao,
                        "data_obj": data_obj,
                    })
                    contador_portal += 1

            print(f"[Scraper] Sucesso ao coletar de: {portal} ({contador_portal} itens válidos)")

        except requests.exceptions.Timeout:
            print(f"[Scraper] Erro: Timeout ao tentar acessar o feed de {portal}.")
        except requests.exceptions.RequestException as e:
            print(f"[Scraper] Erro de rede ao acessar {portal}: {e}")
        except Exception as e:
            print(f"[Scraper] Erro inesperado ao processar {portal}: {e}")

    print(f"[Scraper] Total bruto coletado com sucesso: {len(dados_brutos)} itens.")
    return dados_brutos
