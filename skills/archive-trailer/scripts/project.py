"""Shared paths and settings. Every script works on the project folder it is run from
(or TRAILER_PROJECT), and reads its settings from that project's script.json."""
import json
import os
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
FONTS = SKILL / "assets" / "fonts"


def root() -> Path:
    return Path(os.environ.get("TRAILER_PROJECT") or Path.cwd()).resolve()


def script() -> dict:
    return json.loads((root() / "script.json").read_text())


def candidates() -> dict:
    p = root() / "candidates.json"
    return json.loads(p.read_text()) if p.exists() else {}


def turn_beat(s=None) -> str:
    """The beat where the music cuts from the quiet opening to the climax."""
    s = s or script()
    return s["turn_beat"]


def title_beat(s=None) -> str:
    """The closing title card beat. Falls back to the beat that carries subcards."""
    s = s or script()
    return s.get("title_beat") or next(b["id"] for b in s["beats"] if b.get("subcards"))


def music(s=None) -> dict:
    s = s or script()
    m = s.get("music")
    if not m:
        raise KeyError("script.json has no \"music\" section yet; see references/music.md")
    return m


# ---------- reading time and line wrapping (shared by the assembler and the checks) ----------
def style(s=None) -> dict:
    s = s or script()
    return {"card_s": 1.3, "reading_wps": 2.0, "reading_lead_s": 0.8, **s.get("style", {})}


def words(*texts) -> int:
    return sum(len([w for w in (t or "").replace("·", " ").split() if any(ch.isalnum() for ch in w)]) for t in texts)


def reading_time(*texts, s=None) -> float:
    """Seconds a slow reader needs: a lead-in to notice the text, then words at reading_wps.
    Defaults (0.8 s + 2 words/s) are deliberately slow; set style.reading_wps to change."""
    st = style(s)
    n = words(*texts)
    return st["reading_lead_s"] + n / st["reading_wps"] if n else 0.0


def wrap(text: str, font_file: str, size: int, max_w: float = 1920 * 0.86) -> list[str]:
    """One line if it fits, else the most balanced two-line split (never more than two)."""
    from PIL import ImageFont
    f = ImageFont.truetype(font_file, size)
    if f.getlength(text) <= max_w:
        return [text]
    ws = text.split()
    best = min(range(1, len(ws)), key=lambda k: max(f.getlength(" ".join(ws[:k])), f.getlength(" ".join(ws[k:]))))
    return [" ".join(ws[:best]), " ".join(ws[best:])]


def title_sizes(beat: dict, s=None) -> tuple[int, int]:
    """(card px, subcard px) for a title-style card: the beat's own title_size/sub_size if set,
    else style.title_size/title_sub_size, else 110/40. The fit check uses the same sizes."""
    st = (s or script()).get("style", {})
    return (int(beat.get("title_size", st.get("title_size", 110))),
            int(beat.get("sub_size", st.get("title_sub_size", 40))))
