#!/usr/bin/env python3
"""Merge a review-page export into a running state file.

Usage: python3 merge_export.py state.json export.json

- Saves the export verbatim under rounds/ next to the state file (the audit trail).
- Per item: a "pick" replaces the chosen options (old picks kept in history); text edits,
  requests for other options, drops and notes are recorded. "keep" with no edits changes nothing.
- Decisions MERGE: a round that only answers some questions never wipes earlier answers.
- Idempotent: merging the same export twice gives the same state.
The state file is generic on purpose; project code reads it and applies it (e.g. re-cuts a video).
"""
import json
import sys
from pathlib import Path


def merge(state: dict, export: dict) -> dict:
    items = state.setdefault("items", {})
    for e in export.get("items", []):
        cur = items.setdefault(e["id"], {"picks": list(e.get("current") or []), "history": []})
        action = e.get("action", "keep")
        if action == "pick" and e.get("picks"):
            if e["picks"] != cur["picks"]:
                cur["history"].append({"picks": cur["picks"], "run": export.get("run")})
                cur["picks"] = list(e["picks"])
        cur["status"] = {"pick": "picked", "more": "wants_other_options", "drop": "dropped"}.get(
            action, cur.get("status", "kept"))
        if action == "more":
            cur["request"] = e.get("request", "")
        if e.get("text_changed"):
            cur["text"] = e.get("text")
        if e.get("notes"):
            cur["notes"] = e["notes"]
    decisions = state.setdefault("decisions", {})
    for d in export.get("decisions", []):
        if d.get("decision") or d.get("notes"):          # unanswered questions don't erase answers
            decisions[d["id"]] = {"decision": d.get("decision", ""), "notes": d.get("notes", "")}
    overall = (export.get("freetext") or {}).get("overall")
    if overall:
        state["overall"] = overall
    runs = state.setdefault("runs", [])
    if export.get("run") and export["run"] not in runs:
        runs.append(export["run"])
    return state


def main(argv):
    if len(argv) != 3:
        sys.exit(__doc__)
    sp, ep = Path(argv[1]), Path(argv[2])
    export = json.loads(ep.read_text())
    state = json.loads(sp.read_text()) if sp.exists() else {}
    rounds = sp.parent / "rounds"
    rounds.mkdir(parents=True, exist_ok=True)
    stamp = (export.get("exported_at") or "unknown").replace(":", "").replace(".", "")[:17]
    (rounds / f"{export.get('run', 'round')}_{stamp}.json").write_text(json.dumps(export, indent=1))
    sp.write_text(json.dumps(merge(state, export), indent=1, ensure_ascii=False))
    changed = [e["id"] for e in export.get("items", []) if e.get("action") != "keep" or e.get("text_changed")]
    print(f"merged {ep.name} into {sp.name}; items changed: {', '.join(changed) or 'none'}")


if __name__ == "__main__":
    main(sys.argv)
