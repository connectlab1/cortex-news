#!/usr/bin/env python3
"""Script de Saneamento em 4 Etapas (fix-posts.py).

Etapa 0: Ignora arquivos que já estão perfeitamente nos padrões válidos.
Etapa 1: Valida os arquivos existentes em _posts/ com base nas regras oficiais.
Etapa 2: Move posts com falhas estruturais ou inválidos para data/quarantine_posts/.
Etapa 3: Reescreve e padroniza completamente os posts que precisam de correção.
"""

from datetime import datetime, timezone
import glob
import os
import re
import shutil

from src.cleaner import limpar_html
from src.config import DATA_DIR, POSTS_DIR
from src.processor import gerar_slug
from src.rules import montar_front_matter, validar_regras_post

# Cores ANSI para destaque no terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def exibir_banner(titulo, cor=CYAN):
    """Exibe um cabeçalho destacado com cores no terminal."""
    print("\n" + cor + BOLD + "=" * 65 + RESET)
    print(f"{cor}{BOLD} {titulo}{RESET}")
    print(cor + BOLD + "=" * 65 + RESET + "\n")


def garantir_diretorios():
    """Garante que os diretórios essenciais existam."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "quarantine_posts"), exist_ok=True)


def extrair_dados_post(caminho_arquivo):
    """Extrai com segurança os metadados e o conteúdo do post existente."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo_total = f.read()

        titulo = None
        link = None
        portal = "Tech"
        data_obj = datetime.now(timezone.utc)

        partes = conteudo_total.split("---", 2)
        front_matter = partes[1] if len(partes) >= 3 else conteudo_total
        corpo = partes[2] if len(partes) >= 3 else conteudo_total

        for linha in front_matter.split("\n"):
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                chave = chave.strip().lower()
                valor = valor.strip().strip('"').strip("'")

                if chave == "title":
                    titulo = valor.replace('\\"', '"')
                elif chave == "link":
                    link = valor.split()[0].strip('")(\'*')
                elif chave == "categories":
                    portal = valor.strip("[]").strip()
                elif chave == "date":
                    match_data = re.search(r"\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}", valor)
                    if match_data:
                        try:
                            data_str = match_data.group(0).replace("t", " ").replace("T", " ")
                            data_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                        except Exception:
                            pass
                    else:
                        match_data_simples = re.search(r"\d{4}-\d{2}-\d{2}", valor)
                        if match_data_simples:
                            try:
                                data_obj = datetime.strptime(match_data_simples.group(0), "%Y-%m-%d").replace(tzinfo=timezone.utc)
                            except Exception:
                                pass

        if not link:
            match_link_solto = re.search(r"https?://[^\s<>\"'\)]+", conteudo_total)
            if match_link_solto:
                link = match_link_solto.group(0)

        corpo_limpo = re.sub(r"> \*\*Gostou do assunto\?\*\*.*", "", corpo, flags=re.DOTALL).strip()

        return titulo, link, portal, corpo_limpo, data_obj
    except Exception as e:
        print(f"[Erro] Falha ao ler {caminho_arquivo}: {e}")
        return None, None, None, None, None


def arquivo_ja_esta_padronizado(caminho_arquivo, titulo, link, data_obj):
    """ETAPA 0: Verifica se o arquivo já possui nome correto, metadados íntegros e sem poluição."""
    nome_arquivo = os.path.basename(caminho_arquivo)
    slug_esperado = gerar_slug(titulo) if titulo else ""
    data_str_esperada = data_obj.strftime("%Y-%m-%d")
    nome_esperado = f"{data_str_esperada}-{slug_esperado}.md"

    # Se o nome do arquivo atual já bate com o padrão gerado pelo sistema
    if nome_arquivo == nome_esperado:
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()
            # Se não contém resíduos antigos ou marcações duplicadas de rodapé
            if "> **Gostou do assunto?**" not in conteudo and "layout: post" in conteudo:
                return True
        except Exception:
            pass
    return False


