#!/usr/bin/env python3
"""
build_asset_index.py — generate ASSETS.md and a browsable HTML contact sheet.

    python3 build_asset_index.py --dir "/path/to/Example-Assets" \
        --company "Example" --source example.com \
        --palette "#F4EEE2,#F2A02B,#152028,#005577" \
        --serif "Source Serif 4" --sans "Open Sans"

The contact sheet is the artifact people actually use. A folder of 156 files with
CMS-hash filenames is unusable; a thumbnail grid grouped by category, styled in the
company's own palette, gets browsed. Passing --palette makes the sheet look like the
company it documents, which matters more than it sounds — it doubles as a check that
the extracted tokens are right.

Dimensions come from Pillow. If Pillow is unavailable the sheet still builds; the
dimension column just reads "?", which is a cosmetic loss, not a failure.
"""

import argparse, hashlib, html as html_mod, json, os, urllib.parse

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

# Fallback descriptions. Override per project by editing the generated ASSETS.md —
# the point of these is that an unedited index is still informative.
DEFAULTS = {
    '01-brand':          ('Brand marks', 'Logos, wordmarks, certification badges. Check for a vector file — it is the only asset that scales cleanly.', 'Title slide, footer lockup, close'),
    '02-customer-logos': ('Customer logos', 'Customer and partner marks. Confirm naming permissions before external use.', 'Traction / customer proof'),
    '03-icons':          ('Icons', 'Small UI and decorative marks.', 'Process diagrams, feature rows'),
    '04-illustration':   ('Illustration', 'The house illustration style. Usually the highest-value set for building diagrams that look native to the brand.', 'Process, architecture, how-it-works'),
    '05-product-ui':     ('Product UI', 'Screenshots of the product. Check capture dates — older shots may show a stale interface.', 'Product and platform slides'),
    '06-photography':    ('Photography', 'People, team, and facilities. Confirm releases for identifiable individuals.', 'Team, mission, impact'),
    '07-blog-social':    ('Blog & social', 'Resource headers and OG cards.', 'Reference / appendix'),
    '08-misc':           ('Uncategorised', 'Everything the classifier could not place. Worth a skim — real assets hide here.', 'Review individually'),
}


def scan(base):
    """Walk the asset tree, recording dimensions and flagging byte-identical twins."""
    hashes, data = {}, {}
    for cat in sorted(os.listdir(base)):
        p = os.path.join(base, cat)
        if not os.path.isdir(p):
            continue
        rows = []
        for f in sorted(os.listdir(p)):
            fp = os.path.join(p, f)
            if not os.path.isfile(fp):
                continue
            size = os.path.getsize(fp)
            try:
                h = hashlib.md5(open(fp, 'rb').read()).hexdigest()
            except Exception:
                h = None
            dup = h in hashes if h else False
            if h and not dup:
                hashes[h] = f'{cat}/{f}'
            if f.lower().endswith('.svg'):
                dim, w, ht = 'vector', 10**6, 10**6      # sort vectors first: most useful
            elif HAVE_PIL:
                try:
                    with Image.open(fp) as im:
                        dim, w, ht = f'{im.width}x{im.height}', im.width, im.height
                except Exception:
                    dim, w, ht = '?', 0, 0
            else:
                dim, w, ht = '?', 0, 0
            rows.append({'f': f, 'dim': dim, 'kb': round(size / 1024), 'w': w, 'h': ht,
                         'dup': dup, 'rel': urllib.parse.quote(f'{cat}/{f}')})
        if rows:
            data[cat] = rows
    return data


