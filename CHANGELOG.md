# Changelog

Versions refer to the `portco-skills` plugin as a whole. Bump the version in
**both** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — a
version set in one and not the other means installed copies never see the update.
`tests/test_plugin_manifest.py` enforces that they agree.

## 1.4.0

- **archive-trailer** — cuts a movie-trailer-style promo (60 s, plus 30 s and 15 s
  cutdowns) entirely from public-domain archival footage: script beats, clip search and
  screening on movingimagearchive.com, clip selection on a review page, face-aware
  letterboxing, cards over or between shots, synthesized trailer hits, a public-domain
  music edit that lands the climax on the turn, a -14 LUFS mix, and cutdowns that re-time
  themselves.

  Built on the premise that archival footage reads as metaphor and modern footage reads as
  fact: a 1939 World's Fair can promise the future, but modern footage of someone else's
  hardware under a card about your product reads as your product. Rights are treated as
  claims to verify, including the layer most people miss — a band transcription of a
  public-domain symphony is its own copyrighted arrangement.

  Every project inherits a set of checks written from real failures: cards too wide for the
  frame, cards on screen too briefly for a slow reader, picks too short to fill their beat,
  faces cut off by the crop, and approvals that silently carry over to a different clip.
  Needs `ffmpeg` and network access; clip-selection pages use a separate `visual-review` skill.
  Title cards can set their own `title_size` and `sub_size`; the renderer and the fit check
  use the same sizes, so a larger title can't slip past the width check.
- **visual-review** — builds a review page for choosing among visual options across many
  items (clips, photos, design variants), answering open decisions, and exporting JSON to
  paste back into chat. Rounds merge rather than replace, so a round that only edits one
  caption can't erase earlier answers. archive-trailer uses it for clip selection.

## 1.3.0

- **model-router** — picks the executor and effort for a unit of work: which Claude
  tier, what effort level, or whether the work belongs on another vendor entirely.
  Built on the asymmetry that makes model choice worth thinking about at all — a
  too-weak model on judgment work doesn't error, it quietly produces a worse answer
  that looks fine — so the default stance is accuracy-first with cost breaking ties.

  Three questions about the work (would a failure be noticed, is judgment happening
  or just transformation, who is watching while it runs), a capability-gate table
  that overrides tier logic, and the effort ladder as the lever to try before
  switching models.

  It deliberately refuses to route on benchmark leads. The frontier coding gap sits
  inside measurement noise and changes hands every few weeks, while switching costs
  are permanent — so "vendor X benchmarks better" is not accepted as a reason to
  move a workflow. The reference tables carry prices and capabilities and no
  leaderboard positions, for the same reason.

  First skill in the bundle that isn't about fundraising, brand, or reporting; the
  plugin description now covers AI operations too.

## 1.2.0

- **startup-deck-generator** — tailors a pitch deck for one named target investor:
  researches the fund, diffs the deck against what that audience needs, builds the
  tailored version on a token-driven HTML shell, and writes the approach strategy.
  Closes the loop the bundle previously left open — `pitch-content-guide` specs deck
  content and stops, `portco-brand-extract` measures the brand, and nothing rendered
  a deck.

## 1.1.0

Licensing. The repo shipped with no LICENSE, which meant that despite being
public, nobody had a granted right to use it.

- LICENSE: Mozilla Public License 2.0, verbatim from mozilla.org
- NOTICE: copyright line, and an explicit statement that the Third Sphere and
  CapStack Compass marks are not licensed (MPL section 2.3)
- `license: MPL-2.0` declared in both manifests, with a CI check that the
  declaration matches the LICENSE file actually present
- README: a plain-language summary of what the license does and does not allow

Why MPL-2.0 rather than MIT or Apache-2.0: modified skills that get distributed
have to stay open, so improvements remain available to the next founder. The
copyleft is file-level, so a portfolio company can combine these skills with
proprietary work and only the files they change carry the obligation. Internal
use and private forks carry no obligation at all.

## 1.0.0

First release as an installable plugin. The seven skills below were already in
this repo; this version packages them for `claude plugin install` and adds
manifest/README consistency checks to CI.

- better-writing
- capstackcompass-public-portco-skill
- founder-update
- pitch-content-guide
- portco-brand-extract
- seed-pitch-kit
- tufte-viz
