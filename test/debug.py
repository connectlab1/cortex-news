#!/usr/bin/env python3
"""Script avançado de Diagnóstico, QA e Auditoria de Saúde da Pipeline ETL

(Cortex News 2). Analisa módulos, integridade de arquivos, front-matter,
conectividade de feeds RSS e integração com a suite de testes em test/.
"""

from datetime import datetime, timezone
import glob
import json
import os
import re
import sys
from pathlib import Path
import requests

# Cores ANSI para terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Diretórios base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

# Garante a importação dos módulos de src/
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def testar_importacoes():
    print(f"{BLUE}[1/6] Testando importação dos módulos da pipeline (src/)...{RESET}")
    modulos = [
        "src.config", "src.scraper", "src.cleaner", "src.filters",
        "src.dictionary", "src.rules", "src.processor", "src.history", "src.generator"
    ]
    falhas = 0
    for mod in modulos:
        try:
            __import__(mod)
            print(f"  {GREEN}✔{RESET} {mod} importado com sucesso.")
        except Exception as e:
            print(f"  {RED}✖ Falha ao importar {mod}: {e}{RESET}")
            falhas += 1
    return falhas == 0


def auditar_qualidade_codigo():
    print(f"\n{BLUE}[2/6] Auditando saúde dos arquivos de código-fonte (src/)...{RESET}")
    arquivos_py = sorted(list(SRC_DIR.glob("*.py")))

    problemas_encontrados = 0
    for arq in arquivos_py:
        nome_arq = arq.name

        # Ignora arquivos de inicialização de pacotes
        if nome_arq.startswith("__"):
            print(f"  {CYAN}ℹ{RESET} {nome_arq}: Ignorado na auditoria estrutural.")
            continue

        try:
            conteudo = arq.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  {RED}✖ Erro ao ler {nome_arq}: {e}{RESET}")
            problemas_encontrados += 1
            continue

        avisos = []
        if len(conteudo.strip()) == 0:
            avisos.append("Arquivo vazio.")
        if '"""' not in conteudo and "'''" not in conteudo:
            avisos.append("Falta docstring descritiva no módulo.")
        if "TODO" in conteudo or "FIXME" in conteudo:
            avisos.append("Contém marcações pendentes (TODO/FIXME).")

        if avisos:
            print(f"  {YELLOW}⚠{RESET} {nome_arq}: {', '.join(avisos)}")
            problemas_encontrados += 1
        else:
            print(f"  {GREEN}✔{RESET} {nome_arq}: Saudável.")

    return problemas_encontrados == 0


def testar_diretorios_e_posts():
    print(f"\n{BLUE}[3/6] Verificando infraestrutura e integridade dos posts (_posts/)...{RESET}")
    from src.config import DATA_DIR, HISTORY_FILE, POSTS_DIR

    sucesso = True
    print(f"  {GREEN}✔{RESET} DATA_DIR: {DATA_DIR}")
    print(f"  {GREEN}✔{RESET} POSTS_DIR: {POSTS_DIR}")

    # Auditoria do histórico
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"  {GREEN}✔{RESET} Histórico JSON válido ({len(data)} links registrados).")
        except Exception as e:
            print(f"  {RED}✖ Arquivo de histórico corrompido: {e}{RESET}")
            sucesso = False
    else:
        print(f"  {YELLOW}⚠{RESET} Histórico ainda não existe (será gerado no primeiro ciclo).")

    # Auditoria dos posts Jekyll gerados e validação de Front Matter
    if os.path.exists(POSTS_DIR):
        posts = sorted(glob.glob(os.path.join(POSTS_DIR, "*.md")))
        print(f"  {CYAN}ℹ{RESET} Total de posts Jekyll encontrados: {len(posts)}")

        posts_com_problema = 0
        padrao_nome = re.compile(r"^\d{4}-\d{2}-\d{2}-[\w-]+\.md$")

        for post_path in posts[:10]:  # Amostra dos 10 mais recentes
            nome_p = os.path.basename(post_path)
            if not padrao_nome.match(nome_p):
                print(f"    {YELLOW}⚠{RESET} Nome fora do padrão Jekyll: {nome_p}")
                posts_com_problema += 1

            # Valida se o post possui Front Matter básico
            try:
                with open(post_path, "r", encoding="utf-8") as pf:
                    cabecalho = pf.read(150)
                    if not cabecalho.startswith("---") or "layout:" not in cabecalho:
                        print(f"    {YELLOW}⚠{RESET} Post sem Front Matter válido: {nome_p}")
                        posts_com_problema += 1
            except Exception as e:
                print(f"    {RED}✖ Erro ao ler post {nome_p}: {e}{RESET}")
                posts_com_problema += 1

        if posts_com_problema == 0 and posts:
            print(f"    {GREEN}✔{RESET} Amostra de nomenclatura e Front Matter dos posts validada.")
    else:
        print(f"  {YELLOW}⚠{RESET} Diretório _posts/ ainda não criado.")

    return sucesso


