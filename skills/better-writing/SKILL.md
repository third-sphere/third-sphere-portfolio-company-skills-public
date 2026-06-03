---
name: better-writing
description: Diagnose and strengthen a piece of writing at the level of narrative structure, not just prose. Use this skill whenever the user shares a draft — a short story, chapter, scene, essay, blog post, or any creative or narrative writing — and wants feedback, a critique, an edit, or to make it "less generic," "less AI-sounding," "more original," "more compelling," or "better." Also use it when the user wants to understand why their writing feels flat, formulaic, or predictable, or asks for a structural read rather than a line edit. Triggers on "can you critique this," "make this less AI," "how do I make this more original," "what's weak about this draft," "give me feedback on my story," "tighten this chapter," or any time a draft arrives with an implied or explicit ask to improve it. Even a bare "thoughts?" attached to a draft should use this skill.
---

# Better Writing

This skill diagnoses where a draft falls into *default, low-risk storytelling* and proposes concrete structural revisions. It is built on the StoryScope study (Russell et al., 2026), which found that the features most reliably separating human-written from AI-generated fiction are **structural, not stylistic** — and that editing out clichés and purple prose barely changed how generic a story read (a 1.6-point drop in detectability). The genericness lives in the *choices*, not the sentences. So this skill works at the level of choices.

## The core idea: rarity, not a "human score"

The single most important thing to understand before using this skill: the StoryScope models all *converged on the same region* of narrative space. They didn't fail by being individually weird — they failed by all making the same safe, central choices. Human writing scored as more original because it was **rarer**: it took less-common options at each fork (point of view, chronology, how emotion is rendered, whether the ending resolves).

This has a sharp consequence for how to give feedback. **Do not mechanically push a draft toward the "human-elevated" features in the reference table.** If you tell every writer to add a flashback, name a real author, and break the fourth wall, you just manufacture a *new* default cluster — you've moved the writing from one generic center to another. The goal is not to max a checklist. The goal is to help the writer make *intentional, distinctive* choices and to protect what's already idiosyncratic in their voice. The feature table is a map of where defaults live so you can spot them — not a list of moves to install.

## Workflow

### 1. Read the whole draft first, and figure out what it's trying to be

Read it through before saying anything. Identify the form (literary short story, genre fiction, personal essay, argumentative essay, blog post) and what the piece is reaching for — its intended effect, tone, and ambition. A taut, linear thriller and a sprawling literary mosaic have opposite ideals. Many of the "AI-default" features below are *virtues* in the right piece: a clean causal chain is good in a heist story; an explicit moral is the point of a fable. Calibrate every diagnosis to what *this* piece wants to do, not to an abstract average.

### 2. Diagnose against the feature map — but only flag what's load-bearing

Read `references/narrative-features.md` for the full set of 30 discriminating features with the human-vs-AI gaps. Use it to notice where the draft has reflexively taken the obvious option. But **resist flagging everything** — a critique that lists twenty issues is noise, and most of the gaps are small. Find the three-to-five places where a default choice is actually costing the piece something: where it's flattening tension, foreclosing ambiguity the story wanted, or making the reader feel they've seen this exact move before.

The highest-yield patterns to look for, roughly in order of how often they matter:

- **Over-explained meaning.** Does a narrator (or, in an essay, the writer) state the theme/lesson the prose has already earned? This is the strongest single tell. The fix is usually deletion: trust the reader.
- **One technique on repeat.** "Show, don't tell" taken to the limit reads as machine-made. If *every* emotion is rendered as a bodily sensation (tight chest, cold sweat) and the plain word for the feeling never appears, that uniformity is the problem — not embodiment itself. Vary the register.
- **Everything too tidy.** Single track, no subplots, a clean cause→effect line, the protagonist's own choice resolving everything into quiet acceptance. Ask whether a loose end, a competing storyline, or an unresolved moral question would serve the piece.
- **Genericized specifics.** Hedged, unnamed allusions ("an old poem," "a famous painting") where a real, named, specific thing would land harder.
- **Frictionless morality.** A protagonist who is simply good. Ambivalence is more interesting when the piece can bear it.

### 3. Separate structural notes from cosmetic ones — and lead with structure

This is the skill's whole reason for existing. Line-level polish (word choice, rhythm, cutting a cliché) is real editing but it does **not** fix a generic draft — the research is explicit on this. If you only have prose-level notes, say so honestly, but always look for the structural lever first: reorder the timeline, add or deepen a subplot, withhold a revelation, complicate a character's motive, change who tells the story. These are the edits that move the needle.

### 4. Propose specific, optional revisions — don't auto-rewrite

Give concrete moves, not vague encouragement. Not "add more tension" but "the funeral is your strongest scene and it's buried in paragraph nine — consider opening there and letting us discover the cause of death backward." Show, where useful, a short before/after of a single passage to make a move legible — but **do not silently rewrite the whole piece** unless the user explicitly asks for a rewrite. Writers want to keep authorship of their own work; your job is to widen their options, not to replace their voice with yours. When you do illustrate, preserve their diction and intent.

### 5. Be honest about the limits

Say plainly, when relevant: these are statistical tendencies, not rules; "more human" is not the same as "better"; and plenty of excellent writing is linear, tidy, and explicit. If the draft is already strong, say that and stop — manufacturing problems to look useful is its own failure.

## Tone

Be direct and specific, the way a good workshop peer is — generous about what works, clear about what doesn't, never flattering and never harsh for its own sake. Name the strongest thing in the draft before the weaknesses; it tells the writer you actually read it and orients the revision around their strengths.

## For non-narrative writing

The framework is strongest for fiction and narrative. A subset transfers to essays, blog posts, and nonfiction: don't pre-state your conclusion before the argument earns it; name specific real examples instead of hedged generalities; vary how you make points instead of running one rhetorical move on a loop; let genuine tension or counterargument stand instead of resolving everything tidily. The temporal-structure and subplot features mostly don't apply — don't force them.
