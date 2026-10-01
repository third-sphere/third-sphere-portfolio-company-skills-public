# Evidence and the optional market feed

## What supports a decision

Keep three kinds of evidence distinct:

| Kind | Use | Limitation |
|---|---|---|
| Documented fact | Model limits, accepted parameters, pricing, data controls | Scoped to provider, product, endpoint, date; not proof of account access |
| Measured task result | Quality, completion, latency, total cost on representative work | Record model, surface, effort, task, checks, sample size, and date; do not generalize beyond coverage |
| Anecdote or preference | Suggest a trial or preserve the user's workflow | Not a hard capability gate or permanent vendor judgment |

Official provider documentation governs that provider's API; the installed
surface's schema/help governs available controls; account state governs actual
access. If these disagree, resolve the relevant scope rather than choosing the
newest timestamp mechanically. State unresolved uncertainty. A model's report
about its own quality or identity is not independent validation.

Record a source link, verification date, and provider/product scope beside
retained facts. Check decisive facts during routing if missing, disputed, tied
to a recent launch/promotion, or older than six weeks. Check account access and
supported controls at execution time. Six weeks is a refresh ceiling, not a
promise that younger facts are correct. Do not refresh the entire market to
answer a narrow question. If retrieval is unavailable, use still-supported facts
and qualify the recommendation; do not invent exact prices or limits.

Treat security-related availability and privacy requirements as actual workflow
constraints. Do not infer a blanket security-review ban from restrictions on a
different activity, or move a task to evade safeguards.

## Optional market feed

You may keep a market feed: for example, a scheduled job that snapshots
OpenRouter's public model listings and writes any discrepancies it finds as
proposals. If one exists, read its dated snapshot and its proposals. It is
optional; do not create one, start a job, or change the feed as part of routing.
Without one, use primary documentation.

OpenRouter facts describe its offered routes and prices. They do not override
direct-provider prices, endpoint features, privacy terms, or account access.
Check provider-specific terms when that route is under consideration.

Interpret proposal content, not file size: a nonempty file may say no threshold
rule fired. A real proposal identifies a claim to investigate; it does not
invalidate every gate or authorize an edit. Absence of proposals does not verify
the skill. The feed never changes routing policy automatically, but routing
policy remains revisable when task evidence or corrected facts warrant it.