def write_md(data, base, company, source):
    total = sum(len(v) for v in data.values())
    mb = sum(r['kb'] for v in data.values() for r in v) / 1024
    L = [f'# {company} — Image Asset Library\n',
         f'\n**Source:** {source} · **{total} files · {mb:.0f} MB**\n',
         '\nResponsive variants stripped, so every file here is the largest resolution '
         'the site serves. Filenames keep their CMS hash prefix so each traces back to '
         'a source URL (see `_source_urls.json`).\n',
         '\n---\n\n## Rights caution\n',
         '\nThese are the company\'s own assets, pulled from their public site. Two things '
         'to check before anything ships externally:\n',
         '\n- **Customer logos** — public display on a website is not the same as clearance '
         'for an investor deck. Confirm which customers may be named.\n',
         '- **Photographs of identifiable people** — confirm releases exist, particularly '
         'for anyone who is not an employee.\n',
         '\n---\n']
    for cat in sorted(data):
        title, desc, use = DEFAULTS.get(cat, (cat, '', 'Review individually'))
        rows = sorted(data[cat], key=lambda r: -r['w'] * r['h'])
        cmb = sum(r['kb'] for r in rows) / 1024
        L += [f'\n## {title}\n', f'`{cat}/` · {len(rows)} files · {cmb:.1f} MB\n',
              f'\n{desc}\n', f'\n**Deck use:** {use}\n\n',
              '| File | Dimensions | Size |\n|---|---|---|\n']
        for r in rows:
            flag = ' _(dup)_' if r['dup'] else ''
            L.append(f"| `{r['f']}`{flag} | {r['dim']} | {r['kb']} KB |\n")
    L += ['\n---\n\n## Notes\n',
          '\n- Files marked _(dup)_ are byte-identical to another file — the same image '
          're-uploaded under a new CMS id. Safe to ignore.\n',
          '\n- Some CMS filenames contain non-obvious characters (narrow no-break spaces '
          'from macOS screenshots, double-encoded entities). If a literal filename match '
          'fails, glob the hash prefix instead.\n']
    open(os.path.join(base, 'ASSETS.md'), 'w').write(''.join(L))
    return total, mb


def write_sheet(data, base, company, source, palette, serif, sans):
    bg, accent, dark, deep = (palette + ['#FAFAF8', '#E07B39', '#1A1A1A', '#2C5F7C'])[:4]
    total = sum(len(v) for v in data.values())
    mb = sum(r['kb'] for v in data.values() for r in v) / 1024
    e = html_mod.escape
    fam = f'{serif or "Georgia"}, Georgia, serif'
    sfam = f'{sans or "Helvetica Neue"}, -apple-system, sans-serif'
    gf = ''
    if serif or sans:
        q = '&'.join(f'family={urllib.parse.quote_plus(f)}:wght@400;700;800'
                     for f in [serif, sans] if f)
        gf = (f'<link rel="preconnect" href="https://fonts.googleapis.com">'
              f'<link href="https://fonts.googleapis.com/css2?{q}&display=swap" rel="stylesheet">')

    H = [f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(company)} — Asset Contact Sheet</title>{gf}
