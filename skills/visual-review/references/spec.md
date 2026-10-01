# Spec and export formats

## Spec (input to `build_page.py`)

The `//` comments below are explanations only; real spec files are plain JSON.

```json
{
  "title": "Launch trailer: clip selections",
  "heading": "Pick the shots",                     // optional, defaults to title
  "intro": ["First paragraph.", "Second."],        // optional, sensible default
  "storage_key": "launch-trailer-clips-r1",          // unique per page AND per round
  "run": "trailer-v2-round-1",                     // echoed in the export; names the round
  "current_label": "in rough cut",                 // badge on current options (default "current")
  "actions": [["keep","Keep current"],["pick","Use my picks"],["more","Show me other options"],["drop","Drop this item"]],
  "items": [
    {
      "id": "08_turn",
      "label": "This October, tomorrow shows up.",
      "group": "Act 3",                            // optional section heading; consecutive items share it
      "meta": "3s · Acme",                    // optional, right-aligned
      "flag": "Current pick is mostly black.",     // optional, item-level warning
      "max_picks": 2,                              // optional: 1 = single choice; omit = unlimited, ordered
      "current": ["clipA"],                        // option ids in use now; must exist in options
      "text_field": {"label": "Card text", "value": "This October, tomorrow shows up."},  // optional editable text
      "options": [
        {"id": "clipA", "label": "World of Tomorrow", "caption": "1939 · 3.0s · color",
         "source": "clips/a.mp4",                  // local image/video path or URL
         "link": "https://…", "link_label": "Open clip",
         "flag": "Identifiable people"},           // optional, shown on the tile
        {"id": "clipB", "sprite": "sprites/b.jpg", "frames": 4},   // prebuilt N-frame strip
        {"id": "clipC", "source": "…", "exclude": "NASA logo in frame"}  // dropped, reason reported
      ]
    }
  ],
  "decisions": [
    {"id": "music", "question": "Music direction", "options": [["orchestral","Orchestral"],["modern","Modern pulse"]]}
  ]
}
```

Option images: still images are fit into 240×180. Videos become a 4-frame flipbook (184×138 each).
`sprite` takes an existing horizontal strip. Anything already `data:` is used as is.

## Export (pasted back by the user)

```json
{
  "title": "…", "run": "trailer-v2-round-1", "exported_at": "2026-09-29T04:37:35.129Z",
  "items": [
    {"id": "08_turn", "action": "pick", "picks": ["clipB"], "current": ["clipA"],
     "text": "This October, tomorrow shows up.", "text_changed": false,
     "request": "", "notes": ""}
  ],
  "decisions": [{"id": "music", "question": "Music direction", "decision": "orchestral", "notes": ""}],
  "freetext": {"overall": ""}
}
```

`action`: `keep` (no change), `pick` (use `picks`, in order), `more` (wants other options; see
`request`), `drop` (remove the item). `text` is null when the item has no text field.

## State (output of `merge_export.py`)

```json
{
  "items": {"08_turn": {"picks": ["clipB"], "history": [{"picks": ["clipA"], "run": "…"}],
                         "status": "picked", "text": "…", "request": "…", "notes": "…"}},
  "decisions": {"music": {"decision": "orchestral", "notes": ""}},
  "overall": "…",
  "runs": ["trailer-v2-round-1"]
}
```

`status`: `kept`, `picked`, `wants_other_options`, `dropped`.
