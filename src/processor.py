from datetime import datetime, timezone
import re
import html
from src.config import MIN_PALAVRAS
from src.history import carregar_historico
from src.filters import limpar_texto_com_filtros


def _obter_timestamp(item):
    """Retorna um valor seguro de datetime em UTC para ordenação cronológica.

    Trata casos onde as datas possuem ou não fuso horário (naive vs. aware)
    para evitar erros de comparação durante o .sort().
    """
    dt = item.get("data_obj")
    if not isinstance(dt, datetime):
        return datetime.min.replace(tzinfo=timezone.utc)

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt


def _limpar_para_contagem(texto: str) -> str:
    """Remove tags HTML residuais, links e formatações Markdown estritamente

    para fins de métrica precisa de tamanho de texto.
    """
    if not texto:
        return ""

    texto_limpo = html.unescape(texto)
    texto_limpo = re.sub(r"<[^>]+>", " ", texto_limpo)
    texto_limpo = re.sub(r"\[([^\]]+)\]\([^)]+\)", "", texto_limpo)
    texto_limpo = re.sub(r"[*_~`#>]", " ", texto_limpo)
    texto_limpo = re.sub(r"https?://\S+", "", texto_limpo)
    return re.sub(r"\s+", " ", texto_limpo).strip()


def filtrar_e_ordenar(dados_limpos):
    """Filtra itens já processados pelo histórico, remove ruídos via filters.py,

    aplica filtro de tamanho mínimo rigoroso e organiza a ordem cronológica.
    """
    print("[3/4] Processando itens, aplicando filtros de ruído, qualidade e histórico...")

    if not dados_limpos:
        print("[Processor] Nenhum item recebido para processamento.")
        return []

    historico = set(carregar_historico() or [])
    links_vistos_no_lote = set()

    novos_itens = []
    contador_duplicados = 0
    contador_curtos = 0
    contador_invalidos = 0

    for item in dados_limpos:
        if not isinstance(item, dict):
            contador_invalidos += 1
            continue

        link = item.get("link", "").strip()
        titulo = item.get("titulo", "Sem Título").strip()
        descricao_bruta = item.get("descricao") or ""

        if not link:
            contador_invalidos += 1
            continue

        # 1. Filtro de duplicatas (histórico ou lote atual)
        if link in historico or link in links_vistos_no_lote:
            contador_duplicados += 1
            continue

        # 2. Aplica as regras de blacklist/ruídos centralizadas no módulo filters.py
        descricao_sem_ruido = limpar_texto_com_filtros(descricao_bruta)

        # Atualiza a descrição no item para que o gerador receba o conteúdo limpo
        item["descricao"] = descricao_sem_ruido

        # 3. Sanitização estrutural para contagem precisa de palavras
        descricao_para_contagem = _limpar_para_contagem(descricao_sem_ruido)
        total_palavras = len(descricao_para_contagem.split()) if descricao_para_contagem else 0

        # 4. Filtro de qualidade por tamanho mínimo
        if total_palavras >= MIN_PALAVRAS:
            novos_itens.append(item)
            links_vistos_no_lote.add(link)
        else:
            contador_curtos += 1
            portal = item.get("portal", "Desconhecido")
            print(
                f"[Processor] Ignorado ({portal} - muito curto: {total_palavras} palavras): "
                f"\"{titulo}\""
            )

    # 5. Ordenação cronológica segura
    novos_itens.sort(key=_obter_timestamp)

    print(
        f"[Processor] Resumo: {len(novos_itens)} aprovados | "
        f"{contador_duplicados} duplicados | {contador_curtos} curtos | "
        f"{contador_invalidos} inválidos."
    )
    return novos_itens
