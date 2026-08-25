# startup-deck-generator — design notes

## Why this exists

Most founders have one deck and send it to forty funds. That is efficient, and it is
also why the response rate is what it is: a seed fund, a multistage firm, a sector
specialist, and a corporate investor are underwriting four different questions, and
the slide that answers one of them is rarely the slide that leads.

This skill re-aims an existing argument at one named target. It does not invent the
argument — a weak deck is a `pitch-content-guide` problem and should be fixed there
first. Here the base deck is assumed sound and the work is a **diff**: three to six
changes, usually one added slide, each traceable to something specific about the
target.

## Design decisions worth knowing

**A named target is required.** No fund name, no run. The whole method is a diff
against a specific audience, so "make our deck better" has nothing to diff against
and gets handed to `pitch-content-guide` instead. This refusal is the feature.

**The diff is presented before anything is built.** Founders routinely know something
public research cannot surface — a pass two years ago, a partner who left, a prior
conversation. Building before that checkpoint means building twice.

**Archetype is asked, not inferred.** A $200M fund with "seed" in its materials and a
sector thesis on its homepage could plausibly be three different archetypes, and
guessing misdirects every later decision. Two archetypes at once is common and
correct; deciding which one *governs* is the skill's job, not the founder's, and it
has to say which one it led with.

**It publishes no slide order.** Two skills in one bundle publishing competing slide
orders is how a bundle starts contradicting itself. Order comes from the founder's own
deck, or from `pitch-content-guide`'s stage reference when that skill is installed
alongside — and the run states which of the two it used, because a silent fallback is
how a made-up order gets mistaken for a considered one.

**Unbranded beats confidently off-brand.** With no brand extract available, the shell
ships with its neutral defaults and says so. Inventing a palette because the company
"feels green" produces a deck that is wrong in a way nobody flags.

## The honesty guardrail

`references/honest-tailoring.md` is the load-bearing reference, and the failure mode it
guards against is not a fabricated number — it is a **drifting definition**.

A founder pitching a growth-focused fund lets ARR include signed LOIs; pitching a
discipline-focused fund the same week, contracted revenue only. Neither number is
invented, both are defensible alone, and together they are misrepresentation — the
same label now means two things to two parties evaluating the same round. It surfaces
during diligence on a term sheet rather than in a first meeting.

So: tailoring changes ordering, framing, which proof points lead, and which slides
exist. It never changes metrics, the definitions behind them, round terms, or
competitive claims. Asked to change a number, the skill declines, says why in one
line, and offers the emphasis change that was actually wanted.

## The deck shell

`assets/deck-shell.html` is a self-contained HTML deck: a cover plus five layout
patterns — stat-led, two-column, full-bleed image, chart frame, table — with keyboard,
click, and swipe navigation. No build step, no dependencies, no network calls; it opens
in a browser and prints to PDF.

Branding is a contract: every visual value is a CSS custom property in `:root`, and
the property names are **role-named** (`--ground`, `--ink`, `--accent`) rather than
brand-named, so a style guide that publishes a site's own token names maps onto the
roles mechanically instead of by translation. Fill them from a
`portco-brand-extract` style guide and change nothing else.

Two values carry most of the resemblance, both documented in
`references/branding-the-shell.md`: headline leading (sub-1.0 leading is a deliberate signature on many sites and
the first thing lost when a deck is rebuilt from a screenshot), and the proportion of
grounds across slides (the right colors in the wrong ratio still reads as off-brand).

The authoring guidance lives in `references/branding-the-shell.md` rather than in a
comment at the top of the shell, because the shell becomes the founder's deck — build
notes left in an HTML comment travel into the delivered file and are readable from
view-source by whoever it is sent to.

HTML rather than `.pptx` for one specific reason: font substitution fails silently. A
missing face in a pptx does not error, the deck just quietly stops looking like the
company. In HTML the font stack is visible, declared, and reviewable.

## Known limitations

Stated so nobody assumes coverage that isn't there. This version does not check
whether the target already holds a **direct competitor**, whether the round structure
can deliver the **ownership** the fund needs, or whether the fund has **drifted** to a
later stage than it advertises. Any of the three can sink a meeting the deck otherwise
deserved. Where research happens to surface one, it goes in the strategy doc anyway.

## Works well with

- `pitch-content-guide` — run first when the base argument is weak; also canonical for
  base slide order at each stage.
- `portco-brand-extract` — run before the build step to brand the shell from measured
  values rather than guesses.
- `seed-pitch-kit` — when the raise needs the memo, market sizing, model, and investor
  list rather than one tailored deck.
- `pdf` / `pptx` — for reading a founder's existing deck, or emitting a file version.

## Changelog

- **Initial release** — four investor archetypes, research checklist, four tailoring
  moves with an active-risk list, honesty guardrail, and a token-driven HTML deck shell.
