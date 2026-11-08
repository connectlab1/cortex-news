from datetime import datetime
import os
import sys
import time
from src.cleaner import limpar_e_tratar_dados
from src.config import DATA_DIR, POSTS_DIR
from src.generator import gerar_arquivo_jekyll
from src.history import carregar_historico, salvar_historico
from src.processor import filtrar_e_ordenar
from src.scraper import buscar_feeds

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


def executar_pipeline():
    """Executa um ciclo completo da pipeline ETL local: RSS -> Cleaner -> Processor -> Generator."""
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    exibir_banner(f"🚀 [ {data_hora} ] Executando Pipeline ETL Local: RSS para Jekyll", CYAN)

    try:
        garantir_diretorios()

        # 1. Extração (Scraper)
        dados_brutos = buscar_feeds()
        if not dados_brutos:
            print(f"{YELLOW}[Main] Nenhum dado coletado nesta execução.{RESET}")

        # 2. Limpeza (Cleaner)
        dados_limpos = limpar_e_tratar_dados(dados_brutos) if dados_brutos else []
        if dados_brutos and not dados_limpos:
            print(f"{YELLOW}[Main] Nenhum item permaneceu após a etapa de limpeza.{RESET}")

        # 3. Processamento, Filtro de Ruídos (Filters) e Validação de Qualidade (Processor)
        itens_aprovados = filtrar_e_ordenar(dados_limpos) if dados_limpos else []
        if dados_limpos and not itens_aprovados:
            print(f"{YELLOW}[Main] Nenhum item novo atingiu os critérios de qualidade e inédita.{RESET}")

        # 4. Geração de Posts Jekyll (Generator)
        links_novos_processados = []
        if itens_aprovados:
            print(f"{BLUE}[4/4] Gerando {len(itens_aprovados)} post(s) em Markdown para o Jekyll...{RESET}")
            for item in itens_aprovados:
                try:
                    gerar_arquivo_jekyll(item)
                    links_novos_processados.append(item["link"])
                except Exception as e:
                    print(f"{RED}[Main] Erro ao gerar post Jekyll para o link {item.get('link')}: {e}{RESET}")

        # Se houver novos links processados, atualiza o histórico em disco
        if links_novos_processados:
            historico_atual = carregar_historico()
            historico_atual.extend(links_novos_processados)
            salvar_historico(historico_atual)
            print(f"{GREEN}{BOLD}[✔] Histórico atualizado com {len(links_novos_processados)} novos itens gerados localmente.{RESET}")
            emitir_alerta_terminal()
        else:
            print(f"{YELLOW}[Main] Nenhuma nova postagem gerada neste ciclo.{RESET}")

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
            executar_pipeline()
            print(f"\n{CYAN}⏳ Próxima varredura em 1 hora. Aguardando no terminal...{RESET}")
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}{BOLD}🛑 Execução interrompida via Ctrl+C. Saindo...{RESET}\n")
