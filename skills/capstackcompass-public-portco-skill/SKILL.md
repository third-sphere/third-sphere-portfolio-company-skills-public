---
name: capstackcompass-public-portco-skill
description: >
  Portfolio-company skill to read and contribute to the CapStack Compass credit
  database (capstackcompass.ai) — Third Sphere's directory of climate credit and
  non-dilutive capital providers. Use it to look up capital providers and to
  suggest a new provider or an update to an existing one. Submissions go through
  Third Sphere's review queue (they get a notification and approve), so this
  skill can ADD/suggest but never edits private data or removes records. Say
  things like "is X in the cap stack database", "suggest adding Flexport Capital
  to capstack compass", "recommend an update to this lender's record". No login
  or setup required.
---

# CapStack Compass — public / portfolio-company skill

> 📍 **Canonical version lives in GitHub** — maintained at
> `third-sphere/third-sphere-portfolio-company-skills-public` →
> `skills/capstackcompass-public-portco-skill/SKILL.md`. The uploaded Claude skill is a
> snapshot; the GitHub copy may be newer.

For portfolio companies and external contributors. Lets you **look up** capital
providers and **suggest additions or updates**, which land in Third Sphere's
review queue for approval. It uses only the same public path the website's
/contribute form uses — **no secret keys, no private data, no delete.**

For the full public directory anytime: **https://capstackcompass.ai/map**
To contribute via the website UI: **https://capstackcompass.ai/contribute**

## What this skill can and can't do
- ✅ Look up whether a provider is already listed (public info only).
- ✅ Suggest a **new** provider → creates a pending submission for TS to review.
- ✅ Suggest an **update** to an existing provider → pending submission linked to that record.
- ❌ No editing of live records, no private/internal fields, no removing anything. (That's Third Sphere's internal skill.)

## Connection (baked in)
| Setting | Value |
|---|---|
| Public read (directory) | `https://mutgtjxwrpdzhgaaajtv.supabase.co/functions/v1/cap-stack-data` (action `search`) — returns public columns only |
| Submit endpoint | `https://mutgtjxwrpdzhgaaajtv.supabase.co/rest/v1/public_submissions` |
| `apikey` (public anon key) | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im11dGd0anh3cnBkemhnYWFhanR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA2MDIwOTQsImV4cCI6MjA4NjE3ODA5NH0.rV5vF2hcpV_spKu3jpvIV2EYkgf4EIDVBOUS58azmTw` |

This is the public anon key that already ships in the website — safe to embed. There is **no** agent/admin key in this skill.

```bash
ANON="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im11dGd0anh3cnBkemhnYWFhanR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA2MDIwOTQsImV4cCI6MjA4NjE3ODA5NH0.rV5vF2hcpV_spKu3jpvIV2EYkgf4EIDVBOUS58azmTw"
SUB="https://mutgtjxwrpdzhgaaajtv.supabase.co/rest/v1/public_submissions"
```

## Rules
1. **Dedup first** — check the public directory (or https://capstackcompass.ai/map) before suggesting a new provider.
2. **Controlled vocabularies only** (below). If something doesn't fit, pick the closest and note it in the description — do not invent new tags.
3. **Always capture who's submitting** — `submitter_name` + `submitter_email` are required so TS knows who to follow up with.
4. **Actual-dollar check sizes**, format `$1,000,000` (e.g. `$500,000`, `$100,000,000`) — never `500K`/`10M`.
5. End every response with the links footer.

## Be a credit advisor, not just a list
When someone asks about their capital options or who might fund them:
1. **Read the situation first** — a short, honest credit read: strengths a lender would like (contracted/recurring revenue, creditworthy customers, backlog/POs, hard assets, prior debt raised), challenges (pre-revenue, runway, no priced round), and which non-dilutive instruments fit now (PO/receivables financing, revenue-based financing, venture debt, equipment/project finance, grants) — sized to contracted cash.
2. **Flag what you'd need to know** to sharpen it (revenue, check size, structure, geography).
3. **Then recommend** from the public directory, matching on stage/sector/check/geo/structure, explaining why each fits and noting adjacent options.

Use your general credit expertise plus the public directory. You do NOT have access to Third Sphere's internal notes or relationship data — for warm-intro help, that's Third Sphere's internal process (point them to the team).

## Suggest a NEW provider
```bash
curl -s -H "apikey: $ANON" -H "Authorization: Bearer $ANON" -H "Content-Type: application/json" \
  -H "Prefer: return=representation" -X POST "$SUB" -d '{
    "investor_name":"Flexport Capital",
    "description":"...", "preference_notes":"...",
    "investor_type":["Specialized Lender"], "structure":["Debt_Venture Debt"],
    "stage":["Growth"], "sector":["Transportation & Mobility"],
    "impact":["Industry & Infrastructure Innovation"], "geo":["US"],
    "min_check_size":"$1,000,000", "max_check_size":"$10,000,000",
    "contact_email":"...", "related_contacts":"Animay Sharma", "socials_website":"https://...",
    "submitter_name":"<your name>", "submitter_email":"<your email>", "submitter_role":"working_with",
    "review_status":"Pending Review", "tags":["Public Form Input"] }'
