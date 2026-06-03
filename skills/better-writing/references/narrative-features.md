# Narrative feature reference

The 30 core narrative features from StoryScope (Russell et al., 2026, Table 15) that most reliably separate human-written from AI-generated fiction. Use this as a diagnostic map for spotting default choices — **not** as a list of moves to install in every draft (see the rarity principle in SKILL.md).

**Reading the numbers.** Each entry shows the human-vs-AI gap. Percentages are how often each group makes that choice; decimals are mean scores on a 1–5 scale (or ordinal codes). A larger gap means the feature is a stronger discriminator — i.e. a more reliable place defaults hide. Direction matters: "AI-elevated" features are ones AI does *more* (watch for over-use); "human-elevated" features are ones humans do *more* (under-used by default, but only worth adding when the piece actually calls for it).

---

## AI-elevated — over-used by default; watch for these

### Thematic over-determination (spelling out meaning)
| Feature | Human | AI |
|---|---|---|
| Thematic explicitness / moralizing (1–5) | 3.28 | 3.94 |
| Moral or philosophical weighting (1–5) | 3.26 | 3.68 |
| Thematic unity — everything serves one concern (1–5) | 4.41 | 4.74 |
| Narrator explicitly states the theme | 52% | 77% |
| Dialogue used for philosophical debate | 34% | 59% |
| References are vague "implicit echoes" | 50% | 72% |

The strongest cluster of tells. The reflex is to make sure the reader *gets it*. The fix is almost always subtraction — cut the line that announces the point.

### Sensory & embodied over-performance (one technique on repeat)
| Feature | Human | AI |
|---|---|---|
| Emotion conveyed through the body | 38% | 81% |
| Setting mirrors characters' inner states (1–5) | 3.58 | 4.07 |
| Environmental / ecological emphasis (1–5) | 2.83 | 3.21 |
| Smell (olfactory) imagery present | 57% | 82% |
| Sensory density (1–5) | 3.66 | 3.93 |
| Depth of interior access (1–5) | 3.67 | 3.93 |

"Show don't tell" turned to maximum. The tell is the *uniformity* — never just naming a feeling, never letting a scene go un-lush. Vary it.

### Structural streamlining (everything too tidy)
| Feature | Human | AI |
|---|---|---|
| Continuous single causal chain (1–5) | 3.92 | 4.20 |
| Resolution driven by protagonist's own choice | 46% | 69% |
| Lead introduced by external description | 30% | 52% |
| No subplots | 57% | 79% |
| Resolved by internal understanding/acceptance | 27% | 47% |
| Opening over-grounds physical space (ord) | 2.12 | 2.33 |
| Spatial granularity (ord) | 2.27 | 2.53 |
| Heavy investment-building before danger (1–5) | 2.76 | 2.99 |

Single-track, frictionless, neatly resolved. Ask whether a loose end, a second storyline, or an unresolved ending would serve the piece better.

---

## Human-elevated — under-used by default; add only when the piece calls for it

### Intertextual richness
| Feature | Human | AI |
|---|---|---|
| Names a specific real reference (text/author/work) | 47% | 24% |
| Balances explicit and implicit references | 37% | 16% |

### Reader engagement
| Feature | Human | AI |
|---|---|---|
| Breaks the fourth wall (ord) | 0.67 | 0.39 |
| Directly addresses the reader (ord) | 0.28 | 0.07 |

### Temporal complexity (scrambling time)
| Feature | Human | AI |
|---|---|---|
| A reveal forces reinterpretation of earlier scenes (1–5) | 3.28 | 2.95 |
| Chronological discontinuity (1–5) | 2.40 | 2.12 |
| Nonlinear framing to stage revelations (1–5) | 1.96 | 1.68 |
| Flashback/flash-forward intensity (1–5) | 2.58 | 2.31 |

### Narrative diversity
| Feature | Human | AI |
|---|---|---|
| More distinct locations (ord) | 1.34 | 1.08 |
| More dialogue relative to narration (1–5) | 2.95 | 2.70 |
| A subplot that thematically rhymes with the main line | 42% | 21% |
| Morally ambivalent protagonist | 59% | 38% |
| Sometimes just names the emotion plainly | 29% | 8% |

Note the deliberate tension with the AI-elevated table: "emotion through the body" is AI-heavy, "naming the emotion plainly" is human-heavy. These are the same dial. The point is never *only* one setting.

---

## Per-model fingerprints (context, not for diagnosis)

StoryScope also found each model has a signature. Useful background, not something to check a draft against:

- **Claude** — flattest event escalation, most uniform voice, reverent toward literary tradition, favors epilogues and quiet endings, avoids dream sequences.
- **GPT** — gossip/rumor as plot engine, distant-retrospective framing, ensemble casts, ambiguous reconciliations.
- **Gemini** — tidiest endings, extended denouements, bleak settings, defaults to external character description.
- **DeepSeek** — front-loads crucial context early.
- **Kimi** — fewest distinctive choices; sits at the generic center.

---

*Source: Russell, Rajendhran, Pham, Iyyer & Wieting, "StoryScope: Investigating idiosyncrasies in AI fiction" (arXiv:2604.03136v4, 2026), Tables 13–16.*
