---
name: seed-pitch-kit
description: >-
  Generate the complete set of seed-stage fundraising materials for a startup —
  long-form investment memo, TEA & market sizing, financial model, live pitch
  deck, email deck, intro/outreach emails, and a tiered investor list. Use
  whenever a founder wants to build, draft, refine, or pressure-test any
  fundraising deliverable: "write our investor memo," "build a pitch deck,"
  "draft an intro email to a VC," "size our market / TAM," "build a seed
  financial model," "make an investor list," or "turn our deck into a memo."
  Also trigger when a founder pastes deck content, traction data, customer
  quotes, or a financial model and asks for it to be turned into investor-facing
  materials. Output can be generated in Notion, Google Workspace, or Microsoft
  Office, with Canva as an option for decks.
---

# Seed Stage Pitch Kit

A system for producing the seven materials a founder needs to run a focused seed
fundraise. It encodes the structure of each deliverable, a shared voice, and a
set of conventions that keep everything credible and consistent — and it generates
output in whichever platform the team already lives in.

This is one self-contained file. It covers what gets built, how to choose a
platform, the voice that applies everywhere, the cross-cutting rules, and then the
full template for each of the seven deliverables. Read the relevant deliverable
section before drafting that deliverable.

---

## What this produces — the seven deliverables

A well-prepared seed raise needs seven distinct outputs. They serve different
audiences and moments, and they are **built from comprehensive to concise**: do
the deep thinking first, then progressively distill.

| # | Deliverable | Type | Purpose |
|---|---|---|---|
| 1 | Long-Form Memo | document | Give the champion ammunition to sell the deal internally at IC |
| 2 | TEA & Market Sizing | doc + charts | Prove the market is real and the economics work |
| 3 | Financial Model | spreadsheet | Show the founder understands the levers and the path to Series A |
| 4 | Live Pitch Deck | presentation | Guide a 25–30 min live conversation |
| 5 | Email Deck | presentation | Stand alone in an inbox — no presenter |
| 6 | Intro & Outreach Emails | text | Earn the meeting — warm intros, cold outreach, follow-ups |
| 7 | Investor List | table | Target the right investors and track outreach |

### Why build in this order

Most founders start with a deck and work backwards — which produces slides that
look polished but collapse the moment an investor asks a hard question. Starting
with the **memo** forces the founder to confront the full story: why this market,
why now, why them, how the economics actually work, what the real risks are. You
can't hide behind a bullet point in 6 pages of prose.

The **TEA and financial model** come next because they are the quantitative
backbone the memo references — building them early means narrative claims are
backed by real numbers, not retrofitted later. From there each step is shorter and
more targeted: the **email deck** extracts the stand-alone version, the **live
deck** extends it for a conversation, the **intro email** sharpens it to a hook,
and the **investor list** decides where to send it all.

> Note on the decks: send order lists the live deck before the email deck, but
> **build order is the reverse** — build the email-deck core first, then extend it
> into the live deck. The sections below are in build order.

If a founder asks for just one deliverable, build it — but if it's a deck or email
with no memo behind it, flag that the upstream thinking is missing and offer to do
it. A deck built on a memo is dramatically stronger.

---

## Start here — what to gather before drafting

The single biggest lever on quality is **what you bring to the table before you
start.** The materials are only as grounded as their inputs. Spend 30 minutes
gathering the items below and the kit produces drafts that are specific and
credible; skip it and you'll get drafts full of `[REVIEW: ...]` placeholders you
have to fill in by hand.

You don't need everything — bring what you have. Rough is fine. A messy deck and a
back-of-envelope model beat nothing.

**1. Existing materials (even rough ones)**
- Any pitch deck you already have — the single most useful starting point, however unpolished.
- Past investor updates — these are gold. They capture your traction trajectory over time, your milestones, and your own voice. Pull every monthly/quarterly update you've sent.
- One-pagers, prior memos, website/product copy, demo videos, or recorded pitches.

**2. Traction & customer proof**
- Revenue and key metrics (current and historical — show the trajectory).
- Customer list and logos; pipeline data.
- LOIs, signed contracts, paid pilots, design wins, waitlist numbers.
- Customer quotes, testimonials, case studies, or interview notes.

**3. Financials**
- Any financial model or projections you have (even a rough spreadsheet).
- Historical actuals: P&L, monthly burn, current runway, cash balance.
- Cap table.
- Unit-economics inputs: pricing, gross margin, CAC/LTV; for hardware/deep-tech, BOM/cost history, yield data, and supplier quotes.

**4. Market & technical context**
- Market research, industry reports, analyst figures, competitor notes.
- For hardware/deep-tech (feeds the TEA): cost and performance 12+ months ago vs. today, and your assumptions for 12–24 months out.
- Technical overview / architecture, IP and patent status, regulatory situation.

**5. Team**
- Bios and LinkedIn profiles, prior exits or relevant roles, and what the team has built together before.

**6. Round details**
- How much you're raising, structure (SAFE vs. priced), target valuation/cap.
- Initial use-of-proceeds thinking and the milestones this round should hit.
- Anyone already committed; your target timeline.

**7. Investor context**
- Existing investor/advisor relationships and any CRM or contact list.
- Notes from prior investor conversations and the feedback you've gotten.
- Names of investors you already want to target.

**How to feed it in.** Best: connect your data sources (Google Drive, Gmail,
Notion, Slack, a CRM) so the kit can pull current, complete context on its own and
cross-reference across them before drafting. Also fine: paste text directly, or
upload files (decks, spreadsheets, PDFs, docs). For anything you can't share, just
describe it. When a key input is missing, don't invent it — flag it (see Review
Convention) and keep going.

---

## Step 1 — Choose the platform (do this first)

Before generating anything, establish where the team wants their materials to
live. **Ask once, then remember the answer for the whole session.** If an earlier
message already states it, don't re-ask.

> Quick question before I start building: where do you want these to live —
> **Notion**, **Google Workspace** (Docs/Slides/Sheets), or **Microsoft Office**
> (Word/PowerPoint/Excel)? For the decks specifically, I can also build in
> **Canva** if you'd prefer.

Then route each deliverable by type (full mechanics in the Platform Guide near the
end of this document):

