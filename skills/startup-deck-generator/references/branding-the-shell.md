# Branding the deck shell

Everything in `assets/deck-shell.html` that is visual is a CSS custom property in
`:root`. Fill those from a `<Company>-Style-Guide.md` produced by
`portco-brand-extract` and change nothing else.

This guidance lives here rather than in a comment at the top of the shell for a
reason: the shell becomes the founder's deck. Build notes left in an HTML comment
travel into the delivered file, where anyone the deck is sent to can read them from
view-source.

## The shell is a shell, not a deck

A cover plus five layout patterns — stat-led, two-column, full-bleed image, chart
frame, table — and the navigation wiring. The slides actually needed come from the
diff; duplicate a pattern and fill it.

## The token contract is role-named

The properties are named for the **role** a value plays (`--ground`, `--ink`,
`--accent`), not for the brand's own name for it. A style guide that publishes the
site's own token names — `--alabaster`, `--bondi-blue` — maps onto these roles; keep
the site's names as comments if useful, but keep the roles stable. That is what makes
hydration mechanical rather than a translation exercise.

Do not re-derive or "improve" measured values. They were measured off the live DOM;
adjusting them by eye is the most common way that work is wasted.

## Two values carry most of the resemblance

1. **`--h1-leading`.** Sub-1.0 headline leading is a deliberate signature on many
   sites and the detail most often lost when a deck is rebuilt from a screenshot. If
   the style guide reports it, reproduce it exactly.

2. **The proportion of grounds.** The style guide's area-weighted census gives the
   brand's real balance. Distribute `.ground` / `.ground-alt` / `.ground-ink` /
   `.ground-accent` across slides to roughly match those percentages. A deck with the
   right colors in the wrong proportion still reads as off-brand.

## Fonts

Google Fonts may be linked. For licensed faces, self-host or embed as base64 — and
give every stack a real fallback, because a silently substituted font is the failure
mode nobody notices until it is printed.

## Missing assets

Use `<div class="placeholder">[REVIEW: ...]</div>` for an image or chart that does not
exist yet. Never point an `<img>` at a file you haven't got: a broken image icon reads
as a bug, a labelled placeholder reads as the task it is.

## Review flags

Wrap unconfirmed claims in `<span class="review">[REVIEW: confirm X]</span>`. They
render red and loud on purpose; none should survive to an investor. Count them before
handing off.

## Metric definitions

Any metric that could be read two ways — ARR, customers, pipeline, users — carries a
`<p class="defn">` with its definition on the slide. This is not fine print. An
undefined number gets discounted by a careful reader, and a definition that travels
with the number is what stops it quietly drifting between one audience and the next.
