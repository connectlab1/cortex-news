from datetime import datetime
import os
import subprocess
import sys
import time
from src.cleaner import limpar_e_tratar_dados
from src.config import DATA_DIR, POSTS_DIR
from src.generator import gerar_arquivo_jekyll
from src.history import carregar_historico, salvar_historico
from src.processor import filtrar_e_ordenar
from src.scraper import buscar_feeds

# Cores ANSI para destaque no terminal do Arch Linux
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


def executar_pipeline():
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    exibir_banner(f"🚀 [ {data_hora} ] Executando Pipeline ETL: RSS para Jekyll", CYAN)

    try:
        garantir_diretorios()

        # 1. Extração
        dados_brutos = buscar_feeds()
        if not dados_brutos:
            print(f"{YELLOW}[Main] Nenhum dado coletado nesta execução.{RESET}")
            return

        # 2. Limpeza
        dados_limpos = limpar_e_tratar_dados(dados_brutos)

        # 3. Processamento e Filtro de Qualidade
        itens_aprovados = filtrar_e_ordenar(dados_limpos)
        if not itens_aprovados:
            print(f"{YELLOW}[Main] Nenhum item novo atingiu os critérios de qualidade.{RESET}")
            return

        # 4. Geração de Posts Jekyll
        print(f"{BLUE}[4/4] Gerando {len(itens_aprovados)} post(s) em Markdown para o Jekyll...{RESET}")
        links_novos_processados = []

        for item in itens_aprovados:
            try:
                gerar_arquivo_jekyll(item)
                links_novos_processados.append(item["link"])
            except Exception as e:
                print(f"{RED}[Main] Erro ao gerar post para o link {item.get('link')}: {e}{RESET}")

        # 5. Atualização do Histórico e Disparo do Deploy (deploy1.sh)
        if links_novos_processados:
            historico_atual = carregar_historico()
            historico_atual.extend(links_novos_processados)
            salvar_historico(historico_atual)

            print(f"{GREEN}{BOLD}[✔] Histórico atualizado com {len(links_novos_processados)} novos itens.{RESET}")

            # Alerta sonoro + pausa de 3 segundos
            emitir_alerta_terminal()
            print(f"\n{YELLOW}{BOLD}⏳ Aguardando 3 segundos antes de iniciar o deploy (deploy1.sh)...{RESET}")
            time.sleep(3)

            # Aciona o script de deploy de testes
            print(f"{BLUE}{BOLD}🚀 Executando deploy via ./deploy1.sh...{RESET}\n")
            try:
                # Executa o deploy1.sh e exibe os logs no terminal
                resultado = subprocess.run(
                    ["./deploy1.sh"], check=True, text=True, capture_output=True
                )

                if resultado.stdout:
                    print(resultado.stdout)

                exibir_banner("✨ DEPLOY CONCLUÍDO COM SUCESSO!", GREEN)
                emitir_alerta_terminal()

            except subprocess.CalledProcessError as e:
                exibir_banner("❌ FALHA AO EXECUTAR O DEPLOY", RED)
                if e.stdout:
                    print(e.stdout)
                if e.stderr:
                    print(f"{RED}{e.stderr}{RESET}")
                emitir_alerta_terminal()

    except Exception as e:
        exibir_banner(f"🔥 ERRO CRÍTICO NO PIPELINE: {e}", RED)
        emitir_alerta_terminal()


if __name__ == "__main__":
    INTERVALO_SEGUNDOS = 3600  # 1 hora

    # Limpa a tela do terminal ao iniciar
    print("\033[H\033[J", end="")
    exibir_banner("🤖 Robô ETL Persistente Iniciado (Terminal Mode)", BLUE)
    print(f"{BOLD}Conectado ao script de deploy: ./deploy1.sh{RESET}")
    print(f"{BOLD}Pressione Ctrl+C a qualquer momento para sair.{RESET}\n")

    try:
        while True:
            executar_pipeline()
            print(f"\n{CYAN}⏳ Próxima execução em 1 hora. Aguardando no terminal...{RESET}")
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}{BOLD}🛑 Execução interrompida via Ctrl+C. Saindo...{RESET}\n")
