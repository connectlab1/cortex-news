from datetime import datetime
import html
import re
from email.utils import parsedate_to_datetime
import html2text
from .filters import BLACKLIST_EXACT_PHRASES, BLACKLIST_REGEX_PATTERNS


def limpar_html(texto_html):
  """Converte o HTML do RSS para Markdown limpo, aplicando os filtros

  centralizados e realizando correções tipográficas e de espaçamento.
  """
  if not texto_html:
    return ""

  # Decodifica entidades HTML
  texto_decodificado = html.unescape(texto_html)

  # Configura o conversor de HTML para Markdown
  h = html2text.HTML2Text()
  h.ignore_links = True
  h.ignore_images = True
  h.body_width = 0

  markdown = h.handle(texto_decodificado)

  # 1. Filtra linhas contendo frases exatas indesejadas
  linhas = markdown.splitlines()
  linhas_limpas = []
  for linha in linhas:
    if any(frase in linha for frase in BLACKLIST_EXACT_PHRASES):
      continue
    linhas_limpas.append(linha)

  texto_final = "\n".join(linhas_limpas)

  # 2. Aplica as Regex restritas definidas no módulo de filtros
  for pattern in BLACKLIST_REGEX_PATTERNS:
    texto_final = re.sub(pattern, "", texto_final, flags=re.IGNORECASE | re.DOTALL)

  # 3. Limpeza genérica de placeholders residuais (ex: chaves duplas)
  texto_final = re.sub(r"\{\{.*?\}\}", "", texto_final)

  # 4. Correção tipográfica: remove espaços entre aspas de abertura e formatações (ex: " _")
  texto_final = re.sub(r'([“"‘’])\s+([_*\w])', r'\1\2', texto_final)

  # 5. Ajuste tipográfico: remove espaços indevidos antes de pontuações e parênteses/aspas finais
  texto_final = re.sub(r"\s+([,\.\?!”\)])", r"\1", texto_final)

  # 6. Normaliza quebras de linha excessivas
  texto_final = re.sub(r"\n{3,}", "\n\n", texto_final)

  return texto_final.strip()


def limpar_e_tratar_dados(dados_brutos):
  """Recebe os dados brutos e executa a limpeza modularizada."""
  print("[2/4] Limpando e convertendo HTML com base no dicionário de filtros...")
  dados_limpos = []

  for item in dados_brutos:
    titulo = limpar_html(item.get("titulo", ""))
    descricao_md = limpar_html(item.get("descricao", ""))
    link = item.get("link", "").strip()
    portal = item.get("portal", "Desconhecido")
    data_str = item.get("data_str", "")

    try:
      # astimezone() garante objeto timezone-aware para evitar falhas no Front Matter (%z)
      data_obj = parsedate_to_datetime(data_str) if data_str else datetime.now().astimezone()
    except Exception:
      data_obj = datetime.now().astimezone()

    if titulo and link:
      dados_limpos.append({
          "portal": portal,
          "titulo": titulo,
          "link": link,
          "descricao": descricao_md,
          "data_obj": data_obj,
      })

  print(f"[Cleaner] {len(dados_limpos)} itens formatados e limpos com sucesso.")
  return dados_limpos
