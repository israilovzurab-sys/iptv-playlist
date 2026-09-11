"""One-shot pipeline run by GitHub Actions on a schedule.
Writes docs/playlist.m3u, docs/epg.xml, docs/status.json.
If the freshly built playlist doesn't pass validation, it does NOT touch the
existing docs/ files - the workflow then sees no git changes and skips the
commit, so the previous (last known good) version stays published on Pages.
"""
import os
import json
import logging
import datetime

import config
import playlist_builder
import checker
import epg_builder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("build")


def main():
    os.makedirs(config.DOCS_DIR, exist_ok=True)

    candidates = playlist_builder.collect_all_candidates()
    found_total = len(candidates)

    def progress(done, total, working):
        if done % 500 == 0:
            log.info("checked %d/%d, working so far: %d", done, total, working)

    working = checker.check_channels(candidates, progress_cb=progress)
    dead_total = found_total - len(working)

    working = playlist_builder.cap_total(working, config.MAX_TOTAL_CHANNELS)
    working_total = len(working)

    if working_total < config.MIN_ACCEPTABLE_TOTAL:
        log.error(
            "Only %d working channels (minimum %d) - aborting without touching "
            "published files, previous good version stays live.",
            working_total, config.MIN_ACCEPTABLE_TOTAL,
        )
        return 1

    epg_url = f"{config.PAGES_BASE_URL}/epg.xml"
    m3u_text = playlist_builder.render_m3u(working, epg_url)

    if not m3u_text.startswith("#EXTM3U") or m3u_text.count("#EXTINF") < config.MIN_ACCEPTABLE_TOTAL:
        log.error("Validation failed on freshly built playlist - aborting.")
        return 1

    with open(config.CURRENT_M3U, "w", encoding="utf-8") as f:
        f.write(m3u_text)

    tvg_ids = {ch.tvg_id for ch in working if ch.tvg_id}
    epg_ok = epg_builder.build_epg(tvg_ids, config.CURRENT_EPG)

    by_group = {}
    for ch in working:
        by_group[ch.group] = by_group.get(ch.group, 0) + 1

    status = {
        "last_update": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "found_total": found_total,
        "working_total": working_total,
        "dead_total": dead_total,
        "by_group": by_group,
        "epg_ok": epg_ok,
        "playlist_url": f"{config.PAGES_BASE_URL}/playlist.m3u",
        "epg_url": f"{config.PAGES_BASE_URL}/epg.xml",
    }
    with open(config.STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)

    log.info("Build OK: %d working / %d found, EPG ok=%s", working_total, found_total, epg_ok)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
