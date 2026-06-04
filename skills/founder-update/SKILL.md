---
name: founder-update
description: >
  Build a portfolio company's recurring (weekly or monthly) investor update — the update a
  FOUNDER sends to THEIR investors. Use whenever the user wants to draft, assemble, or
  refresh a founder investor update: "write the monthly investor update for [company]",
  "build [company]'s update", "draft the founder update", "turn these notes/metrics into
  an investor update", "monthly update with OKRs and a metrics chart", or when the user
  pastes a founder's metrics, OKR progress, or check-in notes and wants them structured.
  Also triggers on "continue [company]'s running update doc" or "what changed since last
  update". Pulls prior update(s) from Drive for the month-over-month columns and trend
  chart. Even if the user just says "update for [company]" with material attached — use
  this skill.
---

# Founder Update — Portfolio Company Investor Updates

This skill produces a **portfolio company's investor update** — the recurring note a
founder sends to their own investors and strategic partners. These are the updates founders
maintain as a running, shared Google Doc and email out ahead of board meetings or regular
check-ins, so investors and advisors can engage between meetings.

**Primary operator: the founder**, running this on their own startup. (Investors, board
members, or advisors may also build it on the company's behalf — same skill, the only
difference is which connectors you have access to; see "Input sourcing.")

The body is organized around seven key business dimensions (Product/Approach, Traction/
Distribution, Market, Competition, Impact, Team, Financial/Runway). These are spelled out
inline here and in `references/template.md`, so this skill is fully self-contained and
needs no dependencies installed.

---

## What a good update is

Investors skim. A strong update lets a reader answer "is this going up and to the
right, and what do they need from me?" in under two minutes. That means:

- **Numbers, not adjectives.** Every claim of progress carries a figure. "Strong
  pipeline" is noise; "pipeline grew $350K → $550K across 7 networks" is signal.
- **Month-over-month, always.** Every metric shows current vs. last period vs. target.
  A single snapshot hides the trend; the trend *is* the story.
- **One picture.** At least one chart of a headline metric over the last several
  periods (new qualified leads, pipeline $, ARR, revenue, or runway).
- **A running asks list.** Asks accumulate and stay until resolved — never silently
  dropped — so nothing falls through the cracks between calls.
- **Honest.** Concerns and misses are stated plainly. Investors help more when they
  see the real picture.

---

## Two modes — detect first

Before gathering anything, decide which mode you're in. Search for the company's prior
update first (Drive: `name contains 'update' and name contains '{company}'`; Notion if
connected). What you find determines the path:

- **Ongoing** — a prior update exists. Read the last 1–3, then build a *delta*: pull
  current metrics from source systems, compare to last period, carry forward open asks.
