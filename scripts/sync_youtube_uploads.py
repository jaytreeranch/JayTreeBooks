#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.js"
INDEX_PATH = ROOT / "index.html"
REGISTRY_PATH = ROOT / "data" / "youtube-sync.json"
CHANNEL_HANDLE = "@JayTreeBooks"
CHANNEL_URL = f"https://www.youtube.com/{CHANNEL_HANDLE}"
FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
WATCH_URL = "https://www.youtube.com/watch?v={video_id}"
USER_AGENT = "Mozilla/5.0 (compatible; JayTreeBooksYouTubeSync/2.0; +https://www.JayTreeBooks.com)"

BOOKS = {
    "second-draft": "Second Draft",
    "the-hollow-year": "The Hollow Year",
    "the-hollow-bell": "The Hollow Bell",
    "the-absconding": "The Absconding",
    "the-correction": "The Correction",
}
BOOK_EXCLUDE_TERMS = ("short", "teaser", "audiobook", "chapter", "reading", "read aloud", "first chapter", "reel")
ATOM = "http://www.w3.org/2005/Atom"
YT = "http://www.youtube.com/xml/schemas/2015"


def _fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def _resolve_channel_id() -> str:
    page = _fetch_text(CHANNEL_URL)
    for pattern in (
        r'"channelId":"(UC[A-Za-z0-9_-]+)"',
        r'"externalId":"(UC[A-Za-z0-9_-]+)"',
        r'https://www\.youtube\.com/channel/(UC[A-Za-z0-9_-]+)',
    ):
        match = re.search(pattern, page)
        if match:
            return match.group(1)
    raise SystemExit(f"Could not resolve YouTube channel ID for {CHANNEL_HANDLE}")


def _feed_entries(channel_id: str) -> list[dict]:
    root = ET.fromstring(_fetch_text(FEED_URL.format(channel_id=channel_id)))
    entries = []
    for entry in root.findall(f"{{{ATOM}}}entry"):
        video_id = (entry.findtext(f"{{{YT}}}videoId") or "").strip()
        title = (entry.findtext(f"{{{ATOM}}}title") or "").strip()
        published = (entry.findtext(f"{{{ATOM}}}published") or "").strip()
        if video_id and title and published:
            entries.append({
                "video_id": video_id,
                "title": title,
                "url": WATCH_URL.format(video_id=video_id),
                "published": published,
            })
    return entries


