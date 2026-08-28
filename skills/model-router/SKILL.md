---
name: model-router
description: "Pick the executor and effort for a unit of work — which Claude tier (Fable 5 / Opus 5 / Sonnet 5 / Haiku 4.5), what effort level, or whether it belongs on another vendor entirely: Gemini, OpenAI/Codex, MiMo, or the local Gemma. Use whenever a model or executor choice is being made or implied: \"which model should I use\", \"is this an Opus task\", \"should this run on Haiku\", \"what model for this scheduled task\", \"audit my tasks' models\", \"should I offload this\", \"is this a Gemini job\", \"send this to Codex\". Use PROACTIVELY, unasked, when about to (a) write or revise a scheduled task or routine, (b) produce a handoff, first prompt, or offload brief, (c) spawn subagents where the model is a free parameter, or (d) advise on a prompt whose cost, privacy, or reliability is in question. Also use when changing models, since a tier change usually needs prompt edits too. Not for prompt wording once the executor is already fixed, or for the mechanics of an offload after the executor is chosen."
---

# model-router — choose the executor before you write the prompt

The model is a parameter of the work, not a preference. Picking it well costs one
minute of thought and changes the outcome more than most prompt edits do. Picking
it badly is usually invisible: a too-weak model on judgment work doesn't error,
it just quietly produces a worse answer that looks fine.

That asymmetry sets the default stance: **be accuracy-first and let cost break
ties.** Down-tier only where judgment genuinely isn't happening. Never down-tier
to save money on work whose failures are silent.

Before you route, read [references/model-specs.md](references/model-specs.md) for
the current verified Claude numbers, and
[references/non-claude-executors.md](references/non-claude-executors.md) when any
other vendor is in play. Don't route from memory; these lineups move fast and
stale numbers produce confidently wrong advice.

For any **non-Claude price, context window, modality, or max-output figure**,
check the vendor's own pricing page before you quote it. The tables in this skill
are hand-maintained and they drift — a stale price is the most common way this
skill gives confidently wrong advice.

## First: is there a capability gate?

Most routing is a judgment call, but a few requirements have exactly one answer.
Check these before anything else — a gate overrides the whole tier discussion,
because one option can do the thing and the others cannot.

A gate names the **constraint that is forced**, not the vendor that happens to
satisfy it today. Those are different claims with different shelf lives, and
conflating them is how this table went wrong once already — see the note below.

| Requirement | Forces | Why |
|---|---|---|
| Video or audio input | **Off Claude** | Claude is text + image only — a categorical gap, not a quality difference. Gemini is the default pick; many models now take video, considerably fewer take audio. |
| Raw content must never leave the machine | **A local model** | The only option with no network hop. |
| Current-world knowledge | **Claude Opus 5** | May 2026 cutoff beats GPT-5.6 (Feb 2026) and Gemini (effectively Jan 2025). |
| No-train guarantee / ZDR | **Claude** | Gemini's *free* tier trains on submissions and permits human review. |
| One response over 128k tokens | **Claude batch, or off Claude** | Claude's synchronous ceiling is 128k; batch reaches 300k via beta header. A number of non-Claude models exceed 128k in a single synchronous call. |
| Under $0.30/MTok input at 1M context | **Off Claude** | No Claude model exists in that band. Gemini Flash-Lite is the stable default; cheaper entrants appear and vanish monthly, so verify before quoting one. |
| A genuinely independent second opinion | **Any other vendor** | A second Claude shares Claude's blind spots. Diversity is the product. |

**Verify a row before quoting it.** A gate is stated as single-answer, so a stale
gate doesn't degrade a recommendation — it inverts it.

The rows that rot are the ones that named a vendor. Three of them did, and all
three broke the same way: the sub-$0.30 band, the video/audio gate, and the 128k
output ceiling were each written as "forces Gemini" or "forces Claude batch," and
each became wrong the moment a fourth vendor shipped something comparable — while
the underlying constraint ("Claude cannot do this") stayed perfectly true. The
fix was to move the vendor out of the *Forces* column and into the *Why*, where
it is an example rather than a rule.

So when you add a gate, write the capability Claude does or doesn't have. If you
catch yourself naming a vendor in the Forces column, you are recording this
month's market rather than a routing rule.

No gate? Then work the three questions.

## The three questions, in order

Ask these about the *work*, not the tool. They resolve most cases faster than a
tier table does.

### 1. If this went wrong, would anyone notice?

This is the question that matters most, and it's the one people skip.

**Invisible failures** — a contact misrouted to the wrong todo list, a security
finding not surfaced, a metric that's plausible but wrong, an investor update
that reads slightly off, a "no issues found" that was really "didn't look hard
enough." Nothing errors. The mistake ships and compounds. **Up-tier. Cost is not
a consideration here.**

