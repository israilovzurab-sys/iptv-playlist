import gzip
import logging
import urllib.request
import xml.etree.ElementTree as ET

import config
import sources

log = logging.getLogger("epg_builder")


def _pull_from_source(url, ids_lower, seen_channel_ids, out):
    req = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
    kept_channels = 0
    kept_programmes = 0
    with urllib.request.urlopen(req, timeout=60) as resp:
        fileobj = resp
        if url.endswith(".gz"):
            fileobj = gzip.GzipFile(fileobj=resp)
        context = ET.iterparse(fileobj, events=("end",))
        for event, elem in context:
            if elem.tag == "channel":
                cid = (elem.get("id") or "").split("@")[0].lower()
                if cid in ids_lower and cid not in seen_channel_ids:
                    out.write(ET.tostring(elem, encoding="unicode"))
                    seen_channel_ids.add(cid)
                    kept_channels += 1
                elem.clear()
            elif elem.tag == "programme":
                cid = (elem.get("channel") or "").split("@")[0].lower()
                if cid in ids_lower:
                    out.write(ET.tostring(elem, encoding="unicode"))
                    kept_programmes += 1
                elem.clear()
    return kept_channels, kept_programmes


def build_epg(tvg_ids: set, output_path: str):
    if not tvg_ids:
        log.warning("No tvg-ids to match against, skipping EPG build")
        return False

    ids_lower = {i.split("@")[0].lower() for i in tvg_ids if i}
    seen_channel_ids = set()
    total_channels = 0
    total_programmes = 0
    any_source_ok = False

    with open(output_path, "w", encoding="utf-8") as out:
        out.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="posuti-iptv-cloud">\n')
        for url in sources.EPG_SOURCES:
            try:
                ch, pr = _pull_from_source(url, ids_lower, seen_channel_ids, out)
                total_channels += ch
                total_programmes += pr
                any_source_ok = True
                log.info("EPG source OK %s: +%d channels, +%d programmes", url, ch, pr)
            except Exception as e:
                log.warning("EPG source unreachable, skipping: %s (%s)", url, e)
        out.write("</tv>\n")

    log.info("EPG build total: %d channels, %d programmes matched", total_channels, total_programmes)
    return any_source_ok and total_channels > 0
