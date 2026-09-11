import logging
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import config

log = logging.getLogger("checker")


def _check_one(channel):
    req = urllib.request.Request(channel.url, headers={"User-Agent": config.USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=config.CHECK_TIMEOUT_CONNECT) as resp:
            if resp.status and resp.status >= 400:
                return channel, False
            data = resp.read(config.MIN_BYTES_FOR_ALIVE)
            return channel, len(data) > 0
    except Exception:
        return channel, False


def check_channels(channels, progress_cb=None):
    """Concurrently check which channels are actually alive right now.
    Returns list of channels that responded successfully."""
    working = []
    total = len(channels)
    done = 0
    with ThreadPoolExecutor(max_workers=config.CHECK_CONCURRENCY) as pool:
        futures = {pool.submit(_check_one, ch): ch for ch in channels}
        for fut in as_completed(futures):
            done += 1
            try:
                ch, ok = fut.result()
                if ok:
                    working.append(ch)
            except Exception:
                pass
            if progress_cb and done % 50 == 0:
                progress_cb(done, total, len(working))
    log.info("Checked %d channels, %d working", total, len(working))
    return working
