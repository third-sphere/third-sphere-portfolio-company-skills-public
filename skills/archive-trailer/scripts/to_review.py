#!/usr/bin/env python3
"""Turn the project's script + candidates into a visual-review page.

Usage (from the project folder):
  python3 <skill>/scripts/to_review.py <round-name> [beat_id ...]
Writes review/<round>.spec.json and build/review-<round>.html, and runs the page check.
Limit to some beats by listing their ids. Needs the visual-review skill; its location is found
automatically, or set VISUAL_REVIEW_SKILL.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import project  # noqa: E402

UA = "Mozilla/5.0 (archive-trailer skill)"
FW, FH, N = 184, 138, 4


def visual_review() -> Path:
    here = project.SKILL
    for p in [os.environ.get("VISUAL_REVIEW_SKILL"), here.parent / "visual-review",
              "/mnt/skills/user/visual-review", Path.home() / ".claude/skills/visual-review"]:
        if p and (Path(p) / "scripts" / "build_page.py").exists():
            return Path(p)
    sys.exit("visual-review skill not found; install it or set VISUAL_REVIEW_SKILL")


def sprite(c: dict, root: Path) -> Path:
    """4-frame strip for one clip, cached in sprites/. Local clips (e.g. NASA shots) are used if present."""
    dst = root / "sprites" / f"{c['id']}.jpg"
    if dst.exists():
        return dst
    dst.parent.mkdir(exist_ok=True)
    local = root / "clips" / f"{c['id']}.mp4"
    src = str(local) if local.exists() else c["videoUrl"].split("#")[0]
    ua = [] if local.exists() else ["-user_agent", UA]
    fps = N / max(c["durationSeconds"], 0.5)
    vf = (f"fps={fps:.4f},scale={FW}:{FH}:force_original_aspect_ratio=decrease,"
          f"pad={FW}:{FH}:(ow-iw)/2:(oh-ih)/2:black,tile={N}x1")
    tmp = dst.with_suffix(".part.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ua, "-i", src, "-vf", vf, "-frames:v", "1",
                    "-q:v", "7", str(tmp)], check=True, timeout=240)
    tmp.replace(dst)
    return dst


def spec_for(round_name: str, only=None) -> dict:
    s, cands, root = project.script(), project.candidates(), project.root()
    screen = s.get("screening", {})               # {"excluded": {id: reason}, "flagged": {id: note}}
    excluded, flagged = screen.get("excluded", {}), screen.get("flagged", {})
    acts = {"1": "Act 1", "2": "Act 2", "3": "Act 3", **s.get("acts", {})}
    items, jobs = [], []
    for b in s["beats"]:
        if b.get("cut") or (only and b["id"] not in only):
            continue
        current, seen, opts = [], set(), []
        for p in b.get("picks", []):
            r, i = map(int, p.split("."))
            current.append(cands[b["id"]][r]["clips"][i]["id"])
        for row in cands.get(b["id"], []):
            for c in row["clips"]:
                if c["id"] in seen:
                    continue
                seen.add(c["id"])
                prov = c.get("provenance") or {}
                link = (f"https://archive.org/details/{prov['identifier']}" if prov.get("source") == "archive.org"
                        else c["videoUrl"])
                o = {"id": c["id"], "label": c["sourceTitle"][:70],
                     "caption": f'{c.get("sourceYear") or "year unknown"} · {c["durationSeconds"]:.1f}s · '
                                f'{"color" if c.get("colorMode") == "color" else "b&w"}'
                                f'{" · " + prov["collection"].upper() if prov.get("collection") else ""}'
                                f' · from “{row["query"]}”',
                     "link": link, "link_label": "Open clip"}
                if c["id"] in excluded:
                    o["exclude"] = excluded[c["id"]]
                if c["id"] in flagged:
                    o["flag"] = flagged[c["id"]]
                opts.append(o)
                if c["id"] not in excluded:
                    jobs.append(c)
        tf = {"label": "Card text", "value": b.get("card") or ""}
        items.append({"id": b["id"], "label": b.get("card") or "(no card)", "group": acts[str(b["act"])],
                      "meta": f'{b["dur_s"]}s' + (f' · reading {project.reading_time(b.get("card") or "", *b.get("subcards", []), s=s):.1f}s'
                                                  if b.get("card") else "") + (f' · {b["demo"]}' if b.get("demo") else ""),
                      "flag": b.get("flag", ""), "current": current, "text_field": tf, "options": opts})
    with ThreadPoolExecutor(6) as ex:                              # sprites are the slow part; cache them
        paths = dict(zip([c["id"] for c in jobs], ex.map(lambda c: _safe_sprite(c, root), jobs)))
    for it in items:
        keep = []
        for o in it["options"]:
            if o.get("exclude"):
                keep.append(o)
            elif paths.get(o["id"]):
                o["sprite"], o["frames"] = str(paths[o["id"]]), N
                keep.append(o)
            else:
                o["exclude"] = "preview could not be generated (clip unreachable)"
                keep.append(o)
        it["options"] = keep
    return {"title": f'{s.get("title") or "Trailer"}: selections', "heading": s.get("review_heading") or "Pick the shots",
            "storage_key": f'{(s.get("title") or "trailer").lower().replace(" ", "-")}-{round_name}',
            "run": round_name, "current_label": "in the cut",
            "intro": ["Each beat shows the clip in the current cut (if any) and every candidate the searches returned. "
                      "Hover a frame to flip through it.",
                      "Click frames to choose them; the numbers set the order they play. Edit a card line in place. "
                      "When you’re done, copy the JSON at the bottom and paste it into the chat."],
            "items": items, "decisions": s.get("open_decisions", [])}


def _safe_sprite(c, root):
    try:
        return sprite(c, root)
    except Exception:
        return None


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    round_name, only = argv[1], set(argv[2:]) or None
    root, vr = project.root(), visual_review()
    spec = spec_for(round_name, only)
    (root / "review").mkdir(exist_ok=True)
    sp = root / "review" / f"{round_name}.spec.json"
    sp.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    out = root / "build" / f"review-{round_name}.html"
    subprocess.run([sys.executable, str(vr / "scripts" / "build_page.py"), str(sp), str(out)], check=True)
    subprocess.run([sys.executable, str(vr / "scripts" / "check_page.py"), str(out),
                    str(root / "build" / f"review-{round_name}.png")], check=True)
    print(f"ready to publish: {out}")


if __name__ == "__main__":
    main(sys.argv)
