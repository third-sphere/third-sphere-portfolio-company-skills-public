# model-router

Pick the executor and the effort level for a unit of work — which Claude tier, what effort, or whether the work belongs on another vendor entirely.

## About

The model is a parameter of the work, not a preference. Picking it well costs a minute of thought and changes the outcome more than most prompt edits do. Picking it badly is usually invisible: a too-weak model on judgment work doesn't error, it quietly produces a worse answer that looks fine.

That asymmetry is what the skill is built around, and it sets the default stance — **accuracy-first, cost breaks ties.** Down-tier only where judgment genuinely isn't happening, and never to save money on work whose failures are silent.

Routing runs on three questions about the *work* rather than the tool:

1. **If this went wrong, would anyone notice?** A build that breaks is a cheap failure — the failure is the alarm. A misrouted record or a plausible-but-wrong number is expensive, because nothing errors and the mistake compounds.
2. **Is judgment happening, or just transformation?** The tell for judgment: you can't write the assertion that would grade it.
3. **Who is watching while it runs?** An unattended hourly task deserves a better model than something you're reading turn by turn, because there the human is the error-correction loop.

Ahead of those sits a short table of **capability gates** — requirements with exactly one answer (video or audio input, data that can't leave the machine, current-world knowledge, a no-train guarantee) which override the tier discussion entirely.

The skill also pushes the **effort ladder** as the lever people skip: try Opus 5 at `medium` before dropping to Sonnet 5, and use `xhigh` for unattended coding, where the default `high` undersells it. Per Anthropic's own guidance, tuning effort is often a better lever than switching models.

Two deliberate refusals are worth knowing about, since both look like missing features:

- **It won't route on benchmarks.** The frontier coding gap is inside measurement noise and changes hands every few weeks, while switching costs — context files, skills, MCP servers, accumulated prompt tuning — are real and permanent. "Vendor X benchmarks better" is not accepted as a reason to move a workflow; capability gates, price floors, quota, privacy, and diversity are.
- **It treats the doctrine as reasoning, not data.** Prices belong in the reference files and are expected to rot. The three questions and the invisible-failure asymmetry do not get revised because a price moved.

Finally, changing the model means editing the prompt. A tier is not a drop-in swap — prompts carry instructions that were workarounds for a specific model's weaknesses, and those don't become harmless when the weakness goes away. The one that bites most often: **strip "include a final verification step" when moving up to Opus 5**, which verifies its own work and will otherwise charge you twice for one check.

## Usage

Trigger this skill by saying things like:

- "Which model should I use for this?"
- "Is this an Opus task, or can it run on Haiku?"
- "Audit the models on my scheduled tasks"
- "Should I offload this, or keep it here?"
- "Is this a Gemini job?"

It also applies unasked wherever the model is a silent free parameter — writing a scheduled task or routine, producing a handoff or offload brief, and spawning subagents. Subagent fan-out is the highest-frequency, lowest-visibility model decision there is: ten searches on the wrong tier is ten times the mistake.

**A note on the numbers.** Every price, context window, and cutoff here has a shelf life measured in weeks. Each reference file carries a *last verified* date and a rule to re-fetch if it's more than about six weeks old — please honor it rather than quoting from the file on faith. Model lineups move fast, and confidently-wrong pricing is worse than saying "let me check."

## Reference files

- `references/model-specs.md` — Claude specs, prices, context windows, cutoffs, per-model traps, and where the model gets set on each surface (routine, session, subagent, API).
- `references/non-claude-executors.md` — Gemini, OpenAI/Codex, MiMo, and small local models: lineups, pricing, what each is genuinely good at, and the failure modes that matter when one is doing the work unsupervised.
- `references/prompt-retrofits.md` — the prompt edits each model change requires, organized by the direction of the move, plus a retrofit checklist.

## Dependencies

None. Reference-only skill — no MCP servers, API keys, or network access required.

## Changelog

### v1.0.0 — 2026-08-28
Initial public release.