def _duration_seconds(video_id: str) -> int:
    try:
        page = _fetch_text(WATCH_URL.format(video_id=video_id))
        match = re.search(r'"lengthSeconds":"(\d+)"', page)
        return int(match.group(1)) if match else 0
    except Exception:
        return 0


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _load_registry(channel_id: str) -> dict:
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else {}
    data["schema_version"] = 2
    data["channel_handle"] = CHANNEL_HANDLE
    data["channel_id"] = channel_id
    data.setdefault("sync_started_at", datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"))
    data.setdefault("books", {})
    data.setdefault("mystery_cases", {})
    return data


def _is_after_cutoff(entry: dict, registry: dict) -> bool:
    try:
        return _parse_time(entry["published"]) >= _parse_time(registry["sync_started_at"])
    except Exception:
        return False


def _is_book_feature(entry: dict, book_title: str) -> bool:
    lowered = entry["title"].casefold()
    if book_title.casefold() not in lowered or any(term in lowered for term in BOOK_EXCLUDE_TERMS):
        return False
    duration = _duration_seconds(entry["video_id"])
    return duration >= 90 or any(term in lowered for term in ("cinematic", "official trailer", "long feature", "book trailer"))


def _case_number(title: str) -> str | None:
    match = re.search(r"\bcase(?:\s+file)?\s*#?\s*0*(\d+)\b", title, flags=re.I)
    return f"{int(match.group(1)):03d}" if match else None


def _update_registry(registry: dict, entries: list[dict]) -> bool:
    before = json.dumps(registry, sort_keys=True, ensure_ascii=False)
    eligible = [entry for entry in entries if _is_after_cutoff(entry, registry)]
    if eligible:
        registry["latest_upload"] = eligible[0]

    books = registry.setdefault("books", {})
    cases = registry.setdefault("mystery_cases", {})

    for entry in reversed(eligible):
        title = entry["title"]
        lowered = title.casefold()
        for slug, book_title in BOOKS.items():
            if _is_book_feature(entry, book_title):
                entry_with_duration = dict(entry)
                entry_with_duration["duration_seconds"] = _duration_seconds(entry["video_id"])
                books[slug] = entry_with_duration

        number = _case_number(title)
        if not number:
            continue
        record = cases.setdefault(number, {})
        duration = _duration_seconds(entry["video_id"])
        entry_with_duration = dict(entry)
        entry_with_duration["duration_seconds"] = duration
        if "reveal" in lowered or "solution" in lowered or "solved" in lowered:
            if duration >= 90 or "reveal" in lowered:
                record["reveal"] = entry_with_duration
        elif "teaser" in lowered or "short" in lowered or duration < 120:
            record["teaser"] = entry_with_duration
        elif duration >= 180 or "full case" in lowered or "can you solve it" in lowered:
            record["case"] = entry_with_duration

    latest_number = None
    latest_stamp = ""
    for number, record in cases.items():
        stamp = max([str((record.get(kind) or {}).get("published") or "") for kind in ("case", "reveal", "teaser")] or [""])
        if stamp > latest_stamp:
            latest_stamp = stamp
            latest_number = number
    if latest_number:
        record = cases[latest_number]
        registry["latest_mystery_case"] = {
            "case_number": latest_number,
            "case": record.get("case"),
            "reveal": record.get("reveal"),
            "teaser": record.get("teaser"),
        }
    else:
        registry.pop("latest_mystery_case", None)

    return before != json.dumps(registry, sort_keys=True, ensure_ascii=False)


def _update_config(registry: dict) -> bool:
    original = CONFIG_PATH.read_text(encoding="utf-8")
    updated = original
    for slug, video in (registry.get("books") or {}).items():
        url = str((video or {}).get("url") or "")
        if slug not in BOOKS or not url:
            continue
        pattern = re.compile(rf'(\{{\s*"slug"\s*:\s*"{re.escape(slug)}".*?"trailerUrl"\s*:\s*")[^"]*(")', flags=re.S)
        updated, count = pattern.subn(lambda m: m.group(1) + url + m.group(2), updated, count=1)
        if count != 1:
            raise SystemExit(f"Could not update trailerUrl for {slug}")
    if updated != original:
        CONFIG_PATH.write_text(updated, encoding="utf-8")
        return True
    return False


def _video_lite(video: dict, title: str) -> str:
    video_id = html.escape(str(video["video_id"]), quote=True)
    safe_title = html.escape(title, quote=True)
    url = f"https://www.youtube.com/watch?v={video_id}"
    return (
        '<div class="video-lite-inner">'
        f'<button class="video-lite" type="button" data-youtube-id="{video_id}" data-title="{safe_title}" aria-label="Play {safe_title}">'
        f'<img src="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" alt="" loading="lazy" decoding="async">'
        '<span class="video-lite-play" aria-hidden="true">▶</span><span class="video-lite-label">Play video</span></button>'
        f'<a class="video-lite-fallback" href="{url}" target="_blank" rel="noopener">Open on YouTube ↗</a></div>'
    )


def _render_challenge(latest: dict) -> str | None:
    if not latest:
        return None
    number = str(latest.get("case_number") or "001")
    case_video = latest.get("case")
    reveal_video = latest.get("reveal")
    if not case_video and not reveal_video:
        return None
    current = reveal_video or case_video
    current_title = str(current.get("title") or f"Mystery Challenge Case #{number}")
    current_url = str(current.get("url") or "https://www.youtube.com/@JayTreeBooks")
    is_reveal = bool(reveal_video)
    if is_reveal:
        status, heading = f"CASE #{number} REVEAL LIVE", "The truth is out."
        lead = "See which clues mattered, which details were distractions, and whether you solved the case before the reveal."
        video_heading = f"Case #{number}: The Reveal"
        video_copy = "Watch the complete solution, then go back to the original case and see what you caught—and what you missed."
    else:
        status, heading = f"CASE #{number} OPEN NOW", f"Mystery Challenge Case #{number} is open."
        lead = "Watch the evidence. Study the suspects. Follow the clues. Make your accusation before the truth is revealed."
        video_heading = f"Solve Case #{number}"
        video_copy = "Study every detail, decide who is lying, and lock in your answer before the reveal goes live."
    actions = []
    if case_video:
        actions.append(f'<a class="cta solid" href="{html.escape(case_video["url"], quote=True)}" target="_blank" rel="noopener" data-event="challenge_case_youtube">Watch Full Case</a>')
    if reveal_video:
        actions.append(f'<a class="cta" href="{html.escape(reveal_video["url"], quote=True)}" target="_blank" rel="noopener" data-event="challenge_reveal_youtube">Watch the Reveal</a>')
    actions.append('<a class="cta" href="case-files.html" data-event="challenge_case_files">Join Case Files</a>')
    return f'''<section class="challenge challenge-launch" id="challenge">
            <div class="wrap">
                <div class="challenge-teaser">
                    <div class="challenge-art"><img src="images/mystery-challenge-case-001.webp" alt="Mystery Challenge Case File {html.escape(number)}" loading="lazy" decoding="async"><div class="case-stamp">CASE FILE #{html.escape(number)}</div></div>
                    <div class="challenge-copy"><div class="eyebrow">A JayTree Books Original</div><div class="coming-soon">{status}</div><h2>{heading}</h2><p class="challenge-lead">{lead}</p><div class="challenge-question">Can you solve Case File #{html.escape(number)}?</div><div class="hero-actions">{''.join(actions)}</div><small class="challenge-note">{('The reveal is live now.' if is_reveal else 'The case is open. Make your accusation before the reveal.')}</small></div>
                </div>
                <div class="challenge-video-block" id="case-{html.escape(number)}-video">
                    <div class="challenge-video-copy"><div class="eyebrow">Mystery Challenge Case #{html.escape(number)}</div><span class="challenge-video-kicker">Now Playing</span><h3>{video_heading}</h3><p>{video_copy}</p><div class="hero-actions"><a class="cta" href="{html.escape(current_url, quote=True)}" target="_blank" rel="noopener" data-event="challenge_current_youtube">Watch on YouTube →</a></div></div>
                    <div class="challenge-short-player" style="aspect-ratio:16/9;max-width:680px">{_video_lite(current, current_title)}</div>
                </div>
            </div>
        </section>'''


def _update_index(registry: dict) -> bool:
    challenge = _render_challenge(registry.get("latest_mystery_case") or {})
    if not challenge:
        return False
    original = INDEX_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r'<section class="challenge challenge-launch" id="challenge">.*?</section>\s*\n\s*<!-- JAYTREE_CASE_FILES_START -->', flags=re.S)
    updated, count = pattern.subn(challenge + "\n\n<!-- JAYTREE_CASE_FILES_START -->", original, count=1)
    if count != 1:
        raise SystemExit("Could not replace homepage Mystery Challenge section")
    if updated != original:
        INDEX_PATH.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    channel_id = _resolve_channel_id()
    entries = _feed_entries(channel_id)
    if not entries:
        raise SystemExit("YouTube feed returned no uploads")
    registry = _load_registry(channel_id)
    registry_changed = _update_registry(registry, entries)
    config_changed = _update_config(registry)
    index_changed = _update_index(registry)
    registry["last_checked"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if registry_changed or config_changed or index_changed:
        registry["last_synced"] = registry["last_checked"]
        REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("YouTube sync updated website metadata.")
    else:
        REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("YouTube sync: no new matching uploads.")
    print(f"Channel: {CHANNEL_HANDLE} ({channel_id})")
    print(f"Feed latest: {entries[0]['title']} -> {entries[0]['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
