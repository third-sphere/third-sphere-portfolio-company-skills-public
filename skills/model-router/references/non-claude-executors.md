# Non-Claude executors — verified reference

**Last verified: 2026-07-26.** Same staleness rule as `model-specs.md`: if that date is
more than ~6 weeks old, re-fetch before quoting numbers. This space moves faster than
the Claude lineup does.

## Contents

- [The frontier coding gap is noise — don't route on it](#the-frontier-coding-gap-is-noise)
- [Google Gemini](#google-gemini)
- [OpenAI / Codex](#openai--codex)
- [MiMo (Xiaomi)](#mimo-xiaomi)
- [Local: Gemma 4 E4B on MLX](#local-gemma-4-e4b-on-mlx)
- [Capability gates — the only hard routing rules](#capability-gates)
- [Cross-vendor price floor](#cross-vendor-price-floor)

## The frontier coding gap is noise

Between July 9 and July 24 2026 the top spot on Artificial Analysis's Coding Agent Index
changed hands twice: GPT-5.6 Sol in Codex took it from Fable 5, then Opus 5 in Claude Code
drew level. SWE-bench Verified is saturated at ~96–97% for both and carries almost no
decision-relevant signal.

**So "vendor X is better at coding" is not a valid reason to move a workflow.** The delta is
inside measurement noise, it inverts every few weeks, and switching costs — CLAUDE.md files,
skills, MCP servers, hooks, accumulated prompt tuning — are real and permanent. Route on
capability gates, price floors, quota, privacy, and diversity. Those are stable. Benchmark
leads are not.

## Google Gemini

Current lineup (paid tier, USD per 1M tokens, Standard SKU):

| Model | ID | In | Out | Context | Notes |
|---|---|---|---|---|---|
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | $2 (≤200K) / $4 (>200K) | $12 / $18 | 1M | **Preview only, no GA.** Doubles price above 200K. |
| Gemini 3.6 Flash | `gemini-3.6-flash` | $1.50 | $7.50 | 1M | Newest workhorse (2026-07-21) |
| Gemini 3.5 Flash | `gemini-3.5-flash` | $1.50 | $9.00 | 1M | |
| **Gemini 3.5 Flash-Lite** | `gemini-3.5-flash-lite` | **$0.30** | **$2.50** | 1M | Newest cheap tier; much stronger than 3.1 |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | **$0.25** | **$1.50** | 1M | Cheapest anywhere |
| 2.5 family | — | — | — | — | **Shuts down 2026-10-16** |

**Structural fact worth knowing:** Google's frontier tier is stale — Pro is preview-only at
3.1 with no GA path, unrefreshed for five months, while all investment goes into Flash. Don't
plan around a Gemini Pro tier.

**Knowledge cutoff is the catch.** Model cards claim March 2026 for the newest models but add
verbatim that in some domains "the model's knowledge is limited to January 2025." Treat Gemini
as effectively **Jan 2025 with patchy 2026 coverage** — a 16-month gap behind Opus 5.

**Thinking:** `thinking_level` enum (`minimal`/`low`/`medium`/`high`). No token budgets —
passing both 400s. Cannot be fully disabled on any 3.x model; `minimal` is the floor.

**Traps:**
- **Free tier trains on your data and permits human review.** The ToS says so in bold: *"Do not
  submit sensitive, confidential, or personal information to the Unpaid Services."* Paid tier
  (any active billing account) does not train and has no human review. **Never route real data
  through the free tier.** No ZDR equivalent to Anthropic's.
- Rate limits are no longer published — sign-in gated at AI Studio. Plan for 429 backoff.
- `temperature`/`top_p`/`top_k` deprecated and ignored on 3.x.
- Thought signatures must be echoed back unmodified on function calling, and echoing them
  increases your input bill.
- Mismatched `FunctionResponse` IDs make `generateContent` silently return empty with
  `finish_reason: STOP` — a nasty silent failure.
- Safety filters default to **OFF** on 2.5 and 3.x — opt-in, not opt-out.

**Where Gemini genuinely beats Claude** (see [capability gates](#capability-gates)): video and
audio input, the price floor, a real free tier, native Search/Maps grounding, and throughput.

**Where the advantage is fake:** context is a tie at 1M and Claude is *cheaper at length*
(Anthropic doesn't surcharge long prompts; Gemini 3.1 Pro doubles above 200K). Claude wins max
output (128K vs 65K, 300K via batch beta) and knowledge cutoff. Mid-tier price is roughly a
wash once Claude's tokenizer inflation is accounted for — compare cost-per-task, not
cost-per-token.

## OpenAI / Codex

Current family is **GPT-5.6** (July 9 2026): `gpt-5.6-sol` $5/$30, `gpt-5.6-terra` $2.50/$15,
`gpt-5.6-luna` $1/$6. All 1.05M context, 128K max output, **Feb 2026 cutoff**. Prompts over
272K tokens bill at 2× input / 1.5× output for the whole request. Reasoning effort ladder:
`none`/`low`/`medium`/`high`/`xhigh`/`max`, plus an **Ultra** level in Codex that adds
automatic subagent delegation.

**Codex is a product family, not a model:** CLI (Rust, open source), IDE extensions, desktop
app, cloud VMs, iOS, and GitHub/Slack/Linear integrations — all sharing one account and one
5-hour rate-limit window. Included in ChatGPT Plus ($20) and above; API-key auth gets
CLI/SDK/IDE only, **no cloud features**.

`AGENTS.md` is the `CLAUDE.md` analogue — auto-loaded, hierarchical, scaffolded by `/init`.
Headless mode is well developed: `codex exec "<task>"`, `--json` for a JSONL event stream,
`--output-schema` for schema-conformant output, read-only sandbox by default.

**Documented behavioral profile** (from practitioner reports, not controlled studies): faster
and more token-efficient per task, strong on terminal/CLI/infra, steadier over long unattended
runs. Against that: **sprawling diffs** — it edits adjacent files it decides need updating,
which is expensive to review when the assumption was wrong — plus inefficient repo search and
weak frontend/visual iteration.

**What's actually worth sending to Codex**, given the gap is noise:

1. **A second, independent PR reviewer.** `@codex review` on GitHub. The value is *model
   diversity* — different family, different blind spots — not superiority. Highest-value item
   here, cheap and async.
2. **Overflow capacity when rate-limited.** A separate quota pool. The most common real reason
   people run both.
3. **High-volume mechanical grunt work** — codegen from schemas, mass codemods, dependency
   bumps, test scaffolding. Luna is cheap, and this work has cheap verification (tests pass or
   don't), which neutralizes the sprawling-diff problem.
4. **Terminal/CLI/infra tasks** — the one edge that has held steady across index revisions.
5. **Adversarial second opinion on a stuck bug** after the primary agent has burned two sessions.

**Don't** send it architecture, large cross-cutting refactors, or frontend work — its documented
weak spots.

## MiMo (Xiaomi)

**MiMo-V2.5-Pro** (Apr 2026): 1.02T total / 42B active MoE, 1M context, text-only, MIT
open weights. **MiMo-V2.5** (non-Pro): 310B/15B, omnimodal. **MiMo Code** is the CLI agent (a
fork of OpenCode); **MiMo Auto** is the zero-config channel inside it.

Pricing direct from Xiaomi: Pro $0.435/M in, $0.87/M out, and **$0.0036/M on a cache hit** —
a 99% discount, which is the real story. One measured run reported a 96.3% cache-hit rate
across 125 autonomous sessions. (OpenRouter's $1/$3 listing is stale — go direct.) Exposes an
**Anthropic-compatible endpoint**, so swapping `ANTHROPIC_BASE_URL` points Claude Code at MiMo.

⚠️ **Two live constraints:**
- **The free MiMo Auto window closed 2026-07-26.** Continued use needs a Token Plan
  subscription (Lite $6 / Standard $16 / Pro $50 / Max $100 monthly) or pay-as-you-go.
- **Token Plan is contractually limited to interactive coding tools.** Xiaomi's docs prohibit
  using Token Plan keys for "automated scripts and custom application backends" and reserve
  the right to ban the key. A human-in-the-loop paste workflow is fine; a scripted/headless
  one needs pay-as-you-go.

**Honest capability read:** genuinely at the top of *open-weights*, meaningfully behind
frontier. Xiaomi's own comparisons are against Sonnet 4.6 — not Opus — and were run inside
Xiaomi's harness. Independent AA scoring puts it #5 in its open-weights class, with
below-average speed and above-average verbosity.

**Failure modes that matter for an executor role:**
- **Chain-of-thought infinite loops** — the signature MiMo failure. A documented case burned
  569s emitting 1,803 identical repetitions and **zero output tokens**. Trigger was a one-word
  ambiguous instruction on top of contradictory harness rules. Mitigation:
  `repetition_penalty=1.2`. Note this presents as a long-running turn producing *nothing*, not
  as a missing commit — so a monitor watching for commits won't catch it.
- **Premature "done."** Xiaomi names this itself; the `/goal` verifier subsystem exists to catch
  it. This is the #1 risk in unsupervised execution.
- Instruction-following degrades with context length; code-quality regressions and logic bugs
  reported by community reviewers.

**What a MiMo spec must eliminate: ambiguity and internal contradiction.** No optional or
conditional items — every task binary and ordered. Never two rules that can conflict. Explicit
file allowlist and do-not-touch list. One named exemplar file per pattern rather than a
described pattern. A machine-checkable definition of done plus an explicit stop condition.

Safe unsupervised: mechanical multi-file implementation from a fully-decided design,
scaffolding, tests against a stated contract, migrations, boilerplate. Expect drift on anything
requiring a judgment the spec didn't make.

## Local: Gemma 4 E4B on MLX

`mlx-community/gemma-4-E4B-it-qat-4bit` — Gemma 4 (Apr 2026, Apache 2.0), instruction-tuned,
quantization-aware-trained, 4-bit MLX conversion.

**"E4B" = effective parameters: 8B total with embeddings, 4.5B effective.** The mechanism is
Per-Layer Embeddings, *not* MatFormer (that was Gemma 3n). Practically: you pay 8B-scale memory
for 4.5B-scale compute. ~6.8 GB on disk; budget ~7–8 GB resident before context.

**Context is 128K officially — not 256K** (that's the 12B+ models). On 16 GB unified memory,
plan ~16–32K comfortable, 64K tight.

**The quant matters more than expected.** QAT beats post-training quantization only if the
downstream conversion respects the QAT lattice, and a uniform 4-bit cast partly throws that
away: measured 90.94% top-1 agreement with BF16, versus 98.54% for a dynamic quant.
`mlx-community/gemma-4-e4b-it-qat-OptiQ-4bit` is a strict upgrade at +0.7 GB — biggest gains in
long context (+2.0) and instruction following (+1.3).

**What to trust it with:**

| Task | Verdict |
|---|---|
| Classification against a closed label set | **Trust** — strongest use |
| Semantic filtering / per-chunk relevance | **Trust** — this is classification |
| Single-doc summarization ≤16K | **Trust** |
| PII redaction | **Trust with a deterministic backstop** — pair with regex/NER; never the sole compliance gate |
| Structured extraction → JSON | **Conditional** — ~70% on *simple* schema benchmarks. Validate and retry; flat schemas, enums over free strings |
| Translation | Gist yes, publication no |
| Prose writing | **Escalate** — competent but generic |
| Extraction from >32K transcripts | **Do not trust** — see below |

**The hard floor is long-context recall:** 25.4% on MRCR v2 8-needle at 128K; 34% HashHop on
this quant. **Chunk aggressively — cap extraction passes at ~16K tokens.** This is the single
biggest quality lever, bigger than the quant choice. The failure mode is *omission, not
fabrication*: a long transcript silently drops records rather than erroring.

**Also:** instruction-following degrades with constraint count (~68% IFEval strict), so split
multi-constraint prompts into single-purpose passes. Safe when *transforming provided text*,
unsafe whenever *recalling* anything — world knowledge is thin at this size.

## Capability gates

These are the only hard rules. Everything else is a judgment call, but these override tier
logic entirely because one option can do the thing and the others cannot.

Each row names the **constraint**, not the vendor. Where a vendor appears it is an example of
something that satisfies the row, not the only thing that does — the exception being the rows
that force *onto* Claude, where the constraint genuinely is Anthropic-specific.

| Requirement | Forces | Why |
|---|---|---|
| **Video or audio input** | Off Claude | Claude is text+image only; animated formats use the first frame only. Categorical gap. Gemini is the default pick — many models now accept video, distinctly fewer accept audio, so check the specific modality. |
| **Raw content must never leave the machine** | A local model | The only option with no network hop. Redaction before anything else sees it. |
| **Current-world knowledge** | Claude Opus 5 | May 2026 cutoff beats GPT-5.6 (Feb 2026) and Gemini (effectively Jan 2025). |
| **Zero data retention / no-train guarantee** | Claude | Anthropic doesn't train on API traffic at any tier and offers ZDR. Gemini's free tier explicitly does train and permits human review. |
| **One response over 128K tokens** | Claude batch, or off Claude | Claude's synchronous ceiling is 128K; batch reaches 300K via `output-300k-2026-03-24`. Several non-Claude models exceed 128K synchronously, so batch is no longer the only route. Gemini is *not* one of them — it caps at 65K. |
| **Sub-$0.30/MTok input at 1M context** | Off Claude | No Claude model exists in this band; Haiku is 4× the price with 200K context. Gemini Flash-Lite is the stable occupant; cheaper entrants churn, so verify one before quoting it. |
| **A genuinely independent second opinion** | Any *other* vendor | Diversity is the product. A second Claude shares Claude's blind spots. |

## Cross-vendor price floor

Output-token cost, cheapest first. Use for order-of-magnitude reasoning only — cost-per-*task*
diverges from cost-per-token because of tokenizer and verbosity differences.

**This table is scoped to the executors above — the ones actually under consideration — not to
the whole market.** Cheaper models than these exist at any given moment, and the bottom of the
open-weights market re-sorts monthly. That churn is not decision-relevant: the reason to reach
for the floor is that a *specific* cheap executor is already set up and trusted for mechanical
bulk, not that it is this week's cheapest. Chasing the true minimum means re-qualifying an
executor every month for a saving that rounds to nothing on the volumes this table describes.

| Executor | $/MTok out | Notes |
|---|---|---|
| Local Gemma 4 E4B | **$0** | Free and private; ~4.5B-effective quality ceiling |
| MiMo V2.5-Pro (cache hit) | $0.0036 in | Cache economics dominate; 96%+ hit rates reported |
| Gemini 3.1 Flash-Lite | $1.50 | Cheapest hosted anywhere, 1M context |
| Gemini 3.5 Flash-Lite | $2.50 | Much stronger than 3.1 for +67% |
| Haiku 4.5 | $5 | 200K context is the constraint |
| GPT-5.6 Luna | $6 | |
| Gemini 3.6 Flash | $7.50 | |
| Sonnet 5 | $10 → $15 Sept 1 | |
| GPT-5.6 Terra | $15 | |
| Opus 5 | $25 | |
| GPT-5.6 Sol | $30 | |
| Fable 5 | $50 | |
