---
name: portco-brand-extract
description: Reverse-engineer a company's visual identity from its live website into a reusable style guide, a downloaded image-asset library, and a browsable brand board. Use this skill whenever any deliverable needs to look like a company whose brand book you do not have — a portfolio company's pitch deck, one-pager, LP memo, microsite, or event page. Triggers on "make this look like their website", "match [company]'s brand", "build a style guide for [company]", "extract their brand", "what are [company]'s colors and fonts", "pull their logo and images", "grab their assets", "brand board for [url]", or any request to design something on-brand for a company whose guidelines are not in hand. Also use it before building a deck or document for a portfolio company, even when the user hasn't asked for a style guide, because measuring the brand first is what makes the deliverable look native instead of approximated. NOT for a company whose brand guidelines you already have in hand, and NOT for inventing a new identity from scratch.
---

# Portfolio Company Brand Extract

Most companies you build materials for have a website and no brand book. The
website *is* the brand book — it just needs reading properly. This skill turns a
URL into three artifacts:

| Artifact | What it is | Who uses it |
|---|---|---|
| `<Company>-Style-Guide.md` | Measured tokens: palette, type scale, components, voice, layout | Whoever writes the next deliverable |
| `<Company>-Assets/` | Every image the site serves, categorised, with `ASSETS.md` and a contact sheet | Whoever builds it |
| `<Company>-Brand-Board.html` | The tokens rendered visually, in the brand's own styling | Everyone, as a sanity check |

The reason to measure rather than eyeball: a screenshot gives you approximate
colors and no type scale, and "looks about right" is how a deck ends up in the
uncanny valley — recognisably attempting the brand and visibly missing it. Computed
CSS gives you the actual values, and the actual *proportions*, which matter more.

## Workflow

### 1. Establish where the output goes, and confirm scope

Ask once, then remember: which folder, and is this for a specific deliverable
(deck, one-pager, site) or a general-purpose brand reference? The answer changes
how prescriptive the "application" sections of the style guide should be.

Default layout, which keeps the assets travelling with the guide that describes
them:

```
<Company>-Brand/
├── <Company>-Style-Guide.md
├── <Company>-Brand-Board.html
└── <Company>-Assets/
    ├── ASSETS.md
    ├── _source_urls.json
    ├── <Company>-Asset-Contact-Sheet.html
    └── 01-brand/ … 08-misc/
```

### 2. Measure the tokens

Use the Chrome tools — `navigate` to the homepage, then run each block of
[`scripts/extract_tokens.js`](scripts/extract_tokens.js) via `javascript_tool`.
Run the blocks **separately**; a combined return reliably exceeds the tool's output
limit and truncates mid-JSON, costing a retry.

`WebFetch` is not a substitute here. It returns raw HTML without executing
JavaScript, so it cannot tell you computed style — which is the entire point.

The five blocks give you, in order: design-system variables, a color census
weighted by rendered area, the real type scale, button treatments and loaded font
weights, and the internal link map. Read the header comments in the file; each
block explains what it is for and what to watch for in its output.

Then take screenshots — homepage hero plus two or three scrolled sections. You
need these for the imagery and layout sections, which cannot be derived from CSS.

**What to attend to in the results.** Three things carry most of the signal:

- **The area-weighted background census.** This is the brand's actual proportion.
  A color used across two full-bleed sections outranks one used on forty badges,
  and reproducing that ratio is most of what makes a deck feel native. Convert the
  raw pixel areas to percentages in the style guide — they're more useful than the
  absolute numbers.
- **Headline line-height.** Sub-1.0 leading on an H1 is a deliberate signature and
  it is the detail most often lost when someone rebuilds a deck from a screenshot.
  If you see it, say so explicitly and loudly in the guide.
- **Design-system variable names.** If the site publishes `--alabaster` and
  `--bondi-blue`, keep those names. They let you talk to the company's designer in
  their own vocabulary, and they signal the guide was measured rather than guessed.

### 3. Harvest the assets

```bash
python3 scripts/harvest_assets.py \
  --url https://example.com \
  --slug example \
  --pages / /about /team /product /impact \
  --out "<Company>-Assets"
```

