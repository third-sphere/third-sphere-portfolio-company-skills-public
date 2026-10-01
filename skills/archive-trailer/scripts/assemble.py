#!/usr/bin/env python3
"""Rough assembly of the archive trailer from trailer/script.json picks.

Per beat: optional black title card (CARD_S), then the beat's picks split evenly across the
remaining time, each trimmed from the middle of its clip. Everything is normalized to
1920x1080 @30fps with a 2.39:1 letterbox, rendered as segments, then concatenated.
Silent (music TBD) but with a silent AAC track so players and social uploaders behave.
Usage (from the project folder): python3 <skill>/scripts/assemble.py [version]  -> build/picture.mp4
"""
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

import framing
import project

HERE = Path(__file__).parent
ROOT = project.root()
FONTS = project.FONTS
CLIPS = ROOT / "clips"            # downloaded archive clips (gitignored, re-fetchable)
SEGS = ROOT / "build" / "segments"
OUT = ROOT / "build" / "picture.mp4"
W, H, FPS = 1920, 1080, 30
PIC_H = 804                       # 1920 / 2.39 ≈ 803, rounded to even
CARD_S = 1.3                      # black interstitial card length
UA = {"User-Agent": "Mozilla/5.0 (archive-trailer skill)"}


def run(cmd):
    subprocess.run(cmd, check=True)


def esc(text: str) -> str:
    # Text sits inside '...' in the filter graph: swap straight quotes for typographic ones.
    return text.replace("\\", "").replace("'", "’").replace("%", r"\%")


def fetch(clip: dict) -> Path:
    CLIPS.mkdir(exist_ok=True)
    dst = CLIPS / f"{clip['id']}.mp4"
    if not dst.exists():
        req = urllib.request.Request(clip["videoUrl"], headers=UA)
        with urllib.request.urlopen(req, timeout=120) as r:
            dst.write_bytes(r.read())
    return dst


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def letterbox(fy: float = 0.5) -> str:
    """Crop to 2.39:1. fy picks the vertical window: 0 = top of frame, 0.5 = center, 1 = bottom."""
    return (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{PIC_H}:0:(ih-{PIC_H})*{fy},"
            f"pad={W}:{H}:0:(oh-ih)/2:black,setsar=1,fps={FPS},format=yuv420p")
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-c:a", "aac", "-ar", "48000", "-ac", "2", "-shortest"]


SERIF, SANS = FONTS / "DMSerifDisplay-Regular.ttf", FONTS / "DMSans.ttf"


def card_lines(card: str, subcards=(), card_size: int = 84, sub_size: int = 40):
    """(text, font, size) specs: the card in serif (wrapped to two lines if too wide), subcards in sans."""
    spec = [(t, SERIF, card_size) for t in project.wrap(card, str(SERIF), card_size)]
    for sub in subcards:
        spec += [(t, SANS, sub_size) for t in project.wrap(sub, str(SANS), sub_size)]
    return spec


def text_lines(spec, y_center, outline: bool = False):
    """drawtext chain for centered lines from (text, font, size) specs."""
    sizes = [z for _, _, z in spec]
    parts, y = [], y_center - (sum(sizes) + 24 * (len(spec) - 1)) // 2
    for line, font, size in spec:
        halo = ":borderw=3:bordercolor=black@0.6:shadowx=0:shadowy=3:shadowcolor=black@0.5" if outline else ""
        parts.append(f"drawtext=fontfile={font}:text='{esc(line)}':fontsize={size}:"
                     f"fontcolor=white:x=(w-text_w)/2:y={y}{halo}")
        y += size + 24
    return ",".join(parts)


def card_segment(path: Path, text: str, dur: float):
    fade = f"fade=t=in:st=0:d=0.25,fade=t=out:st={dur - 0.25:.2f}:d=0.25"
    vf = f"{text_lines(card_lines(text), H // 2)},{fade},format=yuv420p"
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={dur}",
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{dur}", "-vf", vf, *ENC, str(path)])


def shot_segment(path: Path, src: Path, dur: float, overlay=None, fy: float = 0.5,
                 style: str = "title", bw: bool = False, in_s=None, sizes=(110, 40)):
    avail = duration(src)
    start = max(0.0, (avail - dur) / 2)          # middle of the clip, where the match usually is
    if in_s is not None:                         # per-pick in-point from script.json overrides the middle
        start = max(0.0, min(float(in_s), avail - dur))
    vf = letterbox(fy)
    if bw:                                       # past = black-and-white (review v1 decision)
        vf += ",hue=s=0"
    if overlay and style == "title":             # title beat: dim the picture and set type on it
        vf += ",eq=brightness=-0.18," + text_lines(card_lines(overlay[0], overlay[1:], *sizes), H // 2, True)
    elif overlay and style == "card":            # Act 3 card over footage: lighter dim, card-size type
        vf += ",eq=brightness=-0.12," + text_lines(card_lines(overlay[0]), H // 2, True)
    vf += f",fade=t=out:st={dur - 0.3:.2f}:d=0.3" if overlay and style == "title" else ""
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(src),
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v:0", "-map", "1:a:0",
         "-t", f"{dur:.3f}", "-vf", vf, *ENC, str(path)])


