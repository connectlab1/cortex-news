#!/usr/bin/env python3
"""Script principal de desenvolvimento (main-dev.py) para execução

manual e local da pipeline ETL do Cortex News 2.
"""

from datetime import datetime
import os
import sys
import time

from src.cleaner import limpar_e_tratar_dados
from src.config import DATA_DIR, POSTS_DIR, RSS_FEEDS
from src.generator import buscar_feeds_rss
from src.processor import processar_e_salvar_posts

# Cores ANSI para destaque no terminal (Arch Linux / Linux CLI)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def emitir_alerta_terminal():
    """Emite um alerta sonoro nativo do terminal (bip ANSI)."""
    sys.stdout.write("\a")
    sys.stdout.flush()


def exibir_banner(titulo, cor=CYAN):
    """Exibe um cabeçalho destacado com cores no terminal."""
    print("\n" + cor + BOLD + "=" * 65 + RESET)
    print(f"{cor}{BOLD} {titulo}{RESET}")
    print(cor + BOLD + "=" * 65 + RESET + "\n")


def garantir_diretorios():
    """Garante que os diretórios essenciais do projeto existam."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(POSTS_DIR, exist_ok=True)


def executar_pipeline_local():
    """Executa um ciclo completo da pipeline ETL local: RSS -> Cleaner -> Processor (Jekyll)."""
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    exibir_banner(f"🚀 [ {data_hora} ] Executando Pipeline ETL Local: RSS para Jekyll", CYAN)

    try:
        garantir_diretorios()

        # 1. Extração (Scraper via Generator)
        dados_brutos = buscar_feeds_rss()
        if not dados_brutos:
            print(f"{YELLOW}[Main-Dev] Nenhum dado coletado nesta execução.{RESET}")
            return

        # 2. Limpeza (Cleaner)
        dados_limpos = limpar_e_tratar_dados(dados_brutos)
        if not dados_limpos:
            print(f"{YELLOW}[Main-Dev] Nenhum item permaneceu após a etapa de limpeza.{RESET}")
            return

        # 3. Processamento, Validação de Palavras, Deduplicação e Salvamento (Processor)
        posts_salvos = processar_e_salvar_posts(dados_limpos)

        if posts_salvos > 0:
            print(f"{GREEN}{BOLD}[✔] Processamento concluído com sucesso. {posts_salvos} novo(s) post(s) gerado(s) em _posts/.{RESET}")
            emitir_alerta_terminal()
        else:
            print(f"{YELLOW}[Main-Dev] Nenhum novo post gerado (conteúdo duplicado ou abaixo do limite mínimo de palavras).{RESET}")

    except Exception as e:
        exibir_banner(f"🔥 ERRO CRÍTICO NO PIPELINE: {e}", RED)
        emitir_alerta_terminal()


if __name__ == "__main__":
    INTERVALO_SEGUNDOS = 3600  # 1 hora

    # Limpa a tela do terminal ao iniciar o daemon local
    print("\033[H\033[J", end="")
    exibir_banner("🤖 Robô ETL Local Iniciado (Modo Desenvolvimento)", BLUE)
    print(f"{BOLD}Gerando posts diretamente na pasta _posts/ para teste local.{RESET}")
    print(f"{BOLD}Pressione Ctrl+C a qualquer momento para interromper.{RESET}\n")

    try:
        while True:
            executar_pipeline_local()
            print(f"\n{CYAN}⏳ Próxima varredura em 1 hora. Aguardando no terminal...{RESET}")
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}{BOLD}🛑 Execução interrompida via Ctrl+C. Saindo...{RESET}\n")
