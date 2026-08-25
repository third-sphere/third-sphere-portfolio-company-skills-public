---
name: startup-deck-generator
description: >
  Tailor a startup's pitch deck for ONE NAMED target investor: research that fund or
  partner, diff the deck against what they need, build the tailored version, write the
  approach strategy. A named target is required — a fund, partner, syndicate, or
  corporate/strategic investor. Triggers on "build a deck for [fund]", "tailor our deck
  for [fund]", "how should we pitch [partner]", "what would we change for [fund]", "prep
  me for the [fund] meeting", or a founder pasting a fund's thesis or portfolio page and
  wanting the deck adapted to it — even without the word "deck". NOT for a deck with no
  specific investor in mind: a generic deck or "our seed deck" is `pitch-content-guide`.
  NOT for the full fundraise package (memo, market sizing, model, investor list) — that
  is `seed-pitch-kit`. NOT for a company's colors, fonts, logos, or images — that is
  `portco-brand-extract`. If no target investor is named, ask for one or hand off to
  `pitch-content-guide` rather than building a generic deck.
---

# Startup Deck Generator

A deck aimed at everyone is aimed at no one. Most founders have one deck and send it
to forty funds, which is efficient and also why the response rate is what it is: a
seed fund, a multistage firm, a sector specialist, and a corporate investor are
underwriting four different questions, and the slide that answers one of them is
rarely the slide that leads.

This skill takes a company's existing argument and re-aims it at one named target. It
does not invent a new argument — if the deck itself is wrong, that's a
`pitch-content-guide` problem and worth fixing there first. Here the base deck is
treated as sound and the work is a **diff**: three to six changes and usually one
added slide, each traceable to something specific about the target.

Three artifacts come out: the tailored deck, the diff that produced it, and the
strategy for the approach.

---

## Step 0 — Confirm scope

Four things, asked in a single message — with a question tool if one is available in
this surface, otherwise as a short numbered list. Ask them together rather than one at
a time: each changes the work materially, and discovering an answer late means redoing
the run.

1. **Which investor?** A fund name, a partner name, or both. This is required — the
   whole method is a diff against a specific audience, and without one there is
   nothing to diff against. If the founder doesn't have a target yet, say so plainly
   and hand off to `pitch-content-guide`.

2. **Which archetype — and it may be two?** Seed VC, multistage/platform VC, sector
   specialist, or corporate & strategic VC. **Ask rather than assume**, because a
   $200M fund with "seed" in its materials and a sector thesis on its homepage could
   plausibly be any of three, and guessing wrong misdirects every subsequent decision.
   `references/investor-archetypes.md` has the questions that settle it.

   Two archetypes at once is common and correct — a climate-focused seed fund is a
   sector specialist *and* a seed VC. Let the founder name both. Deciding **which one
   governs** is then your job, not theirs: apply the "which constraint fails first"
   rule in the archetype reference and say out loud which one you led with and why.
   The founder can tell you what the fund is; they can't be expected to know which
   constraint binds harder.

3. **Which base deck?** Theirs, or the bundled shell. See §3 for reading an existing
   deck out of PDF or pptx.

4. **What do they already know?** A first-call note, an intro email, a partner's
   reply, a friend at the firm. This outranks any public research and founders
   routinely fail to mention it because it doesn't feel like "research."

---

## Step 1 — Research the target

Work through `references/research-checklist.md` in order and stop when the diff is
well-founded. The goal is four or five signals that justify specific slide changes,
not a dossier — research past that point makes the run slower without making the deck
better.

Public sources only. This has to work for a founder with nothing but a browser, so
never build a step that requires a CRM or a paid database; if one happens to be
connected, treat it as a bonus.

Where something material can't be sourced publicly — their current pacing, whether
they've seen a competitor — name it as a question for the call rather than guessing.
The checklist lists the usual unknowables.

---

## Step 2 — Gap analysis, then stop

Read `references/tailoring-moves.md` and work the base deck slide by slide: keep,
modify, remove, or add. Check the active-risk list first; a single active risk can
undo an otherwise strong deck, and those are assessable from the archetype alone.

**Slide order is not decided here, and this skill deliberately does not publish one.**
Two skills publishing competing slide orders is how a bundle starts contradicting
itself. Take the base order from the first of these that's available:

1. **The founder's existing deck.** For a diff, their order *is* the baseline — that's
   the whole premise, and it needs no external reference.
2. **The `pitch-content-guide` skill's stage reference** — `references/stages.md`
   inside that skill — when it is installed alongside this one. It is canonical for
   the base order at each stage. To check: look for `pitch-content-guide` in the
   available skills, or for a sibling `pitch-content-guide/` directory next to this
   skill. If a quick look doesn't find it, move on; it is not worth a filesystem hunt.
3. **Neither?** Then there is no deck and no baseline, which means this is a
   content-design problem rather than a tailoring one. Hand off to
   `pitch-content-guide` rather than inventing an order here.

Say which of the three you used. A silent fallback is how a made-up slide order gets
mistaken for a considered one. Note that (2) missing is never a reason to abort — with
a founder's deck in hand, (1) already settles it.

**Present the diff to the founder and wait.** This is the cheapest place to catch a
wrong read of the target, and founders frequently know something no amount of public
research surfaces — a prior conversation, a pass two years ago, a partner who left.
Building before this checkpoint means building twice.

Show it as a table (slide · move · change · signal that justified it), then the active
risks found, then any observation about the deck's overall shape. The structural
observation is often the most valuable line in the document: the most common and most
useful version is that the company's genuinely strongest fact is scattered across
three slides instead of being the spine.

---

