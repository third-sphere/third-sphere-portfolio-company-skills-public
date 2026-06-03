# better-writing — design notes

A skill for structural critique of drafts, derived from the StoryScope study (arXiv:2604.03136v4, 2026).

## What it is
Diagnoses where a draft takes *default, low-risk narrative choices* and proposes concrete structural revisions. Not a line editor or proofreader — those operate on prose, and the source research shows prose-level edits barely change how generic a piece reads.

## Architecture
- `SKILL.md` — the workflow (read → diagnose → separate structural from cosmetic → propose optional revisions → state limits) and the governing philosophy. No scripts, no dependencies, no MCP. Entry point is the description's trigger conditions.
- `references/narrative-features.md` — the 30 discriminating features with human-vs-AI gaps and the per-model fingerprints. Loaded only when the skill needs the specifics, per progressive disclosure.

## Key design decisions (the load-bearing ones)
1. **Rarity, not a "human score."** The central decision. StoryScope's finding is that AI models *converged on a shared region* — they were generic by being central, not by being individually odd. So the skill explicitly refuses to mechanically push drafts toward the "human-elevated" features, because that just builds a new default cluster. It optimizes for intentional, distinctive choices and protects existing voice. If this principle ever gets diluted in editing, the skill stops being useful and becomes a homogenizer.
2. **Structural over cosmetic.** The skill leads with structure (timeline, subplots, withheld revelations, character motive) because the research shows that's where genericness actually lives (editing out clichés/purple prose = 1.6-point detectability drop).
3. **Diagnose, don't auto-rewrite.** Default is feedback + optional moves + short illustrative before/afters, never a silent full rewrite — to preserve the writer's authorship. Full rewrite only on explicit request.
4. **Flag 3–5 things, not everything.** Most gaps are small; an exhaustive critique is noise. Calibrate to what the piece is trying to be (a clean causal chain is a virtue in a thriller).
5. **Honest about limits.** "More human" ≠ "better." Tendencies, not rules.

## Evaluation
Subjective skill (writing quality), so per skill-creator guidance it's evaluated qualitatively, not with pass/fail assertions. Sanity-test by running it on real drafts of varied form (literary short story, genre scene, personal essay) and checking that it (a) leads with the strongest structural lever, (b) doesn't homogenize voice, (c) stays quiet when a draft is already strong.

## Changelog
- v0.1 — initial draft. 30-feature reference + structural-critique workflow.
