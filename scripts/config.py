import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

CURRENT_M3U = os.path.join(DOCS_DIR, "playlist.m3u")
CURRENT_EPG = os.path.join(DOCS_DIR, "epg.xml")
STATUS_FILE = os.path.join(DOCS_DIR, "status.json")

# filled in after the GitHub repo + Pages are created
PAGES_BASE_URL = "https://israilovzurab-sys.github.io/iptv-playlist"

CHECK_TIMEOUT_CONNECT = 5
CHECK_CONCURRENCY = 40
MIN_BYTES_FOR_ALIVE = 512

CANDIDATES_PER_WORLD_CATEGORY = 350
MIN_ACCEPTABLE_TOTAL = 400
MAX_TOTAL_CHANNELS = 1800

USER_AGENT = "Mozilla/5.0 (SMART-TV; Tizen 5.5) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/76.0.3809.146 TV Safari/537.36"
