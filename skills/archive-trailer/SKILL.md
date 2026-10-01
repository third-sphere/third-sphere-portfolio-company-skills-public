---
name: archive-trailer
description: Make a movie-trailer-style promo (60s, with 30s and 15s cutdowns) cut entirely from public-domain archival footage, with text cards, synthesized trailer hits and a public-domain music track. Covers the whole pipeline - script beats, clip search on movingimagearchive.com, contact sheets, clip selection through a visual-review page, assembly with letterboxing and card treatments, sound design, music edit, loudness, cutdowns, and tests. Use it whenever someone wants a promo, teaser, trailer, sizzle reel or launch video for an event, book, product or company built from archive, stock-free or public-domain footage, or says things like "make a trailer from old footage", "movie-preview style promo", "use the moving image archive", "cut a 30-second version", or wants to revise an archive trailer already in progress (swap clips, change cards, re-time music). Not for editing someone's own footage into a video with no archive component.
---

# Archive trailer

A trailer built from archival footage works because the footage reads as metaphor: a 1939
World's Fair promises the future, a 1920 lumberjack climbs a tree, and the cards say what it all
means for the thing being promoted. This skill is the pipeline for making one, proven on an
event promo and a book promo, then generalized. The scripts carry the mechanics; your job is the
script, the curation and the judgment calls.

Run everything from the **project folder** (or set `TRAILER_PROJECT`). Scripts live in
`<skill>/scripts/`. The companion skill `visual-review` builds the clip-selection pages.

## Workflow

1. **Understand the subject before writing a beat.** Read the source material (the book, the event
   page, the brief). Find its actual argument and the facts the cards may claim. A trailer that
   misstates its subject is worse than none. Note in CONTEXT.md what the cards must never claim.

2. **Scaffold the project.** `python3 new_project.py <folder> "<working title>"` creates
   `script.json`, `CONTEXT.md` (the living project doc; keep it current at every step),
   `.gitignore` and `tests/test_plan.py`. Put the folder under git.

3. **Write the script** in `script.json` (`references/script-format.md`). The shape that works:
   three acts (a setup the footage can show, a complication or wait, a turn into the payoff),
   15 to 18 beats, one card per beat, a title beat last. Cards must stay up long enough for a slow
   reader (0.8 s + 2 words/s by default; `project.reading_time`), so fewer, shorter cards keep the
   runtime down: at that pace, 16 cards make roughly 85 seconds. Long cards wrap to two lines.
   Set `turn_beat` (where the music cuts to the climax) and `title_beat`. Fill `rules`:
   `allowed_names` for anything named on a card, `banned_text` for claims the cards must not make.
   Write two search queries per beat as **concrete visual nouns** ("tall metal humanoid robot at a
   world's fair"), never ideas ("the promise of technology"). The search is visual similarity.

4. **Search, then screen.** `python3 search.py` queries movingimagearchive.com per beat and writes
   `candidates.json` plus `sheets/<beat>.jpg`. Look at every contact sheet. Match scores are flat
   (about 0.25 to 0.29) and rank is not relevance. Re-query weak beats with different concrete
   wording: `search.py` re-searches a beat only when its queries change and otherwise keeps
   the cached results (picks point into them), so edit queries rather than deleting cache. Record cuts
   and risks in `script.json["screening"]` (`excluded`: id→reason, `flagged`: id→note).

5. **Make the first selection yourself**, then let the user choose. Set `picks` per beat from the sheets
   (row.col refs), then `python3 to_review.py round-1` builds and checks a visual-review page. Publish
   it. When the JSON comes back: `python3 apply_review.py export.json`. Decisions merge; nothing is
   lost between rounds. Beats marked "show me other options" get their request as
   `requery_pending`: add it to `queries`, re-run search, and do another round.

6. **Choose music** (`references/music.md`). `python3 find_music.py "<piece or mood>"` searches
   Wikimedia Commons for public-domain recordings; U.S. military band recordings (marked GOV) are
   federal works and the cleanest basis. Download the file into `assets/music/`, then
   `python3 music_map.py <file> --act3 <seconds from turn to end>` suggests `opening_in`,
   `climax_end` and `opening_gain_db`. Listen before trusting it. Record the choice and its rights
   basis in `script.json["music"]` and CONTEXT.md.

7. **Assemble and mix.** `python3 mix.py` builds the picture, the synthesized hits and the music
   bed, mixes to -14 LUFS and writes `build/trailer.mp4`. Cutdowns: define
   `script.json["versions"]["30"]` and `["15"]` (beats kept, per-version durations), then
   `python3 mix.py 30` and `python3 mix.py 15`. The music re-times itself per version.

8. **Check your own work before showing it.** Grab a frame from every segment into a grid and
   look at it: cropped heads (framing is automatic; the checks stop on shots whose faces can't
   all fit, which you then look at and accept with `crop_ok` or fix with `frame_y`), small print
   the contact sheets were too small to show, blown-out shots, unreadable card text,
   dark shots (fix with `in_s` or accept with a written `dark_ok`). Run the project tests:
   `python3 -m unittest discover -s tests -v`. Then deliver, with the weak spots named.

## Judgment calls that matter

- **Metaphor vs. misattribution.** Archival footage under a card about a real product reads as
  metaphor. Modern footage of someone else's product or agency hardware reads as that product.
  Keep modern footage to things that can't be mistaken for the subject.
- **Rights.** The archive says public domain; verify per source (`references/rights.md`).
  Pre-1931 US films are public domain; 1931 to 1977 only without notice or renewal; later only if a
  government work or dedicated. List the picks that need checking.
- **Logos and people.** Cut shots with third-party logos, brand signs, or title cards burned in.
  Flag identifiable people; publicity and endorsement rules apply.
- **Cards carry the claims.** Every card is a claim about the subject. Tie each one to the source
  material and get the subject's owner to OK the lines.

## When something looks wrong

Read `references/lessons.md`. It lists what already went wrong once: the 403 from the video CDN,
white text vanishing on bright footage, a center crop decapitating a robot, background jobs
killed mid-download, single-pass loudness landing 2 dB hot, and a partial review round that
nearly wiped earlier decisions.
