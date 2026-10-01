# Other executors

Use the section relevant to the actual candidate. Model selection is shared
across environments; this filename is retained for existing callers.
Apply [evidence rules](evidence.md) and confirm access through the intended route.

## OpenAI / Codex

### GPT-6 Astra

**Verified: 2026-09-06. Scope: direct OpenAI API.**

| Property | Verified value |
|---|---|
| Model ID | `gpt-6-astra` |
| Context / max output | 1,050,000 / 128,000 tokens |
| API effort | `low`, `medium`, `high`, `xhigh`, `max` |
| Input / output modalities | Text and image / text; no native audio or video |
| Standard USD per million tokens | Input $10; cached input $1; cache writes $12.50; output $50 |
| Long prompts | Above 272K input tokens: 2× input/cache rates and 1.5× output rates for the entire request |
| Processing modes | Batch/Flex 50% of Standard; Fast 2× applicable rates |

Tool support includes search, computer use, shell, patching, MCP, and structured
outputs. Model support does not establish tool availability in the chosen app.
Source: [Astra specifications](https://developers.openai.com/api/docs/models/gpt-6-astra).

**Provider positioning:** OpenAI presents Astra as its strongest model for
complex reasoning, coding, research, document work, and multistep tool workflows.
It reports lower task costs in some evaluations despite higher token prices.
The API also supports asynchronous tools and mid-turn steering when implemented
by the harness.
Source: [Astra guide](https://developers.openai.com/api/docs/guides/latest-model).

**Routing interpretation:** put Astra on the shortlist for demanding work in an
available OpenAI environment, including architecture and browser-based execution.
Do not require another model to fail first. Where a current executor works well,
keep it unless a representative trial, capability, quota, or total-cost case
supports changing. Provider positioning warrants evaluation, not a universal
cross-vendor ranking or an automatic switch.

**Observed 2026-09-03, standard access.** Cyber-related refusals have stopped
API tasks outright, sometimes on work adjacent to but not itself exploit
development. Treat that as an availability risk to plan around on standard
access, and name the check and escalation before routing unattended work here.
It is not a blanket security-review exclusion, and not a reason to move a task
to evade a safeguard. OpenAI also reports reduced chain-of-thought
monitorability for this model, which matters where an unattended run's reasoning
is itself the thing under review.

Price a full task, including long-prompt rates, cache writes/hits, retries, tools,
and review. Do not reject Astra solely for its output-token price or assume the
provider's task-cost result transfers to this workload. These are API rates,
not a Codex subscription charge. Check the selected surface's effort controls;
app-only labels must not be sent as API effort values.

For migration and recurring pauses or excessive output, read the Astra section
in [prompt retrofits](prompt-retrofits.md).

GPT-5.6 Sol, Terra, and Luna remain candidate names from this skill's existing
coverage; resolve their current availability, specs, and price from the actual
surface and official catalog before selecting one. No static price or ranking
is asserted here. Architecture, refactors, frontend work, and reviews are
eligible when supported by task evidence and tools.

**`gpt-6-astra-pro`, listed 2026-09-07 (OpenRouter).** It carried the same
published input/output price, context, max output, and effort ladder as
`gpt-6-astra`. **What distinguishes the two is unverified.** Resolve the
difference from OpenAI's own catalog before selecting one. Do not assume Pro is
the stronger route because of the name, and do not quote a price premium the
listing does not show. An OpenRouter listing is also not proof of access on the
account or surface in use.

**Verified: 2026-09-06. Scope: OpenAI API data controls.** API data is not used
for training unless the customer opts in. Retention is a separate question:
ZDR has eligibility and endpoint limitations, and some capabilities can still
store application state. Check the selected account and workflow rather than
extending API terms to consumer products or every Codex authentication mode.
Source: [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data).

## Google Gemini

**Verified: 2026-09-06. Scope: Gemini API terms.** Paid Services do not use
prompts/responses to improve Google's products; limited logging for abuse
prevention remains. Billing status and regional exceptions affect which terms
apply, so the old blanket rule that every free use trains on data is inadequate.
Do not infer ZDR from no-training terms.
Source: [Gemini API terms](https://ai.google.dev/gemini-api/terms).

Resolve the current Pro, Flash, or Flash-Lite candidate from the
[Gemini model catalog](https://ai.google.dev/gemini-api/docs/models), inspected
2026-09-06. Verify the specific model's modalities, release status, limits, and
pricing before using them as a gate. Do not treat all Gemini models as having
one cutoff, context limit, or modality set.

**Price floor, verified 2026-09-03; recheck before quoting.** Flash-Lite was
listed in the $0.25-$0.30 per million input-token band with 1M context, a band
no Claude model occupies. The gap is the routable fact, not the model name: it
is why genuinely mechanical bulk work can leave Claude at all. Resolve the
current model and rate from the catalog before committing a budget. Cheap
entrants appear and vanish monthly, and chasing the true market minimum is a
re-qualification treadmill rather than a saving.

## Xiaomi MiMo

MiMo and the previously used V2.5 / V2.5-Pro routes remain candidates when
configured. **Status checked: 2026-09-06; current specs, pricing, plan terms,
and compatibility remain unverified.** The
[official platform](https://platform.xiaomimimo.com/) returned no readable
specifications during this review. Resolve its current documentation or
account details before a decision depends on these facts. Do not reuse the
old token-plan allowances, cache discounts, or API-compatibility claims.

For an authorized worker, preserve a decided scope, acceptance checks, and
observable progress. Check actual task performance; historical loop anecdotes
are not grounds for a universal model exclusion or a guessed API parameter.

## Local Gemma

Gemma remains a local-runtime candidate. The
[official Gemma overview](https://ai.google.dev/gemma/docs) was inspected
2026-09-06; **the user's installed model, quantization, memory budget, tool
availability, and reliable extraction length have not been verified**.
Inspect the runtime and its exact model card before quoting limits. Do not
reuse the former universal 16K chunk threshold or unverified benchmark scores.

Prefer deterministic extraction where sufficient. For semantic extraction,
qualify the actual runtime on representative chunks, retain source IDs/spans,
and check coverage and sampled accuracy. Use a supported chunk size with
boundary handling for records split across chunks. Smaller inputs alone do
not guarantee complete extraction. A local model has compute and review costs;
local-only routing also requires local tools, logs, and preprocessing.
