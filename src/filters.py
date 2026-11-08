"""Módulo centralizado de filtros e regras para limpeza de ruídos em feeds RSS.

Contém padrões conhecidos de templates, marcadores e avisos de syndication,
garantindo que o conteúdo útil nunca seja afetado por falsos positivos.
"""

# Frases exatas injetadas por templates de feeds que devem ser descartadas por completo
BLACKLIST_EXACT_PHRASES = [
    "{{WHATSAPP_CHANNEL}}",
    "Veja as melhores promoções de hoje no WhatsApp do CT Ofertas",
]

# Expressões regulares restritas apenas a rodapés de syndication e links promocionais isolados
# (Projetadas com âncoras de início/fim de linha para não engolir frases comuns do texto principal)
BLACKLIST_REGEX_PATTERNS = [
    # Remove avisos padrão do WordPress de syndication (ex: "O post X apareceu primeiro em Y.")
    r"^O post\s+.+?\s+apareceu primeiro em\s+.+?(\.|$)",
    # Remove chamadas promocionais isoladas que começam com emoji de celular no início de linha
    r"^\s*📱\s*Veja as melhores promoções.*$",
]
