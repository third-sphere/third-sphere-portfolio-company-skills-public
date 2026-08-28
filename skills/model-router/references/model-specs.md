# Model specs — verified reference

**Last verified: 2026-07-24** against `platform.claude.com/docs/en/about-claude/models/`.

This file exists so routing advice cites real numbers instead of remembered ones.
Model lineups move fast and confidently-wrong pricing is worse than saying "let me
check." **If the date above is more than ~6 weeks old, re-fetch before quoting
specifics:**

- `https://platform.claude.com/docs/en/about-claude/models/overview` — the spec table
- `https://platform.claude.com/docs/en/about-claude/models/choosing-a-model` — selection matrix + effort guidance
- `https://code.claude.com/docs/en/desktop-scheduled-tasks` — where per-task model lives

## Contents

- [Spec table](#spec-table)
- [Per-model traps](#per-model-traps)
- [Effort ladder](#effort-ladder)
- [Cost intuition](#cost-intuition)
- [Where model gets set](#where-model-gets-set)

## Spec table

| | Fable 5 | Opus 5 | Sonnet 5 | Haiku 4.5 |
|---|---|---|---|---|
| API ID | `claude-fable-5` | `claude-opus-5` | `claude-sonnet-5` | `claude-haiku-4-5` |
| Positioning (Anthropic's words) | Next-generation intelligence for long-running agents | For complex agentic coding and enterprise work | The best combination of speed and intelligence | The fastest model with near-frontier intelligence |
| Price in / out per MTok | $10 / $50 | $5 / $25 | $3 / $15 (intro $2/$10 through Aug 31 2026) | $1 / $5 |
| Context window | 1M | 1M | 1M | **200k** |
| Max output | 128k | 128k | 128k | 64k |
| Thinking | Adaptive, always on | Adaptive, on by default | Adaptive, on by default | Manual extended thinking |
| Effort ladder | — | `low`→`max`, defaults `high` | supported, defaults `high` | — |
| Reliable knowledge cutoff | **Jan 2026** | **May 2026** | Jan 2026 | Feb 2025 |
| Relative latency | Slowest | Moderate (fast mode avail.) | Fast | Fastest |

Batch API on Opus 5 / Sonnet 5 / Fable 5 supports up to 300k output tokens with the
`output-300k-2026-03-24` beta header — relevant when a job's output is the bottleneck.

## Per-model traps

### Fable 5

- **Older knowledge than Opus 5.** Jan 2026 vs May 2026. Counterintuitive given the
  price and positioning. For anything touching the current state of the world, the
  cheaper model is the fresher one.
- **Silent downgrade on cyber/bio.** Announced safeguards route high-risk-area
  requests to Opus 4.8. Security work on Fable 5 means premium pricing for an older
  model. Never recommend Fable 5 for security review.
- **2× Opus 5 and slower.** Anthropic's own docs frame Opus 5 as "frontier
  intelligence at half the cost of Claude Fable 5." Fable 5 is for when Opus 5 at
  `max` effort has demonstrably failed — not as the default top of a ladder.

### Opus 5

- **Self-verifies.** The docs say to *remove* verification instructions carried over
  from earlier models ("include a final verification step", "use a subagent to
  verify") because they cause over-verification. See `prompt-retrofits.md`.
- **Thinking on by default.** `max_tokens` is a hard cap on thinking + response
  together, so budgets tuned on a no-thinking model can truncate.
- **`thinking: disabled` requires effort `high` or below.** Combining it with
  `xhigh`/`max` returns a 400. Also, with thinking disabled it can occasionally emit
  a tool call as plain text — prefer lowering effort over disabling thinking.
- **Behavioral drift to expect:** longer default deliverables, more progress
  narration, more eager subagent delegation.

### Sonnet 5

- **New tokenizer: ~30% more tokens for the same text** vs Sonnet 4.6. Per-token
  price is unchanged, so equivalent requests cost more and the 1M window holds less
  text. Any token budget or "keep it under N tokens" instruction predating Sonnet 5
  is miscalibrated.
- **Sampling params rejected.** Non-default `temperature` / `top_p` / `top_k` → 400.
  Steer via system prompt instead.
- **Manual extended thinking removed** (`thinking: {type: "enabled", budget_tokens}`)
  → 400. Use adaptive thinking + effort.
- **Assistant prefill unsupported** → 400. Use structured outputs.
- First Sonnet-tier model with real-time cybersecurity safeguards; refusals come back
  as HTTP 200 with `stop_reason: "refusal"`, not an error — worth knowing if a
  pipeline branches on error codes.

### Haiku 4.5

- **200k context, not 1M.** The single most common way a Haiku routing decision goes
  wrong: the work is mechanical, so Haiku looks right, but the payload doesn't fit.
  Check payload size before routing bulk work here.
- **Feb 2025 knowledge cutoff** — meaningfully behind the rest.
- Uses manual extended thinking rather than adaptive.
- Weak on hard multi-step reasoning. Strong on classification, extraction, routing,
  triage, and latency-stable high-volume work.

## Effort ladder

Available on Opus 5 (`low`, `medium`, `high`, `xhigh`, `max`) and recent Sonnet.
Defaults to `high` on the API and Claude Code.

| Level | When |
|---|---|
| `low` / `medium` | Cost-pressured reasoning work. Opus 5 specifically improved quality here — **try Opus 5 at `medium` before dropping to Sonnet 5.** |
| `high` | Default. Fine for most orchestration and drafting. |
| `xhigh` | Documented sweet spot for coding and high-autonomy agentic work. Recommend explicitly for unattended execution; the default undersells it. |
| `max` | Deepest reasoning, Opus 5 only. Pair with a large `max_tokens` so there's room to think and act across tool calls. |

Anthropic's framing, worth repeating to anyone weighing a downgrade: *"Tuning effort
is often a better lever than switching models."*

## Cost intuition

Relative output-token cost, Haiku = 1×:

| Haiku 4.5 | Sonnet 5 | Opus 5 | Fable 5 |
|---|---|---|---|
| 1× | 3× (2× at intro pricing) | 5× | 10× |

Two things this table hides, and both usually dominate it:

1. **Frequency swamps tier.** A weekly Opus 5 run costs less than a 30-minute Haiku
   loop. Compute cost as tier × frequency before arguing about tier.
2. **Context is often the real bill.** Digesting bulk content with a small local
   model before it reaches Claude can cut more cost than any tier change, because
   it removes the tokens rather than repricing them.

The documented cascade pattern for high-volume classification: run Haiku first, re-route
low-confidence results (< ~0.85) to a stronger model. Reported to cut 60–70% of cost on
classification pipelines while preserving accuracy on the hard cases.

## Where model gets set

| Surface | Mechanism |
|---|---|
| Scheduled task / routine | Per-task model picker in **Routines → task → Edit**, beside the instructions box. **Not** in the task's `SKILL.md` (frontmatter holds only `name` + `description`), and **not** exposed by `update_scheduled_task` — so no programmatic batch edit. |
| Interactive session | `/model` at runtime — overrides everything else |
| Session default | `model` field in `settings.json` |
| Environment | `ANTHROPIC_MODEL` env var (overridden by `/model`) |
| Subagent | `model:` field in the agent definition's frontmatter, or the `model` param on the Agent/Task call |
| API | `model` param, plus `output_config.effort` |
