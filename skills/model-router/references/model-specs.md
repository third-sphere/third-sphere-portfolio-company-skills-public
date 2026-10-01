# Claude facts

**Verified: 2026-09-06; Opus 5.5 row 2026-09-23; Sonnet 5.5 row, effort
sentence, and Haiku 4.5 retirement 2026-09-29. Scope: direct Claude API**, unless stated otherwise.
These are a dated starting point, not a model lock. Recheck decisive facts under
[evidence rules](evidence.md); discover account availability separately.

| Model | Direct API ID | Input/output USD per million tokens | Context / max output |
|---|---|---|---|
| Fable 5.1 | `claude-fable-5-1` | $10 / $50 | 1M / 128K |
| Opus 5.5 | `claude-opus-5-5` | $4 / $20 (cache read $0.20) | 1M / 128K |
| Opus 5 (previous) | `claude-opus-5` | $5 / $25 | 1M / 128K |
| Sonnet 5.5 | `claude-sonnet-5-5` | $2 / $10 (cache read $0.20) | 1M / 128K |
| Sonnet 5 (previous) | `claude-sonnet-5` | $2 / $10 | 1M / 128K |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | $1 / $5 | 200K / 64K |

The overview lists text/image input and text output for this lineup. Haiku does
not support the effort control. Opus 5.5 defaults to `medium` effort and its
thinking is always on (adaptive; it cannot be disabled). Sonnet 5.5 defaults to
`high` in the API but `medium` in Claude Code and the Claude apps; its thinking
is adaptive by default, and its lowest setting is `between_tools` (`disabled`
is rejected). The other listed models default to `high` in the API. Effort names are not equivalent across
models: Opus 5.5 thinks more per turn at a given level than Opus 5. Anthropic
recommends starting with Opus 5 and considering Fable 5.1 when demanding work
or evaluations warrant it (verified 2026-09-06; the Opus 5.5 launch makes it the
current Opus). This is provider guidance, not a reason to move a successful
Codex workflow.

