"""Módulo de testes unitários automatizados com pytest para o src/cleaner.py."""

from datetime import datetime, timezone
import pytest
from src.cleaner import limpar_e_tratar_dados, limpar_html


class TestLimparHtml:
  """Testes unitários focados na função limpar_html."""

  def test_limpar_html_vazio_ou_nulo(self):
    """Garante que entradas vazias ou None retornam string vazia."""
    assert limpar_html("") == ""
    assert limpar_html(None) == ""

  def test_descodificar_entidades_html(self):
    """Verifica a conversão de entidades HTML comuns (ex: &amp;, &nbsp;, &quot;)."""
    html_input = (
        "<p>Texto &amp; Exemplo com&nbsp;espaço e &quot;aspas&quot;.</p>"
    )
    resultado = limpar_html(html_input)
    assert "Texto & Exemplo" in resultado
    assert '"aspas"' in resultado

  def test_conversao_html_para_markdown(self):
    """Verifica se tags HTML básicas são convertidas para sintaxe Markdown."""
    html_input = (
        "<h1>Título</h1><p>Parágrafo com <strong>negrito</strong> e"
        " <em>itálico</em>.</p>"
    )
    resultado = limpar_html(html_input)
    assert "# Título" in resultado
    assert "**negrito**" in resultado
    assert "_itálico_" in resultado

  def test_preservacao_de_links(self):
    """Garante que hiperligações em HTML são mantidas no Markdown resultante."""
    html_input = (
        '<p>Acesse o <a href="https://tecnoblog.net">Tecnoblog</a> para mais'
        " notícias.</p>"
    )
    resultado = limpar_html(html_input)
    assert "[Tecnoblog](https://tecnoblog.net)" in resultado

  def test_remocao_de_links_vazios(self):
    """Verifica a remoção de colchetes vazios ou marcações de link sem texto."""
    html_input = (
        '<p>Texto com link vazio <a href="https://exemplo.com"> </a> aqui.</p>'
    )
    resultado = limpar_html(html_input)
    assert "[](" not in resultado

  def test_aplicacao_dicionario_e_filtros(self):
    """Testa se as regras do dicionário de termos e filtros de syndication são aplicadas."""
    html_input = "<p>Confira o novo i Phone 15 e a tela o LED no KaBu M!.</p>"
    resultado = limpar_html(html_input)
    assert "iPhone" in resultado
    assert "OLED" in resultado
    assert "KaBuM!" in resultado

  def test_normalizacao_espacamento_pontuacao(self):
    """Verifica a remoção de espaços desnecessários antes de pontuações."""
    html_input = "<p>Primeira palavra , segunda palavra . Fim !</p>"
    resultado = limpar_html(html_input)
    assert "palavra, segunda" in resultado
    assert "palavra. Fim!" in resultado


class TestLimparETratarDados:
  """Testes unitários focados na função limpar_e_tratar_dados."""

  def test_dados_brutos_vazios(self):
    """Garante retorno de lista vazia para entradas sem dados."""
    assert limpar_e_tratar_dados([]) == []
    assert limpar_e_tratar_dados(None) == []

  def test_filtragem_de_itens_invalidos(self):
    """Verifica se itens sem título ou sem link são descartados."""
    dados_brutos = [
        {"titulo": "", "link": "https://exemplo.com/1", "descricao": "Teste"},
        {"titulo": "Título Válido", "link": "", "descricao": "Teste"},
        {"item_invalido": True},
        "string_invalida",
    ]
    resultado = limpar_e_tratar_dados(dados_brutos)
    assert len(resultado) == 0

  def test_tratamento_e_padronizacao_de_dados_validos(self):
    """Testa o processamento completo de uma lista com artigos válidos."""
    dados_brutos = [{
        "portal": "Tecnoblog",
        "titulo": "<p>Novo i Phone 15</p>",
        "link": "https://tecnoblog.net/post-1",
        "descricao": "<p>Análise detalhada do novo smartphone.</p>",
        "data_str": "Sun, 08 Mar 2026 12:00:00 +0000",
    }]
    resultado = limpar_e_tratar_dados(dados_brutos)

    assert len(resultado) == 1
    item = resultado[0]
    assert item["portal"] == "Tecnoblog"
    assert item["titulo"] == "Novo iPhone 15"
    assert item["link"] == "https://tecnoblog.net/post-1"
    assert "Análise detalhada" in item["descricao"]
    assert isinstance(item["data_obj"], datetime)

  def test_fallback_data_utc_quando_invalida(self):
    """Garante que a data assume fallback UTC caso data_str seja inválida."""
    dados_brutos = [{
        "portal": "Canaltech",
        "titulo": "Notícia Importante sobre Wi Fi 6",
        "link": "https://canaltech.com.br/noticia-1",
        "descricao": "<p>Conteúdo da notícia...</p>",
        "data_str": "Data Invalida em Texto",
    }]
    resultado = limpar_e_tratar_dados(dados_brutos)

    assert len(resultado) == 1
    assert isinstance(resultado[0]["data_obj"], datetime)
    assert resultado[0]["data_obj"].tzinfo == timezone.utc
