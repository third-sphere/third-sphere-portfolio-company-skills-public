# archive-trailer

Make a movie-trailer-style promo (60 s, plus 30 s and 15 s cutdowns) cut entirely from
public-domain archival footage: text cards, synthesized trailer hits, and a public-domain music
track, with every step checked by tests. `SKILL.md` is the workflow; `references/` holds the
script format, music, rights and lessons.

## Requirements
- Python 3.10+ with `numpy` and `Pillow`; `opencv-python-headless` for face-aware framing
  (optional; without it framing falls back to an upward-biased crop)
- `ffmpeg` and `ffprobe` on the PATH
- Network access to movingimagearchive.com (clip search and media) and Wikimedia Commons (music)
- The companion **visual-review** skill for clip-selection pages (`scripts/to_review.py`). Without
  it, everything else works; you pick clips by editing `script.json` directly.

## What's in it
- `scripts/`: project scaffold, archive search with contact sheets, review-page bridge, review
  apply step, assembly (letterbox, face-aware framing, card overlays, black-and-white acts),
  synthesized sound design, music search and loudness mapping, mix to -14 LUFS, cutdowns, and
  reusable checks every project inherits (`checks.py`)
- `assets/fonts/`: DM Serif Display and DM Sans, under the SIL Open Font License (OFL files included)
- `tests/`: an offline suite on a synthetic project, including a full render

Run the tests: `python3 -m unittest discover -s tests -v` (about a minute).

## Status and history
- v1.3: approvals of cropped shots are per clip; hand framing exempts only its own clip.
- v1.2: face-aware framing and crop check, slow-reading card timing and check, two-line wrapping,
  multiple title-style cards, cached segments rendered under a time budget.
- v1.1: search cache keyed on queries, clearer too-short-picks check, calibrated music mapping,
  arrangement-rights guidance.
- v1.0: pipeline generalized from a first event promo, validated on a second (book) promo.

## As is
Provided as is, without warranty. "Public domain" labels on archives and Commons are claims to
verify, not guarantees: see `references/rights.md` before publishing anything made with this.