Pass `--pages` from the link map in BLOCK 5, not just `/`. The homepage is rarely
where the good imagery is; team, about, and impact pages carry the photography that
makes a deck feel human. Pass `--slug` too — without it the company's own logo
cannot be distinguished from its customers' logos, and everything lands in one
undifferentiated pile.

Then build the index, passing the tokens you just measured so the contact sheet is
styled in the company's own palette:

```bash
python3 scripts/build_asset_index.py \
  --dir "<Company>-Assets" --company "Example" --source example.com \
  --palette "#BG,#ACCENT,#DARK,#DEEP" --serif "Display Font" --sans "Body Font"
```

That styling isn't decoration. A contact sheet rendered in the extracted palette is
a live check on whether the palette is right — if it looks wrong, the tokens are
wrong, and you find out in ten seconds rather than after building a deck.

The script handles the parts that quietly lose assets: responsive-variant stripping,
double-encoded filename twins, lazy-loaded images, and byte-identical duplicates. It
reports duplicates rather than deleting them, because mounted folders are often
read-only and a wrongly-deleted original doesn't come back.

**If the crawl returns no HTML,** the script says so and stops rather than producing
an empty library. The usual causes are a client-rendered site (server HTML carries
no `<img>` tags), bot protection, or a wrong base URL — try with and without `www`
first. For a genuinely client-rendered site, fall back to collecting asset URLs from
the *rendered* DOM with the Chrome tools, write them to a file, and download from
that list; the categorisation and indexing steps are unaffected.

### 4. Write the style guide

Follow [`references/style-guide-template.md`](references/style-guide-template.md)
for structure. Two disciplines matter more than the format:

**Separate measured from inferred.** Palette, type scale, and component specs come
off the wire and are facts. Deck scale, chart style, and layout guidance are your
proposals. Mark the second kind `[inferred]`. Someone reading the guide six months
from now needs to know which values they can rely on and which they can overrule.

**Name the gaps as gaps.** A reversed logo variant that doesn't exist, an icon
system that was never built, a missing dark-mode palette — these are findings, not
omissions. Write them down. A gap discovered while writing the guide is cheap; the
same gap discovered mid-build is not.

### 5. Build the brand board

A single self-contained HTML file, styled in the extracted tokens, showing:
swatches with names and hex values, the area-weighted proportion as a stacked bar,
type specimens at real sizes, button variants, four or five example applications on
the different grounds, and a do/don't list.

It is the artifact non-designers actually look at, and it doubles as proof the
tokens are right — a brand board that doesn't look like the company means something
was measured wrong.

### 6. Verify

Before handing off, check the things that fail silently:

- Every `<img src>` in the contact sheet resolves to a real file on disk.
- Every hex in the guide appears in the extracted token set — no drift, no invented
  midtones.
- Fonts resolve at the weights you specified. If they're Google Fonts, fetch the
  CSS and confirm each weight is really served; if they're licensed, say so in the
  guide, because that constrains every downstream deliverable.
- Anchors and markup in the generated HTML are intact.

## Things that will bite you

**Filenames carry invisible characters.** macOS screenshots contain a narrow
no-break space (U+202F) before AM/PM; CMSs emit double-encoded entities. A literal
string match fails and looks like a missing file. Glob the hash prefix instead, and
flag the specific file in any handoff document so the next person doesn't lose
twenty minutes to it.

**Site CSS is less consistent than a brand book.** Real sites ship two button radii
and three greys. Note the inconsistency, pick one, and say you picked it. Silently
standardising is fine; silently standardising *without saying so* means the next
person "corrects" it back.

**Rights are not the same as availability.** Everything harvested is public, which
is not the same as cleared. Customer logos and photographs of identifiable people —
especially non-employees and minors — need explicit permission before external use.
Put this at the top of the manifest, not in a footnote. `ASSETS.md` includes the
warning by default; keep it there.

**One page is not the library.** Crawling only `/` typically yields a third of the
assets and almost none of the photography.

## Handing off

When this feeds a deliverable, the receiving session needs: the style guide, the
brand board, the asset manifest, and an explicit instruction not to re-derive or
"improve" the tokens. Measured values that get creatively adjusted downstream are
the most common way this work is wasted.
