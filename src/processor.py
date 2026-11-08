from src.config import MIN_PALAVRAS
from src.history import carregar_historico


def filtrar_e_ordenar(dados_limpos):
  """Filtra itens já processados pelo histórico, remove conteúdos

  excessivamente curtos com base no limite configurado em config.py
  e organiza a ordem cronológica para publicação.
  """
  print("[3/4] Processando itens, aplicando filtro de qualidade e histórico...")

  historico = set(carregar_historico())
  novos_itens = []
  contador_duplicados = 0
  contador_curtos = 0

  for item in dados_limpos:
    # Verifica se o link já foi processado anteriormente
    if item["link"] in historico:
      contador_duplicados += 1
      continue

    # Conta as palavras da descrição limpa
    total_palavras = len(item["descricao"].split())

    # Aplica o filtro de qualidade utilizando o parâmetro centralizado
    if total_palavras >= MIN_PALAVRAS:
      novos_itens.append(item)
    else:
      contador_curtos += 1
      print(
          f"[Processor] Ignorado (muito curto - {total_palavras} palavras):"
          f" {item['titulo']}"
      )

  # Ordena do mais antigo para o mais recente para a publicação sequencial no Jekyll
  novos_itens.sort(key=lambda x: x["data_obj"])

  print(
      f"[Processor] Resumo: {len(novos_itens)} aprovados |"
      f" {contador_duplicados} já no histórico | {contador_curtos}"
      f" descartados por tamanho."
  )
  return novos_itens
