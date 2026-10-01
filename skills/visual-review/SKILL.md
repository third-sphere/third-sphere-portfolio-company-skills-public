---
name: visual-review
description: Build an interactive review page where the user chooses between visual options for several items at once (video clips, photos, images, design variants, thumbnails, headshots, logos, covers), answers a few open decisions, and pastes a JSON export back into chat; then merge the answers and act on them. Use this whenever the user has to pick, swap, approve or compare visual options across more than a couple of items, e.g. "let me choose the clips", "give me an artifact to make the selections", "show me the options side by side", "which photos should we use for each speaker", "I'd swap some of these out", or after you've gathered candidate images or footage and the choice is the user's. Also use it for the next round when they return with changes. This is the visual counterpart of interactive-eval. Use interactive-eval to grade claims in a text deliverable, and this skill when the answer is a choice among things you have to see.
---

# Visual review

The user picks among visual options on a page built for choosing, instead of reading a wall of
descriptions in chat. You curate the options, they choose, they paste a JSON export back, you
merge it and carry on. The loop repeats cleanly for as many rounds as the work needs.

## When it earns its place

Use it when there are several items and each has image options: shots for each beat of a video,
photos for each section of a page, a cover or logo variant per format. For one or two options,
just show them in chat. For grading a text deliverable, use interactive-eval.

## Workflow

1. **Gather and screen options.** Collect candidates per item, then cut the ones that fail on
   something concrete (logos, watermarks, wrong subject, unusable quality, rights problems).
   Mark cuts with `exclude` and a short reason rather than deleting them, so the build reports
   them. Keep usable-but-risky options and put the risk in a tile `flag`. Aim for 4 to 25
   options per item; more than that and the user stops looking.

2. **Write the spec** (`references/spec.md` has the format). Things to get right:
   - `current` marks what's in use now, so the user can keep it at a glance.
   - A fresh `storage_key` and `run` for every page and every round.
   - `max_picks: 1` when an item takes exactly one option; leave it off when order matters
     (the tile numbers become the play order).
   - `text_field` when a caption or label per item is also up for edit.
   - `decisions` for open questions that aren't per item (music, format, tone). Offer real,
     mutually exclusive options with the trade-off in the label.
   Save the spec with the project, not in a temp folder: later rounds reuse it.

3. **Build and check.**
   ```bash
   python3 <skill>/scripts/build_page.py spec.json out/review.html
   python3 <skill>/scripts/check_page.py out/review.html shot.png
   ```
   The build inlines every image (published pages can't load remote images), drops
   excluded options, and refuses pages over 16 MB. The check confirms clicks reach the export,
   answers survive a reload and the page fits a phone. Look at the screenshot yourself before
   publishing; a passing check doesn't prove the options look right.

4. **Publish.** Copy the page to `/mnt/user-data/outputs/` and publish it with the Artifact tool
   (favicon and title optional). Where there's no Artifact tool, present the file.
   Tell the user briefly: what's on the page, what you cut and why, what's flagged, and that
   they paste the JSON back when done. Don't restate every option in chat.

5. **Merge the export** when it comes back.
   ```bash
   python3 <skill>/scripts/merge_export.py state.json export.json
   ```
   This saves the export verbatim under `rounds/` and merges it into the running state:
   decisions merge instead of being replaced, and merging twice changes nothing. Then apply the
   state to the actual work (re-cut the video, update the page, swap the images). Project code
   reads `state.json`; the skill doesn't know what the options mean.

6. **Report and loop.** Say what changed, flag anything the choices put at risk (a pick that
   won't fit, a rights question), and offer another round if items asked for other options
   (`status: wants_other_options`, with the user's `request`).

## Rounds after the first

Build round two from the same spec with a new `storage_key` and `run`. Narrow it to the items
still open, set `current` from the merged state, and add the new options. Never rebuild state
from only the newest export; a round that changes one caption must not erase earlier answers.

## Before building anything unusual

Read `references/lessons.md`. It lists the failures that already happened once: remote images
that silently don't load, shared storage keys, raw multi-hundred-MB file links, and a partial
round that wiped earlier decisions.
