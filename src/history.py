import json
import os
from src.config import HISTORY_FILE


def carregar_historico():
  """Carrega a lista de links já processados a partir do arquivo JSON de histórico.

  Retorna uma lista vazia caso o arquivo não exista ou esteja corrompido.
  """
  if not os.path.exists(HISTORY_FILE):
    return []

  try:
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
      if isinstance(data, list):
        return data
  except (json.JSONDecodeError, IOError) as e:
    print(f"[History] Aviso: Erro ao ler o histórico ({e}). Iniciando histórico vazio.")

  return []


def salvar_historico(historico):
  """Salva a lista atualizada de links processados no arquivo JSON,

  garantindo que o diretório de dados (data/) exista.
  """
  os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

  try:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
      json.dump(historico, f, ensure_ascii=False, indent=4)
  except IOError as e:
    print(f"[History] Erro crítico ao salvar o arquivo de histórico: {e}")
