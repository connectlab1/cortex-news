"""Módulo centralizado e abrangente de termos técnicos, marcas, acrônimos

e padrões tipográficos para correção automática na limpeza de textos.
"""

import re

# Dicionário expandido: Padrão regex de termos incorretos/separados -> Forma correta unificada
DICIONARIO_TERMOS = {
    # ── Ecossistema Apple ──────────────────────────────────────────
    r"\bi\s+Phone\b": "iPhone",
    r"\bi\s+Pad\b": "iPad",
    r"\bi\s+Mac\b": "iMac",
    r"\bi\s+OS\b": "iOS",
    r"\bMac\s+OS\b": "macOS",
    r"\bWatch\s+OS\b": "watchOS",
    r"\bAir\s+Pods\b": "AirPods",
    r"\bAir\s+Tag\b": "AirTag",
    r"\bMac\s+Book\b": "MacBook",

    # ── Marcas de Varejo, E-commerce e Eletrônicos ──────────────────
    r"\bKa\s*Bu\s*M\s*!\b": "KaBuM!",
    r"\bKa\s*Bu\s*M\b": "KaBuM",
    r"\bMercado\s+Livre\b": "Mercado Livre",  # Mantém correto, evita quebras
    r"\bWhats\s+App\b": "WhatsApp",
    r"\bYou\s+Tube\b": "YouTube",
    r"\bBlue\s+tooth\b": "Bluetooth",
    r"\bWi\s+Fi\b": "Wi-Fi",
    r"\bi\s+Robot\b": "iRobot",

    # ── Termos Técnicos, Hardware e Unidades de Medida ──────────────
    r"\bLi\s+DAR\b": "LiDAR",
    r"\bo\s+LED\b": "OLED",
    r"\bm\s+Ah\b": "mAh",
    r"\bGb\s+ps\b": "Gbps",
    r"\bMb\s+ps\b": "Mbps",
    r"\bWi\s+Fi\s+6\b": "Wi-Fi 6",
    r"\bWi\s+Fi\s+7\b": "Wi-Fi 7",
    r"\bUSB\s+C\b": "USB-C",
    r"\bRay\s+Tracing\b": "Ray Tracing",
}


def aplicar_dicionario_termos(texto: str) -> str:
    """Aplica o dicionário de substituições tipográficas e correção de marcas

    no texto processado, preservando a legibilidade e o formato original.
    """
    if not texto:
        return ""

    texto_corrigido = texto
    for pattern, repl in DICIONARIO_TERMOS.items():
        texto_corrigido = re.sub(pattern, repl, texto_corrigido, flags=re.IGNORECASE)

    return texto_corrigido
