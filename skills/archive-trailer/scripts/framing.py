"""Automatic vertical framing for the 2.39:1 letterbox crop.

The crop keeps only ~56% of a 4:3 frame's height, and a centered window cuts off the tops of
heads, because people's heads sit above center in most footage. For each shot this samples the
frames that will actually play, finds faces, and places the window so every face fits with
headroom above it. With no faces it biases the window upward (cutting feet beats cutting heads).
Results are cached in the project's framing.json; faces that can't all fit are recorded there as
"faces_cut" so the checks can flag the shot. An explicit per-pick frame_y in script.json wins.
"""
import json
import subprocess
from pathlib import Path

import project

W, H, PIC_H = 1920, 1080, 804
NO_FACE_FY = 0.35      # upper-biased default when no faces are found
SAMPLES = 5


def _cache_path() -> Path:
    return project.root() / "framing.json"


def _load() -> dict:
    p = _cache_path()
    return json.loads(p.read_text()) if p.exists() else {}


def _duration(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(p)], capture_output=True, text=True, check=True).stdout)


def _frames(src: Path, start: float, dur: float):
    """Frames scaled exactly as the letterbox filter scales them (cover 1920x1080), before the crop."""
    import cv2
    import numpy as np
    out = []
    for k in range(SAMPLES):
        t = start + dur * (k + 0.5) / SAMPLES
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1",
                              "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,format=gray",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if raw:
            img = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                out.append(img)
    return out


def _faces(img):
    import cv2
    h = img.shape[0]
    found = []
    for name in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"):
        det = cv2.CascadeClassifier(cv2.data.haarcascades + name)
        # Strict settings: archival grain produces false faces at loose ones.
        for (x, y, w, fh) in det.detectMultiScale(img, scaleFactor=1.1, minNeighbors=7, minSize=(int(h * 0.06),) * 2):
            found.append((int(y), int(y + fh)))
    return found


def decide(frames) -> dict:
    """Pure framing decision from frames (numpy grayscale). Separated out for testing."""
    if not frames:
        return {"fy": NO_FACE_FY, "faces": 0, "faces_cut": False}
    ih = frames[0].shape[0]
    spare = ih - PIC_H
    if spare <= 0:                                   # already as wide as the crop: nothing to choose
        return {"fy": 0.5, "faces": 0, "faces_cut": False}
    boxes = [b for f in frames for b in _faces(f)]
    if not boxes:
        return {"fy": NO_FACE_FY, "faces": 0, "faces_cut": False}
    top = min(y0 - 0.35 * (y1 - y0) for y0, y1 in boxes)       # headroom above the highest face
    bottom = max(y1 + 0.15 * (y1 - y0) for y0, y1 in boxes)    # and a little chin room
    if bottom - top <= PIC_H:
        y = (top + bottom) / 2 - PIC_H / 2                     # center the faces in the window
        y = min(max(y, bottom - PIC_H), top)                   # but keep all of them inside
    else:
        y = top                                                # can't fit all: keep the tops of heads
    y = max(0.0, min(float(spare), y))
    cut = top < y - 1 or bottom > y + PIC_H + 1
    return {"fy": round(y / spare, 3), "faces": len(boxes), "faces_cut": bool(cut)}


def frame_y(src: Path, clip_id: str, dur: float, in_s=None) -> float:
    avail = _duration(src)
    start = max(0.0, (avail - dur) / 2) if in_s is None else max(0.0, min(float(in_s), avail - dur))
    key = f"{clip_id}|{start:.2f}|{dur:.2f}"
    cache = _load()
    if key not in cache:
        try:
            cache[key] = decide(_frames(src, start, dur))
        except ImportError:                          # no OpenCV: fall back to the upper-biased default
            cache[key] = {"fy": NO_FACE_FY, "faces": None, "faces_cut": False}
        _cache_path().write_text(json.dumps(cache, indent=1))
    return cache[key]["fy"]
