"""Configuração global e fixture do Pytest para a suite de testes.

Garante que o diretório raiz e o diretório src estejam no sys.path
para permitir a importação direta de módulos em qualquer subdiretório de testes.
"""

from pathlib import Path
import sys

# Caminho absoluto para a raiz do projeto (cortex-news-2)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Adiciona a raiz e o diretório 'src' ao sys.path caso não estejam presentes
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
