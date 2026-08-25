/*
 * extract_tokens.js — measure a site's design tokens from the live DOM.
 *
 * Run each block separately in the Chrome tool (javascript_tool). They are split
 * because a single combined return usually exceeds the tool's output limit and
 * gets truncated mid-JSON, which costs a retry.
 *
 * Why computed CSS rather than reading the stylesheet or eyeballing a screenshot:
 * a screenshot gives you approximate colors, and a stylesheet gives you every
 * value the framework ever shipped. Computed style on rendered elements gives you
 * what the user actually sees, weighted by how much of it they see.
 */

// ---------------------------------------------------------------------------
// BLOCK 1 — Design-system variables
// Many sites (Webflow, Tailwind config, any modern design system) publish their
// palette as CSS custom properties, often with the team's own names for the
// colors. Those names are worth keeping: they let you talk to the company's
// designer in their own vocabulary.
// ---------------------------------------------------------------------------
(() => {
  const vars = {};
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.selectorText && /(^|,)\s*(:root|html|body)\s*(,|$)/.test(rule.selectorText)) {
          for (const p of rule.style) {
            if (p.startsWith('--')) vars[p] = rule.style.getPropertyValue(p).trim();
          }
        }
      }
    } catch (e) { /* cross-origin sheet; skip */ }
  }
  return JSON.stringify(vars, null, 1);
})()


// ---------------------------------------------------------------------------
// BLOCK 2 — Color census weighted by rendered area
// The key output. Counting selectors tells you what the framework defines;
// summing painted pixel area tells you what the brand actually looks like.
// A color used on one full-bleed section outranks one used on forty badges,
// and that ratio is what you reproduce in a deck.
// ---------------------------------------------------------------------------
(() => {
  const text = {}, bg = {}, fonts = {};
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;      // invisible; would skew counts
    const cs = getComputedStyle(el);
    text[cs.color] = (text[cs.color] || 0) + 1;
    if (cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)') {
      bg[cs.backgroundColor] = (bg[cs.backgroundColor] || 0) + Math.round(r.width * r.height);
    }
    fonts[cs.fontFamily] = (fonts[cs.fontFamily] || 0) + 1;
  });
  const top = (o, n) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n);
  return JSON.stringify({
    textColors: top(text, 12),
    backgroundsByArea: top(bg, 12),        // <- the proportion that matters
    fonts: top(fonts, 8),
    bodyBg: getComputedStyle(document.body).backgroundColor,
    bodyFont: getComputedStyle(document.body).fontFamily,
    title: document.title
  }, null, 1);
})()


// ---------------------------------------------------------------------------
// BLOCK 3 — Type scale from real elements
// Takes the first visible instance of each tag rather than a synthetic probe,
// so you capture the site's actual headline treatment. Watch line-height
// especially: a sub-1.0 value on H1 is a deliberate signature and is the single
// detail most often lost when a deck is rebuilt from a screenshot.
// ---------------------------------------------------------------------------
(() => {
  const rows = [];
  ['h1','h2','h3','h4','p','a','li','blockquote'].forEach(tag => {
    const el = [...document.querySelectorAll(tag)]
      .find(e => e.getBoundingClientRect().width > 0 && e.textContent.trim().length > 3);
    if (!el) return;
    const cs = getComputedStyle(el);
    rows.push({
      tag,
      font: cs.fontFamily.split(',')[0],
      size: cs.fontSize, weight: cs.fontWeight,
      lineHeight: cs.lineHeight, tracking: cs.letterSpacing,
      color: cs.color, transform: cs.textTransform,
      sample: el.textContent.trim().slice(0, 60)
    });
  });
  return JSON.stringify(rows, null, 1);
})()


// ---------------------------------------------------------------------------
// BLOCK 4 — Buttons and loaded font weights
// Button treatment is the fastest read on a design system's consistency. Sites
// frequently ship two or three radii; note the inconsistency and standardize in
// the style guide rather than silently picking one.
// document.fonts tells you which weights are actually available — decisive when
// the deck needs an 800 that may not be loaded.
// ---------------------------------------------------------------------------
(() => {
  const btns = [...document.querySelectorAll('a[class*=button],a[class*=btn],button')]
    .filter(e => e.getBoundingClientRect().width > 0).slice(0, 8)
    .map(el => {
      const cs = getComputedStyle(el);
      return el.textContent.trim().slice(0, 25) +
        ' | bg:' + cs.backgroundColor + ' | c:' + cs.color +
        ' | r:' + cs.borderRadius + ' | p:' + cs.padding +
        ' | bd:' + cs.borderWidth + ' ' + cs.borderColor +
        ' | ' + cs.fontFamily.split(',')[0] + ' ' + cs.fontSize + '/' + cs.fontWeight +
        ' ls:' + cs.letterSpacing + ' tt:' + cs.textTransform;
    });
  const faces = new Set();
  document.fonts.forEach(f => faces.add(f.family + ' ' + f.weight + ' ' + f.style));
  return JSON.stringify({ buttons: btns, loadedFontFaces: [...faces] }, null, 1);
})()


// ---------------------------------------------------------------------------
// BLOCK 5 — Internal link map
// Feeds the asset crawler. One page is never the whole asset library; the
// richest imagery usually lives on about/team/impact pages, not the homepage.
// ---------------------------------------------------------------------------
(() => {
  const host = location.hostname.replace(/^www\./, '');
  const links = [...new Set([...document.querySelectorAll('a[href]')]
    .map(a => a.href)
    .filter(h => h.includes(host) && !h.includes('#')))];
  return links.join('\n');
})()
