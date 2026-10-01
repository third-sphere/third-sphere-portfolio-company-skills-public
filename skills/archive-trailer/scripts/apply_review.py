#!/usr/bin/env python3
"""Apply a visual-review export to the project's script.json.

Usage (from the project folder): python3 <skill>/scripts/apply_review.py export.json
- Saves the export verbatim to review/rounds/ first.
- pick  -> picks become "row.col" refs into candidates.json (old picks kept in picks_history)
- more  -> the user's request is stored as requery_pending; add it as a query and rerun search.py
- drop  -> the beat is marked cut (assembler and checks skip it)
- text edits -> the card (old text kept in card_history)
- decisions MERGE into script.json["decisions"]; unanswered questions never erase answers
Idempotent: applying the same export twice gives the same script.json.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import project  # noqa: E402


def ref_for(cands: dict, beat_id: str, clip_id: str) -> str:
    for r, row in enumerate(cands[beat_id]):
        for i, c in enumerate(row["clips"]):
            if c["id"] == clip_id:
                return f"{r}.{i}"
    raise KeyError(f"{beat_id}: clip {clip_id} is not among its candidates")


def apply(export: dict, script: dict, cands: dict) -> dict:
    beats = {b["id"]: b for b in script["beats"]}
    for e in export.get("items", []):
        b = beats[e["id"]]
        action = e.get("action", "keep")
        if action == "pick" and e.get("picks"):
            new = [ref_for(cands, b["id"], cid) for cid in e["picks"]]
            if new != b.get("picks"):
                b.setdefault("picks_history", []).append(b.get("picks", []))
                b["picks"] = new
        elif action == "more" and e.get("request"):
            b["requery_pending"] = e["request"]
        elif action == "drop":
            b["cut"] = True
        if e.get("text_changed") and e.get("text") is not None and e["text"] != b.get("card"):
            b.setdefault("card_history", []).append(b.get("card"))
            b["card"] = e["text"] or None
        if e.get("notes"):
            b["review_notes"] = e["notes"]
    decisions = script.setdefault("decisions", {})
    for d in export.get("decisions", []):
        if d.get("decision") or d.get("notes"):
            decisions[d["id"]] = {"decision": d.get("decision", ""), "notes": d.get("notes", "")}
    if (export.get("freetext") or {}).get("overall"):
        script["review_overall"] = export["freetext"]["overall"]
    return script


def main(argv):
    if len(argv) != 2:
        sys.exit(__doc__)
    root = project.root()
    export = json.loads(Path(argv[1]).read_text())
    rounds = root / "review" / "rounds"
    rounds.mkdir(parents=True, exist_ok=True)
    stamp = (export.get("exported_at") or "unknown").replace(":", "").replace(".", "")[:17]
    (rounds / f"{export.get('run', 'round')}_{stamp}.json").write_text(json.dumps(export, indent=1))
    s = apply(export, project.script(), project.candidates())
    (root / "script.json").write_text(json.dumps(s, indent=1, ensure_ascii=False))
    pend = [b["id"] for b in s["beats"] if b.get("requery_pending")]
    print("applied" + (f"; beats wanting new searches: {', '.join(pend)}" if pend else ""))


if __name__ == "__main__":
    main(sys.argv)
