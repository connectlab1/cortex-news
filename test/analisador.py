#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script avançado para análise sintática (AST), métricas de código e busca

de palavras-chave em scripts Python (Cortex News 2).
Integrado à suíte de testes em test/.
"""

import ast
from dataclasses import dataclass, field
from pathlib import Path

# Diretórios padrão do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

# Palavras-chave padrão para busca rápida de segurança/qualidade
TERMOS_PADRAO = [
    "requests",
    "feedparser",
    "html2text",
    "re.sub",
    "datetime",
    "try",
    "except",
    "TODO",
    "FIXME",
]


@dataclass
class MetricasCodigo:
  """Estrutura de dados para armazenar as métricas extraídas via AST."""

  importacoes: list[str] = field(default_factory=list)
  funcoes: list[tuple[str, int]] = field(default_factory=list)
  classes: list[tuple[str, int]] = field(default_factory=list)
  blocos_try: int = 0
  if_count: int = 0


class AnalisadorASTVisitor(ast.NodeVisitor):
  """Visitor especializado em percorrer a árvore sintática (AST) para recolha de métricas."""

  def __init__(self):
    self.metricas = MetricasCodigo()

  def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
    self.metricas.funcoes.append((node.name, node.lineno))
    self.generic_visit(node)

  def visit_ClassDef(self, node: ast.ClassDef) -> None:
    self.metricas.classes.append((node.name, node.lineno))
    self.generic_visit(node)

  def visit_Import(self, node: ast.Import) -> None:
    for alias in node.names:
      self.metricas.importacoes.append(alias.name)
    self.generic_visit(node)

  def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
    modulo = node.module or ""
    for alias in node.names:
      self.metricas.importacoes.append(f"{modulo}.{alias.name}")
    self.generic_visit(node)

  def visit_Try(self, node: ast.Try) -> None:
    self.metricas.blocos_try += 1
    self.generic_visit(node)

  def visit_If(self, node: ast.If) -> None:
    self.metricas.if_count += 1
    self.generic_visit(node)


def extrair_metricas_ast(conteudo: str, caminho_arquivo: Path) -> MetricasCodigo | None:
  """Analisa o código fonte e devolve as métricas estruturadas via AST."""
  try:
    arvore = ast.parse(conteudo, filename=str(caminho_arquivo))
    visitor = AnalisadorASTVisitor()
    visitor.visit(arvore)
    return visitor.metricas
  except SyntaxError as e:
    print(f"  ❌ Erro de sintaxe (AST) em {caminho_arquivo.name}: {e}")
    return None


def varrer_palavras_chave(linhas: list[str], termos: list[str]) -> list[tuple[int, str, str]]:
  """Varre as linhas do código à procura de termos-chave específicos."""
  encontrados = []
  for num_linha, linha in enumerate(linhas, 1):
    for termo in termos:
      if termo.lower() in linha.lower():
        encontrados.append((num_linha, termo, linha.strip()))
  return encontrados


def analisar_arquivo_profundo(caminho_arquivo: Path, termos: list[str] | None = None) -> None:
  """Coordena a análise profunda (AST + Termos) de um ficheiro Python individual."""
  if termos is None:
    termos = TERMOS_PADRAO

  relativo = caminho_arquivo.relative_to(BASE_DIR)
  print(f"\n📄 [Analisador] Ficheiro: {relativo}")
  print("-" * 65)

  try:
    conteudo = caminho_arquivo.read_text(encoding="utf-8")
  except Exception as e:
    print(f"  ❌ Erro ao ler o ficheiro: {e}")
    return

  # 1. Análise AST
  metricas = extrair_metricas_ast(conteudo, caminho_arquivo)
  if metricas:
    nomes_funcoes = [nome for nome, _ in metricas.funcoes]
    print("  📊 Estrutura e Métricas (AST):")
    print(
        f"     • Importações ({len(metricas.importacoes)}):"
        f" {', '.join(metricas.importacoes[:6])}{'...' if len(metricas.importacoes) > 6 else ''}"
    )
    print(f"     • Funções ({len(metricas.funcoes)}): {', '.join(nomes_funcoes)}")
    print(f"     • Blocos Try/Except: {metricas.blocos_try}")
    print(f"     • Condicionais (If): {metricas.if_count}")

  # 2. Varredura por Termos
  encontrados = varrer_palavras_chave(conteudo.splitlines(), termos)
  print(f"\n  🔍 Termos Encontrados ({len(encontrados)}):")
  if encontrados:
    for num, termo, trecho in encontrados[:8]:
      print(f"     [L{num:03d}] ({termo}) -> {trecho[:60]}")
    if len(encontrados) > 8:
      print(f"     ... e mais {len(encontrados) - 8} ocorrências.")
  else:
    print("     Nenhum dos termos pesquisados foi encontrado.")


def executar_analise_completa(diretorio: Path = SRC_DIR) -> None:
  """Varre todos os ficheiros .py do diretório alvo e exibe o relatório global."""
  print(f"🚀 Iniciando Análise Profunda de Código Python em: {diretorio}\n")

  if not diretorio.exists():
    print(f"❌ Diretório '{diretorio}' não encontrado.")
    return

  arquivos_py = sorted(list(diretorio.glob("**/*.py")))
  analisados = 0

  for arq in arquivos_py:
    if arq.name.startswith("__"):
      continue
    analisar_arquivo_profundo(arq)
    analisados += 1

  print("\n" + "=" * 65)
  print(f"✨ Análise concluída. Total de ficheiros analisados: {analisados}")


if __name__ == "__main__":
  executar_analise_completa()
