import os

# Diretórios Base do Projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
POSTS_DIR = os.path.join(BASE_DIR, "_posts")
HISTORY_FILE = os.path.join(DATA_DIR, "historico.json")

# Configurações de Rede e Scraper
REQUEST_TIMEOUT = 10
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " CachyOS RSS Bot/1.0"
    )
}

# Feeds RSS monitorados
RSS_FEEDS = {
    "Canaltech": "https://canaltech.com.br/rss/",
    "Olhar Digital": "https://olhardigital.com.br/feed/",
}

# Critérios de Qualidade
MIN_PALAVRAS = 40
MAX_SLUG_LENGTH = 40