Source: [Claude model overview](https://platform.claude.com/docs/en/models/overview).
Opus 5.5 (verified 2026-09-23): [announcement](https://www.anthropic.com/claude-opus-5-5),
[what's new](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5),
[migration guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide),
[effort](https://platform.claude.com/docs/en/build-with-claude/effort).
Sonnet 5.5 (verified 2026-09-29): [announcement](https://www.anthropic.com/claude-sonnet-5-5),
[migration guide](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide).

**Haiku 4.5 retires "not sooner than October 15, 2026"** per the overview
(verified 2026-09-29), and Haiku 5.5 has not shipped. Before routing new
unattended work to Haiku 4.5, name what replaces it on retirement; a pinned
`claude-haiku-4-5-20251001` stops working, and the `haiku` alias will move.
Prices above exclude caching, batch, and other billing variations. Verify the
specific route before estimating cost; do not infer subscription pricing.

## Dated per-model caveats

**Verified: 2026-09-03. Scope: direct Claude API.** Observed behaviors and
published rates from the Fable 5.1 launch cycle, retained because each one
changed a routing decision. Recheck any that decides a close call;
[evidence rules](evidence.md) apply.

- **Sonnet 5 tokenization.** Its tokenizer produces roughly 30% more tokens for
  the same text than earlier Sonnets. Token budgets and cost estimates carried
  over from those models under-provision it.
- **Opus 5 self-verification.** It verifies its own work by default, so a generic
  "check your work" instruction tends to buy a second pass rather than more
  assurance. Keep the observable acceptance checks; drop only the generic
  reminder, and only with evidence it is causing waste.
- **Fable 5.1 cache reads at $0.25 per million** — half Opus 5's $0.50, against
  2× Opus 5 on uncached input and output. A long agentic loop that replays the
  same context can land below what list price implies, so price the actual task
  instead of comparing headline rates.
- **Fable 5.1 cyber safeguards.** Exploit generation, pen-testing, and some
  binary vulnerability scanning are restricted or redirected; defensive
  vulnerability discovery is allowed. This is a scoped activity restriction, not
  grounds to exclude a model from defensive security review, and not a reason to
  move a task to a surface that would evade the safeguard.

**Verified: 2026-09-23. Scope: direct Claude API unless stated.** From the Opus
5.5 launch cycle. Each can change a routing or handoff decision; recheck any that
decides a close call.

- **Opus 5.5 unattended runs can end early.** A turn may end (`end_turn`) with a
  text-only progress report while work is still owed. Unattended work needs a
  completion checklist and a run summary so an early stop is visible, not
  silent. Source: [prompting Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5).
- **Opus 5.5 narration moves into thinking.** Text between tool calls now arrives
  as `thinking` blocks, empty at the default display. Code or transcript mining
  that parsed that text, or read `content[0]` as text, needs to select blocks by
  type. Source: [migration guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide).
- **Opus 5.5 thinking portability.** Only Fable 5.1 and Mythos 5.1 read Opus 5.5
  thinking, and Opus 5.5 does not read Fable or Mythos thinking. Moving a
  conversation from Opus 5.5 to any other model, Opus 5 included, continues
  without its earlier reasoning. The request does not fail, but continuity is
  lost, so a handoff or fallback brief must be self-contained. Source:
  [migration guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide).
- **Opus 5.5 refusal categories.** `bio` and `reasoning_extraction` are new,
  alongside `cyber`. A refusal returns HTTP 200 with `stop_reason: "refusal"`
  and names the category in `stop_details.category`. Prompts that ask for
  reasoning written into the output can be refused. Server-side fallback
  (`fallbacks: "default"`, beta) does not retry `reasoning_extraction` refusals.
  Source: [what's new](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5).
- **Haiku 5.5 is announced but pending** ("in the coming weeks"; Sonnet 5.5
  has shipped, see below). Until it ships, Haiku 4.5 is the current
  tier. Re-verify this file when it ships, and re-check any route that uses the
  `haiku` alias, because a silent alias upgrade is a behavior change. Source:
  [Sonnet 5.5 announcement](https://www.anthropic.com/claude-sonnet-5-5).

**Verified: 2026-09-29. Scope: direct Claude API unless stated.** From the
Sonnet 5.5 launch. Source for each: [migration guide](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)
unless noted.

- **The `sonnet` alias has moved (Scope: Claude Code).** On the Anthropic API
  provider it resolves to Sonnet 5.5, from Claude Code v2.1.284; on Bedrock,
  Google Cloud, Foundry, and Claude Platform on AWS it still resolves to an
  older Sonnet. Any route using the alias on the Anthropic API now runs Sonnet
  5.5, a behavior change: re-check it against its acceptance checks rather than
  assuming Sonnet 5 results carry over. What other surfaces (Cowork, the apps)
  resolve it to is unverified. Source: [Claude Code model configuration](https://code.claude.com/docs/en/model-config).
- **Sonnet 5.5 thinking portability.** It reads thinking from Sonnet 5, Opus 4.8,
  Haiku 4.5, and earlier models, but not from Opus 5, Opus 5.5, Fable, or Mythos.
  An Opus 5.5 → Sonnet 5.5 handoff or delegation starts without the Opus
  reasoning, so the brief must be self-contained. Its thinking blocks also work
  only in the account that produced them (or a linked account), including when
  switching accounts mid-session in Claude Code.
- **Sonnet 5.5 refusal categories and fallback.** Declines can name `cyber`,
  `bio`, `frontier_llm`, `reasoning_extraction`, or `general_harms`; benign work
  can trigger `general_harms`. Server-side fallback (beta) retries only `cyber`
  and `frontier_llm`, on Sonnet 5; higher-risk cyber work visibly falls back to
  Sonnet 5. Routine bug finding and fixing is unaffected. Source also:
  [announcement](https://www.anthropic.com/claude-sonnet-5-5).
- **Sonnet 5.5 thinking controls.** `thinking: {type: "disabled"}` returns a 400;
  `between_tools` is the lowest setting and is accepted only at `high` effort or
  below. With `between_tools`, effort cannot change mid-conversation. Effort
  levels are recalibrated against Sonnet 5; re-run the effort sweep and
  re-baseline cost.

## Effort and execution

**Verified: 2026-09-06. Scope: Claude Code.** The documented effort scale is
calibrated per model. Model selection and effort can be changed through session
controls, but persistence and supported values depend on the control and version.
Inspect the installed surface before applying changes. Do not assume an API
level is accepted in persistent settings.

Source: [Claude Code model configuration](https://code.claude.com/docs/en/model-config).

No model-specific instruction here removes verification or guarantees recall,
security-review suitability, or current-world knowledge. For a migration,
consult the selected model's current migration documentation for parameter
compatibility rather than carrying forward unverified historical traps.
