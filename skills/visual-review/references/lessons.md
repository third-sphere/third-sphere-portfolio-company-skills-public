# Lessons from real rounds

Each of these cost a round of rework once. Read before building an unusual page.

## Publishing
- Published claude.ai pages block remote images (content-security policy). Every option image
  has to be inline, which `build_page.py` does. A page that points at image URLs publishes fine
  and then shows empty tiles.
- The published limit is 16 MB. Inline thumbnails run ~15 KB per still and ~15 KB per 4-frame
  video strip, so a few hundred options fit comfortably. Full-size images do not.
- Links on a tile leave the page. Point them at a viewing page (an archive item page, a gallery),
  never a raw file that may be hundreds of MB.
- Some CDNs reject Python's default User-Agent (Cloudflare R2 returned 403). The scripts send a
  browser-style one.

## The review loop
- Give each page and each round its own `storage_key`. Two pages sharing a key load each other's
  saved answers.
- A later round often answers only a few things ("change one caption"). Merge it; never rebuild
  state from the latest export alone. That exact bug once wiped a user's earlier decisions.
- Save every export verbatim before merging (`merge_export.py` does this under `rounds/`).
- Show the current choice on its tile (the badge) so keeping it is one glance, and let the
  user keep everything they don't touch: untouched items export as `keep`.

## Curating options
- Screen options before the user sees them, and write down why each one was cut (`exclude`
  with a reason). Report the cuts in one or two sentences; don't make the user wade through junk.
- If an option is usable but carries a risk (identifiable people, a third party's logo or
  product, unclear rights), keep it and put the risk on the tile as a `flag`. The user decides.
- Watch for options that could mislead a viewer: modern footage of someone else's product under
  a caption about your product reads as that product.
- Order within an item doesn't imply rank unless you say so. If order matters (a sequence of
  shots), multi-pick numbers show the play order.

## Testing
- Run `check_page.py` before publishing. It catches the failures that matter: a click that
  doesn't reach the export, answers lost on reload, and sideways scrolling on a phone.
- Interactive elements can't nest: a link inside a `<button>` breaks clicks on some browsers.
  The template keeps the link outside the tile button; keep it that way if you edit it.
