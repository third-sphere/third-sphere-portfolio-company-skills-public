# Lessons (each one cost a round once)

## Sources
- The movingimagearchive.com search API is undocumented: `POST /api/search {"query": ...}`.
  Its clip CDN (Cloudflare R2) returns 403 to Python's default User-Agent; the scripts send one.
- The endpoint occasionally stalls past 30 s. `search.py` retries with backoff and resumes.
- Concrete visual nouns find shots; abstract ideas return noise ("mechanical robot
  demonstration" returned film projectors; "tall metal humanoid robot at a world's fair" found one).

## Picture
- A 2.39:1 center crop of 4:3 footage keeps ~56% of the height. Check every shot for cropped
  heads and set `frame_y` per pick.
- White card text vanishes on bright footage. Overlays carry an outline and shadow; check anyway.
- A "not blank" check at one instant fails on night shots. Sample several points, and require a
  written `dark_ok` reason to opt out.
- Black-and-white at the source undercuts a "color arrives" treatment. Say so before the user
  finds out.

- A pick shorter than its share of a beat is silently trimmed, so the beat (and the whole
  trailer) runs short while the music follows along and nothing sounds wrong. The checks now
  name it: "plays 2.10s of 3s; its picks are too short."

- Contact-sheet thumbnails are too small to read small print. A bank name on a check passed
  screening and was only caught in the full-size frame grid of the render. Treat the frame grid as
  a second screening pass, and zoom in on any frame with paper, signs or screens in it.

- Heads cut off: the 2.39:1 crop keeps ~56% of a 4:3 frame's height and used to be centered.
  Framing is now automatic (framing.py): faces kept in frame with headroom, upward bias with no
  faces. Its "faces can't all fit" verdicts over-fire on archival texture (curtains, ledger spines),
  so the check stops on them and a person decides: accept with `crop_ok` after looking, or reframe.
- Slow reading changes everything downstream: at 0.8 s + 2 words/s, a 60-second 16-card script
  became 85.5 s, black cards became impractical (they stack reading time on top of footage), and
  cutdowns must drop cards rather than squeeze them.
- A single command has a 300 s limit here. Segments are cached by content and rendered under a
  time budget (TRAILER_TIME_BUDGET_S), so a long render is a few resumable runs, one per command.

- An acceptance must name what it accepts. `crop_ok` was once per beat, so a newly picked clip
  inherited an approval given to the old one and a real head crop shipped past the check. It is now
  `{clip_id: reason}`, and clips framed by hand (`frame_y`) are exempt only individually.
- Lengthening Acts 1-2 can outgrow the track's quiet passage. Search the whole track for a quiet
  window as long as Acts 1-2 that ends in a swell, rather than starting inside a loud bar.
- Card edits are claims. A reviewer's edit once said an early investor still held its stake, when
  it had sold decades earlier;
  check edited claims against the source before rendering, and hold them with a note if wrong.

## Process
- Background jobs die when the tool call ends. Run long work in the foreground, in resumable
  chunks, and write outputs atomically (temp file, then rename).
- `search.py` once skipped beats by whether their contact sheet existed, so a renamed beat was
  re-searched (which could move its row.col picks) and a changed beat kept stale results. It now
  re-searches only when a beat's queries change; a missing sheet is redrawn from the cache.
- Reusing a beat's footage under a new id: copy its candidates to the new id *and* keep its
  queries identical, so the cache is honored.
- A partial review round (one caption edit) once nearly wiped every earlier decision. Decisions
  merge; `apply_review.py` is tested for exactly that.
- The music re-times per cutdown: the opening runs to the turn, the climax is back-timed from
  `climax_end`. Changing a beat's length moves the music with it.
- Loudness: single-pass loudnorm lands ~2 dB hot here; `mix.py` measures and trims.