## Step 3 — Build the tailored deck

### Reading the founder's existing deck

Most founders have a deck and it is rarely HTML. Degrade in this order:

| Source | Approach |
|---|---|
| HTML | Read it directly. |
| PDF or pptx | Use the `pdf` / `pptx` skills to extract text and structure. |
| Neither, or locked | Ask for pasted copy plus screenshots. Lossy on layout, works everywhere. |

### Building on the shell

`assets/deck-shell.html` is a shell, not a deck: a cover plus five layout patterns
(stat-led, two-column, full-bleed image, chart frame, table) and the navigation
wiring. Duplicate patterns to build the slides the diff calls for.

If no brand extract exists, ship the shell's neutral defaults untouched and say so —
"unbranded pending a brand extract" is an honest state and a one-line task for the
founder. Inventing a palette because the company "feels green" is the tempting wrong
move: it produces a deck that is confidently off-brand, which is worse than one that
is visibly unstyled.

Brand it by filling the CSS custom properties in `:root` from a style guide produced
by `portco-brand-extract`, and change nothing else. The contract is **role-named**
(`--ground`, `--ink`, `--accent`) rather than brand-named, so a style guide publishing
the site's own token names maps onto the roles. Read
[`references/branding-the-shell.md`](references/branding-the-shell.md) for the mapping
and the two values that carry most of the resemblance — headline leading, and the
proportion of grounds across slides.

Keep build notes out of the deck itself. The shell becomes the founder's file, and an
HTML comment is readable from view-source by whoever it is sent to.

Do not re-derive or improve measured tokens. They came off the live DOM; adjusting
them by eye is the most common way that measurement gets wasted.

### While building

Mark anything unconfirmed with `[REVIEW: ...]`, rendered red, and count them. Never
invent a metric, a customer name, a date, or a credential to fill a gap — a visible
gap is a task list, an invented number is a liability. `references/honest-tailoring.md`
has the full convention and the line it protects.

Give every ambiguous metric its definition on the slide — ARR, customers, pipeline,
users. The shell has a `.defn` class for this. It reads like fine print and isn't: an
undefined number gets discounted by a careful reader, and a definition that travels
with the number is what stops it drifting between audiences.

Put `Prepared for <Investor> · Confidential` on the cover. Once four tailored versions
exist, the wrong one gets forwarded to the wrong fund, and this is what stops it.

---

## Step 4 — Write the strategy doc

The deck is what you send; this is how you send it. Structure:

- **The one sentence** — how this company should be described to this specific
  audience. If the sentence isn't different from the generic one, the tailoring was
  probably too shallow.
- **Why this fund, in their terms** — the thesis fit as they would state it, not as
  the founder would.
- **Warm path** — who could make the introduction, in preference order, and what
  they'd need. Ask the founder; their network is invisible from public sources.
- **Objection prep** — the four or five hardest questions, *in the order this
  archetype will find them*, each with a specific answer. Ordering matters more than
  completeness: the first objection determines whether the rest of the meeting
  happens.
- **Open questions** — what must be confirmed before the deck can go out, including
  every `[REVIEW: ...]` flag and every publicly-unknowable item from Step 1.

Be honest in the objection section even where it's uncomfortable. "The retention
claim is asserted and never evidenced" is worth more than praise, because the person
reading it is about to present to someone whose job is finding exactly that.

---

## Step 5 — Present

Show both files. Summarise what changed and why, the unresolved flag count, and the
recommended first move. Keep it short — the founder can read the documents.

---

## Reference files

| File | Read when |
|---|---|
| `references/investor-archetypes.md` | Step 0 and throughout. Read **only** the target's section. |
| `references/research-checklist.md` | Step 1. |
| `references/tailoring-moves.md` | Step 2. |
| `references/honest-tailoring.md` | Before Step 3, and any time a founder asks to change a number. |
| `references/branding-the-shell.md` | Step 3, before filling the shell's tokens. |
| `assets/deck-shell.html` | Step 3, when there's no existing deck. |

---

## The line this skill holds

Tailoring changes ordering, framing, which proof points lead, and which slides exist.
It never changes the metrics, the definitions behind them, the round terms, or the
competitive claims.

The failure mode is not a fabricated number — it's a definition that drifts. A
founder tempted to let ARR include LOIs for a growth-focused fund and contracted
revenue only for a discipline-focused one has told two parties different things using
the same word, and it surfaces during diligence on a term sheet rather than during a
first meeting. When asked for a number change, decline it, say why in one line, and
offer the emphasis change that was actually wanted. Full reasoning in
`references/honest-tailoring.md`.

---

## Known limitations

Worth stating so nobody assumes coverage that isn't there.

This version does not check whether the target already holds a **direct competitor**,
whether the round's structure can deliver the **ownership** the fund needs, or whether
the fund has **drifted** to a later stage than it advertises. Any of the three can
sink a meeting that the deck otherwise deserved.

If research happens to surface one of them, put it in the strategy doc anyway. It
isn't a formal step, but a founder who hears from you that this fund led their closest
competitor's Series A is much better off than one who finds out in the room.

---

## Related skills

- `pitch-content-guide` — the deck's content for a general audience, stage by stage.
  Run it first when the base deck itself is weak; this skill assumes a sound argument.
- `portco-brand-extract` — measures a company's real palette, type scale, and assets
  off its live site. Run it before Step 3 when branding the shell.
- `seed-pitch-kit` — the full seven-deliverable fundraise system when the raise needs
  the memo, market sizing, model, and investor list rather than one tailored deck.
- `pdf` / `pptx` — for reading an existing deck, or producing one as a file.
