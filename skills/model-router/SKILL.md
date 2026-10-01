---
name: model-router
description: "Choose the model, execution surface, and effort for a unit of work — which Claude tier (Fable 5.1 / Opus 5.5 / Sonnet 5.5 / Haiku 4.5), what effort, or another executor: OpenAI/Codex, Gemini, MiMo, or local Gemma. Use whenever a model or executor choice is being made or implied: \"which model should I use\", \"is this an Opus task\", \"should this run on Haiku\", \"what model for this scheduled task\", \"audit my tasks' models\", \"should I offload this\", \"is this a Gemini job\", \"send this to Codex\". Use PROACTIVELY, unasked, before (a) writing or revising a scheduled task, (b) producing a handoff, first prompt, or offload brief, (c) spawning subagents where the model is open, or (d) advising on a prompt whose cost, privacy, or reliability is in question. Also use when changing models, since a tier change usually needs prompt edits. Apply authorized routing with available tools; a recommendation alone authorizes nothing. Not for prompt wording with a fixed executor, or offload mechanics after routing is settled."
---

# model-router

Choose a capable, available executor with an appropriate verification plan. Keep
the current executor unless task-specific evidence, capability, quota, or total
cost justifies a change. This default applies equally in Claude and Codex.
Respect the user's explicit model and environment choices. If a choice cannot
satisfy a hard constraint, explain the conflict instead of silently substituting.

## 1. Establish requirements

Identify the unit of work and the constraints that could change the route:
input modalities and size, output needs, required tools, data handling, latency,
budget, supervision, and consequences of failure. Use known task context; ask
only for a missing fact that changes the decision.

- **Current information:** require suitable retrieval or current supplied sources.
  A newer training cutoff does not establish present-day accuracy.
- **Local-only content:** keep raw data within a verified local workflow, including
  preprocessing, tools, logs, and review. Do not upload it to qualify a candidate.
- **Privacy:** distinguish no training, retention, residency, and local-only needs.
  Check the actual provider, product, endpoint, account settings, and downstream
  tools. A vendor name or paid subscription alone proves none of these.
- **Modality and limits:** check the selected model through the intended surface.
  A text transcript may lose information required from original audio or video.
  Include tools and expected output in context budgeting; fitting is not recall.

A hard constraint filters candidates; it does not name a permanently preferred
vendor. If no verified candidate qualifies, report the blocker and the smallest
necessary change. Do not silently relax the requirement.

## 2. Identify available execution paths

Separate **model** (reasoning capability), **surface** (app, CLI, API, local
runtime, worker), and **access** (account, quota, permissions, tools). Discover
what this session can actually use before proposing an executable action.
A catalog entry is not proof of access. A CLI on this machine may call a remote
model. API pricing does not describe the marginal cost of a subscription task.

Read [execution surfaces](references/execution-surfaces.md) when applying a
change, auditing schedules, or preparing a handoff. Read only the relevant
provider section in [Claude facts](references/model-specs.md) or
[other executors](references/non-claude-executors.md) when facts affect selection.
Use [evidence rules](references/evidence.md) when refreshing or
reconciling claims. Do not load every reference for a routine recommendation.

If no current executor is known, start from a qualified executor already
available in the user's chosen environment; prefer one with evidence on similar
work. If no such evidence exists, label the choice provisional and name a
representative acceptance check before relying on unattended output.

## 3. Match quality and effort to the work

Use three questions:

1. **Would a consequential mistake be detected?** Silent omissions, incorrect
   permissions, or plausible misclassifications need stronger evidence and
   verification. A stronger model is not itself a correctness guarantee.
2. **What judgment remains?** A fixed plan reduces ambiguity but does not make
   implementation error-free. Extraction and search can silently miss evidence;
   classify them by consequences and coverage, not by their mechanical appearance.
3. **Who checks the result, and when?** Unattended, multi-step work needs explicit
   acceptance criteria and escalation. Human presence helps only if that person
   actually reviews the consequential decisions before they take effect.

Starting points by tier, **as of 2026-09-06, Opus rows 2026-09-23, Sonnet and Haiku rows 2026-09-29** — observed fits, not capability
limits. A task result overrides a row, and [Claude facts](references/model-specs.md)
carries the dated per-model caveats behind them.

