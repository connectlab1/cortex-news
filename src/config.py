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

# Feeds RSS monitorados (Tecnologia em Português)
RSS_FEEDS = {
    "Canaltech": "https://canaltech.com.br/rss/",
    "Olhar Digital": "https://olhardigital.com.br/feed/",
    "Tecnoblog": "https://tecnoblog.net/feed/",
    "Adrenaline": "https://www.adrenaline.com.br/feed/",
    "Hardware.com.br": "https://www.hardware.com.br/feed/",
    "Manual do Usuário": "https://manualdousuario.net/feed/",
    "TudoCelular": "https://www.tudocelular.com/feed/",
}

# Critérios de Qualidade e Formatação de Slugs/URLs (Aumentado para barrar posts curtos/rasos)
MIN_PALAVRAS = 70
MAX_SLUG_LENGTH = 40
