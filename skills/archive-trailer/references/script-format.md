# script.json

The single source of truth for a trailer. Every script reads it; nothing else holds settings.
The `//` comments are explanations only; the real file is plain JSON.

```json
{
  "title": "Acme launch promo",
  "runtime_target_s": 60,
  "format": "16:9, letterboxed to 2.39:1; archive only; text cards, no VO",
  "acts": {"1": "Act 1: the setup", "2": "Act 2: the wait", "3": "Act 3: the payoff"},
  "turn_beat": "09_turn",           // music hard-cuts from the quiet opening to the climax here
  "title_beat": "16_title",         // must be the last beat
  "style": {"card_s": 1.3},         // black-card length in seconds
  "rules": {
    "allowed_names": ["Acme"],        // anything in a beat's "demo" or "names"
    "banned_text": ["guaranteed", "pm"]       // never on a card; matched on word boundaries
  },
  "beats": [
    {"id": "01_legend", "act": 1, "card": "Every great company has a legend.", "dur_s": 4,
     "queries": ["men in suits signing a contract at a desk", "handshake in a boardroom"],
     "picks": ["0.2", "1.0"],       // row.col into candidates.json[beat]; order = play order
     "frame_y": {"0.2": 0.0},       // optional per pick: vertical crop window, 0 top … 1 bottom
     "in_s": {"1.0": 3.5},          // optional per pick: in-point in seconds (default: middle of clip)
     "dark_ok": "reason",           // optional: a mostly-black shot is intentional
     "demo": "Name", "names": [],   // optional: anything named, checked against allowed_names
     "flag": "note for the review page",
     "cut": true                    // optional: skip this beat everywhere
    },
    {"id": "16_title", "act": 3, "card": "ACME ONE", "dur_s": 5,
     "subcards": ["A one-line subtitle", "Acme · 2026"],
     "queries": ["…"]}
  ],
  "decisions": {                    // written by apply_review.py; read by the assembler
    "card_treatment": {"decision": "overlay_act3"},   // black_all | overlay_act3 | overlay_all
    "color": {"decision": "bw_then_color"}            // as_sourced | bw_then_color
  },
  "open_decisions": [               // questions for the next review page (visual-review format)
    {"id": "music_direction", "question": "Music direction", "options": [["orchestral", "Orchestral build"], ["piano", "Minimal piano"]]}
  ],
  "screening": {"excluded": {"<clip id>": "reason"}, "flagged": {"<clip id>": "note"}},
  "music": {"file": "assets/music/track.ogg", "opening_in": 1.0, "climax_end": 858.0,
            "opening_gain_db": 10.0, "credit": "…", "rights_basis": "…"},
  "versions": {
    "30": {"beats": {"01_legend": {"dur_s": 3, "picks": ["0.2"]}, "09_turn": {"dur_s": 3}, "16_title": {"dur_s": 4}}}
  }
}
```

## Timing rules the checks enforce
- The full cut lands within 15% of `runtime_target_s`; each version lands on its length exactly.
- A shot under a card overlay gets at least 1.2 s (reading time); any other shot at least 0.8 s.
- A black card takes `card_s` out of its beat, so a 3 s beat with a card has 1.7 s of picture.
- Each beat gets one trailer hit; the turn gets a riser; the title gets the big hit.
- Versions must keep the turn and the title beats.

## How a beat becomes picture
Each pick is trimmed from the middle of its clip (or from `in_s`), cropped to 2.39:1 (window set by
`frame_y`), converted to black-and-white if the color decision says so, and gets its card as a
black interstitial or an overlay depending on `card_treatment` and the act. The title beat always
overlays its card and subcards on dimmed footage.