| Deliverable | Notion | Google Workspace | MS Office | Canva |
|---|---|---|---|---|
| Memo | Notion page | Google Doc | Word (`.docx`) | — |
| TEA & Market Sizing | Notion page | Google Doc | Word (`.docx`) | — |
| Financial Model | **`.xlsx`** (link in Notion) | Sheet (import the `.xlsx`) | Excel (`.xlsx`) | — |
| Live Pitch Deck | Notion page | Google Slides | PowerPoint (`.pptx`) | Canva deck |
| Email Deck | Notion page | Google Slides | PowerPoint (`.pptx`) | Canva deck |
| Intro & Outreach Emails | Notion page | Google Doc / Gmail draft | Word / Gmail draft | — |
| Investor List | Notion database | Google Sheet | Excel (`.xlsx`) | — |

Two rules that override the table:
- **The financial model is always built as a script-generated `.xlsx` first**, regardless of platform — a 1,500-formula model can't live in Notion or a slide. Google teams then import it to Sheets; Notion teams link to it.
- **Decks and documents that need a file** are created by reading the matching document-creation skill first (`pptx`, `docx`, `xlsx`, `pdf`) and a frontend-design skill for any visual styling. Don't write slide or document code from memory.

A team can mix platforms (e.g., model in Excel, everything else in Notion). Confirm
per deliverable only if their answer was ambiguous.

---

## Voice & tone (applies to every deliverable)

### The Two-Register Rule

All materials operate in two registers, and knowing which one you're in — at every
section, slide, and sentence — separates a compelling kit from a confusing one.

**Register 1 — the 12–18 month plan: sober and earned.** Near-term content must
read like something a skeptical board member signed off on. Milestones are specific
and tied to capital deployed. Progress claims are anchored to actuals with the
driver stated. Risks are named, not sanitized — the mitigant is where confidence
lives. Test: *would a skeptical Series A investor find this credible?*

**Register 2 — the long-term outcome: genuinely exciting.** What happens if this
works? Name the markets that unlock at cost parity, what gets displaced, what the
world looks like when the technology wins. It must feel like the *logical
consequence* of executing the near-term plan, not a separate leap of faith. The
TEA → market-segment table is the mechanical bridge: sober mechanism, exciting
destination.

**The structural rule: earn the vision before you state it.** Front-loading
excitement without near-term proof destroys credibility. Building near-term proof
without ever landing the vision leaves mission-driven investors cold. Prove the
12–18 months first, then let the scale picture land with force.

### Always

- **Confident but grounded.** A real problem with a credible plan. Don't oversell, don't hedge.
- **Specific > vague.** "$18M in signed LOIs from 3 Fortune 500 customers" beats "significant traction." Name names when impressive.
- **Trajectory, not snapshots.** "From proof-of-concept to $1.2M revenue in 9 months" tells a story; a single number doesn't.
- **Lead with insight, not history.** Open with what the founder figured out that others haven't — not a Wikipedia summary of the industry.
- **Data-forward.** Every claim earns a number, a customer name, or a citation.
- **Investor-literate.** Use terms investors know (TAM/SAM/SOM, unit economics, gross margin, runway) without burying the story in jargon.

---

## Cross-cutting conventions

### Review Convention — flag unverified claims inline

Any time the draft includes a number, assumption, or competitive claim not directly
confirmed from source data — market size, unit economics, growth rates, customer
counts, contract values, timelines — flag it inline so a human verifies it before
the material goes out:

```
[REVIEW: confirm total LOI value and count]
```

In Notion, render the flag in **red text** so it stands out. In Word/Google Docs,
use a red font or a highlight; in slides, a red callout or speaker note. A single
wrong number can destroy credibility with an investor — it is far better to ship a
draft with visible review flags than a polished document with buried inaccuracies.
When in doubt, flag it.

### Keep numbers in sync across materials

The same figures (unit economics, scenario outputs, milestones, traction metrics)
appear across the model, memo, decks, TEA, emails, and investor list. **A change to
any input must propagate to every document that references it**, or investors see
conflicting numbers across your materials.

Treat every update as a two-step job: (1) make the change at the source; (2) walk
through every other material and update each instance of the affected number,
preserving context and formatting. After propagating, report what was updated and
flag anything that looked stale but couldn't be verified. When prompted with things
like "ASP is now $1,000 — update everywhere" or "we hired a 5th person — update
team references," do the full propagation, not just the single edit.

### Charts & visualizations

When a memo, deck, or TEA needs a chart, generate it as a polished PNG, then place
it. This one pipeline works for every platform — see the Platform Guide ("Charts").

---

## Iterate; never one-shot

The best results come from iteration, not a single generation pass:

1. **Generate v1** — get the structure and content down.
2. **Pressure-test** — role-play a skeptical investor: "What are the 5 biggest weaknesses here? Where would you push back?"
3. **Refine** — address the weaknesses, tighten the language, sharpen the data.
4. **Get human feedback** — advisors, current investors, or your investor network. No AI replaces real investor feedback.
5. **Final polish** — consistency, formatting, proof points.

Memo ↔ deck iteration is **bidirectional**: editing a slide surfaces gaps in the
memo, and a sharper framing found while tightening a slide should be pushed back to
the memo. Treat the materials as a connected system, not a one-way distillation.

---

## Fundraise timeline (for context when advising)

A well-run seed raise takes ~8–12 weeks from launch to signed term sheet:
- **Weeks -4 to -1 — Preparation:** build deliverables 1–7 in order; practice the pitch with advisors.
- **Weeks 1–3 — Launch:** send the first batch of intros; take 8–12 first meetings/week; refine the pitch on early feedback.
- **Weeks 3–6 — Momentum:** second/partner meetings; share the memo with champions; share the model on request.
- **Weeks 6–10 — Close:** term-sheet negotiation, diligence, legal.
- **After close:** thank-you note to everyone who took a meeting (even passes); set up an investor-update cadence.

---
---

# Deliverable 1 — Long-Form Memo

**Type:** document · **Platforms:** Notion page / Google Doc / Word `.docx`
**Build first.** It forces the full thinking; every shorter format is then compression, not invention.

## Purpose
After a strong first meeting, the investor championing your deal has to sell it
internally to their partners. The memo is the ammunition — the investment memo
*they* would write, done for them. It is **not a deck**: a 4–8 page narrative
document covering the full thesis. Partners who didn't attend the pitch read this
before the IC discussion.

## When to share it
Don't blast it to everyone. Share when a specific investor signals strong interest
and asks for detail, or when they're about to present to their partnership. Offer:
*"Would it help if I put together a detailed write-up your partners could review
ahead of IC?"*

## Tone register by section
Near-term content (problem, TEA trajectory, traction, unit economics, the raise) is
**sober and earned** — test: would a skeptical Series A investor find it credible?
Long-term content (market at scale, the TEA → segment unlock, the vision behind
"What You Need to Believe") is **genuinely exciting** — test: does a mission-driven
investor *want* in? The transition point is the TEA → market-segment table in
Section 4. Earn the vision; don't front-load it.

