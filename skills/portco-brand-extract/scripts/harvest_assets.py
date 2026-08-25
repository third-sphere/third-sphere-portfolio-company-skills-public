#!/usr/bin/env python3
"""
harvest_assets.py — crawl a company site and download its image library.

    python3 harvest_assets.py --url https://example.com \
        --pages / /about /team /product \
        --out "/path/to/Example-Assets"

Why a script rather than doing this by hand each time: the fiddly parts are all
the same every run, and each one silently costs you assets if you skip it.

  * Responsive variants. CMSs emit `hero-p-500.png`, `hero-p-800.png` alongside
    `hero.png`. Downloading all of them wastes space and buries the original.
  * Lazy loading. Images below the fold never appear in a naive DOM read. Parsing
    server HTML rather than the rendered DOM sidesteps this entirely.
  * Double URL-encoding. `Asset%25201%25404x.png` and `Asset 1@4x.png` are the
    same file; keeping both looks like two assets.
  * Byte-identical duplicates. Teams re-upload the same photo under a new CMS id.
  * One page is not the library. The best photography usually lives on
    about/impact/careers pages.

Categorisation is keyword-based and deliberately loose. It is a first pass to make
a hundred-plus files navigable, not a taxonomy to defend. Re-file by hand after.
"""

import argparse, hashlib, json, os, re, subprocess, sys, urllib.parse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

IMG_RE = re.compile(
    r'https?://[^"\'\\)\s]+?\.(?:png|jpg|jpeg|svg|webp|gif|avif|mp4)',
    re.I)
VARIANT_RE = re.compile(r'-p-\d+\.(png|jpg|jpeg|webp)$', re.I)   # Webflow
SRCSET_RE = re.compile(r'[?&](w|width|h|height|q|quality|fm|auto)=', re.I)

# Ordered — first match wins, so specific patterns must precede general ones.
#
# The ordering here is load-bearing, and the obvious version of it is wrong: a
# generic `logo` rule in 01-brand swallows every customer logo on the site, because
# `instacart-logo-black.png` contains "logo" just as much as the company's own mark
# does. So 01-brand matches on the company's own slug plus a few unambiguous brand
# terms, and everything else containing "logo" is taken to be somebody else's.
CATEGORIES = [
    ('01-brand',            r'{slug}[-_ ]?(logo|mark|wordmark)|logomark|wordmark|b-?corp|favicon|brandmark'),
    ('02-customer-logos',   r'logo|customer|client|partner'),
    ('03-icons',            r'-icon\.|icon-|_icon|/icons?/|chevron|arrow|checkmark|pinpoint|quotes'),
    ('04-illustration',     r'illustration|asset[ _%]*\d|graphic|diagram|\bmap\b|how-?it-?works'),
    ('05-product-ui',       r'screenshot|screen[ _-]shot|-ss[-.]|dashboard|app[-_]|-ui-|product-'),
    ('06-photography',      r'photo|team|headshot|office|facility|factory|portrait|img[-_]?\d|dsc|_mg_'),
    ('07-blog-social',      r'-ftr\.|_blog|blog[-_/]|thumbnail|og-|social|1200x6|share-image'),
]


def fetch_pages(base, paths):
    """Concatenate server HTML for every page. Server HTML beats the rendered DOM
    here because lazy-loaded <img> tags are present in the markup regardless of
    scroll position.

    Reports the HTTP status on failure rather than just "failed", because the two
    common causes need opposite responses: a 404 means the path is wrong, while a
    403 or an empty 200 means the site is client-rendered or bot-protected and the
    whole approach has to change (see the fallback note in SKILL.md)."""
    html, failed = [], []
    for p in paths:
        url = base.rstrip('/') + p if p.startswith('/') else p
        r = subprocess.run(
            ['curl', '-sSL', '-A', UA, '--max-time', '45',
             '-w', '\n__HTTP_STATUS__%{http_code}', url],
            capture_output=True, text=True, errors='ignore')
        body, _, status = (r.stdout or '').rpartition('__HTTP_STATUS__')
        status = status.strip() or '000'
        if r.returncode == 0 and status.startswith('2') and body.strip():
            html.append(body)
        else:
            failed.append(f'{p} (HTTP {status})')
    return '\n'.join(html), failed


def collect(html, same_host_only=None):
    urls = set(IMG_RE.findall(html))
    keep = {}
    for u in urls:
        if VARIANT_RE.search(u):
            continue
        if same_host_only and same_host_only not in u:
            # Third-party CDNs are usually analytics pixels and tracking beacons.
            # Asset CDNs (cdn.prod.website-files.com, cloudfront, imgix) are not
            # on the site host, so this filter is opt-in rather than default.
            continue
        name = urllib.parse.unquote(urllib.parse.unquote(u.split('/')[-1].split('?')[0]))
        if '%25' in u.split('/')[-1]:        # double-encoded twin of a name we have
            continue
        if not name or name.startswith('.'):
            continue
        keep.setdefault(name, u)
    return keep