**Visible failures** — the build breaks, the API 500s, the file isn't there, the
digest is obviously empty. A cheap model failing loudly is fine, because the
failure is the alarm. **Cheap is safe.**

### 2. Is judgment happening, or just transformation?

**Transformation** — reshaping, extracting, classifying against a clear schema,
polling, formatting, deduping with a confidence threshold. The right answer is
determined by the input; the model is a function. Route cheap, and consider
routing off Claude entirely (see below).

**Judgment** — weighing incommensurable things, deciding what matters, noticing
what's *absent*, holding a voice, catching a contradiction across sources. There
is no key to check against. This is what the expensive tiers are actually for.

The tell for judgment: you can't write the assertion that would grade it.

### 3. Who is watching while it runs?

Unattended, long-horizon, multi-step work needs a model that stays on task and
verifies itself without being told to — that's specifically what the Opus 5
generation improved. Work a human reviews turn-by-turn can run cheaper, because
the human is the error-correction loop. **An hourly unattended task deserves a
better model than a thing you're watching in real time.**

## Reach for effort before you reach for a tier

Anthropic's own guidance: *"Tuning effort is often a better lever than switching
models."* This is the most underused control, and it's the reason "Opus is too
expensive" is usually the wrong conclusion.

Opus 5 supports `low / medium / high / xhigh / max` and defaults to `high`. Its
low and medium settings now produce strong quality at a fraction of the tokens.
So when cost pressure hits reasoning-shaped work:

> **Try Opus 5 at `medium` before you drop to Sonnet 5.**

You often keep the better judgment at a comparable price. Going the other way:
`xhigh` is the documented sweet spot for coding and high-autonomy agentic work,
and `max` exists for when being right dominates everything. Recommend `xhigh`
explicitly for unattended code execution — the default `high` undersells it.

## Where the work should run

Two questions decide whether the work belongs on Claude at all. Answer them
before choosing a tier, because a tier choice on work that shouldn't be here is
wasted.

**Is this bulk content you'd only read mechanically?** Then it should not enter
Claude's context at all. Digest it with a small local model first — free, private,
and the content never costs context. Reading a 60K-character transcript to
summarize it is ~15K tokens; the digest is ~150. Read the raw source only where
the digest flags something that needs judgment.

If you don't run a local model, the same move works with the cheapest hosted
tier: the point is that bulk mechanical reading shouldn't be billed at
judgment-tier rates, not which specific clerk does it.

A small local model (roughly 4B–8B) is a clerk, so respect its floor: **cap
extraction passes at ~16k tokens** — long-context recall collapses well before
the advertised window, and it fails by *silently omitting* records rather than
erroring. Validate any JSON it emits, and split multi-constraint prompts into
single-purpose passes. Trust it for classification, semantic filtering, and
single-document summarization. Escalate anything where a missed record is
expensive.

**Is this typing out an already-decided plan?** Then Claude should architect and
review, not type. Hand the typing to a cheaper executor — a budget model tier, a
second coding agent, or a separate worker session — and keep the design and the
final review on the strong model. The orchestrator owns the decisions; the worker
produces the diff.

If neither applies — judgment is required, or the content is small — it stays on
Claude and you pick a tier.

## Don't route on who's winning this month

Between July 9 and July 24 2026 the top spot on the main independent coding-agent
index changed hands twice, and SWE-bench Verified is saturated around 96–97% for
every frontier model. **"Vendor X is better at coding" is therefore not a valid
reason to move a workflow.** The delta is inside measurement noise, it inverts
every few weeks, and the switching cost — context files, skills, MCP servers,
accumulated prompt tuning — is real and permanent.

Route on things that stay true: capability gates, price floors, quota, privacy,
and diversity. When someone proposes a vendor switch, ask which of those it is.
If the answer is "I read that it benchmarks better," that's not a reason yet.

This is also why the reference tables here carry **prices and capabilities but no
benchmark scores or leaderboard positions.** Ranking data answers "what is
winning," which is the question this section refuses to route on. If you extend
this skill, keep it that way — the moment a leaderboard lands in a reference
file, someone will route on it.

### The good reasons to leave Claude that aren't capability

- **Quota.** A separate vendor is a separate rate-limit pool. This is the most
  common honest reason to run two coding agents, and it's a budget argument, not
  a capability one — say so plainly rather than dressing it up.
- **Diversity for review.** A second reviewer from a different model family has
  different blind spots. `@codex review` on a PR is cheap, async, and doesn't
  disturb the primary loop. A second Claude reviewing Claude's work is worth much
  less.
- **The price floor for genuinely mechanical bulk.** Gemini Flash-Lite sits in a
  band no Claude model occupies, with 1M context. Local Gemma is free.