- **Cold start** — no prior update (the founder's first one). Run the baseline pass
  below before building. This is the common case for a startup and must work cleanly.

Note: "cold start" means no prior *update* — it does **not** mean no *data*. A company
that has operated for months has history in its CRM, billing, and finance even if it has
never sent an investor note. Backfill the dashboard and the chart from those systems so
the first update still shows a trend, not a lonely single point.

## Input sourcing — where each number comes from

**The cardinal rule: numbers come from systems of record; narrative comes from
conversation.** Metrics must trace to a CRM, billing, finance, analytics, or OKR tool.
Transcripts, Slack, and email supply the *story* — wins, concerns, asks, product/market/
competitive color — and must **never** be the source of a reported figure. If a number
can't be traced to a system or an explicit figure the founder gave you, it does not go in
as a number — leave a visible `‹TBD — need source›` placeholder and ask.

Source map — for each section, try the connected source, then degrade gracefully:

| Section | Authoritative source | Acceptable fallback |
|---|---|---|
| Pipeline $, qualified leads, conversions | Founder's CRM (HubSpot / Salesforce / Pipedrive) | CSV/screenshot upload, pasted figures |
| Revenue / MRR / ARR | Billing (Stripe) or finance sheet | Screenshot, pasted |
| Cash / burn / runway | Accounting tool or finance tracker sheet | Pasted (how it usually arrives) |
| OKR progress | OKR tracker (Notion / Sheet) | Prior update, pasted |
| Product · Market · Competition · Impact · Team color | Call notes, Slack, email, uploaded transcript | Pasted notes |
| Last-period values + open asks | Prior update (Drive / Notion) | none on cold start |

**Getting access — be specific, never vague.** For each source the founder needs:

1. **Already connected?** Use it. (Check the tool list / `tool_search` before assuming
   it's missing.) Gmail, Drive, Notion, Slack, and call-recording services are common and ideal for narrative.
2. **Not connected but a connector exists?** Offer to connect it — run
   `search_mcp_registry` then `suggest_connectors` so they get a one-tap connect (e.g.
   "connect HubSpot and I'll pull pipeline directly"). Don't make them copy-paste what a
   connector could fetch.
3. **No connector / not worth connecting?** Ask for a *specific* artifact, not a data
   dump: "upload the CRM pipeline export (CSV)" or "screenshot the finance tab showing
   cash, burn, runway" — never "send me your data."
4. **Still unavailable?** Placeholder + ask. Never guess, never infer a metric from prose.

### Cold-start baseline pass

On the first update, offer a short baseline interview — it makes every future update a
cheap delta. **Always make it skippable.** Lead with the offer and an out:

> "Since this is your first update, I can ask ~5 quick questions to set the baseline
> (metrics, targets, OKRs, cadence) so future updates are basically one-click — or skip
> it and I'll infer what I can from what you've given me and flag the gaps. Which?"

If they **do** the interview, ask in one batched round, not a long interrogation:

1. **Cadence & period** — weekly or monthly? what window does this cover?
2. **Metric set & targets** — which 5–9 metrics define this business, and the 2026
   target for each. Always include runway. (Propose a stage-appropriate default set and
   let them trim.)
3. **OKRs** — this period's Objectives and the numeric Key Results under each.
4. **Sources** — for each metric, where does it live? Connect or request per the steps
   above. **Backfill 2–3 months of history** for the headline metric so the chart has a
   trend on day one; if truly no history exists, say the chart starts next period.
5. **Audience & confidentiality** — who receives it; mark confidential if they want.

If they **skip**, don't block — build the update from whatever is available: infer a
stage-appropriate metric set and OKRs from the sources, pasted notes, and any connected
tools; leave `‹TBD — need source›` on anything you can't ground; and surface the gaps as
a short list at the end ("to make next month one-click, I still need: targets for X,
source for Y"). The founder can fill them in then or carry them forward. Skipping costs
them a little polish now and a little setup later — it never costs them an update.

Either way, save the resulting metric set + sources as the "shape" of the update so the
next period reuses it. (When output is a Google Doc, this lives in the doc; otherwise note
it back to the founder so they can keep it.) After a few cycles the shape is stable and
the interview offer becomes unnecessary — at that point just confirm the metric set looks
right and move on.

### Gathering this period (both modes)

Collect, asking only for what the sources didn't supply: headline wins/concerns; OKR
progress (numeric vs. target); the metric set; product/tech progress; biz-dev/traction;
market, competition, impact developments; team changes; fundraising; asks. If the founder
hands you a pile of notes or a transcript, **parse it — don't ask them to reformat.**

### Build the update

Read `references/template.md` for the full canonical structure, the OKR format, the
dashboard spec, and the thesis-subsection mapping. The required spine is:

1. **Header** — Company · period · date · "CONFIDENTIAL" if the company uses it.
2. **General update** — 2–4 sentences: the period in one breath, biggest win, biggest
   concern.
3. **OKRs** — each Objective with its Key Results as **`KR — current / target → status`**.
   KRs are numeric. (Format detail in the template.)
4. **Core Metrics Dashboard** — the `Metric | Status | Current | Last period | Target`
   table. This is the data behind the chart; fill "Last period" from the prior update
   (ongoing) or from backfilled source history (cold start).
5. **Trend chart** — at least one headline metric over the last several periods (below).
6. **Thesis-aligned subsections** — Product/Approach, Traction/Distribution, Market,
   Competition, Impact, Team, Financial/Runway. **Skip any subsection with nothing
   notable this period** rather than padding it (see mapping below).
7. **Fundraising** — only if active; else skip.
8. **Help & Asks** — running list; new asks on top, unresolved old asks retained,
   resolved ones struck through or moved to a short "recently closed" line.
9. **Other** — press, social proof, thanks; skip if empty.

### Generate the trend chart

Use `scripts/trend_chart.py`. It takes a small JSON spec (periods + one or more series +
optional target line) and writes a clean PNG. Default to the metric the user names; if
they don't name one, pick the most investor-relevant series with at least 2–3 historical
points (new qualified leads → pipeline $ → ARR/revenue → runway, in that order).

```bash
python3 scripts/trend_chart.py --spec chart.json --out /mnt/user-data/outputs/{company}_trend.png
```
Spec shape (see the script header for the full schema):
```json
{
  "title": "New qualified leads", "ylabel": "Leads",
  "periods": ["Feb", "Mar", "Apr", "May", "Jun"],
  "series": [{"name": "Qualified leads", "values": [3, 5, 6, 8, 11]}],
  "target": 15
}
```
If you have only one data point and no backfillable history, skip the chart and note that
the trend starts next period — don't fake history.

### Output

**Default: a Google Doc** — this is the real artifact. Founders keep a running, shared
update doc for their investors and advisors. Create it via the Google Drive connector
(or append a new dated section to the company's existing running doc), reproducing the
template structure, the OKR block, and the dashboard table as a real table.
- Charts can't be embedded inline into a Doc via the connector reliably, so **also save
  the chart PNG to `/mnt/user-data/outputs/`** and present it; the founder drops it into
  the Doc (and it's ready to attach to the update email).

**When the user wants a polished, emailable, single-file artifact** (chart rendered
inline, ready to send or PDF): build a **self-contained HTML** document instead — same
structure, dashboard table, and the chart inline. Keep the styling clean and neutral
(it's the founder's voice, not a corporate template).

Always end by surfacing, in chat, the headline numbers and the asks list so the user can
sanity-check before it goes out.

---

## OKRs — show the key result, then the number

OKRs are the heart of the update. Render every Key Result as a measurable line, never a
vibe. Use a status glyph so a reader sees red/yellow/green at a glance.

```
Objective 1 — Close the non-dilutive capital stack
  • KR1: Term sheets signed — 1 / 3 🟡
  • KR2: Non-dilutive $ committed — $2.0M / $3.8M 🟡
  • KR3: Grant applications submitted — 4 / 4 🟢

Objective 2 — Reach commercial validation
  • KR1: Signed paid assessments — 0 / 4 🔴  (pipeline $550K, first close slipped to Q3)
  • KR2: ARR — $0 / path to $1M 🔴
```
Status: 🟢 on track · 🟡 at risk / behind pace · 🔴 off track or stalled. A one-clause
parenthetical on a yellow/red KR (why, and the recovery plan) is worth more than a
paragraph elsewhere.

---

## Business subsections

Structure the body around the core dimensions of how a company makes progress. **Each
subsection is skippable** — if nothing notable happened on that dimension this period,
omit it entirely rather than writing "no update." Crowding the update with empty headers
buries the real signal.

| Business dimension | Update subsection | Skip when |
|---|---|---|
| Product & Technology | **Product & Technology** — shipped features, tech milestones, product-market fit signals | no product/tech movement |
| Sales & Traction | **Traction & Business Development** — pipeline, leads, LOIs, contracts, conversion | no pipeline/sales change |
| Market Position | **Market** — TAM/SAM developments, new segments, geographic expansion, pricing | no market developments |
| Competitive Landscape | **Competition** — competitive shifts, wins/losses vs. incumbents, defensibility (moat) | no competitive change |
| Impact & Sustainability | **Impact** — sustainability/impact metrics, ESG milestones, social outcomes | no impact data |
| Team & Organization | **Team** — hires, departures, role changes, key needs | no team change |
| Financial Health | **Financial & Runway** — cash on hand, monthly burn, runway, path to profitability | almost never skipped — runway is always material |

The mandatory metric in every update is **runway** (cash on hand, monthly burn, months
left). Investors track it whether or not anything changed; never bury or omit it.

---

## House rules

- **Lead with the number.** Bold the figure, not the adjective.
- **Carry asks forward.** Never drop an unresolved ask; investors act on them async.
- **Don't pad.** A skipped subsection is better than a hollow one. Three real lines beat
  ten hedged ones.
- **Keep the founder's voice.** This is their letter to their investors. Don't impose a
  corporate template voice or insert opinions unless asked.
- **Confidential by default** if the company has marked prior updates that way.
- **Period cadence:** weekly updates are lighter (general update + OKR deltas + asks +
  chart); monthly updates carry the full template. Match the cadence the company already
  uses.
