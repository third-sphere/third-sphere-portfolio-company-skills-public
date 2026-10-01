#!/usr/bin/env python3
"""Smoke-test a built review page in headless Chromium before publishing it.

Usage: python3 check_page.py page.html [screenshot.png]

Checks: no JavaScript errors; every item renders with its options; clicking an option shows up
in the JSON export; answers survive a reload; no horizontal scroll at phone width (390px).
Leaves the page's saved answers cleared afterwards. Needs `playwright` with Chromium; if it's
missing, prints a notice and exits 0 so a build isn't blocked (the check is a safety net).
"""
import asyncio
import json
import sys
from pathlib import Path


async def run(page_path: Path, shot):
    from playwright.async_api import async_playwright
    url = page_path.resolve().as_uri()
    problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        await pg.goto(url)
        await pg.wait_for_timeout(800)
        spec = await pg.evaluate("SPEC")
        for it in spec["items"]:
            n = await pg.locator(f'.tile[data-item="{it["id"]}"]').count()
            if n != len(it["options"]):
                problems.append(f"{it['id']}: {n} tiles rendered, expected {len(it['options'])}")
        first = spec["items"][0]
        target = first["options"][-1]["id"]
        await pg.locator(f'.tile[data-item="{first["id"]}"][data-opt="{target}"]').click()
        exp = json.loads(await pg.input_value("#json"))
        got = next(x for x in exp["items"] if x["id"] == first["id"])
        if target not in got["picks"] or got["action"] != "pick":
            problems.append(f"click on {target} did not reach the export: {got}")
        if shot:
            await pg.screenshot(path=shot)
        await pg.reload()
        await pg.wait_for_timeout(500)
        exp2 = json.loads(await pg.input_value("#json"))
        if next(x for x in exp2["items"] if x["id"] == first["id"])["picks"] != got["picks"]:
            problems.append("answers did not survive a reload")
        await pg.set_viewport_size({"width": 390, "height": 844})
        await pg.wait_for_timeout(300)
        width = await pg.evaluate("document.documentElement.scrollWidth")
        if width > 392:
            problems.append(f"page scrolls sideways on a phone ({width}px wide)")
        await pg.evaluate("localStorage.clear()")
        await b.close()
    problems += [f"JS error: {e}" for e in errors]
    return problems


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("playwright not installed; skipped the browser check")
        return
    problems = asyncio.run(run(Path(argv[1]), argv[2] if len(argv) > 2 else None))
    if problems:
        print("FAILED:\n  " + "\n  ".join(problems))
        sys.exit(1)
    print("page OK: renders, picks export, survives reload, fits a phone")


if __name__ == "__main__":
    main(sys.argv)