def paths(version=None):
    """(segments dir, picture output) for a version. None = the full 60s cut (original paths)."""
    if version is None:
        return SEGS, OUT
    return ROOT / "build" / f"segments_{version}", ROOT / "build" / f"picture_{version}.mp4"


def plan(version=None):
    """Yield (segment_name, kind, args) in timeline order. Pure function of the JSON; tested.
    version: a key of script.json["versions"] (e.g. "30"): keeps only the listed beats, with
    their per-version dur_s and optional picks override. None = full cut."""
    script = project.script()
    cands = project.candidates()
    title_id = project.title_beat(script)
    style = script.get("style", {})
    dec = {k: v.get("decision") for k, v in script.get("decisions", {}).items()}
    treatment, color = dec.get("card_treatment") or "black_all", dec.get("color") or "as_sourced"
    cut_spec = script["versions"][version]["beats"] if version else None
    for b in script["beats"]:
        if b.get("cut"):
            continue
        if cut_spec is not None:
            if b["id"] not in cut_spec:
                continue
            b = {**b, **cut_spec[b["id"]]}   # per-version dur_s / picks override the full cut
        is_title = b["id"] == title_id or bool(b.get("title_style"))
        overlay_card = bool(b["card"]) and not is_title and (
            treatment == "overlay_all" or (treatment == "overlay_act3" and b["act"] == 3))
        bw = color == "bw_then_color" and b["act"] < 3
        clips = []
        for p in b["picks"]:
            r, i = map(int, p.split("."))
            clips.append(cands[b["id"]][r]["clips"][i])
        had_card = bool(b["card"]) and not is_title and not overlay_card
        if had_card:
            card_s = max(style.get("card_s", CARD_S), project.reading_time(b["card"], s=script))
            yield f"{b['id']}_card", "card", {"text": b["card"], "dur": card_s, "beat": b["id"], "hit": True}
            shot_time = b["dur_s"] - card_s
        else:
            shot_time = b["dur_s"]
        each = shot_time / len(clips)
        for n, c in enumerate(clips):
            args = {"clip": c, "dur": min(each, c["durationSeconds"]),
                    "fy": b.get("frame_y", {}).get(b["picks"][n]),        # None = automatic (faces kept in frame)
                    "bw": bw, "beat": b["id"], "hit": n == 0 and not had_card,  # one hit per beat start
                    "in_s": b.get("in_s", {}).get(b["picks"][n])}              # optional in-point
            if is_title:
                args["overlay"], args["style"] = [b["card"], *b.get("subcards", [])], "title"
                args["sizes"] = project.title_sizes(b, script)                # per-card override, else style
            elif overlay_card:
                args["overlay"], args["style"] = [b["card"]], "card"
            yield f"{b['id']}_shot{n}", "shot", args


def build(version=None) -> Path:
    segs, out = paths(version)
    segs.mkdir(parents=True, exist_ok=True)
    listing = []
    deadline = time.time() + float(os.environ.get("TRAILER_TIME_BUDGET_S", "1e9"))
    for name, kind, a in plan(version):
        seg = segs / f"{name}.mp4"
        key = segs / f"{name}.key"
        want = json.dumps({"kind": kind, "args": {k: v for k, v in a.items() if k != "clip"},
                           "clip": (a.get("clip") or {}).get("id"), "v": 2}, sort_keys=True, default=str)
        if not (seg.exists() and key.exists() and key.read_text() == want):   # re-render only what changed
            if time.time() > deadline:
                raise TimeoutError("time budget used; rerun to continue (finished segments are kept)")
            tmp = seg.with_name(seg.stem + ".part.mp4")                        # atomic: no half-written segments
            if kind == "card":
                card_segment(tmp, a["text"], a["dur"])
            else:
                src = fetch(a["clip"])
                fy = a["fy"] if a["fy"] is not None else framing.frame_y(src, a["clip"]["id"], a["dur"], a.get("in_s"))
                shot_segment(tmp, src, a["dur"], a.get("overlay"), fy,
                             a.get("style", "title"), a.get("bw", False), a.get("in_s"),
                         tuple(a.get("sizes", (110, 40))))
            tmp.replace(seg)
            key.write_text(want)
        listing.append(f"file '{seg}'")
    lst = segs / "concat.txt"
    lst.write_text("\n".join(listing) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-movflags", "+faststart", str(out)])
    return out


if __name__ == "__main__":
    import sys
    print(build(sys.argv[1] if len(sys.argv) > 1 else None))
