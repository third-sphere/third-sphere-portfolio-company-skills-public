#!/usr/bin/env python3
"""Regenerate SCRIPT.md from script.json + candidates.json. (Logic kept in sync with the one-off above.)"""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
import project  # noqa: E402

HERE = project.root()
DEFAULT_ACTS = {"1": "Act 1", "2": "Act 2", "3": "Act 3"}

def main():
    c = json.loads((HERE / "candidates.json").read_text()); s = json.loads((HERE / "script.json").read_text())
    L = ["# Trailer script and shot plan", "", f"**{s['title']}** · ~{sum(b['dur_s'] for b in s['beats'])}s · {s['format']}", "",
         "Generated from `script.json` + `candidates.json` by `render_script.py`. Edit the JSON, not this file.", ""]
    acts = {**DEFAULT_ACTS, **s.get("acts", {})}
    cur = None
    for b in s["beats"]:
        if b["act"] != cur:
            cur = b["act"]; L += ["", f"## {acts[str(cur)]}", ""]
        card = f"**{b['card']}**" if b["card"] else "_(no card)_"
        demo = f" · demo: {b['demo']}" if b.get("demo") else ""
        L.append(f"### {b['id']} · {b['dur_s']}s{demo}")
        L.append(f"Card: {card}" + (" / " + " / ".join(b["subcards"]) if b.get("subcards") else ""))
        L.append("Queries: " + " · ".join(f"`{q}`" for q in b["queries"]))
        for p in b["picks"]:
            r, i = map(int, p.split(".")); cl = c[b["id"]][r]["clips"][i]
            L.append(f"- Pick {p}: *{cl['sourceTitle'][:70]}* ({cl['sourceYear'] or 'year unknown'}), "
                     f"{cl['startSeconds']:.1f}–{cl['endSeconds']:.1f}s, {cl['colorMode'].replace('_', ' ')}")
        L.append("")
    (HERE / "SCRIPT.md").write_text("\n".join(L))

if __name__ == "__main__":
    main()
