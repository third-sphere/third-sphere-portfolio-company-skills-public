#!/usr/bin/env python3
"""Run every beat's queries against movingimagearchive.com and save candidates.

The search endpoint is undocumented (reverse-engineered from the site's JS):
POST /api/search {"query": str} -> {"clips": [...], "hasMore": bool}
Output: trailer/candidates.json + trailer/sheets/<beat>.jpg contact sheets.
"""
import io
import json
import time
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw

import project

HERE = project.root()   # reads script.json and writes candidates.json + sheets/ in the project
API = "https://www.movingimagearchive.com/api/search"
TOP_N = 6            # candidates kept per query
MIN_DUR, MAX_DUR = 1.5, 60.0
UA = {"User-Agent": "Mozilla/5.0 (archive-trailer skill)"}
KEEP = ("id", "sourceTitle", "sourceSlug", "sourceYear", "startSeconds", "endSeconds",
        "durationSeconds", "colorMode", "aspectRatio", "score", "videoUrl", "thumbnailUrl")


def search(query: str, retries: int = 3) -> list[dict]:
    req = urllib.request.Request(API, data=json.dumps({"query": query}).encode(),
                                 headers={"Content-Type": "application/json", **UA})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                clips = json.load(r)["clips"]
            break
        except (TimeoutError, OSError):
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))  # backoff; the endpoint occasionally stalls
    clips = [c for c in clips if MIN_DUR <= c["durationSeconds"] <= MAX_DUR]
    return [{k: c.get(k) for k in KEEP} for c in clips[:TOP_N]]


def sheet(beat_id: str, rows: list[tuple[str, list[dict]]]) -> None:
    tw, th, pad = 240, 180, 22
    img = Image.new("RGB", (tw * TOP_N, (th + pad) * len(rows)), "white")
    d = ImageDraw.Draw(img)
    for r, (q, clips) in enumerate(rows):
        y = r * (th + pad)
        d.text((4, y + 4), q[:90], fill="black")
        for i, c in enumerate(clips):
            try:
                with urllib.request.urlopen(urllib.request.Request(c["thumbnailUrl"], headers=UA), timeout=30) as t:
                    im = Image.open(io.BytesIO(t.read())).convert("RGB")
                im.thumbnail((tw - 4, th - 4))
                img.paste(im, (i * tw + 2, y + pad))
                d.text((i * tw + 4, y + pad + 2), f"{r}.{i}", fill="yellow")
            except Exception as e:  # thumbnail missing is non-fatal
                d.text((i * tw + 4, y + pad + 20), f"no thumb: {e}"[:30], fill="red")
    (HERE / "sheets").mkdir(exist_ok=True)
    img.save(HERE / "sheets" / f"{beat_id}.jpg", quality=80)


def main() -> None:
    script = json.loads((HERE / "script.json").read_text())
    cache = HERE / "candidates.json"
    out = json.loads(cache.read_text()) if cache.exists() else {}
    for beat in script["beats"]:
        cached = out.get(beat["id"])
        if cached and [r["query"] for r in cached] == beat["queries"]:
            # Same queries as last time: keep the cached results (picks are row.col refs into them,
            # so re-searching could silently move them). Only redraw a missing contact sheet.
            if not (HERE / "sheets" / f"{beat['id']}.jpg").exists():
                sheet(beat["id"], [(r["query"], r["clips"]) for r in cached])
            continue
        rows = []
        for q in beat["queries"]:
            rows.append((q, search(q)))
            time.sleep(0.5)  # be polite to an undocumented endpoint
        out[beat["id"]] = [{"query": q, "clips": c} for q, c in rows]
        sheet(beat["id"], rows)
        print(beat["id"], [len(c) for _, c in rows])
        cache.write_text(json.dumps(out, indent=1))  # save after each beat


if __name__ == "__main__":
    main()
