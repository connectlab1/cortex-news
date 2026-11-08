"""Módulo centralizado de filtros e regras para limpeza de ruídos em feeds RSS.

Contém padrões conhecidos de templates, marcadores e avisos de syndication,
garantindo que o conteúdo útil nunca seja afetado por falsos positivos.
"""

import re

# Frases exatas injetadas por templates de feeds que devem ser descartadas ou limpas
BLACKLIST_EXACT_PHRASES = [
    "{{WHATSAPP_CHANNEL}}",
    "Veja as melhores promoções de hoje no WhatsApp do CT Ofertas",
]

# Expressões regulares restritas a rodapés de syndication, links promocionais e avisos isolados
BLACKLIST_REGEX_PATTERNS = [
    # Remove avisos padrão de syndication (ex: "O post X apareceu primeiro em Y.")
    re.compile(r"^O post\s+.+?\s+apareceu primeiro em\s+.+?(\.|$)", re.IGNORECASE | re.MULTILINE),
    # Remove chamadas promocionais isoladas que começam com emoji no início de linha
    re.compile(r"^\s*📱\s*Veja as melhores promoções.*$", re.IGNORECASE | re.MULTILINE),
    # Remove avisos genéricos de direitos autorais de syndication no rodapé
    re.compile(r"^©.*todos os direitos reservados.*$", re.IGNORECASE | re.MULTILINE),
    # Remove chamadas genéricas de rodapé ou botões de compartilhamento
    re.compile(r"^\s*(compartilhe|leia mais|siga-nos|inscreva-se).*$", re.IGNORECASE | re.MULTILINE),
]


def limpar_texto_com_filtros(texto: str) -> str:
    """Aplica as regras de blacklist exata e padrões regex no texto,

    removendo ruídos conhecidos de syndication sem afetar o conteúdo útil.
    """
    if not texto:
        return ""

    texto_filtrado = texto

    # Remove frases exatas indesejadas
    for frase in BLACKLIST_EXACT_PHRASES:
        if frase in texto_filtrado:
            texto_filtrado = texto_filtrado.replace(frase, "")

    # Aplica padrões regex linha a linha / bloco a bloco
    for pattern in BLACKLIST_REGEX_PATTERNS:
        texto_filtrado = pattern.sub("", texto_filtrado)

    # Normaliza espaços excedentes que possam ter ficado após a remoção
    return re.sub(r"\s+", " ", texto_filtrado).strip()
