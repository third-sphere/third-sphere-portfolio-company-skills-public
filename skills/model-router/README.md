# model-router

Choose the model, execution surface, and effort for a unit of work, in Claude or
Codex. Keep the current executor unless capability, task evidence, quota, or total
cost warrants a switch. Respect explicit model choices and preserve required
verification.

## About

The skill separates four things: the requirements of the work, the execution
paths actually available, the quality and effort the work needs, and how the
result gets checked. Provider facts are dated and scoped, and anecdotes are not
treated as hard rules. Privacy, current-information needs, and test coverage are
assessed for the actual workflow rather than mapped permanently to a vendor.

A recommendation alone never authorizes dispatching work or changing settings.
When the request already authorizes the action, the skill applies it through the
available settings tools or offload skills and reads back the effective model and
effort.

## Usage

Trigger it by saying things like:

- "Which model should I use for this?"
- "Is this an Opus task, or can it run on Haiku?"
- "Audit the models on my scheduled tasks"
- "Should I offload this, or keep it here?"
- "Is this a Gemini job?"

It also applies unasked wherever the model is a silent free parameter: writing a
scheduled task, producing a handoff or offload brief, or spawning subagents.

**A note on the numbers.** Prices, context windows, and effort defaults have a
shelf life measured in weeks. Each reference file dates its facts, and
`references/evidence.md` sets a six-week refresh ceiling. Recheck a decisive fact
before quoting it.

## Reference files

- `references/model-specs.md`: Claude models, prices, limits, effort defaults, and dated per-model caveats.
- `references/non-claude-executors.md`: OpenAI/Codex, Gemini, MiMo, and local Gemma.
- `references/execution-surfaces.md`: sessions, schedules, workers, and verifying a change took effect.
- `references/prompt-retrofits.md`: prompt changes when the model changes, without dropping checks.
- `references/evidence.md`: what counts as evidence, freshness rules, and an optional market feed.

## Dependencies

None. Reference-only skill: no MCP servers, API keys, or routing service required.

## Changelog

### v2.3.0 — 2026-10-01

Rewrite of the routing approach, plus a fact refresh for Claude Opus 5.5 and
Sonnet 5.5.

- **Routing on evidence, not vendor rules.** Keeps the current executor unless
  task evidence, capability, quota, or total cost justifies a change, and applies
  the same rule in Claude and Codex. Fixed vendor preferences and capability gates
  that named one vendor are replaced by scoped, dated facts and task results.
- **Verification travels with the work.** A model change preserves acceptance
  tests, permission checks, and required review. A cheaper or unproven route needs
  an observable escalation trigger, not a promise to escalate once someone notices.
- **Recommend versus apply.** A recommendation authorizes nothing. When the
  request does, the change is applied with available tools and read back.
- **New references:** `execution-surfaces.md` and `evidence.md`.
- **Tier table** dated and marked as observed fits: Haiku 4.5 (retires no sooner
  than 2026-10-15), Sonnet 5.5, Opus 5.5, and Fable 5.1.
- **Claude facts:** Opus 5.5 and Sonnet 5.5 added, with caveats on early stops in
  unattended runs, thinking portability across models, refusal categories, effort
  defaults, and the moved `sonnet` alias in Claude Code.
- **Other executors:** GPT-6 Astra specs, long-prompt pricing, and an availability
  caveat; Gemini data terms and price floor; MiMo and local Gemma marked as
  needing verification before use.
- **Prompt retrofits** for GPT-6 Astra, Claude Opus 5.5, and Claude Sonnet 5.5.

### v1.0.0 — 2026-08-28

Initial public release.
