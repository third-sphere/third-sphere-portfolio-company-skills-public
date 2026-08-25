---
name: pitch-content-guide
description: Write a slide-by-slide content spec for a fundraise deck — verbatim copy, chart specs, named image assets, review flags, and a pressure test — then emit the ready-to-paste prompt and model recommendation for the design session that builds it. Use whenever a deck needs specifying before it is designed, at any stage from pre-seed through growth equity and secondary. Triggers on "write the deck content", "spec out the slides", "what should each slide say", "content guide for [company]'s raise", "draft the deck copy", "prep this for Claude Design", "turn this into a deck brief", or "hand this off to a designer". Also use it when someone asks for "a deck" with no designer lined up — specifying content first and building second beats doing both at once, and this is the content half. NOT for building the .pptx (that is pptx) and NOT for the full seven-deliverable fundraise kit (that is seed-pitch-kit, which this complements).
---

# Pitch Content Guide

A deck has two halves that fail differently. The content half fails by being
unconvincing; the visual half fails by being ugly. Trying to solve both in one pass
usually means solving neither — you end up making argument decisions to fit a layout.

This skill produces the content half as a standalone specification: every slide's
copy written verbatim, every chart specified precisely enough to build without
further judgment, every image named by filename. A designer or a design-focused
Claude session can then execute it without re-deciding what the deck argues.

The output is one markdown document plus a handoff prompt.

## Before drafting: three things you must settle

Ask these up front. Each one changes the structure materially, and discovering the
answer halfway through means rewriting.

**1. What stage and what kind of raise?** Pre-seed and growth equity share almost
no structure. A pre-seed deck argues that a problem is real and a team can attack
it; a growth deck argues that a working machine deserves fuel. Read
[`references/stages.md`](references/stages.md) for the slide order and emphasis at
each stage. Also establish whether it is primary capital, secondary/founder
liquidity, or both — that changes the ask slide and sometimes the whole arc.

**2. Email deck or live deck?** An email deck (10–15 slides) has no presenter and
must self-explain on a phone. A live deck (18–25 plus appendix) is a visual scaffold
for a conversation and can be sparser. Build the email deck first even when both are
wanted; the live deck extends it.

**3. What is actually known?** Round size, valuation, structure, target dates. If
they aren't settled, that is fine and normal — but the answer must be "flag it," not
"invent something plausible." See the review-flag convention below.

Ask these with a question tool if one is available, rather than in prose. They are
genuinely branching decisions and a wrong guess is expensive.

## Gather before you write

The guide is only as good as its inputs. Pull, in rough order of value:

- **The company context file or memo** — whatever durable record exists.
- **The brand extract** — style guide, asset manifest, contact sheet. If none
  exists, run `portco-brand-extract` first. You cannot name image assets you
  haven't inventoried, and a content guide with vague image direction ("a photo of
  the team") pushes the work downstream instead of removing it.
- **Prior investor updates** — the best single source for traction trajectory and
  the founder's own voice.
- **Financials** — revenue and margin history. Two data points are a line; five are
  a trend, and the difference matters enormously on the traction slide.
- **Existing deck**, however rough.

When something important is missing, flag it rather than filling the hole. A guide
full of visible gaps is more useful than a polished one with invented numbers,
because the gaps are a task list.

## The review-flag convention

Any number, date, customer name, or claim not confirmed from a source gets flagged
inline:

```
[REVIEW: confirm round size and structure]
```

Instruct the design session to render these **in red**. They must be impossible to
miss and must not survive to an investor. Count them at the end and state the count
in the handoff notes — an uncounted flag is a flag that gets skipped.

This convention is what makes it safe to draft ahead of complete information, which
in turn is what makes the skill useful early rather than only at the end.

## Structure of the output document

```markdown
# <Company> — Fundraise Deck Content Guide

**Deliverable:** <email|live> deck, <N> slides
**Framing:** <stage and raise type>
**Handoff target:** <who builds it>
**Date:**

## How to use this document
## Deck at a glance          <- table: slide, type, register
# Slide 1 — <name>
  ## Copy                     <- verbatim, in a blockquote
  ## Content type             <- chart | diagram | image | text
  ## Assets                   <- exact filenames, or a written brief
  ## Layout note
  [## Chart spec]             <- table, where applicable
...
## Image gaps — what must be created
## Pressure test — where an investor will push
## Handoff notes
## Changelog
```