| Tier | Fits | Watch for |
|---|---|---|
| **Haiku 4.5** | Deterministic checks, polling, auth refresh, "did X arrive", bulk classification against a schema, first-pass triage that escalates | 200K context and no effort control; drops hard multi-step reasoning; retires no sooner than 2026-10-15, so name its replacement |
| **Sonnet 5.5** | The workhorse: multi-connector orchestration, digests, status diffing, structured extraction, standard drafting, scoped code work | API default effort is `high` but apps default to `medium`, so set it; starts without Opus reasoning on a handoff; results from Sonnet 5 don't carry over |
| **Opus 5.5** | Long-horizon unattended work, code that ships, review and bug-finding, contradiction detection, anything in your voice for outside eyes | Defaults to `medium` effort; unattended runs can stop early with a text-only turn, so require a completion checklist; handing off to any model but Fable or Mythos loses its reasoning |
| **Fable 5.1** | Open-ended multi-hour runs where Opus 5.5 at `xhigh` has demonstrably fallen short | 2.5× Opus 5.5 uncached, and cache reads no longer undercut it — cost the task |

Try an appropriate supported effort on the current model before switching when
reasoning depth is the issue. Preserve a working effort absent contrary evidence;
increase it for demonstrated reasoning failures, or trial a lower setting for
bounded work with adequate checks. Do not equate effort names across models or
copy an API setting into an app blindly. When effort is unsupported, say so;
when it is unknown, verify it rather than inventing a value.

Compare total task cost, including preparation, input/output, cache assumptions,
retries, latency, and review. Consider deterministic tools before models for
mechanical work. Cheaper execution is justified when evidence shows it meets the
quality requirement, not merely because a build or schema validates. For code,
check whether tests cover the consequential behavior and inspect the diff.

Architecture, frontend work, writing, and security review have no blanket vendor
exclusions. Use task results and actual workflow capabilities. Public benchmark
headlines and practitioner anecdotes can suggest a trial; neither establishes a
universal ranking or proves all models equivalent. Different-family review may
add useful perspective, but still needs independent evidence and review criteria.

## 4. Preserve checks and define escalation

Read [prompt retrofits](references/prompt-retrofits.md) for model changes. Preserve
acceptance tests, permission checks, source checks, and required independent
review regardless of tier. Remove redundant generic reminders only when there
is evidence they cause waste and the required checks remain explicit.

Name a check capable of detecting the relevant failure: coverage against source
records, known-answer cases, negative/permission tests, sampled source review,
or a qualified review of judgment-heavy output. Valid JSON proves structure;
self-reported confidence does not prove correctness. Record counts alone cannot
detect a substituted or duplicated record.

For a cheaper or unproven route, name an observable escalation trigger and the
next action. Examples: missing source IDs, failed negative tests, repeated tool
failure, or unacceptable sampled omissions. Pause affected consequential actions,
inspect the failure, then increase effort, strengthen checks, or use a qualified
alternative. Never lift data or authorization constraints to recover. If the
failure cannot be reliably observed, do not justify a downgrade by promising to
escalate after someone notices it.

## 5. Recommend or apply

Keep the response proportional. Name **surface, model, supported effort, decisive
reason, necessary prompt changes, and verification/escalation condition**. For
unchanged prompts, say no change is needed; for unavailable effort, say not
supported or not yet verified. Cite decisive volatile facts and state uncertainty.
A recommendation can be two sentences; audits benefit from a compact table.

Example with supplied capability facts:

> Keep the current Codex worker and its supported `high` effort: it meets the
> task requirements, and there is no evidence a switch helps. Preserve permission
> tests and required review; escalate before merge if negative cases fail.

A routing recommendation does not authorize a model switch, offload, external
message, new spending, or settings change. When the user's request already
authorizes the action, apply it with available tools or an installed offload
skill within that scope; do not ask again. Explicit task creation, delegation,
and communication restrictions still apply. This skill's proactive invocation
is not authorization to spawn agents or dispatch work.

Verify the effective model and effort using the tool result or readback. Report
what changed and what remains unverified. If no supported control exists, give
the specific manual step grounded in that surface's documentation; never claim
that mentioning a model in a prompt changed the running session. On ambiguous
mutation results, inspect state before retrying to avoid duplicate workers.
