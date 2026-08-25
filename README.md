# Third Sphere Portfolio Company Skills

A curated collection of Claude Code skills built and shared by Third Sphere with our portfolio companies.

## Installation

### Option 1: Install as a plugin (recommended)

This repo is also a Claude Code plugin marketplace, so one command adds every
skill and `/plugin update` keeps them current.

```bash
claude plugin marketplace add third-sphere/third-sphere-portfolio-company-skills-public
```

Then install:

```bash
claude plugin install portco-skills@third-sphere
```

Skills are namespaced by the plugin, so you invoke them as
`/portco-skills:seed-pitch-kit`, `/portco-skills:pitch-content-guide`, and so on.
Claude also picks them up on its own when a task matches — that is what each
skill's `description` is for.

To pull later updates:

```bash
claude plugin update portco-skills@third-sphere
```

Install into a single project instead of your whole account with
`--scope project`, which records it in that project's `.claude/settings.json` so
your team gets it on checkout.

### Option 2: Copy the skill folders by hand

Use this when you want only some of the skills, or want to edit them locally.

```bash
git clone https://github.com/third-sphere/third-sphere-portfolio-company-skills-public.git
cp -r third-sphere-portfolio-company-skills-public/skills/* ~/.claude/skills/
```

Then restart Claude Code. Copied this way the skills are not namespaced, so they
invoke as `/seed-pitch-kit` rather than `/portco-skills:seed-pitch-kit`.

### Option 3: Import individual `.skill` files

Download a skill folder, zip it as `<skill-name>.skill`, and import it into
Claude Code via the skills panel. This is the path for Claude Desktop and Cowork.

## Available skills

| Skill | What it does |
|---|---|
| **better-writing** | Diagnose and strengthen narrative structure in drafts (stories, essays, posts) — finds where writing takes default, low-risk choices and proposes concrete structural revisions |
| **capstackcompass-public-portco-skill** | Look up climate credit and non-dilutive capital providers in the CapStack Compass database (capstackcompass.ai), and suggest new providers or corrections through Third Sphere's review queue |
| **founder-update** | Build portfolio company investor updates (weekly/monthly) with OKRs, metrics dashboards, and trend charts — pulls data from CRM, billing, and finance tools to create polished, data-driven founder letters |
| **pitch-content-guide** | Write a slide-by-slide content spec for a fundraise deck — verbatim copy, chart specs, named image assets, review flags, and a pressure test — then emit the ready-to-paste prompt for the design session that builds it |
| **portco-brand-extract** | Reverse-engineer a company's visual identity from its live website into a measured style guide, a categorised image-asset library, and a browsable brand board |
| **seed-pitch-kit** | Generate complete seed-stage fundraising materials — investment memo, TEA & market sizing, financial model, pitch decks, outreach emails, and investor list — all built comprehensive-to-concise from a shared narrative foundation |
| **tufte-viz** | Design and critique data visualizations using Edward Tufte's principles — data-ink ratio, chartjunk elimination, graphical integrity, small multiples, and sparklines for honest, high-density charts in decks, updates, and dashboards |

## Making it yours

The skills are deliberately plain markdown, so adapting them to your company is
editing prose, not writing code.

**Try before installing.** Point Claude Code at a local clone for one session:

```bash
claude --plugin-dir ./third-sphere-portfolio-company-skills-public
```

**Fork and re-point.** Fork this repo, edit the skills, and add your fork as the
marketplace instead. Your team installs from yours, and you can still pull our
changes with a normal `git merge upstream/main`:

```bash
claude plugin marketplace add your-org/your-fork
```

**Override one skill locally.** A skill you copy into `~/.claude/skills/` sits
alongside the plugin copy rather than replacing it — plugin skills are namespaced,
so `/my-version` and `/portco-skills:their-version` both exist. Edit freely without
losing the original.

**Validate before you distribute a fork:**

```bash
claude plugin validate .
```

## What is a skill?

A skill extends Claude Code with a focused capability you can invoke by typing `/<skill-name>` or a trigger phrase.

### Anatomy of a skill
- `SKILL.md` — the core workflow and instructions
- `README.md` — design notes, changelog, and usage examples
- `references/`, `scripts/`, `assets/` — supporting files (optional)

Every skill here lives in exactly one place, `skills/<name>/`, and is served both
ways from there — the plugin manifest in `.claude-plugin/` points at this repo
root, so adding a skill to `skills/` ships it through both install paths at once.

Learn more: [Claude Code documentation](https://claude.com/claude-code)

## Disclaimer

These skills are provided as-is. Third Sphere makes no warranty of fitness for any particular purpose. Each skill's behavior depends on Claude's underlying model and capabilities, which may change over time.

---

Built with [Claude](https://claude.ai).