### Copy is written to be used, not paraphrased

Write the actual words. Headlines, body, stat callouts, bottom banners. If the copy
in the guide is a description of what the slide should say, the person building it
has to write it — which means the argument gets decided by whoever happens to be
laying out slides. Say so explicitly in the document: *use this copy verbatim.*

### Every slide gets a content type

Chart, diagram, image, or text — decided in the guide. Slides without an assigned
content type default to bullet lists, which is how decks become walls of text.

### Charts are specified, not described

A chart spec should be buildable with no further decisions:

```markdown
| Property | Value |
|---|---|
| Type | Grouped vertical bar, two series, two periods |
| Series 1 | Revenue — `#F2A02B` |
| Data | 2024: $28M · 2025: $37M |
| Labels | Direct on bars, no legend |
| Axis | Single 2px baseline, no gridlines |
| Output | PNG, 2×, 1600px+, transparent background |
```

Then state **the one takeaway the chart must deliver in five seconds.** If you
can't write that sentence, the chart is doing too much and should be split or cut.

Charts that depend on numbers nobody has yet are a trap. Say plainly that the slide
should be **cut** rather than built on placeholder data — a 13-slide deck with no
market chart beats a 14-slide deck with a fabricated one, and investors can smell
the difference.

### Images are named by filename

Point at exact files in the asset library. Where an asset doesn't exist, write a
brief for what must be created and mark it in the gap list with a priority. Split
gaps into **blocking** (the deck cannot ship without it) and everything else.

## The pressure test

Close the document by role-playing the investor who will read it. Name the four or
five weakest points **in the order a partner will find them**, each with a specific
fix. This is the highest-value section for the founder and the most likely to be
acted on, because it is concrete and ordered.

Include one structural observation — something about the deck's shape rather than a
single slide. The most common and most useful version: the company's genuinely
strongest fact is scattered across three slides instead of being the spine.

Be honest here even when it's uncomfortable. A guide that says "the retention claim
is asserted and never evidenced" is worth more than one that praises the deck. The
person reading it is about to show this to people whose job is finding exactly that.

## Emit the handoff

Finish by producing the prompt for the session that will build the deck, plus a
model recommendation. Write the prompt as a standalone brief — the session that
receives it will have none of this conversation's context, so everything it needs
must be in the prompt itself.

The recommendation that usually applies, and why it is not obvious: deck production
is long unattended code execution — a slide library, precise positioning, embedded
fonts, many placed images — so it wants a strong model at high effort. The reason
isn't the code, it's that **brand infidelity fails silently.** A substituted font or
a slightly-wrong hex does not error; the deck just quietly stops looking like the
company. Visible failures are safe to run cheap. This one isn't.

The prompt itself must carry:

- Which files to read first, in order, and an instruction **not to re-derive the
  design tokens.** They were measured; "improving" them is the most common way this
  work is wasted.
- Verbatim-copy instruction.
- Font embedding, with an explicit prohibition on system-font fallback.
- The review flags, their count, and the red-rendering requirement.
- A scope fence. Strong models expand scope on their own initiative — they will
  add slides, propose alternate structures, and produce variants unless told the
  ordering is deliberate and load-bearing.
- The blocking gaps, with instructions to place marked placeholders rather than
  improvise around them. Auto-generating a missing reversed logo by recoloring an
  SVG is exactly the kind of helpful improvisation that produces an off-brand deck.
- A "done means" list of observable artifact properties — opens without repair,
  fonts embedded, every image placed, flags present and red.

## Reference files

- [`references/stages.md`](references/stages.md) — slide order, emphasis, and the
  argument being made at each stage from pre-seed to growth and secondary. Read the
  relevant section before drafting.
- [`references/slide-patterns.md`](references/slide-patterns.md) — reusable
  treatments for the slides that recur at every stage: traction, competition, team,
  the ask. Read when drafting those slides.

## Related skills

- `portco-brand-extract` — run first when no style guide or asset library exists.
- `seed-pitch-kit` — the full seven-deliverable fundraise system (memo, TEA, model,
  decks, emails, investor list). This skill is the deck-content portion done in
  depth; use the kit when the raise needs the whole set.
- `tufte-viz` — for interrogating a chart spec before committing to it.
- `pptx` — for actually building the file, if this session is also doing that.