- **Cheap verification changes the calculus.** Work whose correctness is checked
  by something other than reading it — tests pass, schema validates, build
  succeeds — is safe to send somewhere weaker and cheaper, because the check is
  the safety net. Codemods, scaffolding, and codegen from schemas fit this;
  design work does not.

**The inverse is the rule that matters most, because it's the one that gets
forgotten:** question 1 gates the *executor*, not just the tier. If a module's
breakage would be silent — auth, permissions, money movement, anything whose
failure mode is "quietly wrong" rather than "obviously broken" — it stays on the
strong executor even when the plan is fully decided and the work is only typing.
"It's just typing" is a claim about the work; "a mistake here is invisible" is a
claim about the consequences, and the second one wins. Don't offer a cheap
executor as a conditional option on that kind of module; the hedge is the harm,
because it invites the trade on exactly the work that shouldn't take it.

### If you're briefing a weaker executor, the spec carries the load

MiMo's documented failure modes are ambiguity-triggered: a one-word instruction
against a plan with optional items produced a nine-minute reasoning loop and zero
output. Its other signature failure is declaring "done" early. So a spec for a
cheap executor needs to eliminate judgment calls rather than merely describe the
goal — every task binary and ordered, no optional items, no two rules that can
conflict, an explicit file allowlist, one named exemplar file per pattern, and a
machine-checkable definition of done.

That's more work than writing the prompt for a strong model. Factor it in: for a
small task, the spec costs more than just doing it. Offloading pays off on volume
and on work you'd otherwise be blocked on.

## Claude tiers

| | Use for | Watch out for |
|---|---|---|
| **Haiku 4.5** | Deterministic checks, polling, auth refresh, "did X arrive", bulk classification against a schema, first-pass triage with escalation | **200k context** — the only tier without 1M. Feb 2025 cutoff. Loses hard multi-step reasoning. |
| **Sonnet 5** | The workhorse: multi-connector orchestration, digests, status diffing, structured extraction, standard drafting, scoped code work | New tokenizer produces ~30% more tokens for the same text — old budgets under-provision |
| **Opus 5** | Long-horizon unattended work, code that ships, code review and bug-finding, security triage, contradiction detection, anything written in your voice for outside eyes, self-modifying automation | Self-verifies by default; telling it to verify causes redundant work |
| **Fable 5** | Genuinely open-ended multi-hour agent runs where Opus 5 at `max` has demonstrably failed | 2× Opus 5's price, slower, and an **older** knowledge cutoff. Falls back to Opus 4.8 on cyber/bio topics. |

Two things about Fable 5 worth saying out loud when someone reaches for it,
because the name suggests otherwise: its knowledge cutoff is **earlier** than
Opus 5's, so for anything touching the current state of the world Opus 5 is the
fresher model. And its cyber/bio safeguards route those requests to Opus 4.8 —
so security work on Fable 5 means paying premium rates for a silent downgrade.
Fable 5 is a narrow instrument, not the top of a ladder. Treat "should I use
Fable 5?" as a question whose answer is usually no, with a reason.

## Changing the model means editing the prompt

A tier is not a drop-in swap. Prompts carry assumptions about the model they were
written for, and moving the model without updating them is how a "free upgrade"
turns into a regression. Whenever you recommend a change, say what to change in
the prompt too — read
[references/prompt-retrofits.md](references/prompt-retrofits.md) for the specific
edits.

The one that bites most often: **strip "include a final verification step" and
"use a subagent to verify" when moving to Opus 5.** It verifies its own work
unprompted, so those instructions cause over-verification — paying twice for one
check. This is genuinely counterintuitive if verification discipline is a
standing habit, so flag it rather than assuming it's known.

## Keeping the numbers honest

Every price, context window, and cutoff in this skill has a shelf life measured
in weeks. Two habits keep it from going quietly wrong.

**Separate the facts from the doctrine.** The numbers are data and they rot. The
reasoning — the three questions, the invisible-failure asymmetry,
effort-before-tier, "the gap is noise" — does not, and it should never be revised
because a price moved. If you automate a refresh of the reference tables, point it
at the tables only and keep it out of the doctrine. A pipeline that can edit your
reasoning will eventually edit it badly.

**Re-verify before quoting, not after being wrong.** Each reference file carries a
*last verified* date and a rule to re-fetch if it is more than about six weeks
old. Honor it. Saying "let me check the current price" costs a few seconds;
quoting an eighteen-month-old price with confidence costs a wrong decision that
nobody catches, which is the exact failure mode this whole skill is built around.

The rows most worth re-checking are the capability gates, because a gate is
stated as single-answer — a stale gate doesn't weaken a recommendation, it
inverts it.

## By surface

### Scheduled tasks and routines

