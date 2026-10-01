#!/usr/bin/env python3
"""Build a self-contained visual review page from a spec.

Usage: python3 build_page.py spec.json out.html

Every option image is turned into an inline data URI, because published claude.ai pages can't
load remote images. Sources can be local image files, image URLs, or video files/URLs (videos
become a 4-frame flipbook that animates on hover). Options marked "exclude" are dropped before
the page is built; their reasons are printed so they can be reported to the user.
See references/spec.md for the full spec format.
"""
import base64
import io
import json
import mimetypes
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "page.html"
UA = "Mozilla/5.0 (visual-review skill)"   # some CDNs (e.g. Cloudflare R2) 403 Python's default agent
BOX_W, BOX_H = 240, 180                     # max tile size for still images
FW, FH, FRAMES = 184, 138, 4                # video flipbook frame size and count
MAX_BYTES = 16_000_000                      # published-page limit
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi", ".wmv", ".mpg", ".mpeg"}


class SpecError(ValueError):
    pass


def fetch(src: str) -> bytes:
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(src, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    return Path(src).expanduser().read_bytes()


def is_video(src: str) -> bool:
    return Path(src.split("?")[0].split("#")[0]).suffix.lower() in VIDEO_EXT


def still_thumb(data: bytes) -> tuple[str, int, int]:
    """Fit into BOX_W x BOX_H and pad to exactly that size, so tiles of mixed shapes line up."""
    im = Image.open(io.BytesIO(data))
    im = im.convert("RGB") if im.mode != "RGB" else im
    im.thumbnail((BOX_W, BOX_H))
    canvas = Image.new("RGB", (BOX_W, BOX_H), (0, 0, 0))
    canvas.paste(im, ((BOX_W - im.width) // 2, (BOX_H - im.height) // 2))
    buf = io.BytesIO()
    canvas.save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), BOX_W, BOX_H


def video_thumb(src: str) -> tuple[str, int, int]:
    """4 frames spread across the clip, tiled side by side (one JPEG)."""
    with tempfile.TemporaryDirectory() as d:
        remote = src.startswith(("http://", "https://"))
        inp = src if remote else str(Path(src).expanduser())
        ua = ["-user_agent", UA] if remote else []   # ffmpeg rejects -user_agent on local files
        dur = float(subprocess.run(["ffprobe", "-v", "error", *ua, "-show_entries",
                                    "format=duration", "-of", "csv=p=0", inp],
                                   capture_output=True, text=True, check=True).stdout.strip() or 1)
        out = Path(d) / "s.jpg"
        vf = (f"fps={FRAMES / max(dur, 0.5):.4f},scale={FW}:{FH}:force_original_aspect_ratio=decrease,"
              f"pad={FW}:{FH}:(ow-iw)/2:(oh-ih)/2:black,tile={FRAMES}x1")
        subprocess.run(["ffmpeg", "-y", "-v", "error", *ua, "-i", inp, "-vf", vf,
                        "-frames:v", "1", "-q:v", "7", str(out)], check=True, timeout=300)
        return "data:image/jpeg;base64," + base64.b64encode(out.read_bytes()).decode(), FW, FH


def resolve_image(o: dict) -> None:
    """Fill o['image'], o['w'], o['h'], o['frames'] from o['source'] (or a prebuilt sprite)."""
    if o.get("image", "").startswith("data:"):
        o.setdefault("frames", 1)
        return
    src = o.get("sprite") or o.get("source")
    if not src:
        raise SpecError(f"option {o.get('id')!r} has no source image")
    if o.get("sprite"):   # a ready-made horizontal strip of N equal frames
        data = fetch(src)
        im = Image.open(io.BytesIO(data))
        n = int(o.get("frames", FRAMES))
        mime = mimetypes.guess_type(src)[0] or "image/jpeg"
        o["image"] = f"data:{mime};base64," + base64.b64encode(data).decode()
        o["w"], o["h"], o["frames"] = im.width // n, im.height, n
    elif is_video(src):
        o["image"], o["w"], o["h"] = video_thumb(src)
        o["frames"] = FRAMES
    else:
        o["image"], o["w"], o["h"] = still_thumb(fetch(src))
        o["frames"] = 1


def validate(spec: dict) -> list[str]:
    for k in ("title", "storage_key", "items"):
        if not spec.get(k):
            raise SpecError(f"spec needs {k!r}")
    seen_items, report = set(), []
    for it in spec["items"]:
        if it["id"] in seen_items:
            raise SpecError(f"duplicate item id {it['id']!r}")
        seen_items.add(it["id"])
        kept = []
        for o in it.get("options", []):
            if o.get("exclude"):
                report.append(f"{it['id']}: excluded {o.get('label') or o['id']}: {o['exclude']}")
            else:
                kept.append(o)
        ids = [o["id"] for o in kept]
        if len(ids) != len(set(ids)):
            raise SpecError(f"{it['id']}: duplicate option ids")
        missing = [c for c in it.get("current", []) if c not in ids]
        if missing:
            raise SpecError(f"{it['id']}: current option(s) {missing} are not among its options")
        if not kept:
            raise SpecError(f"{it['id']}: no options left to show")
        it["options"] = kept
    for q in spec.get("decisions", []):
        if not q.get("options"):
            raise SpecError(f"decision {q.get('id')!r} has no options")
    return report


def build(spec: dict, out: Path) -> tuple[Path, list[str]]:
    spec = json.loads(json.dumps(spec))            # work on a copy
    report = validate(spec)
    for it in spec["items"]:
        for o in it["options"]:
            resolve_image(o)
            o.pop("source", None); o.pop("sprite", None)
    spec.setdefault("run", "round-1")
    payload = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    title = (spec["title"].replace("&", "&amp;").replace("<", "&lt;"))
    page = TEMPLATE.read_text().replace("__SPEC__", payload).replace("__TITLE__", title)
    size = len(page.encode())
    if size > MAX_BYTES:
        raise SpecError(f"page is {size / 1e6:.1f} MB; the published limit is 16 MB. "
                        "Use fewer options, or smaller thumbnails.")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return out, report


def main(argv):
    if len(argv) != 3:
        sys.exit(__doc__)
    out, report = build(json.loads(Path(argv[1]).read_text()), Path(argv[2]))
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")
    for line in report:
        print(line)


if __name__ == "__main__":
    main(sys.argv)
