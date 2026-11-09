"""Módulo centralizado para gerenciamento, carregamento e salvamento atômico

do histórico de posts processados, registrando links originais e arquivos gerados.
"""

from datetime import datetime
import json
import os
from .config import HISTORY_FILE


def carregar_historico():
    """Carrega o histórico de posts processados.

    Retorna uma lista de dicionários contendo o link original e o arquivo gerado,
    ou converte o formato antigo (lista de strings) automaticamente.
    """
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                historico_normalizado = []
                for item in data:
                    if isinstance(item, dict) and "link" in item:
                        # Garante que a chave 'arquivo' também exista
                        if "arquivo" not in item:
                            item["arquivo"] = "legado.md"
                        historico_normalizado.append(item)
                    elif isinstance(item, str) and item.strip():
                        # Migração retroativa de formato antigo (string simples)
                        historico_normalizado.append({
                            "link": item.strip(),
                            "arquivo": "legado.md"
                        })
                return historico_normalizado
    except (json.JSONDecodeError, IOError) as e:
        print(f"[History] Aviso: Erro ao ler o histórico ({e}). Iniciando histórico vazio.")

    return []


def salvar_historico(historico):
    """Salva a lista estruturada de histórico de forma atômica."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    temp_file = f"{HISTORY_FILE}.tmp"

    try:
        # Garante unicidade com base no link original
        vistos = set()
        dados_unicos = []
        for entry in historico:
            if isinstance(entry, dict) and "link" in entry:
                link = entry["link"]
                if link not in vistos:
                    vistos.add(link)
                    # Padroniza a estrutura do dicionário
                    dados_unicos.append({
                        "link": link,
                        "arquivo": entry.get("arquivo", "desconhecido.md")
                    })

        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(dados_unicos, f, ensure_ascii=False, indent=4)

        os.replace(temp_file, HISTORY_FILE)

    except IOError as e:
        print(f"[History] Erro crítico ao salvar o arquivo de histórico: {e}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass
