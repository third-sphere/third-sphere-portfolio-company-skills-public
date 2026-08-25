# Style guide template

Structure for `<Company>-Style-Guide.md`. Adapt freely — the section order matters
more than the exact headings, because it moves from hardest evidence to softest.

Throughout: mark anything you propose rather than measure as `[inferred]`. The
distinction is the whole value of the document. Measured values are facts a
downstream builder must honour; inferred values are your judgment, which they may
overrule. Blur the two and the guide becomes untrustworthy in both directions.

---

## Header

```markdown
# <Company> — Brand & Style Guide

**Extracted from:** <url> (<CMS/framework if known>) · **Date:** <date>
**Method:** live DOM render + computed CSS via Chrome. Values below are *measured*,
not eyeballed, unless marked `[inferred]`.
**Purpose:** <the deliverable this exists to serve>
```

Naming the method is not ceremony — it tells the reader how much to trust the
numbers, and it tells future-you how to reproduce them.

---

## 1. Color

Lead with the design system's own token names if the site publishes them.

```markdown
| Token | Hex | Role |
|---|---|---|
| `--alabaster` | `#F4EEE2` | Page background. Warm off-white, not gray. |
```

Then the **measured surface distribution** — the area-weighted census, converted to
percentages. This is the most useful single table in the guide and the one most
often missing from real brand books:

```markdown
1. White — 41%
2. Orange `#F2A02B` — 24%
3. Alabaster `#F4EEE2` — 21%
```

Follow it with a one-paragraph read of what the proportion means. "Orange is used
as large calm fields, not small accents" is the kind of sentence that stops a
downstream builder getting it backwards.

Close with **application guidance** for the target deliverable: which ground for
which slide type, chart series order, what to avoid. Mark it `[inferred]`.

---

## 2. Typography

Table of families and roles, then the measured scale:

```markdown
| Element | Family | Size | Weight | Line height | Tracking |
|---|---|---|---|---|---|
| H1 | Source Serif 4 | 64px | 800 | 54.4px (**0.85**) | normal |
```

Call out the **signature move** explicitly — the one typographic gesture that makes
the brand recognisable. Usually it's the headline treatment. Say what it is and
that reproducing it matters more than any other single choice.

Then a converted scale for the target medium (pt for slides, marked `[inferred]`),
and a note on font licensing and availability. Google Fonts embed freely; licensed
faces constrain everything downstream and the constraint needs stating here.

---

## 3. Components

Buttons, cards, panels — measured values in a table. Note inconsistencies you found
and which one you standardised on. Real sites are messier than brand books, and
recording the mess prevents someone "fixing" your standardisation later.

---

## 4. Imagery

Identify the distinct visual modes (illustration style, photography style, product
imagery) and say when each is used. Then give application guidance: which mode for
which kind of content.

Include an explicit **do not** list. It is easier to follow "no gradients, no 3D, no
stock photography" than to infer the absence of those things from examples.

---

## 5. Logo

Asset path, color usage, and — critically — **variants that do not exist**. A
missing reversed logo is a blocking gap for any deliverable using dark grounds, and
finding it here costs nothing while finding it mid-build costs a rebuild.

---

## 6. Voice & tone

Measured from the site's own copy, not invented. Pull real headlines and describe
the pattern: sentence length, register, whether they name products literally or
invent capitalised names, how they handle claims and numbers.

Give a headline formula if one is discernible, and application guidance for the
target deliverable.

---

## 7. Layout & spacing

Content column width as a proportion of viewport, section rhythm, how full-bleed
and contained sections alternate. Note the whitespace discipline — if the site
breathes, say so, because crowding is the most common way a rebuild loses the feel.

---

## 8. Open items

Everything unconfirmed, in a list. Reversed logo, internal brand book, icon system,
chart style, dark mode. Each one is a question for the company, and collecting them
in one place turns the guide into an agenda for a ten-minute conversation.

---

## Changelog

Date, what was extracted, what changed. Brands drift and this guide will need
re-running; a changelog tells you how stale it is.
