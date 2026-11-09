"""Módulo centralizado para orquestração da pipeline ETL (Fetch -> Clean -> Process),

gerenciando a execução completa e registrando logs de status do build.
"""

from datetime import datetime, timezone

from .cleaner import limpar_e_tratar_dados
from .processor import processar_e_salvar_posts


def buscar_feeds_rss():
    """Executa a coleta dos feeds RSS importando a função correta do scraper."""
    print("[1/4] Coletando dados dos feeds RSS...")

    try:
        from .scraper import buscar_feeds
        return buscar_feeds()
    except ImportError as e:
        print(f"[Generator] Erro ao importar o scraper: {e}. Retornando lista vazia.")
        return []


def executar_pipeline():
    """Executa a rotina completa da pipeline de ponta a ponta."""
    inicio = datetime.now(timezone.utc)
    print(f"=== [Cortex News 2] Iniciando pipeline em {inicio.strftime('%Y-%m-%d %H:%M:%S %Z')} ===")

    # Passo 1: Coleta dos dados brutos dos feeds RSS
    dados_brutos = buscar_feeds_rss()
    if not dados_brutos:
        print("[Generator] Nenhum dado bruto coletado. Encerrando pipeline.")
        return 0

    # Passo 2: Limpeza, conversão para Markdown, filtros e aplicação do dicionário
    dados_limpos = limpar_e_tratar_dados(dados_brutos)
    if not dados_limpos:
        print("[Generator] Nenhum dado restou após a limpeza. Encerrando pipeline.")
        return 0

    # Passo 3: Processamento, validação de limite de palavras, deduplicação atômica e salvamento no Jekyll
    posts_gerados = processar_e_salvar_posts(dados_limpos)

    fim = datetime.now(timezone.utc)
    duracao = (fim - inicio).total_seconds()
    print(f"=== [Cortex News 2] Pipeline concluída com sucesso em {duracao:.2f}s. Total de posts gerados: {posts_gerados} ===")

    return posts_gerados


if __name__ == "__main__":
    executar_pipeline()
