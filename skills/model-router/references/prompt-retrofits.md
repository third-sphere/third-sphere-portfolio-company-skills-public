# Prompt retrofits — what to edit when the model changes

A model change is not a drop-in swap. Prompts accumulate instructions that were
workarounds for a *specific* model's weaknesses, and those instructions don't
become harmless when the weakness goes away — they become active cost, and
sometimes active harm. A recommendation that says "switch to Opus 5" and stops
there hands over a regression labeled as an upgrade.

So whenever you recommend a tier change, name the prompt edits it implies. Below,
organized by the direction of the move.

## Moving up to Opus 5

### Strip verification scaffolding

Opus 5 verifies its own work without being told to. Anthropic's docs are explicit
that instructions like *"include a final verification step"* or *"use a subagent
to verify"* should be **removed**, because they cause over-verification — you pay
twice for one check and the run takes longer.

Phrases to hunt for and delete or soften:

- "include a final verification step"
- "use a subagent to verify"
- "double-check your work before reporting"
- "re-read the file after editing to confirm"
- "spawn a verifier agent"

This is counterintuitive for anyone with a standing verification discipline, so
say it out loud rather than editing silently. The discipline isn't wrong — it's
that the enforcement moved from the prompt into the model. Verification you
genuinely want *observable* (a test suite run, a committed doc update, a diff
posted for review) is a different thing and should stay: that's an artifact
requirement, not a nudge to be careful.

### Re-check `max_tokens`

Thinking is on by default and `max_tokens` caps thinking + response *together*.
A budget tuned on a model that ran without thinking can now truncate the actual
answer. Raise it, especially at `xhigh` or `max` effort where the model needs
room to think across tool calls.

### Expect and absorb behavior changes

- Deliverables run **longer** by default. If you want brevity, ask for it
  explicitly — it's no longer the default shape.
- It **narrates progress** more in agentic sessions. Fine unattended; noisy if
  the output goes straight to a Slack DM. Say "report only the outcome" if so.
- It **delegates to subagents more readily.** Good for fan-out, but if the task
  has a tight permission fence, note which tools subagents may use.

### Don't disable thinking to save money

`thinking: {type: "disabled"}` with effort `xhigh` or `max` is a 400 error. And
with thinking off, Opus 5 can occasionally write a tool call into its text output
instead of emitting a proper tool-use block — which silently breaks tool-driven
pipelines. **Lower the effort level instead.** Same savings, no failure mode.

## Moving to Sonnet 5

### Recount every token budget

The new tokenizer produces roughly **30% more tokens for the same text**. Per-token
price didn't change, so the effect is invisible in a price sheet and shows up as:

- `max_tokens` limits sized close to expected output now truncating
- "keep the summary under N tokens" instructions that no longer mean what they meant
- context windows holding less text than the 1M number implies
- costs per equivalent run drifting up

Any budget number in a prompt written before Sonnet 5 should be treated as
provisional and re-measured.

### Remove rejected parameters

These now return 400 rather than being ignored:

- non-default `temperature`, `top_p`, `top_k` → steer via system prompt instead
- `thinking: {type: "enabled", budget_tokens: N}` → use adaptive thinking + effort
- assistant message prefilling → use structured outputs or `output_config.format`

### Handle refusals as success

Cybersecurity refusals come back as **HTTP 200 with `stop_reason: "refusal"`**, not
an error. A pipeline that only branches on error codes will treat a refusal as a
valid empty result. If the task touches security topics, handle that stop reason
explicitly.

## Moving down to Haiku 4.5

### Check the payload against 200k

This is the failure that actually happens. The work is mechanical, so Haiku looks
correct on judgment grounds — and then the transcript, export, or scraped page
doesn't fit the window. Estimate payload size first. If it's borderline, either
stay on Sonnet 5 or split the work.

### Put the schema in the prompt

Haiku is reliable at extraction and classification when the target shape is
explicit, and unreliable when it has to infer what's wanted. Down-tiering to
Haiku usually means the prompt needs to get *more* specific: name the fields,
give an example of the output, state what to do when a field is missing.

### Add an escalation path

Down-tiering without a trip-wire is a bet you never find out you lost. Either:

- **Confidence cascade** — Haiku first, re-route low-confidence results to a
  stronger model. The documented pattern; cuts 60–70% of classification cost.
- **Observable symptom** — name the thing that means this was wrong ("if it starts
  reporting no results on days when the source clearly has results, move it to
  Sonnet 5"). Put it in the task's own notes, not just in conversation.

### Mind the Feb 2025 cutoff

Haiku's knowledge is meaningfully older. Fine for transformation of supplied
content; not fine for anything relying on the model knowing how the world
currently is.

## Moving anything to Fable 5

Almost always the wrong move — but if it's genuinely warranted:

- **Cyber/bio topics fall back to Opus 4.8.** Don't route security work here.
- **Knowledge is older than Opus 5's** (Jan vs May 2026). If the task needs current
  world knowledge, this is a downgrade wearing an upgrade's price tag.
- **It's slower.** For anything in a cron window or a latency-sensitive loop, the
  slowdown may matter more than the capability gain.

Before recommending it, confirm Opus 5 at `max` effort was actually tried. "Opus 5
wasn't good enough" and "Opus 5 at default effort wasn't good enough" are very
different claims, and the second one is usually what happened.

## Retrofit checklist

When handing over a model-change recommendation, walk this:

1. Verification instructions — strip if moving up to Opus 5, add if moving down
2. Token budgets — recount for Sonnet 5's tokenizer; raise for Opus 5's thinking
3. Rejected parameters — remove sampling params, manual thinking, prefills
4. Payload size — check against Haiku's 200k if down-tiering
5. Output schema — make explicit if down-tiering
6. Escalation trigger — name the observable symptom for any down-tier
7. Effort level — state it, don't inherit the default silently