## Structure

**1. Executive Summary (½ page).** The entire thesis in 4–6 sentences: what you do,
why it matters, why now, what you've proven, what the round funds, why this team
wins. An IC member who reads only this should be able to pitch the deal.

**2. The Problem (1 page).** Go beyond the deck. Data, customer quotes, industry
context; who suffers and how much it costs them. Quantify the pain — build a
pain-quantification table where possible (who's affected, today's cost, total annual
loss across the market).

**3. The Solution & Product (1–1.5 pages).** What you built, how it works, why it
beats alternatives. Include screenshots/diagrams. Explain the tech at a level fit
for a generalist investor — the "smart non-expert" version for deep-tech.

**3a. Moats & Defensibility (0.5–1 page).** Why someone else can't replicate this,
and why the advantage *compounds*. At seed, most moats are nascent — show that
current activity is *building* moats, not that a fortress exists. Mechanisms:
- *Proprietary data & feedback loops* — does each deployment make the next better? Name the loop: what data you collect, how it feeds product improvement, why a new entrant faces a growing gap.
- *Process IP & manufacturing know-how* — yield, process, supplier relationships built over hundreds of runs; tacit knowledge that shows up in cost and quality, not patents. Show the gap vs. a day-one entrant.
- *Intellectual property* — be specific: "our core patent on [technique] blocks the obvious replication path" beats "12 patents filed." Address freedom to operate.
- *Switching costs & integration depth* — quantify: "replacing our system = 6 months requalification + $200K integration."
- *Network effects* — rarer in hardware; if present, show the mechanism.
- *Regulatory/certification moats* — a first-mover through FDA/UL/CE/qualification creates a time-based moat a competitor must also pay.
- *Talent/team moat* — when the team *is* the defensibility (rare expertise, track record together).

*How AI compounds moats:* AI as a **data flywheel** (proprietary sensor/process data competitors can't scrape — deployments → data → better models → better product → more deployments); AI as a **design/simulation advantage** (explore more design space; proprietary sim-to-real data a competitor can't buy); AI as a **process-optimization engine** (yield improving run-over-run from a cold start a competitor must repeat); AI as a **customer-value multiplier** (personalization/predictive maintenance that creates switching costs and a data moat). Quantify each where possible.

*Seed framing:* "Here's what we're building, and why every month of execution widens
the gap." Show the moat trajectory, combining 2–3 mechanisms that reinforce.

