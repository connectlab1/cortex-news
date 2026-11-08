import os
from src.cleaner import limpar_e_tratar_dados
from src.config import DATA_DIR, POSTS_DIR
from src.generator import gerar_arquivo_jekyll
from src.history import carregar_historico, salvar_historico
from src.processor import filtrar_e_ordenar
from src.scraper import buscar_feeds


def garantir_diretorios():
  """Garante que os diretórios essenciais do projeto existam."""
  os.makedirs(DATA_DIR, exist_ok=True)
  os.makedirs(POSTS_DIR, exist_ok=True)


def executar_pipeline():
  print("=" * 60)
  print("🚀 Iniciando Pipeline ETL: RSS para Jekyll")
  print("=" * 60)

  try:
    garantir_diretorios()

    # 1. Extração
    dados_brutos = buscar_feeds()
    if not dados_brutos:
      print("[Main] Nenhum dado coletado. Encerrando execução.")
      return

    # 2. Limpeza
    dados_limpos = limpar_e_tratar_dados(dados_brutos)

    # 3. Processamento e Filtro de Qualidade
    itens_aprovados = filtrar_e_ordenar(dados_limpos)
    if not itens_aprovados:
      print("[Main] Nenhum item novo atingiu os critérios de qualidade.")
      return

    # 4. Geração de Posts Jekyll
    print("[4/4] Gerando posts em Markdown para o Jekyll...")
    links_novos_processados = []

    for item in itens_aprovados:
      gerar_arquivo_jekyll(item)
      links_novos_processados.append(item["link"])

    # 5. Atualização do Histórico
    if links_novos_processados:
      historico_atual = carregar_historico()
      historico_atual.extend(links_novos_processados)
      salvar_historico(historico_atual)
      print(f"[Main] Histórico atualizado com {len(links_novos_processados)} novos itens.")

    print("=" * 60)
    print("✨ Pipeline concluído com sucesso!")
    print("=" * 60)

  except Exception as e:
    print(f"[Main] Erro crítico inesperado na execução do pipeline: {e}")
    raise


if __name__ == "__main__":
  executar_pipeline()
