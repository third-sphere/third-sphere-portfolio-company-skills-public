# pitch-content-guide — design notes

## Why this exists

A fundraise deck has two halves that fail in different ways. The content half fails
by being unconvincing; the visual half fails by being ugly. Doing both in one pass
usually means doing neither well — you start making argument decisions to fit a
layout, which is backwards.

This skill produces the content half as a standalone spec: verbatim copy, precise
chart specs, named image assets, and a pressure test. A designer, or a separate
design-focused Claude session, then executes it without re-deciding what the deck
argues.

## Design decisions worth knowing

**Copy is verbatim, not descriptive.** If the guide says "explain the retention
story here," whoever lays out the slides ends up writing the argument. So the guide
writes the actual headline, body, and stat callouts.

**Review flags instead of plausible numbers.** Anything unconfirmed is marked
`[REVIEW: ...]` and rendered in red in the built deck, and the flags are counted in
the handoff notes. This is what makes it safe to draft before the round is settled —
which is when a deck brief is most useful.

**Charts get specs, not descriptions.** A chart spec is a table precise enough to
build with no further judgment, plus one sentence naming the takeaway it must deliver
in five seconds. If that sentence can't be written, the chart is doing too much.

**A missing chart beats a fabricated one.** Where the underlying numbers don't exist
yet, the guide says to cut the slide rather than build it on placeholder data.

**The pressure test is ordered.** The weak points are listed in the order a partner
will actually find them, each with a specific fix, plus one structural observation
about the deck's shape rather than a single slide.

## Stage coverage

`references/stages.md` covers pre-seed through Series B+, growth equity / minority
recap, and secondary / founder liquidity — each as a different argument, not the same
argument with bigger numbers. Growth equity is the one most often got wrong, because
the standard venture arc doesn't fit a profitable, capital-efficient company.

`references/slide-patterns.md` covers the slides that recur at every stage —
traction, competition, team, business model, the ask — each with its failure mode,
because knowing how a slide usually goes wrong is more useful than knowing how it
should look.

## Works well with

- `portco-brand-extract` — run first when there's no style guide or asset library;
  you can't name image assets you haven't inventoried.
- `seed-pitch-kit` — the full fundraise system when the raise needs more than a deck.
- `tufte-viz` — for interrogating a chart spec before committing to it.
- `pptx` — for actually building the file.

## Changelog

- **Initial release** — stage reference (pre-seed → growth + secondary), slide
  patterns, review-flag convention, chart-spec format, pressure test, and design-
  session handoff.