**4. TEA: Price & Performance Trajectory (1–1.5 pages).** The analytical heart for
hardware/deep-tech/cost-sensitive businesses. Answer: *where is this on the cost
curve, and when does it win?* Three-part narrative:
- *Where you were (12+ mo ago)* — starting unit cost, performance, scale. If the tech didn't exist, benchmark the incumbent.
- *Where you are today* — cost reduction, performance gains, yield, scale, each anchored to a driver (learning curve, component declines, process, design). Reference verifiable external trends (Wright's Law, GPU/commodity curves). Include a 12-mo-ago → today → change table.
- *Where you're going (12–24 mo)* — project with explicit assumptions; separate external cost-curve effects from your own learning curve; flag rate limiters; show parity analysis (cost, performance, scale parity with incumbents).

*The critical link — TEA → Market Segments → TAM.* Build the table that turns the
TEA from a technical exercise into an investment thesis: each price/performance
level unlocks a market segment of a given size at a given time (today's cost →
early adopters; XX% cost reduction → mid-market; cost+performance parity → mass
market). This shows the TAM isn't static — it's a function of the cost curve. The
question becomes "how fast do you move down the curve to unlock each segment?"
This is the single most powerful frame in the memo.

**5. Market Opportunity (1 page).** Full TAM/SAM/SOM with methodology shown, built
on Section 4. Three layers: top-down (ceiling from reports), bottom-up (customers ×
price — what investors trust), value-based (economic value created × your capture).
Address timing — why the next 3–5 years are the window. See the TEA & Market Sizing
deliverable for full method.

**6. Traction & Validation (1 page).** Everything proving it works — revenue,
customer metrics, pilots, LOIs, partnerships, press, awards — organized
chronologically to show momentum. Include customer quotes / mini case studies.

**7. Business Model & Unit Economics (1 page).** How you make money, margins, how
they improve with scale. Show current unit economics (even if immature) and at-scale
projections, with assumptions explicit. Connect to the TEA: as cost structure
improves, show margins expanding. Reference the model for detail.

**8. Team (½ page).** Why this team uniquely wins — prior relevant experience, key
relationships, technical depth, what they've built together. Address gaps and the
plan to fill them.

**9. The Raise (½ page).** Round size, structure (priced/SAFE), valuation/cap, use
of proceeds, milestone targets, who's committed, timeline, cap-table transparency.
Frame use of proceeds around the 2–3 milestones that de-risk the next round —
connect them to the TEA trajectory and segment unlocks.

**10. What You Need to Believe (½–1 page).** Reframe "risks" as a positive thesis
test: the 3–5 convictions a rational investor must hold, with evidence for each, in
two tiers. *Near-term beliefs (sober):* must be true in 12–18 months, tied to the
milestones this round funds, grounded in what's proven — link each to the TEA.
*Longer-term beliefs (exciting):* must be true for the full opportunity; connect
to the TEA → segment mapping so the big outcome reads as the mathematical
consequence of the near-term trajectory, not a leap of faith. This pre-answers the
classic IC pushback: "what has to be true for this to work?"

## Formatting
- Narrative prose, not bullets — it's a memo, not a presentation.
- Charts/tables/visuals where they clarify (market sizing, traction, unit economics, TEA trajectory).
- Clear section headers so partners jump to what they care about.
- Bold key metrics so they pop when scanning.
- Link to appendix materials rather than inlining everything.

## Prompts that work
- *"Draft an executive summary using our deck, latest traction, and round details — so a partner who reads nothing else can pitch the deal in 2 minutes."*
- *"Identify our 3 strongest moat mechanisms and why they compound; be honest about which are real today vs. nascent."*
- *"Build a TEA trajectory table from our BOM history, yield data, and supplier quotes; then a price-performance → market-segment mapping."*
- *"Build a unit-economics table: current state and at 3 scale milestones, with margin expansion linked to the cost-reduction trajectory; flag assumptions an investor would challenge."*
- *"Draft 'What You Need to Believe': near-term evidence first, then the longer-term market unlock — honest about proven vs. continued execution."*

---
---

# Deliverable 2 — TEA & Market Sizing

**Type:** document + charts · **Platforms:** Notion page / Google Doc / Word `.docx` (charts via the PNG pipeline)
**Build second.** It's the quantitative backbone the memo references and the model is built on.

## Purpose
Prove the market is real, the economics work, and the projections rest on
verifiable assumptions — not wishful thinking. This backs the deck, memo, and model.

## Market sizing: TAM / SAM / SOM
Investors see hundreds of "$100B TAM" slides. Credible vs. laughable is *methodology*.

**Top-down (least credible, useful as a ceiling).** Start with a large report
number, narrow by geography, segment, applicability. E.g. "Global waste mgmt $500B →
US $100B → sorting $15B → our facility type $8B." Necessary but not sufficient.

**Bottom-up (most credible).** Count actual customers × what they'd pay you. E.g.
"350 MRFs in the US → 200 meet our size criteria → at $500K/yr per facility →
SAM $100M." Investors trust this because you can show the customer list.

**Value-based (most compelling for deep-tech).** What economic value do you create,
and what share do you capture? E.g. "Saves a facility $800K/yr in labor → we charge
$500K/yr → 18-month ROI → we capture 62% of value created."

**Always show your math.** Put the methodology in a table or appendix; name sources;
when in doubt use the conservative number and explain why.

## For hardware & deep-tech — cost/performance trajectory
Build a trajectory slide/section:
- **3-column comparison:** 12 Months Ago → Today → 12–24 Months Out.
- **Key metrics:** unit cost, performance, scale — pick the 2–4 that matter most.
- **Assumptions:** anchor to verifiable external trends (component cost curves, Wright's Law) and what you've already achieved.
- **Parity analysis:** when do you hit cost parity, performance parity, scale parity with incumbents?

This connects mechanically to the memo's **TEA → market-segment → TAM** table:
each cost/performance level unlocks a different segment with different TAM
implications (memo Section 4).

## For software companies
- **Unit economics:** CAC, LTV, payback period, gross margin, net revenue retention.
- **Cohort analysis:** retention and expansion by cohort, if you have the data.
- **Benchmarks:** compare to SaaS benchmarks at your stage (Bessemer, OpenView, a16z publish these).

## Common mistakes
- Citing a TAM number without showing how you got there.
- Using "the market is $X billion" from a report without narrowing to your actual addressable segment.
- Assuming 100% market penetration in projections.
- Not distinguishing TAM (total) / SAM (serviceable) / SOM (obtainable in 3–5 yrs).
- Projecting cost improvements without anchoring to learning curves, external trends, or rate limiters.

## Prompts that work
- *"Build a bottom-up market sizing: here are our segments, customer counts, and price points at current and projected cost levels. Cross-reference the TEA trajectory to show SAM expanding as we move down the cost curve. Also build the top-down version from [report] as a sanity-check ceiling."*
- *"Build a value-based sizing: customer savings, our price, ROI, and our share of value captured."*
- *"Generate a cost-waterfall chart showing how much of our cost reduction comes from component declines vs. learning curve vs. design changes."*

---
---

# Deliverable 3 — Financial Model

**Type:** spreadsheet · **Always built as a script-generated `.xlsx` first**, on every platform.
Google teams import the `.xlsx` to Sheets; MS Office teams keep the `.xlsx`; Notion teams link to it.
**Read the `xlsx` skill before building.**

## Purpose
Show investors you understand the business levers, can allocate capital, and have a
credible path to Series A. At seed, it's not about precision — it's about
demonstrating *how you think*.

## What seed investors actually look for
They know the model is largely speculative. They're evaluating:
- **Do you understand your own business?** Can you name the key drivers — what moves revenue, what drives cost, the path to profitability?
- **Are the assumptions reasonable?** Not "50% MoM growth forever" but rates that fit your sales cycle and market.
- **What does the money buy?** If you raise $3M, what do you spend it on, and what does the company look like when it runs out?
- **What triggers Series A?** Which milestones make a Series A investor excited — and does the plan get there?

## Model structure (5–6 tabs)
**Tab 1 — Assumptions & Drivers.** All inputs in one place. Color-code inputs (blue)
vs. formulas (black). Pricing, acquisition rate, churn, headcount plan, unit costs,
growth rates — each with a source or rationale.

**Tab 2 — Revenue Build.** Bottom-up. SaaS: customers × ACV (new logos, expansion,
churn). Hardware: units × price (production ramp). Marketplace: GMV × take rate.
Monthly for Year 1, quarterly for Years 2–3.

**Tab 3 — Cost Build.** COGS / cost of revenue, then opex by department (R&D, S&M,
G&A). Tie headcount to hiring milestones. Show the gross-margin trajectory.

**Tab 4 — Cash Flow & Runway.** Monthly cash in, cash out, net burn, ending balance.
Show when money runs out under current assumptions and when you need to raise again.
**The most important tab for a seed investor.**

**Tab 5 — Scenarios.** Base, upside, conservative. Vary the 2–3 assumptions that
matter most (growth rate, sales cycle, pricing); show how runway changes.

**Tab 6 — Use of Proceeds.** Map the raise to buckets (headcount, equipment/infra,
GTM, R&D, working capital, buffer) and tie to milestones.

## Formatting & presentation
- **Keep it simple.** A clear 5-tab model beats an opaque 20-tab one. If an investor can't follow the logic in 15 minutes, it's too complex.
- **Monthly granularity for 18–24 months**, quarterly/annual after.
- **Show your work.** Every output links to an input; no hard-coded numbers in formula cells.
- **Summary dashboard** — one page with the 8–10 numbers that matter: revenue, burn, runway, headcount, key milestones by quarter.
- **Version control.** Date models; keep old versions — investors may reference an earlier one.

## Common mistakes
- Hockey-stick projections with no explanation of what changes in month 8 to cause the inflection.
- Assuming zero churn or 100% close rates.
- Not modeling the hiring plan (headcount is usually 70–80% of seed-stage spend).
- 5-year false precision — seed investors care about the next 18–24 months.
- No "things go slower" scenario.
- Forgetting working capital, taxes, or one-time costs (equipment, deposits).

## Script-generated approach (for models with 500+ formulas)
A complex model (1,000+ formulas across tabs) is fragile when edited cell-by-cell.
Regenerating from a parameterized script guarantees formula integrity, consistent
cross-sheet references, and zero-error verification on every version.

Process:
1. Document all parameters (unit economics, headcount plan, production ramp, R&D budget, overhead) in one place — a **Parameters & Changelog** record.
2. Maintain a Python build script that generates the `.xlsx` from those parameters.
3. On each update: regenerate the full `.xlsx`, run the formula recalculation/verification, confirm zero errors.
4. Log the change (what changed and why) on the changelog.
5. The team downloads the new `.xlsx`; a Google team re-imports to Sheets (the working/sharing copy).

**To request an update:** describe the change ("ASP is now $1,000", "add a 4th
scenario with slower customer ramp"). Update the script, regenerate, verify, log —
then propagate the changed numbers to every other material (see "Keep numbers in
sync").

## Prompts that work
- *"Build a 5-tab seed model from these assumptions: [pricing, ramp, headcount, costs]. Monthly Year 1, quarterly Years 2–3, with base/upside/conservative scenarios and a summary dashboard. Verify zero formula errors."*
- *"Update ASP to $1,000 in the model and propagate to all materials."*
- *"Add headcount for a marketing hire starting month 6; regenerate and show the new runway."*

---
---

# Deliverable 4 — Email Deck

*(Build the email deck before the live deck — it's the core both share. Send order is the reverse.)*

**Type:** presentation · **Platforms:** Notion page / Google Slides / PowerPoint `.pptx` / **Canva**
**Derived from the memo, then compressed to stand alone.**
**Read a frontend-design skill for styling and the `pptx` skill before producing a file.** See the Platform Guide for per-platform mechanics and the Canva flow.

## Purpose
Sent ahead of or alongside the intro email. It must **stand alone** — no one is
narrating. An investor flips through it in 2–3 minutes on their phone. If it doesn't
make the case on its own, you don't get the meeting. **10–15 slides.** This is a
distillation of the long-form memo, not a fresh invention — the thinking is already
done; the work here is compression.

## How it differs from the live deck
| | Email Deck | Live Deck |
|---|---|---|
| Audience | Investor reading alone | Investor in a room with you |
| Slides | 10–15 | 15–25 + appendix |
| Text density | Higher — must self-explain | Lower — you narrate |
| Appendix | Optional, keep tight | Yes — anticipate questions |
| Goal | Get the meeting | Get the *next* meeting (partner meeting, diligence) |

## Slide structure (10–15 slides)
1. **Title** — company, tagline, logo, contact, and the round you're raising.
   - *Tagline formula:* `[Company] helps [audience] [solve a specific problem] with [unique solution/secret sauce].` Two versions: a **short** one for the title slide (ends at the punch — "...go from digital design to finished composite in days — no molds, no tooling, no shipping") and a **full** one for emails/memos that adds the mechanism.
   - *Audience specificity:* broad when the platform story matters ("product creators"); specific when beachhead credibility matters ("board shapers"). A generalist may prefer broad; a deep-tech specialist, specific.
   - *Failure modes:* too generic ("the digital manufacturing platform for X" — a category, not a value prop); too long (won't fit at 24pt); missing the problem (leads with tech); missing the secret sauce ("make products faster" — everyone says this).
2. **Problem** — what's broken, for whom, why it matters. A specific story or data point, not an abstract industry overview. Make the investor *feel* it. (Hardware/deep-tech: frame the **design–manufacturing gap** — engineers can design things existing processes can't build — it lands harder than "incumbents are slow.")
3. **Solution** — what you built, in plain language. *Show* the product (screenshots, photos, diagrams). Be **complete about what's replaced** — not just the headline component (e.g. molds *and* hand-laid composite work).
4. **Why now** — the market shift, tech unlock, or regulatory change making this possible and urgent *now*. Often the most underinvested slide — don't skip it. Compress macro trends to one punchy line.
5. **Market size** — TAM/SAM/SOM, methodology shown, bottom-up over top-down. Close with the scale implication of the TEA trajectory (market unlocked at parity), not just static TAM.
6. **Business model** — how you make money, unit economics if you have them, pricing, gross margins (actual or projected with assumptions stated).
7. **Traction** — the slide investors flip to first. Revenue, customers, pilots, LOIs, waitlist, growth rate. Show trajectory ("X to Y in Z months"). Pre-revenue: validated demand (LOIs, paid pilots, design wins).
8. **How it works / Technology** — one slide on what makes the approach defensible. Deep-tech: the insight, not the full science. If an investor can't explain your tech to their partners, it won't pass IC.
9. **Competition / Why us** — positioning matrix or landscape. Never claim "no competitors"; say what you do differently and why it matters. Acknowledge incumbents.
10. **Team** — photos, names, relevant experience. Highlight the 1–2 things that make this team uniquely qualified. **Connect each person to the specific problem**, not just credentials.
11. **Go-to-market** — how you acquire customers; channels, partnerships, sales cycle; for hardware/deep-tech, the adoption path.
12. **The ask** — what you're raising, for what, to what milestone: "Raising $3M to hit [milestone] by [date], positioning us for Series A / breakeven / non-dilutive raise."

## Shared design principles (apply to BOTH decks)
- **One idea per slide.** Two things → two slides.
- **Visuals over text** — charts, product photos, diagrams >> bullets.
- **Readable on a phone** — 24pt+, high contrast.
- **Consistent branding** — brand colors, logo, clean template.
- **No animations** — they break in email/PDF.
- **Stat callouts** (60–72pt number + small label) are the most scannable format — use on Problem, Solution, Traction, Unit Economics.
- **Comparison tables** land fast for Competition and Unit Economics.
- **Diagrams > prose** for systems (flywheels, feedback loops, architecture).
- **Bottom banners** — a one-line takeaway at the bottom of key slides ensures the message lands even on a skim.
- **Traction without logos** — a styled name wall (clean grid, all-caps, muted type), with the single best-known win in a distinct callout card. Lead with the best-known name.
- **Margin story shows causation** — not "45% → 82%" but "automating the most expensive step cuts per-unit cost $450 → $160, driving margin 46% → 72%." If the lever hasn't shipped, pre-answer "what if it's late?" (current margins already work; the milestone is upside).
- **Plan content type per slide** — chart, diagram, image, or text — so no slide defaults to a wall of text.

## Two-register discipline (email deck)
No one is narrating, so structure does the register work. **Sober slides** — Problem
(quantified pain), Traction (actuals), Business Model (current unit economics with
assumptions), The Ask (specific milestones). **Earned-excitement slides** — Why Now
and Market Size, but only *after* Problem → Solution → Traction establish
credibility. **Sequencing rule:** Problem → Solution → Traction comes before Market
Size — the investor must believe the near-term is real before getting excited about
the long-term. Don't lead with the big TAM number; earn it.

## Prompts that work
- *"Distill our long-form memo into a 12-slide email deck that stands alone — no presenter. For each slide, propose the content type (chart, diagram, image, or text)."*
- *"Review my current deck against this email-deck structure. What's missing? What's too long? Rewrite Problem and Solution to be self-explanatory."*

---
---

# Deliverable 5 — Live Pitch Deck

**Type:** presentation · **Platforms:** Notion page / Google Slides / PowerPoint `.pptx` / **Canva**
**Derived from the memo and the email deck.** Build the email-deck core first (above), then extend it here.
**Read a frontend-design skill for styling and the `pptx` skill before producing a file.** See the Platform Guide for per-platform mechanics and the Canva flow.

## Purpose
Guides a 25–30 minute live conversation. Unlike the email deck, **you** are the
main event — the slides support your narrative. **15–25 slides + a 5–15 slide
appendix** for Q&A. The goal of the meeting is to get the *next* meeting (partner
meeting, deep-dive, or diligence).

## How it differs from the email deck
Longer, more visual, less text-heavy — because you're narrating. It carries an
appendix of pre-built answers to the questions you know will come, so the best
founders never say "I'll get back to you" — they flip to the appendix. The two
decks are genuinely different artifacts: the email deck self-explains on a phone;
the live deck is a visual scaffold for a conversation. Build them as separate files,
but apply the same shared design principles (above).

## Slides to add beyond the email-deck core
Start from the 12-slide email-deck spine, then add:
- **Customer case study / testimonial** — one specific story: before, what changed, the outcome. Real quotes are gold.
- **Product roadmap** — next 12–24 months, high-level; show vision beyond the current product.
- **Cost/performance trajectory** — the TEA slide (12 mo ago → today → 12–24 mo) for hardware/deep-tech.
- **Unit-economics deep-dive** — gross-margin breakdown, payback, LTV/CAC.
- **Use of proceeds** — 3–4 spending buckets; show you've thought about capital allocation.
- **Milestones to Series A / breakeven / non-dilutive raise** — what success looks like in 18–24 months; which metrics excite a Series A investor; what unlocks revenue-based or off-balance-sheet finance.

## Appendix (have ready, don't present unless asked)
Detailed competitive analysis · full TAM/SAM/SOM math · technical architecture or
IP · regulatory landscape and timeline · detailed financials · customer-pipeline
detail · org chart and key hires · cap-table summary. **Build a slide that
pre-answers each hard question** ("what if the key milestone ships late?", "how do
current margins work without the target cost reductions?", "what's the moat if
someone copies the hardware?"). The appendix is where partner meetings are won.

## Shared design principles
All the design and visual-communication principles in the email-deck section
(stat callouts, comparison tables, diagrams > prose, bottom banners, traction
display, margin causation, team framing, one idea per slide) apply here too. The
live deck has more room for depth, but the same rules hold.

## Two-register discipline (live deck)
The live deck spans both registers, and the handoff is where the best pitches build
momentum. **Sober slides** (Problem, TEA trajectory, Traction, Unit Economics, Use
of Proceeds, Milestones) are the credibility engine — anchor every claim to actuals;
if a skeptical partner would push back on a number, it must be airtight. **Exciting
slides** (Why Now, Market Opportunity, the vision implied by the Milestones slide)
give investors permission to imagine the big outcome — connect to the TEA → market-
segment unlock (the mass market at parity, what gets displaced, category
leadership). In Q&A or an appendix slide, frame the thesis as "What You Need to
Believe": what must be true in 18 months (sober, evidence-backed) and what follows
if it holds (exciting, scale picture).

## Presentation tips
- **Practice the 3-minute version** — if asked for the quick version, deliver it compellingly, then expand where they lean in.
- **Read the room** — spend time where they're engaged; the deck is a guide, not a script.
- **The first 2 minutes matter most** — open with the most compelling thing about the company, not background or mission statement.
- **End with a clear next step** — "We'd love to meet the full partnership" / "Can we schedule a technical deep-dive?" Don't end without asking for the next meeting.

## Prompts that work
- *"Extend our email deck into a live pitch deck. Add a customer case study, a TEA trajectory slide, and an appendix answering the top 10 questions investors will ask."*
- *"Build appendix slides that pre-answer: what if our key automation milestone ships late, and how do current margins work without the target cost reductions?"*

---
---

# Deliverable 6 — Intro & Outreach Emails

**Type:** text · **Platforms:** Notion page / Google Doc / Word / **Gmail drafts** (offer to create drafts directly if Gmail is connected).

## Purpose
Get the meeting. The intro email is not the pitch — it's the hook. Investors decide
in ~30 seconds whether to take the call. A warm intro is actually **three emails**,
and most founders only draft one. Warm intros convert at ~40–60%; cold at ~5–10% —
always prefer warm.

## The three emails in a warm intro

### Email A — the forwardable blurb (you → connector)
Make saying yes effortless: a short personal note (2–3 sentences) + a clearly
separated, **third-person** blurb the connector can forward in 30 seconds.

```
Subject: Intro request — [Investor Name] at [Fund Name]

Hi [Connector],

I'm kicking off our seed raise and [Investor Name] at [Fund Name] is high on our
list — [1 sentence on why they fit: thesis, a portfolio company, something they
wrote]. Would you be open to making an intro?

I've written a short blurb below you can forward directly or edit. Happy to give
you whatever context helps.

Thanks,
[Your name]

---
FORWARDABLE BLURB:

[Investor first name] — wanted to connect you with [Founder Name], CEO of [Company].
They're building [one sentence: what you do, for whom]. [Why interesting — 1–2
sentences: a specific traction proof point + a why-now]. [Founder]'s background is
[1 sentence on credibility]. They're raising a seed round and I think it's a strong
fit for [Fund]'s [thesis/focus]. Happy to make the intro if you're interested.
```

- **Third person**, because it comes from the connector's mouth ("They're building X," not "We're building X"). The #1 mistake is writing it in first person.
- **Separable** — set it off below a line break / labeled so it's copy-paste-ready.
- **Under 100 words.** The connector's credibility opens the email; the blurb just needs to earn the meeting.

### Email B — the connector's intro (connector → investor)
You don't write it, but draft it for them. The connector answers two questions in
2–3 sentences: why trust this founder, and why is this relevant to you.
**Double opt-in (preferred):** connector asks the investor "want an intro?" with the
blurb, *without* cc'ing the founder; if yes, sends a separate email cc'ing both.
Protects the relationship if the answer is no. **Single opt-in (faster):** connector
emails the investor and cc's the founder directly. Coach connectors gently: "I've
drafted a short blurb — forward as-is or edit; double opt-in is fine too."

### Email C — your follow-up after the intro (you → investor)
Reply within 24 hours. **Move the connector to BCC** (say so — good etiquette).
3–4 sentences max; the connector already did the selling.

```
Subject: [keep the existing thread subject]

Hi [Investor first name],

Thanks [Connector] for the intro — moving you to BCC to save your inbox.

[Investor], great to connect. [Optional: 1 sentence showing you did your homework —
a portfolio company, a post, a thesis. Not flattery.] I'd love 30 minutes to walk
you through what we're building. I've attached a brief overview deck — would any of
these times work? [2–3 specific windows or a scheduling link.]

Best,
[Your name] · [Title, Company]
```

- **Shorter than you think** (4–8 lines). Re-pitching everything signals you don't trust the intro.
- **The "why you specifically" sentence** is the highest-ROI line — concrete and authentic; skip it rather than fake it.
- **Deck: attach or link?** Warm intros → **attach a PDF** (lowest friction). Cold → **DocSend link** (track engagement); don't email-gate at this stage.

## Cold outreach (no connector)
Use only for Tier 2–3 after warm paths are exhausted. The "why this investor
specifically" sentence is **non-negotiable** here — it's the difference between
"I'm emailing 80 people" and "I chose you."

```
Subject: [Company] — [one-line description]

Hi [Investor first name],

I'm [Name], founder of [Company]. We [what you do — one sentence, plain English].

I'm reaching out because [why this investor specifically — their thesis, a portfolio
company, a post or talk]. [Why now — one sentence: the shift/regulation/unlock
creating urgency.] [Traction — your single most impressive, specific metric.] [Team
— one sentence: prior exits, domain expertise, unfair advantage.]

Would you be open to a 25-minute call? Brief deck here: [DocSend link].

Best,
[Name] · [Title, Company]
```

Lead with traction, not market context. A "why now" is a specific event with a date
("EPA contamination standards effective Jan 2027 force 350 MRFs to upgrade"), not
"the market is growing."

**Use an LLM for thesis research.** Feed the investor's name + firm with web search:
"What is their stated thesis? What have they invested in recently adjacent to [our
space]? Have they published on [our sector]?" Batch this across the whole list; you
pick the most authentic detail and write the sentence yourself. This also fills the
"Thesis Fit" column on the investor list.

## Follow-up sequence
Non-response usually means "haven't gotten to it," not "no." **Two follow-ups max**
for both warm and cold — after that, silence is an answer; move to a revisit list
and circle back in 2–3 months with a real update.

- **Warm:** Day 4–5 short bump (don't re-pitch); Day 10–12 optional bump with a *new* proof point.
- **Cold:** Day 3–4 short bump; Day 8–10 last bump.
- **Timing:** send initial outreach Tue–Thu, 8–10 AM in the investor's time zone. Avoid Mondays/Fridays. Never weekends.

## Common mistakes
Over-written emails (4 sentences beat 3 paragraphs) · spray-and-pray with no
personalization · burying traction below background · vague "why now" · not writing
the forwardable blurb · waiting >24h after an intro · leaving the connector on the
thread · following up more than twice.

---
---

# Deliverable 7 — Investor List

**Type:** tracker · **Platforms:** Notion database / Google Sheet / Excel `.xlsx`
A database (Notion) or sheet gives you filtering and status views for free.

## Purpose
Target the right 40–80 investors, prioritize them, and track outreach. A well-built
list is the difference between a focused 8-week raise and a scattered 6-month slog.
Organize by **fit, not prestige.**

## Three tiers
- **Tier 1 (10–20): high-conviction.** Stated interest in your sector, adjacent portfolio companies, and a warm path. You can name why each fits in one sentence.
- **Tier 2 (15–30): strong fit, weaker path.** Right thesis and check size, no warm intro yet. Where you invest effort building connections.
- **Tier 3 (15–30): spray zone.** Generalists, newer funds, angels. Fill the pipeline; sometimes surprise you.

## Filtering criteria (know or research for each)
- **Thesis fit** — sector, stage, geography; have they written about your problem?
- **Check size** — does their typical check match your need? (A $500K check from a $50M fund ≠ from a $500M fund.)
- **Portfolio conflicts** — any competing investment? Check carefully.
- **Recent activity** — deployed from this fund recently? A fund 4 years into a 5-year period may be mostly deployed.
- **Warm path** — who can intro you, and how strong is the connection?
- **Decision maker** — who at the firm owns this deal? Don't pitch the wrong partner.

## List structure (columns)
`Firm` · `Contact` · `Tier` · `Thesis Fit (1 sentence)` · `Check Size` · `Warm Path`
· `Intro Requester` · `Status` · `Next Step` · `Notes`

Example row: *Example Fund · Jane Partner · 1 · "Leads climate hardware seed rounds,
invested in [similar co]" · $1–3M · "Our advisor Bob knows her well" · Bob ·
Intro requested · "Follow up with Bob by Fri" · "Spoke at [conf] about our space."*

## How to build it
1. **Start with your network.** Ask every current investor and advisor: "Who are the 3 best seed investors for a company like ours?"
2. **Mine portfolio companies.** Who invested in similar companies (sector, stage, model)? Crunchbase, PitchBook, fund sites. A deal in your space 18 months ago = probably still interested.
3. **Check fund timing.** A just-closed fund is hungry to deploy; one late in its period may not have room.
4. **Use NFX Signal** (signal.nfx.com) — a free interest-based matching platform, useful for discovering smaller funds, solo GPs, and sector-specific investors, and for seeing who's signaling interest in *you*.
5. **Cross-reference with AI.** Connect your assistant to your CRM, email, and any contact database: "For each firm on this list, do we know someone there? Who owns the relationship?" Turns hours of spreadsheet work into minutes.
6. **Lean on your investors and advisors.** If you're backed by a fund or accelerator, ask them to cross-reference their network for warm paths to your target firms — this is one of the highest-value things they can do for you.

## Cadence
Once you launch, aim for 8–12 new investor meetings/week. Front-load Tier 1 in weeks
1–3 to build momentum and create urgency — but don't blast all 60 in week one;
you'll burn your best meetings before the pitch is refined.

## Prompts that work
- *"Using our CRM data, build a tiered investor list. Sector [X], stage [seed], geography [Y], round size [Z]. Cross-reference our contacts to identify warm paths and who on our team owns each relationship."*
- *"For each Tier 1 firm, research the partner's thesis and recent adjacent deals, and draft the one-sentence Thesis Fit."*

---
---

# Platform Guide — generating output in Notion, Google, MS Office, or Canva

Read this before producing any file. The team picks one home platform at kickoff
(Step 1). This tells you how to honor that choice for each deliverable type:
**documents**, **presentations**, and **spreadsheets**.

## 1. Documents — memo, TEA & market sizing, emails

**Notion.** Create the document as a Notion page using Notion-flavored Markdown. Use
clear `##` section headers so partners can jump around, bold key metrics, and use
real tables for comparison data. Render `[REVIEW: ...]` flags in **red**
(`{color="red"}`). If creating under a fundraise hub the founder already has, pass
it as the parent. Before editing an existing page, fetch it with discussions
included and **do not overwrite text that has an open comment** (see §5).

**Google Workspace.** Two reliable paths:
- *Produce-then-import (default):* generate a `.docx` by reading the `docx` skill, then upload it to Google Drive. Drive converts a `.docx` to a native Google Doc on import.
- *Copy-a-template:* if your team has a narrative template (a Google Doc), the cleanest path is to copy that file and fill it, preserving styling.

For emails specifically, a Google team usually wants either a Google Doc they can
share or **Gmail drafts** — offer to create the drafts directly if Gmail is connected.

**Microsoft Office.** Read the `docx` skill, then generate a Word document with
clean headings, tables, and a letterhead-style layout. Save and present it.

**Format guidance for all documents.** Write memos in **narrative prose**, not
bullet points — it should read like a memo, not a deck. Bold key stats so they pop.
Link to appendix materials (model, TEA) rather than inlining everything.

## 2. Presentations — live pitch deck & email deck

A deck is the one deliverable with four possible homes. Always **read a
frontend-design skill** for visual styling, and the `pptx` skill when producing a
PowerPoint file.

**Notion.** No native slide mode. Build a **deck-style page**: one `##` heading per
slide, with the single key point as a callout and supporting visuals as images
below. A readable substitute for an email deck, but not for a presented deck — for
real slides, steer the team to Google, Office, or Canva.

**Google Workspace.** *Copy-a-template (preferred for decks):* copy the team's
Google Slides investor-deck template and fill it, keeping brand styling intact.
*Produce-then-import:* generate a `.pptx` (read the `pptx` skill), upload to Drive;
Drive converts to Google Slides on import.

**Microsoft Office.** Read the `pptx` skill and generate a PowerPoint, honoring the
slide structure in the deck sections (one idea per slide, stat callouts, comparison
tables).

**Canva.** Offered **for decks only**. If the team chooses Canva and the Canva
connector is available, use it so they can collaboratively edit and brand it in
Canva afterward. If the Canva connector is **not** connected, say so plainly and
offer to (a) connect it, or (b) produce a `.pptx`/Google Slides deck instead — don't
silently fall back. Still follow the one-point-per-slide discipline.

**Deck rules on every platform.** One idea per slide · visuals over text · readable
on a phone (24pt+) · no animations (they break in email/PDF) · stat callouts · decide
each slide's content type (chart, diagram, image, text) up front.

## 3. Spreadsheets — financial model & investor list

**Financial model (always xlsx-first).** Built as a script-generated `.xlsx` on
every platform (see the Financial Model deliverable). Then: Google team imports the
`.xlsx` to Sheets (their working/sharing copy); MS Office team keeps the `.xlsx`;
Notion team keeps the `.xlsx` as source of truth and links to it (or its Sheets
copy) from the fundraise page — don't rebuild the model as a Notion table.

**Investor list.** Match the home platform. Notion: a database with the columns
above (filtering and status views for free). Google: a Google Sheet (produce an
`.xlsx` and import, or build directly) with a tier filter. MS Office: an `.xlsx`
(read the `xlsx` skill).

## 4. Charts & visualizations

One pipeline serves all platforms: **generate → download → place.**

**Generate.** Use Python (matplotlib, plotly, or seaborn) to produce investor-grade
PNGs. Generate all requested charts in a single batch and present them together.

**Place.** The same PNGs drop into any destination: Notion (bulk-upload to the
bottom of the page, then move each block to its spot — if your Notion integration
can't upload files, you'll do the drag-and-drop; provide a clear list of which chart
goes where); Google Slides/Docs, PowerPoint, Word, Canva, email (insert directly).

**Quality standards:** investor-grade polish (no chartjunk, no 3D); PNG at 2×
resolution, 1600px+ wide, transparent background when the destination is unknown;
sans-serif typography with clear labels; consistent modern palette (default
blues/teals unless the company has brand colors); label key data points directly;
small source attribution bottom-left when citing third-party data.

**Highest-value chart types:** techno-economic trajectory (cost/margin over time);
TAM breakdown (treemap or proportional bars by segment); financial scenario overlay
(base/bull/bear); gross-margin bridge (waterfall); process comparison (grouped bar
or radar vs. incumbents); pipeline funnel; unit-economics snapshot. *Tip:* the best
visuals tell their story alone — if a chart needs a paragraph, iterate on the one
5-second takeaway.

## 5. Notion-specific care

**Preserve comment threads.** Notion comments are anchored to specific text. If you
overwrite text that has a comment, the thread detaches and unresolved feedback is
lost. Before editing a page, fetch with discussions included, note which ranges have
active threads, and **never replace commented text** — insert new content after it
instead, and let humans resolve threads manually. Resolved threads' anchored text
can be edited safely.

**Red review flags.** Use `{color="red"}` so `[REVIEW: ...]` flags are obvious to
whoever verifies the numbers.

## 6. Deal-room requirements by stage

As conversations progress, investors request a deal room. Prepare by stage:

**Seed.** Essential: pitch deck; one-page executive summary; team bios + LinkedIn;
cap-table summary; high-level 3-year projections; any LOIs or customer commitments.
Nice to have: product demo video; 1–2 page technical architecture; market-research
sources.

**Seed+ / Bridge.** Everything from Seed, plus: updated financials with actuals
since Seed; 2–3 customer references willing to take calls; detailed product roadmap;
key-metrics dashboard; use-of-funds breakdown for this round.

**Series A.** Everything from Seed+, plus: full financial model with detailed
assumptions; 12+ months of monthly actuals; cohort analysis (if applicable);
unit-economics breakdown; competitive landscape analysis; org chart and key-hire
plan; IP summary; material-contracts summary; recent board decks/minutes.
