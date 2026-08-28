# Third Sphere Portfolio Company Skills

A curated collection of Claude Code skills built and shared by Third Sphere with our portfolio companies.

## Installation

The same marketplace works everywhere Claude supports plugins — Claude Code,
Cowork, and chat on claude.ai or the desktop app. Nothing to download first, and
no GitHub account needed: the repo is public.

**Marketplace:** `https://github.com/third-sphere/third-sphere-portfolio-company-skills-public`

### Claude Code

Two commands, from inside a session:

```
/plugin marketplace add third-sphere/third-sphere-portfolio-company-skills-public
```

```
/plugin install portco-skills@third-sphere
```

If the install summary says `Run /reload-plugins to activate`, run that. Claude
Code clones the marketplace, so `git` needs to be on your PATH — it almost
certainly already is.

Skills are namespaced by the plugin: `/portco-skills:pitch-content-guide`. Add
`--scope project` to the install to share it with everyone on a repo via
`.claude/settings.json`.

### Cowork

**Customize** in the sidebar → **Plugins** → **Add marketplace** → paste the repo
URL (or the `owner/repo` shorthand) → install **Third Sphere Portfolio Company
Skills**. Click **Update** on the marketplace later to pull new versions.

### claude.ai and the Claude desktop app (chat)

Requires a paid plan (Pro, Max, Team, or Enterprise).

**Customize** in the left sidebar → **Plugins** tab → under **Personal plugins**
click **+** → **Add marketplace** → **Add from a repository** → paste the repo
URL. Then **Browse plugins** and **Install**.

Installed skills show up via `/` or the **+** button in a conversation.

Note that hooks and subagents only run in Cowork and Claude Code. This plugin
ships neither, so nothing is lost in chat.

### Copying the folders by hand

Use this if you want only some of the skills, or want to edit them locally
without forking.

```bash
git clone https://github.com/third-sphere/third-sphere-portfolio-company-skills-public.git
cp -r third-sphere-portfolio-company-skills-public/skills/* ~/.claude/skills/
```

Then restart Claude Code. Copied this way the skills are not namespaced, so they
invoke as `/seed-pitch-kit` rather than `/portco-skills:seed-pitch-kit`.

For claude.ai without a paid plan, individual skills can be uploaded one at a
time under **Customize → Skills → + → Upload a skill**, as a `.zip` whose root is
the skill folder itself. Code execution must be enabled in Settings →
Capabilities. The plugin route above is easier where it is available.

### What needs what

Most of these skills are instructions and work anywhere. Two caveats:

| Skill | Needs |
|---|---|
| `portco-brand-extract` | Browser tools to read computed CSS, plus network access for the asset crawl. Use it in **Claude Code**; it degrades badly where Claude cannot reach the live site. |
| `capstackcompass-public-portco-skill` | Network access to reach the CapStack Compass database. |

## Available skills

| Skill | What it does |
|---|---|
| **better-writing** | Diagnose and strengthen narrative structure in drafts (stories, essays, posts) — finds where writing takes default, low-risk choices and proposes concrete structural revisions |
| **capstackcompass-public-portco-skill** | Look up climate credit and non-dilutive capital providers in the CapStack Compass database (capstackcompass.ai), and suggest new providers or corrections through Third Sphere's review queue |
| **founder-update** | Build portfolio company investor updates (weekly/monthly) with OKRs, metrics dashboards, and trend charts — pulls data from CRM, billing, and finance tools to create polished, data-driven founder letters |
| **model-router** | Pick the executor and effort level for a unit of work — which Claude tier, what effort, or whether it belongs on another vendor entirely; built on the premise that a too-weak model doesn't error, it quietly returns a worse answer that looks fine |
| **pitch-content-guide** | Write a slide-by-slide content spec for a fundraise deck — verbatim copy, chart specs, named image assets, review flags, and a pressure test — then emit the ready-to-paste prompt for the design session that builds it |
| **portco-brand-extract** | Reverse-engineer a company's visual identity from its live website into a measured style guide, a categorised image-asset library, and a browsable brand board |
| **seed-pitch-kit** | Generate complete seed-stage fundraising materials — investment memo, TEA & market sizing, financial model, pitch decks, outreach emails, and investor list — all built comprehensive-to-concise from a shared narrative foundation |
| **startup-deck-generator** | Tailor a pitch deck for one named target investor — research the fund, diff the deck against what they need, build the tailored HTML version from a brandable shell, and write the approach and objection strategy |
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

## License

[Mozilla Public License 2.0](LICENSE). In practical terms:

- **Use it however you like, including commercially.** No permission needed, no
  fee, no requirement to be a Third Sphere portfolio company.
- **Internal use carries no obligations at all.** Fork it, rewrite every skill,
  never tell anyone. The license only engages when you *distribute* your version.
- **If you distribute a modified skill, that file stays open.** Publish your
  changed files under the MPL so the next person gets what you got. This is
  file-level copyleft: you can combine these skills with proprietary work, and
  only the files you changed carry the obligation — not your product.
- **Keep the notices.** Copyright and license notices travel with the files.
- **The trademarks are not included.** "Third Sphere" and "CapStack Compass" are
  ours; MPL section 2.3 grants no rights in them. Name your fork something else.

Contributions are accepted under the same license.

## Disclaimer

These skills are provided as-is, without warranty of any kind, as stated in
section 6 of the [LICENSE](LICENSE). Third Sphere makes no warranty of fitness
for any particular purpose. Each skill's behavior depends on Claude's underlying
model and capabilities, which may change over time.

---

Built with [Claude](https://claude.ai).
