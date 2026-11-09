"""Módulo centralizado de filtros, blaclist e regras para remoção

de ruídos, rodapés de syndication e chamadas promocionais em feeds RSS.
"""

import re

# Frases exatas injetadas por templates de feeds que devem ser descartadas
BLACKLIST_EXACT_PHRASES = [
    "{{WHATSAPP_CHANNEL}}",
    "Veja as melhores promoções de hoje no WhatsApp do CT Ofertas",
    "Confira as melhores ofertas de hoje",
]

# Expressões regulares para remoção de rodapés, promoções e resíduos de syndication
BLACKLIST_REGEX_PATTERNS = [
    # 1. Chamadas de canais de ofertas (WhatsApp, Telegram, redes sociais)
    re.compile(r"^\s*\*\s*Veja as melhores promoções.*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*📱\s*Veja as melhores promoções.*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*🔥\s*Entre no canal de ofertas.*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*👉\s*\[?Ler artigo completo.*$", re.IGNORECASE | re.MULTILINE),

    # 2. Syndication de rodapé ("O post X apareceu primeiro em Y." ou trechos cortados)
    re.compile(r"O post\s+.+?\s+apareceu primeiro em\s+.+?(\.|$)", re.IGNORECASE),
    re.compile(r"A matéria\s+.+?\s+apareceu primeiro em\s+.+?(\.|$)", re.IGNORECASE),
    re.compile(r".*apareceu primeiro em.*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"O post\s+.*?\s+em\s*$", re.IGNORECASE | re.MULTILINE),

    # 3. Marcadores de resumos truncados e colchetes vazios (ex: "[...]")
    re.compile(r"\[\s*\.\.\.\s*\]", re.IGNORECASE),
    re.compile(r"\[\s*leia mais\s*\]", re.IGNORECASE),

    # 4. Direitos autorais e avisos institucionais de rodapé
    re.compile(r"^©.*todos os direitos reservados.*$", re.IGNORECASE | re.MULTILINE),

    # 5. Botões de compartilhamento ou chamadas soltas de rodapé
    re.compile(r"^\s*(compartilhe|leia mais|siga-nos|inscreva-se|veja também).*$", re.IGNORECASE | re.MULTILINE),
]


def limpar_texto_com_filtros(texto: str) -> str:
    """Aplica blacklist e padrões regex mantendo a estrutura de quebras de linha

    do Markdown intacta, sem colapsar listas ou parágrafos.
    """
    if not texto:
        return ""

    texto_filtrado = texto

    # Remove frases exatas da blacklist
    for frase in BLACKLIST_EXACT_PHRASES:
        if frase in texto_filtrado:
            texto_filtrado = texto_filtrado.replace(frase, "")

    # Aplica os padrões Regex linha a linha ou globalmente conforme o escopo
    for pattern in BLACKLIST_REGEX_PATTERNS:
        texto_filtrado = pattern.sub("", texto_filtrado)

    # Normaliza múltiplos espaços internos dentro de cada linha SEM destruir as quebras de linha (\n)
    linhas = texto_filtrado.splitlines()
    linhas_limpas = [re.sub(r"[ \t]+", " ", linha).strip() for linha in linhas]

    return "\n".join(linhas_limpas).strip()
