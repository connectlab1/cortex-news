import feedparser
import requests
from .config import HEADERS, REQUEST_TIMEOUT, RSS_FEEDS


def buscar_feeds():
  """Varre os feeds RSS configurados centralmente no config.py,

  tratando falhas de rede individualmente e estruturando os dados brutos.
  """
  print("[1/4] Coletando dados dos feeds RSS...")
  dados_brutos = []

  for portal, url in RSS_FEEDS.items():
    try:
      # Requisição com timeout centralizado para evitar travamentos de rede
      response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
      response.raise_for_status()

      # Passa o conteúdo decodificado para o feedparser
      feed = feedparser.parse(response.content)

      if feed.bozo and not feed.entries:
        print(f"[Scraper] Aviso: Feed malformado ou corrompido em {portal}.")
        continue

      for entry in feed.entries:
        # Extração segura dos campos básicos do RSS
        titulo = entry.get("title", "")
        link = entry.get("link", "")

        # Tenta pegar o sumário ou o conteúdo completo disponível no feed
        descricao = entry.get("summary", "")
        if not descricao and "content" in entry:
          descricao = entry["content"][0].get("value", "")

        # Captura a data de publicação (várias tags possíveis dependendo do padrão)
        data_str = (
            entry.get("published")
            or entry.get("updated")
            or entry.get("pubDate", "")
        )

        if titulo and link:
          dados_brutos.append({
              "portal": portal,
              "titulo": titulo,
              "link": link,
              "descricao": descricao,
              "data_str": data_str,
          })

      print(f"[Scraper] Sucesso ao coletar de: {portal} ({len(feed.entries)} itens)")

    except requests.exceptions.Timeout:
      print(f"[Scraper] Erro: Timeout ao tentar acessar o feed de {portal}.")
    except requests.exceptions.RequestException as e:
      print(f"[Scraper] Erro de rede ao acessar {portal}: {e}")
    except Exception as e:
      print(f"[Scraper] Erro inesperado ao processar {portal}: {e}")

  print(f"[Scraper] Total bruto coletado: {len(dados_brutos)} itens.")
  return dados_brutos
