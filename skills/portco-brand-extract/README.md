# portco-brand-extract — design notes

## Why this exists

Most companies you build materials for have a website and no brand book. The website
*is* the brand book — it just needs reading properly. This skill turns a URL into a
measured style guide, a categorised image-asset library, and a brand board that
renders the tokens visually.

The reason to measure rather than eyeball: a screenshot gives you approximate colors
and no type scale, and "looks about right" is how a deck lands in the uncanny valley —
recognisably attempting the brand and visibly missing it.

## Design decisions worth knowing

**Computed CSS, not fetched HTML.** Tokens are read from the live DOM via the browser
tools. A plain HTTP fetch returns markup without executing JavaScript, so it cannot
report computed style — which is the whole point.

**The color census is area-weighted.** A color spanning two full-bleed sections
outranks one used on forty badges. Reproducing that *proportion* is most of what makes
a deliverable feel native, and it's the part eyeballing always gets wrong.

**Measured is marked separately from inferred.** Palette, type scale, and component
specs come off the wire and are facts. Deck scale, chart style, and layout guidance
are proposals, marked `[inferred]`. Six months later, someone needs to know which
values they can overrule.

**Gaps are findings, not omissions.** A missing reversed logo or an unbuilt icon
system gets written down. A gap found while writing the guide is cheap; the same gap
found mid-build is not.

**Server HTML for the asset crawl.** Lazy-loaded `<img>` tags are present in the
markup regardless of scroll position, so parsing server HTML beats reading the
rendered DOM. The script also handles responsive-variant stripping, double-encoded
filename twins, and byte-identical duplicates — it reports duplicates rather than
deleting them, because mounted folders are often read-only.

**Categorisation is ordered, and the obvious ordering is wrong.** A generic `logo`
rule swallows every customer logo on the site, since `acme-logo-black.png` contains
"logo" just as much as the company's own mark does. So the brand bucket matches on the
company's own slug, and everything else containing "logo" is taken to be somebody
else's. Pass `--slug` or this distinction collapses.

## Rights, not just availability

Everything harvested is public, which is not the same as cleared. Customer logos and
photographs of identifiable people — especially non-employees and minors — need
explicit permission before external use. The generated `ASSETS.md` and contact sheet
carry this warning at the top by default. Keep it there.

## Scripts

| Script | What it does | Notes |
|---|---|---|
| `scripts/extract_tokens.js` | Five DOM-measurement blocks: design-system variables, area-weighted color census, type scale, buttons and loaded font weights, internal link map | Run the blocks separately — a combined return exceeds the browser tool's output limit and truncates mid-JSON |
| `scripts/harvest_assets.py` | Crawls the pages you name and downloads the image library, categorised | Shells out to `curl` for each page and asset; only ever fetches URLs derived from the site you pass in |
| `scripts/build_asset_index.py` | Builds `ASSETS.md` and an HTML contact sheet, styled in the extracted palette | The styling is a live check on the tokens: if the sheet looks wrong, the palette is wrong |

Both Python scripts are standard-library only and take no credentials.

## Works well with

- `pitch-content-guide` — the usual next step; a content guide can name exact asset
  filenames once the library exists.
- `seed-pitch-kit`, `founder-update` — any deliverable that should look native to the
  company.

## Changelog

- **Initial release** — token extraction blocks, asset harvester with categorisation
  and dedup, asset indexer and contact sheet, style-guide template, brand board spec.
