"""Módulo de testes unitários automatizados com pytest para o src/rules.py."""

import pytest
from src.rules import (
    RegrasPost,
    validar_regras_post,
    montar_front_matter,
)


class TestRegrasPost:
  """Testes para a classe de contrato RegrasPost."""

  def test_constantes_padrao(self):
    """Verifica se os valores padrão do contrato estão definidos."""
    assert RegrasPost.min_palavras > 0
    assert RegrasPost.layout_obrigatorio == "post"


class TestValidarRegrasPost:
  """Testes para o validador completo de posts da pipeline."""

  def test_post_valido(self):
    """Valida um post completo que cumpre todos os critérios exigidos."""
    titulo = "Artigo Exemplo sobre Tecnologia"
    # Conteúdo suficiente para atingir o mínimo (ex: 150 palavras)
    conteudo = (
        "Esta é uma descrição detalhada com conteúdo suficiente para passar nos"
        " testes. "
        * 30
    )
    link = "https://exemplo.com/artigo-tecnologia"

    valido, msg = validar_regras_post(titulo, conteudo, link)
    assert valido is True

  def test_post_sem_titulo(self):
    """Rejeita post com título vazio ou ausente."""
    valido, msg = validar_regras_post(
        "",
        "Conteúdo longo o suficiente para passar no teste de contagem de"
        " palavras "
        * 30,
        "https://exemplo.com",
    )
    assert valido is False
    assert "título" in msg.lower()

  def test_post_link_invalido(self):
    """Rejeita post sem URL HTTP válida."""
    valido, msg = validar_regras_post(
        "Título Válido",
        "Conteúdo longo o suficiente para passar no teste de contagem de"
        " palavras "
        * 30,
        "link-invalido",
    )
    assert valido is False
    assert "link" in msg.lower() or "url" in msg.lower()

  def test_post_descricao_vazia(self):
    """Rejeita post com descrição vazia."""
    valido, msg = validar_regras_post("Título Válido", "", "https://exemplo.com")
    assert valido is False
    assert "descrição" in msg.lower() or "vazio" in msg.lower()

  def test_post_abaixo_minimo_palavras(self):
    """Rejeita post com menos palavras que o mínimo exigido."""
    valido, msg = validar_regras_post(
        "Título Válido", "Poucas palavras.", "https://exemplo.com"
    )
    assert valido is False
    assert "mínimo" in msg.lower() or "palavras" in msg.lower()


class TestMontarFrontMatter:
  """Testes para a montagem do Front Matter Jekyll."""

  def test_montar_front_matter_jekyll(self):
    """Garante a estrutura correta do cabeçalho YAML para o Jekyll."""
    titulo = 'Notícia com "Aspas" de Última Hora'
    data_iso = "2026-03-08 14:00:00 +0000"
    portal = "Tecnoblog"
    link = "https://exemplo.com/noticia"

    fm = montar_front_matter(titulo, data_iso, portal, link)

    assert "---" in fm
    assert "layout: post" in fm
    assert 'title: "Notícia com \\"Aspas\\" de Última Hora"' in fm
    assert f"date: {data_iso}" in fm
    assert f"categories: [{portal}]" in fm
    assert f'link: "{link}"' in fm