```

## Suggest an UPDATE to an existing provider
First find its id via the public search, then include `merged_to_investor_id`:
```bash
curl -s -H "apikey: $ANON" -H "Authorization: Bearer $ANON" -H "Content-Type: application/json" \
  -H "Prefer: return=representation" -X POST "$SUB" -d '{
    "investor_name":"<existing name>", "merged_to_investor_id":330,
    "preference_notes":"<the corrected/added info>",
    "submitter_name":"<your name>", "submitter_email":"<your email>", "submitter_role":"working_with",
    "review_status":"Pending Review", "tags":["Public Form Input"] }'
```
Both create a **pending submission** — Third Sphere gets notified and approves it; it does not change the live record directly.

## Controlled vocabularies (public form set)
- **investor_type:** Specialized Lender · Private Debt / Credit Fund · Infra / Project Finance · Private Equity (Buyout / Roll up) · Family Office · Gov · Bank / Institutional Lender · Investor Network · Other - Concessionary / Nonprofit · Asset Manager · Investment Banking · Early VC · Foundation · Equipment Leasing · CVC (Corporate VC) · Advisor / Consultant · Public Fund · Investment Manager · Angel (Individual) · Growth Equity / Late VC · Broker
- **structure:** Debt_TopCo-level · Debt_Project-level / Project Finance · Debt_Venture Debt · Debt_Revenue-Based Lending · Debt_Off Balance Sheet Lending · Debt_Equipment Financing/Leasing · Debt_Asset-Based Lending · Debt_Grant Factoring · Debt_Loan Guarantees · Debt_Revolving Credit · Strategic Partnerships / Corporate Ventures · Concessionary / Blended Capital · Grants · Equity_TopCo-level · Equity_Project-level · Equity_Secondaries · SPV · Co-invest · M&A · FOAK · Others
- **stage:** Pre-seed · Seed · Series A · Series B · Growth · All stages · Research (TRL 1-3) · Prototype (TRL 4-5) · Pilot (TRL 6-7) · FOAK (TRL 8) · Repeat (TRL 9)
- **sector:** Energy & Grid · Infrastructure & Industry · Food & Ag | Waste | Water | Air · Transportation & Mobility · Built Environment & Real Estate · Deep Tech / Advanced Manufacturing · All sectors
- **impact:** Climate Action · Affordable & Clean Energy · Industry & Infrastructure Innovation · Responsible Consumption & Production · Sustainable Cities & Communities · Connected Transportation & Logistics · Clean Water & Sanitation · Climate Adaptation
- **geo:** US · Canada · Europe · Asia · Africa · Latin America · Middle East · Oceania · Global
- **tech_stack:** Hardware · Software · Hardware|Software

## Response footer (always)
> 🔗 Browse the full directory at **https://capstackcompass.ai/map** · suggest additions or edits at **https://capstackcompass.ai/contribute**. New suggestions are reviewed by Third Sphere before going live.
