#!/usr/bin/env python3
"""Scaffold a trailer project folder.

Usage: python3 new_project.py <folder> "<working title>"
Creates script.json (a skeleton to fill in), CONTEXT.md (the living project doc), .gitignore,
and a tests/ file wired to the skill's plan checks. Refuses to overwrite an existing script.json.
"""
import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]

SCRIPT = {
    "title": "", "runtime_target_s": 60,
    "format": "16:9, letterboxed to 2.39:1; archive only; text cards, no VO",
    "acts": {"1": "Act 1", "2": "Act 2", "3": "Act 3"},
    "turn_beat": "", "title_beat": "",
    "style": {"card_s": 1.3},
    "rules": {"allowed_names": [], "banned_text": []},
    "beats": [
        {"id": "01_example", "act": 1, "card": "A card line.", "dur_s": 4,
         "queries": ["a concrete visual description", "a second angle on the same shot"]}
    ],
}

CONTEXT = """# {title}: context

Living doc. Update it on every change; nothing ships without an update here and to tests/.

## Goal
(What this trailer is for, where it runs, who it's for, and what it must not claim.)

## Sources of truth
(Where the facts on the cards come from: the book, the event page, a brief. Link them.)

## Decisions
(Each choice with its date and reason. Review-round decisions are copied here after merging.)

## Status
- Scaffolded {date}.

## Known risks / open questions

## Lessons
"""

TEST = '''"""Project checks: the skill's plan rules applied to this project's script.json."""
import os
import sys
import unittest
from pathlib import Path

os.environ["TRAILER_PROJECT"] = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, "{skill}/scripts")
from checks import make_plan_tests  # noqa: E402

PlanTests = make_plan_tests()

if __name__ == "__main__":
    unittest.main()
'''


def main(argv):
    if len(argv) != 3:
        sys.exit(__doc__)
    folder, title = Path(argv[1]), argv[2]
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / "script.json").exists():
        sys.exit(f"{folder}/script.json already exists; not overwriting")
    from datetime import date
    s = dict(SCRIPT, title=title)
    (folder / "script.json").write_text(json.dumps(s, indent=1, ensure_ascii=False))
    (folder / "CONTEXT.md").write_text(CONTEXT.format(title=title, date=date.today().isoformat()))
    (folder / ".gitignore").write_text("build/\nclips/\nsprites/\nsheets/\nassets/music/*.ogg\nassets/music/*.mp3\n__pycache__/\n")
    (folder / "tests").mkdir(exist_ok=True)
    (folder / "tests" / "test_plan.py").write_text(TEST.format(skill=SKILL))
    print(f"scaffolded {folder}: fill in script.json, then run search.py")


if __name__ == "__main__":
    main(sys.argv)