def executar_pipeline_4_etapas():
    exibir_banner("🛡️ [Cortex News 2] Auditoria e Saneamento em 4 Etapas", BLUE)
    garantir_diretorios()

    quarentena_dir = os.path.join(DATA_DIR, "quarantine_posts")
    arquivos_posts = glob.glob(os.path.join(POSTS_DIR, "*.md"))

    if not arquivos_posts:
        print(f"{YELLOW}[Fix-Posts] Nenhum post encontrado em {POSTS_DIR}.{RESET}")
        return

    print(f"{CYAN}ℹ Total de posts encontrados para auditoria: {len(arquivos_posts)}\n{RESET}")

    ignorados = 0
    enviados_quarentena = 0
    reescritos = 0

    for caminho_post in arquivos_posts:
        nome_arquivo = os.path.basename(caminho_post)

        # Leitura e extração de metadados
        titulo, link, portal, corpo, data_obj = extrair_dados_post(caminho_post)

        if not titulo or not link or not corpo:
            # ETAPA 2: Envio para Quarentena por falha estrutural
            enviados_quarentena += 1
            shutil.move(caminho_post, os.path.join(quarentena_dir, nome_arquivo))
            print(f"{YELLOW}  📦 Quarentena (Metadados ausentes):{RESET} {nome_arquivo}")
            continue

        # ETAPA 0: Ignora arquivos que já estão perfeitamente nos padrões válidos
        if arquivo_ja_esta_padronizado(caminho_post, titulo, link, data_obj):
            ignorados += 1
            print(f"{CYAN}  ⏩ Ignorado (Já está padronizado):{RESET} {nome_arquivo}")
            continue

        # ETAPA 1: Validação de regras oficiais
        corpo_higienizado = limpar_html(corpo)
        valido, mensagem_regra = validar_regras_post(titulo, corpo_higienizado, link)

        if not valido:
            # ETAPA 2: Envio para Quarentena por infração de regras
            enviados_quarentena += 1
            shutil.move(caminho_post, os.path.join(quarentena_dir, nome_arquivo))
            print(f"{YELLOW}  📦 Quarentena ({mensagem_regra}):{RESET} {nome_arquivo}")
            continue

        # ETAPA 3: Reescrever e padronizar completamente o post que precisa de correção
        try:
            slug = gerar_slug(titulo)
            data_str_jelly = data_obj.strftime("%Y-%m-%d")
            novo_nome_arquivo = f"{data_str_jelly}-{slug}.md"
            novo_caminho = os.path.join(POSTS_DIR, novo_nome_arquivo)

            data_iso = data_obj.strftime("%Y-%m-%d %H:%M:%S %z")
            front_matter = montar_front_matter(titulo, data_iso, portal, link)
            conteudo_final = f"{front_matter}\n{corpo_higienizado}\n"

            if caminho_post != novo_caminho and os.path.exists(caminho_post):
                os.remove(caminho_post)

            with open(novo_caminho, "w", encoding="utf-8") as f:
                f.write(conteudo_final)

            reescritos += 1
            print(f"{GREEN}  🔄 Etapa 3 (Corrigido e Reescrito):{RESET} {novo_nome_arquivo}")

        except Exception as e:
            print(f"{RED}  ✖ Erro ao reescrever {nome_arquivo}: {e}{RESET}")

    print(f"\n{BLUE}=== Resumo do Saneamento em 4 Etapas ===")
    print(f"  {CYAN}⏩ Ignorados (Já padronizados - Etapa 0):{RESET} {ignorados}")
    print(f"  {YELLOW}📦 Enviados para Quarentena (Etapa 2):{RESET} {enviados_quarentena}")
    print(f"  {GREEN}🔄 Corrigidos e reescritos (Etapa 3):{RESET} {reescritos}\n")


if __name__ == "__main__":
    executar_pipeline_4_etapas()
