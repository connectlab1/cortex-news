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


def executar_pipeline():
    """Executa um ciclo completo da pipeline ETL: RSS -> Cleaner -> Processor -> Generator -> Deploy."""
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    exibir_banner(f"🚀 [ {data_hora} ] Executando Pipeline ETL: RSS para Jekyll", CYAN)

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
            print(f"{GREEN}{BOLD}[✔] Histórico atualizado com {len(links_novos_processados)} novos itens.{RESET}")

        # 5. Verificação de Alterações no Repositório e Disparo do Deploy
        script_deploy = "./deploy.sh"

        # Checa se há qualquer arquivo modificado na árvore do Git (scripts, posts, layouts ou configs)
        status_git = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()

        if links_novos_processados or status_git:
            if not validar_script_deploy(script_deploy):
                print(f"{RED}[Main] Abortando deploy automatizado devido a problemas no script.{RESET}")
                return

            if links_novos_processados:
                print(f"{GREEN}{BOLD}[✔] Novos posts detectados para publicação.{RESET}")
            else:
                print(f"{YELLOW}{BOLD}[i] Nenhum post novo no RSS, mas foram detectadas alterações locais em arquivos/scripts.{RESET}")

            # Alerta sonoro + pausa de segurança
            emitir_alerta_terminal()
            print(f"\n{YELLOW}{BOLD}⏳ Aguardando 3 segundos antes de iniciar o deploy ({script_deploy})...{RESET}")
            time.sleep(3)

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
            print(f"{YELLOW}[Main] Nenhuma alteração pendente no RSS ou no repositório. Deploy ignorado nesta execução.{RESET}")

    except Exception as e:
        exibir_banner(f"🔥 ERRO CRÍTICO NO PIPELINE: {e}", RED)
        emitir_alerta_terminal()


if __name__ == "__main__":
    INTERVALO_SEGUNDOS = 3600  # 1 hora

    # Limpa a tela do terminal ao iniciar o daemon
    print("\033[H\033[J", end="")
    exibir_banner("🤖 Robô ETL Persistente Iniciado (Terminal Mode)", BLUE)
    print(f"{BOLD}Conectado ao script de deploy oficial: ./deploy.sh{RESET}")
    print(f"{BOLD}Pressione Ctrl+C a qualquer momento para interromper.{RESET}\n")

    try:
        while True:
            executar_pipeline()
            print(f"\n{CYAN}⏳ Próxima execução em 1 hora. Aguardando no terminal...{RESET}")
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}{BOLD}🛑 Execução interrompida via Ctrl+C. Saindo...{RESET}\n")
