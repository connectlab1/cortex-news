"""Módulo centralizado para gerenciamento, carregamento e salvamento atômico

do histórico de links processados, garantindo deduplicação e resiliência.
"""

from datetime import datetime
import json
import os
from .config import HISTORY_FILE


def carregar_historico():
    """Carrega a lista de links já processados a partir do arquivo JSON de histórico.

    Garante validação de tipo e sanitização dos itens para evitar a inclusão de
    dados corrompidos no conjunto de busca. Retorna uma lista vazia caso o
    arquivo não exista ou esteja corrompido.
    """
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                # Sanitiza e aceita apenas strings válidas e não vazias
                return [str(link).strip() for link in data if link and isinstance(link, str)]
    except (json.JSONDecodeError, IOError) as e:
        print(f"[History] Aviso: Erro ao ler o histórico ({e}). Iniciando histórico vazio.")

    return []


def salvar_historico(historico):
    """Salva a lista atualizada de links processados no arquivo JSON

    utilizando escrita atômica para prevenir a perda ou corrupção do arquivo
    em caso de interrupção abrupta da execução.
    """
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    # Define o caminho temporário para a gravação segura
    temp_file = f"{HISTORY_FILE}.tmp"

    try:
        # Deduplica, sanitiza e ordena os links antes da persistência
        dados_unicos = sorted(list(set(str(l).strip() for l in historico if l)))

        # Grava os dados primeiro no arquivo temporário
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(dados_unicos, f, ensure_ascii=False, indent=4)

        # Substituição atômica: o arquivo principal só é substituído se a gravação for concluída
        os.replace(temp_file, HISTORY_FILE)

    except IOError as e:
        print(f"[History] Erro crítico ao salvar o arquivo de histórico: {e}")
        # Limpa o arquivo temporário caso tenha ocorrido falha no meio do processo
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass
