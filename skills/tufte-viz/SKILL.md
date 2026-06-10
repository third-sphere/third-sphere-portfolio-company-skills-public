---
name: tufte-viz
description: |
  Ideate and critique data visualizations using Edward Tufte's principles. Use when: (1) designing charts for investor decks, investor updates, board materials, dashboards, or any pptx/xlsx/HTML output with a chart; (2) critiquing or improving an existing visualization; (3) reviewing dashboards or reports for graphical integrity; (4) choosing between chart types; (5) reducing chartjunk or improving data-ink ratio; (6) planning small multiples, sparklines, or dense displays. Triggers on "make this chart better", "is this chart honest", "too busy", "chartjunk", "what chart type", "Tufte", or whenever a deliverable includes a metrics chart, time series, or comparison graphic. Applies: data-ink ratio, chartjunk elimination, graphical integrity, lie factor, small multiples, data density.

---

# Tufte Visualization Ideation

Apply Edward Tufte's principles to design clear, honest, high-density data visualizations.

## Workflow

### For new visualizations:

1. **Clarify the data story**
   - What comparisons matter?
   - What's the key insight to communicate?
   - Who's the audience?

2. **Select approach** using Tufte principles:
   - High comparison need → Small multiples
   - Dense data → Consider data tables, sparklines
   - Time-series → Line charts with minimal grid
   - Part-to-whole → Avoid pie charts; prefer bar/table

3. **Design with data-ink in mind**
   - Start minimal, add only what's necessary
   - Every element must earn its ink
   - Default to grayscale; use color purposefully

4. **Apply the Tufte test** (see references/tufte-principles.md)

### For critiquing visualizations:

1. **Check graphical integrity**
   - Calculate lie factor if proportions seem off
   - Verify baselines and scales
   - Look for 3D distortion

2. **Identify chartjunk**
   - Decorative elements
   - Heavy grids
   - Unnecessary 3D effects
   - Moiré patterns

3. **Evaluate data-ink ratio**
   - What can be erased?
   - What's redundant?

4. **Suggest improvements** with specific before/after recommendations

## Pairing with a brand system

Tufte principles set the *design*; your brand palette sets the *ink*. If your company
has a brand or style skill, load it alongside this one and map its colors onto Tufte's
guidance: one purposeful brand color for single-series data, muted near-background hexes
for grids, hierarchy by weight rather than hue, and direct labels over legends.

## Key Principles Reference

- `references/tufte-principles.md` — core principles from *Visual Display of Quantitative Information*: lie factor, data-ink, chartjunk, small multiples, integrity.
- `references/analytical-design.md` — extensions from *Envisioning Information*, *Visual Explanations*, and *Beautiful Evidence*: the 6 principles of analytical design, sparklines, layering & separation, micro/macro, range-frames, causality, confections. Load when designing dashboards, dense displays, sparklines, or explanatory graphics.

**Quick checklist:**
- [ ] Lie Factor ≈ 1.0 (no visual distortion)
- [ ] Maximum data-ink ratio
- [ ] Zero chartjunk
- [ ] Clear labeling
- [ ] Answers "compared to what?"
- [ ] Shows causality or mechanism where relevant
- [ ] Multivariate (not over-reduced)
- [ ] Words, numbers, images integrated — not segregated
- [ ] Reveals multiple levels of detail (micro + macro)
- [ ] Layering: primary data dominates, secondary recedes
- [ ] Appropriate data density
