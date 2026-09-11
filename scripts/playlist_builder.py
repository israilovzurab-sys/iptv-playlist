import re
import random
import logging
import urllib.request

import config
import sources

log = logging.getLogger("playlist_builder")

EXTINF_RE = re.compile(r'#EXTINF:(?P<duration>-?\d+)\s*(?P<attrs>.*?),(?P<name>.*)')
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')


class Channel:
    __slots__ = ("name", "url", "tvg_id", "tvg_logo", "category", "group", "extra_attrs")

    def __init__(self, name, url, tvg_id, tvg_logo, category, extra_attrs=None):
        self.name = name.strip()
        self.url = url.strip()
        self.tvg_id = tvg_id
        self.tvg_logo = tvg_logo
        self.category = category
        self.group = None
        self.extra_attrs = extra_attrs or {}


def fetch_text(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "ignore")


def parse_m3u(text):
    """Yield Channel objects from raw m3u text."""
    lines = text.splitlines()
    i = 0
    pending = None
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            m = EXTINF_RE.match(line)
            if m:
                attrs = dict(ATTR_RE.findall(m.group("attrs")))
                pending = {
                    "name": m.group("name").strip(),
                    "tvg_id": attrs.get("tvg-id", ""),
                    "tvg_logo": attrs.get("tvg-logo", ""),
                    "category": attrs.get("group-title", "Undefined"),
                }
        elif line.startswith("#EXTVLCOPT") or line.startswith("#EXT"):
            pass
        elif line and not line.startswith("#"):
            if pending:
                yield Channel(
                    pending["name"], line, pending["tvg_id"],
                    pending["tvg_logo"], pending["category"],
                )
                pending = None
        i += 1


def is_federal(name: str) -> bool:
    low = name.lower()
    return any(f.lower() in low for f in sources.FEDERAL_CHANNELS_RU)


def categorize_ru(ch: Channel):
    if is_federal(ch.name):
        return sources.GROUP_RU_FEDERAL
    return sources.RU_CATEGORY_MAP.get(ch.category, sources.GROUP_RU_OTHER)


def categorize_world(ch: Channel):
    return sources.WORLD_CATEGORY_MAP.get(ch.category, sources.GROUP_WORLD_OTHER)


def collect_ru_candidates():
    text = fetch_text(sources.RU_PLAYLIST_URL)
    channels = list(parse_m3u(text))
    for ch in channels:
        ch.group = categorize_ru(ch)
    log.info("RU source: %d channels", len(channels))
    return channels


def collect_world_candidates():
    text = fetch_text(sources.WORLD_CATEGORY_PLAYLIST_URL)
    all_world = list(parse_m3u(text))

    # exclude channels already tvg-id-flagged as .ru (avoid double counting with RU source)
    all_world = [c for c in all_world if not c.tvg_id.lower().endswith(".ru") and not c.tvg_id.lower().endswith(".ru@sd") and ".ru@" not in c.tvg_id.lower()]

    by_category = {}
    for ch in all_world:
        by_category.setdefault(ch.category, []).append(ch)

    selected = []
    for cat, chans in by_category.items():
        random.shuffle(chans)
        selected.extend(chans[: config.CANDIDATES_PER_WORLD_CATEGORY])

    for ch in selected:
        ch.group = categorize_world(ch)

    log.info("World source: %d categories, %d candidates selected out of %d total",
              len(by_category), len(selected), len(all_world))
    return selected


def dedupe(channels):
    seen_urls = set()
    seen_names_per_group = {}
    result = []
    for ch in channels:
        if ch.url in seen_urls:
            continue
        seen_urls.add(ch.url)
        key = (ch.group, ch.name.lower())
        if key in seen_names_per_group:
            continue
        seen_names_per_group[key] = True
        result.append(ch)
    return result


def cap_total(channels, max_total):
    """Keep every RU channel, trim the world pool evenly across its
    categories so the final list stays performant on a low-end TV."""
    ru = [c for c in channels if c.group.startswith("🇷🇺")]
    world = [c for c in channels if not c.group.startswith("🇷🇺")]

    budget = max_total - len(ru)
    if budget <= 0 or len(world) <= budget:
        return ru + world

    by_group = {}
    for c in world:
        by_group.setdefault(c.group, []).append(c)

    n_groups = len(by_group) or 1
    per_group = max(1, budget // n_groups)

    trimmed = []
    for chans in by_group.values():
        random.shuffle(chans)
        trimmed.extend(chans[:per_group])

    return ru + trimmed


def collect_all_candidates():
    ru = collect_ru_candidates()
    world = collect_world_candidates()
    combined = dedupe(ru + world)
    log.info("Total candidates after dedupe: %d", len(combined))
    return combined


GROUP_ORDER = [
    sources.GROUP_RU_FEDERAL, sources.GROUP_RU_NEWS, sources.GROUP_RU_SPORT,
    sources.GROUP_RU_MOVIES, sources.GROUP_RU_SERIES, sources.GROUP_RU_ENTERTAINMENT,
    sources.GROUP_RU_KIDS, sources.GROUP_RU_MUSIC, sources.GROUP_RU_DOC, sources.GROUP_RU_OTHER,
    sources.GROUP_WORLD_NEWS, sources.GROUP_WORLD_MOVIES, sources.GROUP_WORLD_SPORTS,
    sources.GROUP_WORLD_KIDS, sources.GROUP_WORLD_MUSIC, sources.GROUP_WORLD_DOC,
    sources.GROUP_WORLD_ENTERTAINMENT, sources.GROUP_WORLD_OTHER,
]


def render_m3u(channels, epg_url):
    lines = [f'#EXTM3U x-tvg-url="{epg_url}" url-tvg="{epg_url}"']
    channels_sorted = sorted(
        channels,
        key=lambda c: (GROUP_ORDER.index(c.group) if c.group in GROUP_ORDER else 999, c.name.lower()),
    )
    for ch in channels_sorted:
        tvg_id = ch.tvg_id or ""
        logo = f' tvg-logo="{ch.tvg_logo}"' if ch.tvg_logo else ""
        lines.append(
            f'#EXTINF:-1 tvg-id="{tvg_id}"{logo} group-title="{ch.group}",{ch.name}'
        )
        lines.append(ch.url)
    return "\n".join(lines) + "\n"
