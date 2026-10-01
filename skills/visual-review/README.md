# visual-review

Build an interactive review page where someone chooses between visual options for several items
at once (video clips, photos, design variants, thumbnails, logos), answers a few open decisions,
and pastes a JSON export back into the chat. Then merge the answers without losing earlier rounds.
`SKILL.md` is the workflow; `references/` holds the spec and export formats and the lessons.

## Requirements
- Python 3.10+ with `Pillow`; `ffmpeg`/`ffprobe` for video options (shown as 4-frame flipbooks)
- Optional: `playwright` with Chromium for `scripts/check_page.py`, the pre-publish browser check
- Images are inlined into the page, so it works where pages can't load remote images (16 MB cap)

## What's in it
- `assets/page.html`: the page template (items x options, decisions, autosave, JSON export)
- `scripts/build_page.py`: validates a spec, thumbnails stills and videos, drops excluded options
- `scripts/check_page.py`: headless check that clicks export, answers survive reload, and it fits a phone
- `scripts/merge_export.py`: merges an export into running state; partial rounds never erase answers
- `tests/`: offline tests with generated images and video

Run the tests: `python3 -m unittest discover -s tests -v`.

## As is
Provided as is, without warranty.
