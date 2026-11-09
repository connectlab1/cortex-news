#!/usr/bin/env python3
"""Script principal de produção (main.py) para execução

contínua e automatizada da pipeline ETL com deploy integrado.
"""

from datetime import datetime
import os
import subprocess
import sys
import time

from src.cleaner import limpar_e_tratar_dados
from src.config import DATA_DIR, POSTS_DIR
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


def validar_script_deploy(script_path="./deploy.sh") -> bool:
    """Verifica preventivamente a existência e as permissões de execução do script de deploy."""
    if not os.path.exists(script_path):
        print(f"{RED}[Main] Erro crítico: O script de deploy '{script_path}' não foi encontrado.{RESET}")
        return False

    if not os.access(script_path, os.X_OK):
        print(f"{YELLOW}[Main] Aviso: '{script_path}' não possui permissão de execução. Ajustando permissões (chmod +x)...{RESET}")
        try:
            os.chmod(script_path, 0o755)
        except Exception as err:
            print(f"{RED}[Main] Falha ao atribuir permissão de execução em '{script_path}': {err}{RESET}")
            return False
    return True


def executar_pipeline_producao():
    """Executa um ciclo completo da pipeline ETL de produção: RSS -> Cleaner -> Processor -> Deploy."""
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    exibir_banner(f"🚀 [ {data_hora} ] Executando Pipeline ETL de Produção: RSS para Jekyll", CYAN)

    try:
        garantir_diretorios()

        # 1. Extração (Scraper via Generator)
        dados_brutos = buscar_feeds_rss()
        if not dados_brutos:
            print(f"{YELLOW}[Main] Nenhum dado coletado nesta execução.{RESET}")
            return

        # 2. Limpeza (Cleaner)
        dados_limpos = limpar_e_tratar_dados(dados_brutos)
        if not dados_limpos:
            print(f"{YELLOW}[Main] Nenhum item permaneceu após a etapa de limpeza.{RESET}")
            return

        # 3. Processamento, Validação de Palavras, Deduplicação e Salvamento (Processor)
        posts_salvos = processar_e_salvar_posts(dados_limpos)

        # 4. Verificação de Alterações no Repositório e Disparo do Deploy
        script_deploy = "./deploy.sh"

        # Checa se há arquivos modificados na árvore do Git (posts novos, histórico ou scripts)
        status_git = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()

        if posts_salvos > 0 or status_git:
            if not validar_script_deploy(script_deploy):
                print(f"{RED}[Main] Abortando deploy automatizado devido a problemas no script.{RESET}")
                return

            if posts_salvos > 0:
                print(f"{GREEN}{BOLD}[✔] {posts_salvos} novo(s) post(s) gerado(s). Iniciando publicação...{RESET}")
            else:
                print(f"{YELLOW}{BOLD}[i] Nossos posts novos, mas foram detectadas alterações locais em arquivos/scripts.{RESET}")

            # Alerta sonoro + pausa de segurança
            emitir_alerta_terminal()
            print(f"\n{YELLOW}{BOLD}⏳ Aguardando 2 segundos antes de iniciar o deploy ({script_deploy})...{RESET}")
            time.sleep(2)

            # Aciona o script de deploy capturando e unificando stdout e stderr
            print(f"{BLUE}{BOLD}🚀 Executando deploy via {script_deploy}...{RESET}\n")
            try:
                resultado = subprocess.run(
                    [script_deploy],
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )

                if resultado.stdout:
                    print(resultado.stdout)

                exibir_banner("✨ DEPLOY CONCLUÍDO COM SUCESSO!", GREEN)
                emitir_alerta_terminal()

            except subprocess.CalledProcessError as e:
                exibir_banner("❌ FALHA AO EXECUTAR O DEPLOY", RED)
                if e.stdout:
                    print(e.stdout)
                emitir_alerta_terminal()
            except Exception as e:
                exibir_banner(f"❌ ERRO INESPERADO AO EXECUTAR DEPLOY: {e}", RED)
                emitir_alerta_terminal()
        else:
            print(f"{YELLOW}[Main] Nenhum novo post gerado e nenhuma alteração pendente no repositório. Deploy ignorado.{RESET}")

    except Exception as e:
        exibir_banner(f"🔥 ERRO CRÍTICO NO PIPELINE: {e}", RED)
        emitir_alerta_terminal()


if __name__ == "__main__":
    INTERVALO_SEGUNDOS = 3600  # 1 hora

    # Limpa a tela do terminal ao iniciar o daemon de produção
    print("\033[H\033[J", end="")
    exibir_banner("🤖 Robô ETL de Produção Iniciado (Daemon Mode)", BLUE)
    print(f"{BOLD}Conectado ao script oficial de deploy: ./deploy.sh{RESET}")
    print(f"{BOLD}Pressione Ctrl+C a qualquer momento para interromper.{RESET}\n")

    try:
        while True:
            executar_pipeline_producao()
            print(f"\n{CYAN}⏳ Próxima varredura em 1 hora. Aguardando no terminal...{RESET}")
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}{BOLD}🛑 Execução interrompida via Ctrl+C. Saindo...{RESET}\n")