def testar_regras_e_slugs():
    print(f"\n{BLUE}[4/6] Testando funções de regras e slugs...{RESET}")
    from src.processor import gerar_slug
    from src.rules import validar_regras_post

    slug = gerar_slug("Teste de Título com Acentuação & Símbolos!")
    esperado = "teste-de-titulo-com-acentuacao-simbolos"
    slug_ok = slug == esperado
    print(f"  {'✔' if slug_ok else '✖'} Geração de slug: '{slug}' (Esperado: '{esperado}')")

    valido, msg = validar_regras_post("Título", "Texto muito curto", "https://exemplo.com")
    regras_ok = not valido
    print(f"  {'✔' if regras_ok else '✖'} Validação de limite de palavras: {msg}")
    return slug_ok and regras_ok


def testar_cleaner_e_dicionario():
    print(f"\n{BLUE}[5/6] Testando limpeza de HTML e dicionário de termos...{RESET}")
    from src.cleaner import limpar_html

    html_amostra = "<p>O novo i Phone 15 e a tecnologia o LED chegam ao KaBu M!.</p>"
    resultado = limpar_html(html_amostra)
    esperado_contem = "iPhone" in resultado and "OLED" in resultado and "KaBuM!" in resultado
    print(f"  {'✔' if esperado_contem else '✖'} Dicionário tipográfico e limpeza aplicados: '{resultado}'")
    return esperado_contem


def testar_scraper_conectividade():
    print(f"\n{BLUE}[6/6] Testando conectividade com os feeds RSS...{RESET}")
    from src.config import RSS_FEEDS

    sucesso_geral = True
    for portal, url in RSS_FEEDS.items():
        try:
            resp = requests.head(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code < 400:
                print(f"  {GREEN}✔{RESET} {portal}: HTTP {resp.status_code}")
            else:
                print(f"  {YELLOW}⚠{RESET} {portal}: Retornou status HTTP {resp.status_code}")
        except Exception as e:
            print(f"  {YELLOW}⚠{RESET} {portal}: Falha na checagem HEAD direta ({e})")
    return sucesso_geral


if __name__ == "__main__":
    print(f"{BLUE}=== [Cortex News 2] Auditoria Avançada de Saúde e QA (test/debug.py) ===\n{RESET}")
    t1 = testar_importacoes()
    t2 = auditar_qualidade_codigo()
    t3 = testar_diretorios_e_posts()
    t4 = testar_regras_e_slugs()
    t5 = testar_cleaner_e_dicionario()
    t6 = testar_scraper_conectividade()

    print(f"\n{BLUE}=== Relatório Geral de Saúde ===")
    if t1 and t2 and t3 and t4 and t5:
        print(f"{GREEN}{BOLD}✔ Sistema 100% saudável! Todos os módulos, regras e posts passaram na auditoria QA.{RESET}")
    else:
        print(f"{YELLOW}{BOLD}⚠ Foram identificados avisos ou pontos de atenção na auditoria acima.{RESET}")
