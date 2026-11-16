"""Generate a fully offline JayTree Search Console rank-history dashboard.

No external JS, fonts, CSS, tracking, or third-party requests.
"""
from __future__ import annotations

import csv
import html
from pathlib import Path


def _sparkline(values: list[float | None]) -> str:
    """A real average position has a point; absent data never becomes 51."""
    points = [(i, value) for i, value in enumerate(values) if value is not None]
    if not points:
        return '<span class="quiet">No reportable position yet</span>'
    scale_max = max(max(v for _, v in points), 10)
    width, height = 140, 40
    if len(values) == 1:
        xs = [width / 2]
    else:
        xs = [8 + (width - 16) * i / (len(values) - 1) for i in range(len(values))]
    paths = []
    segment: list[str] = []
    for i, value in enumerate(values):
        if value is None:
            if segment:
                paths.append(" ".join(segment))
                segment = []
            continue
        x = xs[i]
        y = 5 + (height - 10) * value / scale_max
        segment.append(("M" if not segment else "L") + f"{x:.1f},{y:.1f}")
    if segment:
        paths.append(" ".join(segment))
    circles = "".join(
        f'<circle cx="{xs[i]:.1f}" cy="{5+(height-10)*value/scale_max:.1f}" r="2.2" />'
        for i, value in points)
    return (
        f'<svg role="img" aria-label="Average ranking position history, '
        f'lower is better" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        + "".join(f'<path d="{p}" fill="none" stroke-width="2" />' for p in paths)
        + circles + '</svg>'
    )


def render(history_csv: Path, *, fixture: bool = False) -> str:
    with history_csv.open(encoding="utf-8", newline="") as f:
        observations = list(csv.DictReader(f))
    groups: dict[tuple[str, str], list[dict]] = {}
    for record in observations:
        if record["source"] != ("fixture_test" if fixture else "gsc_api"):
            raise ValueError("Cannot mix fixture with authoritative Google rankings")
        groups.setdefault((record["keyword"], record["device"]), []).append(record)
    lines = []
    for (keyword, device), records in groups.items():
        records = sorted(records, key=lambda r: r["as_of"])
        latest = records[-1]
        pos = latest["avg_position"] or None
        prior = latest["prior_avg_position"] or None
        values = [float(r["avg_position"]) if r["avg_position"] else None for r in records]
        trend = latest["trend"]
        trend_class = "good" if trend == "up" else "bad" if trend == "down" else "quiet"
        lines.append(
            "<tr><td><strong>" + html.escape(keyword) + "</strong></td>"
            "<td>" + html.escape(device.lower()) + "</td>"
            "<td>" + html.escape(latest["impressions"]) + "</td>"
            "<td>" + html.escape(latest["clicks"]) + "</td>"
            "<td>" + html.escape(pos or "—") + "</td>"
            "<td>" + html.escape(prior or "—") + "</td>"
            '<td class="' + trend_class + '">' + html.escape(trend) + "</td>"
            "<td>" + _sparkline(values) + "</td></tr>")
    last_date = max((r["as_of"] for r in observations), default="no readings")
    title = "JayTree Books — Google Search Rankings"
    if fixture:
        title += " — TEST DATA ONLY"
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>""" + html.escape(title) + """</title>
<style>
:root{color-scheme:dark}
body{font:16px/1.6 system-ui,Segoe UI,sans-serif;background:#101923;color:#eef3f8;max-width:1150px;margin:0 auto;padding:24px}
h1{line-height:1.2;color:#fbde9c} h2{font-size:1.1rem}
.info{border:1px solid #415164;border-radius:12px;padding:15px 20px;margin:24px 0;background:#172332}
table{width:100%;border-collapse:collapse;margin-top:14px}
td,th{text-align:left;border-bottom:1px solid #38485b;padding:10px 12px}
th{color:#f5d58e} td{font-variant-numeric:tabular-nums}
tr:nth-child(2n){background:#172332}
.good{color:#85e0b2}.bad{color:#ffafa8}.quiet{color:#b8c5d2}
svg path{stroke:#f5ce72}svg circle{fill:#f5ce72}
.scroller{overflow-x:auto}p{max-width:78ch}
small{color:#b8c5d2}
</style></head><body><main>
<h1>""" + html.escape(title) + """</h1>
<p>Self-hosted, no subscription, no external network requests. Google Search Console's actual
average position by exact query, US Google Web, and device.</p>
<div class="info"><strong>Latest snapshot: """ + html.escape(last_date) + """</strong>
<p>Our two principal page-one goals remain <strong>psychological mystery books</strong>
and <strong>new mystery book</strong>. Supporting searches are diagnostic only.</p></div>
<h2>Current positions and historical movement</h2>
<div class="scroller"><table><thead><tr>
<th>Search query</th><th>Device</th><th>Impressions</th><th>Clicks</th>
<th>Avg position</th><th>Previous avg</th><th>Trend</th><th>History</th>
</tr></thead><tbody>""" + "\n".join(lines) + """</tbody></table></div>
<div class="info"><strong>How to read these numbers</strong>
<p>A lower average position is better: moving from 25 to 18 is an improvement.
A dash does not mean position 51 or that Google has deindexed the page. It means no
reportable impressions for that exact query and device. Google hides some low-volume queries.
This chart is NOT a live exact-position SERP checker.</p></div>
<p><small>Source: official Google Search Console API, read-only. Data is on JayTree LAN only.
The report is static HTML and contains no external scripts, pixels, or analytics.</small></p>
</main></body></html>
"""


def save_dashboard(history_csv: Path, target: Path, *, fixture: bool = False) -> Path:
    # Reuse the collector's atomic private-LAN writer, without a network dependency.
    from gsc_weekly_tracker import atomic
    atomic(target, render(history_csv, fixture=fixture))
    return target
