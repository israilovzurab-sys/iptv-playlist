# Legal, publicly listed IPTV sources.
# iptv-org (https://github.com/iptv-org/iptv) aggregates only channels whose owners
# broadcast them as free, publicly accessible streams (official websites, YouTube-style
# public CDNs, etc.). We do not use any paid/pirated/leaked source.

RU_PLAYLIST_URL = "https://iptv-org.github.io/iptv/countries/ru.m3u"
WORLD_CATEGORY_PLAYLIST_URL = "https://iptv-org.github.io/iptv/index.category.m3u"

# supplemental country playlists merged into the "world" pool (kept small & relevant)
EXTRA_COUNTRY_PLAYLISTS = {
    "UA": "https://iptv-org.github.io/iptv/countries/ua.m3u",
    "US": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "DE": "https://iptv-org.github.io/iptv/countries/de.m3u",
    "FR": "https://iptv-org.github.io/iptv/countries/fr.m3u",
    "TR": "https://iptv-org.github.io/iptv/countries/tr.m3u",
}

# Multiple free public XMLTV sources - merged together. The first ones focus
# on Russian channels (our priority), the last is a huge worldwide guide used
# as a fallback for everything else. If a source is unreachable it is simply
# skipped - EPG is best-effort and must never block the playlist itself.
EPG_SOURCES = [
    "https://epg.one/ru.xml.gz",
    "https://iptvx.one/epg/epg.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_ALL_SOURCES1.xml.gz",
]

# Russian federal / most-watched channels we always try to pin at the top of
# "Федеральные", matched case-insensitively against the channel name from the source.
FEDERAL_CHANNELS_RU = [
    "Первый канал", "ОРТ", "Channel One",
    "Россия 1", "Russia 1", "РТР",
    "Россия 24", "Russia 24", "Вести 24",
    "НТВ", "NTV",
    "РЕН ТВ", "REN TV",
    "ТНТ", "TNT",
    "СТС", "STS",
    "ТВ3", "ТВ-3", "TV3",
    "Пятый канал", "5 канал", "Channel 5",
    "Звезда", "Zvezda",
    "Домашний", "Domashny",
    "Ю ТВ", "Yu TV",
    "Пятница", "Friday",
    "Мир", "Mir TV",
    "ОТР",
    "Культура", "Kultura", "Russia K",
    "Матч ТВ", "Match TV",
    "Победа", "Pobeda",
    "Муз ТВ", "Muz TV", "MuzTV",
]

# our own top-level group taxonomy
GROUP_RU_FEDERAL = "🇷🇺 Россия/Федеральные"
GROUP_RU_NEWS = "🇷🇺 Россия/Новости"
GROUP_RU_SPORT = "🇷🇺 Россия/Спорт"
GROUP_RU_MOVIES = "🇷🇺 Россия/Фильмы"
GROUP_RU_SERIES = "🇷🇺 Россия/Сериалы"
GROUP_RU_ENTERTAINMENT = "🇷🇺 Россия/Развлечения"
GROUP_RU_KIDS = "🇷🇺 Россия/Дети"
GROUP_RU_MUSIC = "🇷🇺 Россия/Музыка"
GROUP_RU_DOC = "🇷🇺 Россия/Познавательные"
GROUP_RU_OTHER = "🇷🇺 Россия/Региональные и другие"

GROUP_WORLD_NEWS = "🌍 Мир/News"
GROUP_WORLD_MOVIES = "🌍 Мир/Movies"
GROUP_WORLD_SPORTS = "🌍 Мир/Sports"
GROUP_WORLD_KIDS = "🌍 Мир/Kids"
GROUP_WORLD_MUSIC = "🌍 Мир/Music"
GROUP_WORLD_DOC = "🌍 Мир/Documentary"
GROUP_WORLD_ENTERTAINMENT = "🌍 Мир/Entertainment"
GROUP_WORLD_OTHER = "🌍 Мир/Other"

# iptv-org category (from group-title attr) -> our RU group
RU_CATEGORY_MAP = {
    "News": GROUP_RU_NEWS,
    "Sports": GROUP_RU_SPORT,
    "Movies": GROUP_RU_MOVIES,
    "Series": GROUP_RU_SERIES,
    "Kids": GROUP_RU_KIDS,
    "Animation": GROUP_RU_KIDS,
    "Music": GROUP_RU_MUSIC,
    "Documentary": GROUP_RU_DOC,
    "Science": GROUP_RU_DOC,
    "Education": GROUP_RU_DOC,
    "Culture": GROUP_RU_DOC,
    "Travel": GROUP_RU_DOC,
    "Cooking": GROUP_RU_DOC,
    "Auto": GROUP_RU_DOC,
    "Entertainment": GROUP_RU_ENTERTAINMENT,
    "Comedy": GROUP_RU_ENTERTAINMENT,
    "Family": GROUP_RU_ENTERTAINMENT,
    "Lifestyle": GROUP_RU_ENTERTAINMENT,
    "Relax": GROUP_RU_ENTERTAINMENT,
    "General": GROUP_RU_ENTERTAINMENT,
}

# iptv-org category -> our WORLD group
WORLD_CATEGORY_MAP = {
    "News": GROUP_WORLD_NEWS,
    "Weather": GROUP_WORLD_NEWS,
    "Movies": GROUP_WORLD_MOVIES,
    "Series": GROUP_WORLD_MOVIES,
    "Sports": GROUP_WORLD_SPORTS,
    "Kids": GROUP_WORLD_KIDS,
    "Animation": GROUP_WORLD_KIDS,
    "Family": GROUP_WORLD_KIDS,
    "Music": GROUP_WORLD_MUSIC,
    "Documentary": GROUP_WORLD_DOC,
    "Science": GROUP_WORLD_DOC,
    "Education": GROUP_WORLD_DOC,
    "Culture": GROUP_WORLD_DOC,
    "Travel": GROUP_WORLD_DOC,
    "Cooking": GROUP_WORLD_DOC,
    "Auto": GROUP_WORLD_DOC,
    "Entertainment": GROUP_WORLD_ENTERTAINMENT,
    "Comedy": GROUP_WORLD_ENTERTAINMENT,
    "Lifestyle": GROUP_WORLD_ENTERTAINMENT,
    "Relax": GROUP_WORLD_ENTERTAINMENT,
    "General": GROUP_WORLD_ENTERTAINMENT,
    "Public": GROUP_WORLD_ENTERTAINMENT,
    "Business": GROUP_WORLD_NEWS,
    "Legislative": GROUP_WORLD_NEWS,
    "Classic": GROUP_WORLD_MOVIES,
    "Religious": GROUP_WORLD_DOC,
    "Outdoor": GROUP_WORLD_DOC,
}