def categorise(name, slug=''):
    """Classify by filename. `slug` is the company's own name — it is the only thing
    that reliably separates the company's logo from its customers' logos, so pass it
    whenever you know it."""
    low = name.lower()
    for cat, pattern in CATEGORIES:
        # An empty slug would make the brand alternation match everything, so
        # substitute a token that cannot occur in a filename.
        p = pattern.replace('{slug}', re.escape(slug.lower()) if slug else 'zznomatchzz')
        if re.search(p, low):
            return cat
    return '08-misc'


def download(plan, out):
    ok, failed = 0, []
    for cat, items in plan.items():
        d = os.path.join(out, cat)
        os.makedirs(d, exist_ok=True)
        for name, url in items:
            path = os.path.join(d, name.replace('/', '-'))
            try:
                r = subprocess.run(['curl', '-sSL', '-A', UA, '--max-time', '60',
                                    '-o', path, url], capture_output=True, text=True)
                size = os.path.getsize(path) if os.path.exists(path) else 0
                if r.returncode == 0 and size > 200:
                    ok += 1
                else:
                    failed.append(name)
            except Exception as e:
                failed.append(f'{name} ({e})')
    return ok, failed


def find_duplicates(out):
    """Report, don't delete. A mounted folder may be read-only, and a duplicate is
    a five-second annoyance while a wrongly-deleted original is not recoverable."""
    seen, dupes = {}, []
    for root, _, files in os.walk(out):
        for f in sorted(files):
            fp = os.path.join(root, f)
            try:
                h = hashlib.md5(open(fp, 'rb').read()).hexdigest()
            except Exception:
                continue
            rel = os.path.relpath(fp, out)
            if h in seen:
                dupes.append((rel, seen[h]))
            else:
                seen[h] = rel
    return dupes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', required=True, help='Base site URL')
    ap.add_argument('--pages', nargs='+', default=['/'],
                    help='Paths to crawl. Get these from extract_tokens.js BLOCK 5.')
    ap.add_argument('--out', required=True, help='Output asset directory')
    ap.add_argument('--slug', default='',
                    help="Company name as it appears in filenames (e.g. 'revivn'). "
                         "Without it, the company's own logo cannot be told apart "
                         "from its customers' logos.")
    ap.add_argument('--host-filter', default=None,
                    help='Only keep URLs containing this string (e.g. a CDN hostname)')
    args = ap.parse_args()

    if not args.slug:
        print('Note: no --slug given; brand marks will land in 02-customer-logos.')

    os.makedirs(args.out, exist_ok=True)

    print(f'Crawling {len(args.pages)} pages of {args.url} ...')
    html, failed_pages = fetch_pages(args.url, args.pages)
    if failed_pages:
        print(f'  could not fetch: {", ".join(failed_pages)}')
    print(f'  {len(html):,} bytes of HTML')

    if not html.strip():
        print('\nNo HTML retrieved. Every page failed.\n'
              'Most likely one of:\n'
              '  * the site is client-rendered, so server HTML carries no <img> tags\n'
              '  * bot protection is rejecting the request\n'
              '  * the base URL is wrong (try with/without the www subdomain)\n'
              'Fall back to collecting asset URLs from the rendered DOM via the\n'
              'Chrome tools, then feed them to this script. See SKILL.md.')
        return 1

    keep = collect(html, args.host_filter)
    print(f'  {len(keep)} unique assets after stripping variants and encoding twins')

    if not keep:
        print('\nHTML retrieved but no image URLs matched. If the site serves images\n'
              'from a CDN this pattern misses, inspect the HTML and widen IMG_RE.')
        return 1

    plan = {}
    for name, url in keep.items():
        plan.setdefault(categorise(name, args.slug), []).append((name, url))
    for cat in sorted(plan):
        print(f'    {cat:22} {len(plan[cat]):3}')

    ok, failed = download(plan, args.out)
    print(f'\nDownloaded {ok}, failed {len(failed)}')
    for f in failed[:10]:
        print('  FAIL', f)

    dupes = find_duplicates(args.out)
    if dupes:
        print(f'\n{len(dupes)} byte-identical duplicates (reported, not deleted):')
        for d, o in dupes[:10]:
            print(f'  {d}\n    == {o}')

    manifest = {c: [{'name': n, 'url': u} for n, u in v] for c, v in plan.items()}
    with open(os.path.join(args.out, '_source_urls.json'), 'w') as fh:
        json.dump(manifest, fh, indent=1)
    print(f'\nSource URLs written to {args.out}/_source_urls.json')
    print('Next: build_asset_index.py to generate ASSETS.md and the contact sheet.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
