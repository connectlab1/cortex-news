"""Módulo centralizado de regras de formatação, contrato de estrutura e

validação de qualidade para os posts gerados para o Jekyll.
"""

from dataclasses import dataclass
from .config import CATEGORIAS_PADRAO, LAYOUT_OBRIGATORIO, MAX_SLUG_LENGTH, MIN_PALAVRAS


@dataclass
class RegrasPost:
    """Contrato de regras e validações que definem a estrutura de um post."""
    min_palavras: int = MIN_PALAVRAS
    max_slug_length: int = MAX_SLUG_LENGTH
    layout_obrigatorio: str = LAYOUT_OBRIGATORIO
    categorias_padrao: str = CATEGORIAS_PADRAO


def validar_regras_post(titulo: str, descricao: str, link: str) -> tuple[bool, str]:
    """Valida se um post atende rigorosamente a todas as regras de negócio

    estabelecidas pelo pipeline ETL antes de sua persistência em _posts/.
    """
    if not titulo or not titulo.strip():
        return False, "Título inválido ou ausente."

    if not link or not link.startswith(("http://", "https://")):
        return False, "Link de origem inválido ou ausente."

    if not descricao or not descricao.strip():
        return False, "Descrição/Conteúdo do post vazio."

    # Validação do limite mínimo de palavras
    palavras = descricao.split()
    total_palavras = len(palavras)
    if total_palavras < RegrasPost.min_palavras:
        return False, f"Abaixo do limite mínimo de palavras ({total_palavras}/{RegrasPost.min_palavras})."

    return True, "Post aprovado pelas regras de qualidade."


def montar_front_matter(titulo: str, data_iso: str, portal: str, link: str) -> str:
    """Gera o bloco estruturado de Front Matter padrão do Jekyll,

    garantindo o escape correto de aspas e formatação de categorias.
    """
    titulo_escapado = titulo.replace('"', '\\"')
    categoria_limpa = portal.strip() if portal else RegrasPost.categorias_padrao

    return f"""---
layout: {RegrasPost.layout_obrigatorio}
title: "{titulo_escapado}"
date: {data_iso}
categories: [{categoria_limpa}]
link: "{link}"
---
"""