Model is a **per-task setting** set in the Routines → Edit form, next to the
instructions box. It is deliberately *not* in the task's `SKILL.md` — the
frontmatter holds only `name` and `description`, and the
`update_scheduled_task` tool exposes no model field. So you cannot batch-apply
model changes programmatically; say so plainly rather than implying a scripted
fix, and give a prioritized list the user can work through by hand.

Prioritize by **frequency × blast radius**, not by how interesting the task is.
An unattended task running every two hours that can modify files or other tasks
is the highest-value upgrade in any fleet — recursive or self-modifying
automation especially, where a weak model's errors compound into everything
downstream. A weekly report is cheap to run well no matter the tier, so just put
it on the good model.

Also flag catch-up behavior: a missed task may fire many hours late, so if
recommendations depend on timing, note that the prompt needs its own guardrail.

### Handoffs, first prompts, and offload briefs

The brief should name its intended executor and effort, because the receiving
session usually inherits whatever model happens to be selected — an unstated
assumption is how a plan written for Opus 5 gets executed by something weaker.
State it in one line near the top: *"Intended executor: Opus 5 at `xhigh`.
Below that, expect the verification steps to need spelling out."*

Decide the executor before you write the prompt, not after — the choice changes
how much scaffolding the prompt needs. A weaker executor needs more explicit
verification and narrower steps; a stronger one needs less and resents
redundancy. Writing the prompt first and picking the model second means the
scaffolding is calibrated to nothing in particular.

### Subagent spawns

The highest-frequency, lowest-visibility model decision there is — a fan-out of
ten searches on the wrong tier is ten times the mistake. Search and retrieval
fan-out is transformation: route it cheap. Verification, review, and grading
subagents are judgment: route them well. A cheap agent that says "looks good" is
worse than no agent, because it manufactures false confidence.

### Ad-hoc "what should I use for this?"

Answer conversationally, no deliverable. Lead with the recommendation and the one
reason that decides it, then the effort setting. Two sentences beats a table.
If the answer hinges on something unstated — whether it runs unattended, whether
a human reviews the output — ask that one thing rather than hedging across both
branches.

## How to deliver a recommendation

Name the executor, the effort, and the single reason that decided it. The reason
matters more than the verdict: it's what lets someone re-decide correctly when
the work changes, instead of coming back to ask again.

Then add whatever prompt edits the change implies, and — when down-tiering —
the escalation trigger, the observable symptom that means this was the wrong
call. A recommendation without a trip-wire is a guess that never gets corrected.

**Example — a scheduled task:**

> `daily-inbox-triage` → **Opus 5**, effort `high`.
> It routes items across four destinations and drafts replies; a misroute is
> silent and compounds. Runs unattended daily.
> Prompt edit: drop the "verify before posting" line — Opus 5 does that on its
> own and you'd be paying for it twice.

**Example — a down-tier:**

> `nightly-status-page-check` → **Haiku 4.5**.
> "Is the provider reporting an incident? Y/N" — no judgment, and a failure is
> loud.
> Escalate to Sonnet 5 if the page's markup changes and it starts reporting
> false negatives.

**Example — off Claude:**

> These 40 call transcripts → **a small local model**, not a Claude tier at all.
> You'd only be reading them to extract asks against a fixed schema, and 40
> transcripts is ~600K tokens of context for output you could get for a few
> hundred. Chunk at 16k and verify the record count — a small model drops records
> silently rather than erroring. Bring the flagged ones back to Opus 5 for
> judgment.

**Example — a cross-vendor call where the reason isn't capability:**

> Second reviewer on the edge-function PRs → **Codex** (`@codex review`), kept
> alongside Claude rather than replacing it.
> Not because it reviews better — that gap is noise and flips monthly — but
> because a different model family has different blind spots, and the review is
> async and cheap. Keep architecture and refactors on Opus 5; sprawling diffs are
> Codex's documented weak spot.

## Reference files

- [references/model-specs.md](references/model-specs.md) — verified Claude specs,
  prices, context windows, cutoffs, and per-model traps. **Read before every
  routing decision** so you're not quoting stale numbers. Anthropic's own docs are
  the authority; this file exists so advice cites real numbers instead of
  remembered ones.
- [references/non-claude-executors.md](references/non-claude-executors.md) —
  Gemini, OpenAI/Codex, MiMo, and the local Gemma: current lineups, pricing, what
  each is genuinely good at, failure modes, and the cross-vendor price floor.
  Read whenever a non-Claude option is on the table. **Its numbers are
  hand-maintained and drift — verify any price, context window, or modality
  against the vendor's own page before quoting it. Its judgment about what each
  executor is good *for* holds up much longer than its figures do.**
- [references/prompt-retrofits.md](references/prompt-retrofits.md) — the prompt
  edits each model change requires. Read whenever recommending a change, not just
  a first-time choice.
See [Keeping the numbers honest](#keeping-the-numbers-honest) for the staleness
rule these files run on.