<style>
:root{{--bg:{bg};--accent:{accent};--dark:{dark};--deep:{deep};
--serif:{fam};--sans:{sfam}}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--dark);font-family:var(--sans);font-size:15px;line-height:1.55}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 34px}}
header{{padding:64px 0 36px;border-bottom:1px solid rgba(0,0,0,.15)}}
.eyebrow{{font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(--accent)}}
h1{{font-family:var(--serif);font-size:52px;font-weight:800;line-height:.9;margin:14px 0 12px}}
.stats{{display:flex;gap:34px;margin-top:22px;flex-wrap:wrap}}
.stat .n{{font-family:var(--serif);font-size:32px;font-weight:800;line-height:1}}
.stat .l{{font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;opacity:.65;margin-top:2px}}
nav{{position:sticky;top:0;background:var(--bg);padding:13px 0;border-bottom:1px solid rgba(0,0,0,.15);z-index:9}}
nav .wrap{{display:flex;gap:8px;flex-wrap:wrap}}
nav a{{font-size:11px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;text-decoration:none;
color:var(--dark);border:1.5px solid rgba(0,0,0,.25);padding:6px 12px;border-radius:8px}}
nav a:hover{{background:var(--accent);border-color:var(--accent);color:#fff}}
section{{padding:44px 0 10px}}
h2{{font-family:var(--serif);font-size:29px;font-weight:800;line-height:1.05}}
.cmeta{{font-size:12px;font-family:ui-monospace,Menlo,monospace;opacity:.65;margin-top:5px}}
.cdesc{{font-size:14.5px;opacity:.8;max-width:720px;margin-top:9px}}
.use{{display:inline-block;margin-top:11px;background:var(--deep);color:#fff;font-size:11px;
font-weight:600;letter-spacing:.8px;text-transform:uppercase;padding:6px 13px;border-radius:8px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:16px;margin-top:24px}}
.card{{background:#fff;border:1px solid rgba(0,0,0,.13);border-radius:8px;overflow:hidden;display:flex;flex-direction:column}}
.thumb{{height:150px;display:flex;align-items:center;justify-content:center;background:var(--bg);
border-bottom:1px solid rgba(0,0,0,.1);padding:10px;position:relative}}
.thumb img{{max-width:100%;max-height:100%;object-fit:contain}}
.dup{{position:absolute;top:7px;right:7px;background:var(--accent);color:#fff;font-size:9px;
font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:2px 6px;border-radius:4px}}
.cap{{padding:9px 11px 11px}}
.fn{{font-size:10.5px;font-family:ui-monospace,Menlo,monospace;word-break:break-all;line-height:1.35}}
.dm{{font-size:10.5px;opacity:.65;margin-top:5px;font-weight:600}}
.warn{{background:#fff;border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:17px 21px;margin-top:28px}}
.warn h3{{font-family:var(--serif);font-size:18px;font-weight:700;margin-bottom:7px}}
.warn li{{font-size:14px;margin-left:18px;padding:3px 0}}
footer{{padding:40px 0 64px;margin-top:40px;border-top:1px solid rgba(0,0,0,.15);font-size:12.5px;opacity:.7}}
@media(max-width:700px){{h1{{font-size:36px}}.wrap{{padding:0 18px}}}}
</style></head><body><div class="wrap"><header>
<div class="eyebrow">Asset Contact Sheet · {e(source)}</div>
<h1>{e(company)}</h1>
<div class="stats">
<div class="stat"><div class="n">{total}</div><div class="l">Files</div></div>
<div class="stat"><div class="n">{mb:.0f}<span style="font-size:19px"> MB</span></div><div class="l">Total</div></div>
<div class="stat"><div class="n">{len(data)}</div><div class="l">Categories</div></div>
</div></header>
<div class="warn"><h3>Before anything ships externally</h3><ul>
<li><strong>Customer logos</strong> — public website display is not clearance for an investor deck.</li>
<li><strong>Photos of identifiable people</strong> — confirm releases, especially for non-employees.</li>
</ul></div></div>''']
    H.append('<nav><div class="wrap">')
    for cat in sorted(data):
        H.append(f'<a href="#{cat}">{e(DEFAULTS.get(cat, (cat,))[0])} ({len(data[cat])})</a>')
    H.append('</div></nav><div class="wrap">')
    for cat in sorted(data):
        title, desc, use = DEFAULTS.get(cat, (cat, '', 'Review individually'))
        rows = sorted(data[cat], key=lambda r: -r['w'] * r['h'])
        cmb = sum(r['kb'] for r in rows) / 1024
        H += [f'<section id="{cat}"><h2>{e(title)}</h2>',
              f'<div class="cmeta">{cat}/ · {len(rows)} files · {cmb:.1f} MB</div>',
              f'<p class="cdesc">{e(desc)}</p><div class="use">Deck use — {e(use)}</div><div class="grid">']
        for r in rows:
            dup = '<div class="dup">dup</div>' if r['dup'] else ''
            H.append(f'<div class="card"><div class="thumb">{dup}'
                     f'<img src="{r["rel"]}" alt="" loading="lazy"></div>'
                     f'<div class="cap"><div class="fn">{e(r["f"])}</div>'
                     f'<div class="dm">{r["dim"]} · {r["kb"]} KB</div></div></div>')
        H.append('</div></section>')
    H.append(f'<footer><strong>Source:</strong> {e(source)}. Responsive variants stripped — '
             'every file is the largest resolution the site serves.<br>'
             'Files badged <em>dup</em> are byte-identical to another file.</footer>'
             '</div></body></html>')
    out = os.path.join(base, f'{company.replace(" ", "-")}-Asset-Contact-Sheet.html')
    open(out, 'w').write(''.join(H))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', required=True)
    ap.add_argument('--company', required=True)
    ap.add_argument('--source', default='')
    ap.add_argument('--palette', default='', help='Comma-separated hex: bg,accent,dark,deep')
    ap.add_argument('--serif', default='')
    ap.add_argument('--sans', default='')
    a = ap.parse_args()

    if not os.path.isdir(a.dir):
        print(f'{a.dir} does not exist. Run harvest_assets.py first.')
        return 1
    data = scan(a.dir)
    if not data:
        print(f'No populated asset subfolders in {a.dir}. Run harvest_assets.py first.')
        return 1
    palette = [c.strip() for c in a.palette.split(',') if c.strip()]
    total, mb = write_md(data, a.dir, a.company, a.source)
    sheet = write_sheet(data, a.dir, a.company, a.source, palette, a.serif, a.sans)
    if not HAVE_PIL:
        print('Note: Pillow not installed — dimensions omitted. '
              'pip install pillow --break-system-packages')
    print(f'ASSETS.md      {total} files, {mb:.0f} MB')
    print(f'Contact sheet  {sheet}')
    print('\nVerify before handing off: every <img src> in the sheet should resolve.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
