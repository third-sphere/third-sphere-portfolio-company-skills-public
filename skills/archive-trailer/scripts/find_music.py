#!/usr/bin/env python3
"""Search Wikimedia Commons for public-domain music recordings, with license metadata.

Usage: python3 find_music.py "<piece or mood>" [more queries ...]
Prints title, duration, license, performer and file URL for audio files whose Commons license
field says public domain. Recordings by U.S. military bands (Marine Band, Air Force Band, Army
Band, Navy Band) are federal works and a strong public-domain basis; they're marked GOV.
Always confirm on the file page before use: Commons licenses are uploader-entered.
"""
import json
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "archive-trailer skill (music search)"}
API = "https://commons.wikimedia.org/w/api.php"
GOV = re.compile(r"(United States|U\.S\.|US) (Marine|Air Force|Army|Navy|Coast Guard)( Band|)", re.I)


def search(q: str, limit: int = 20):
    params = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
              "gsrsearch": f"{q} filetype:audio", "gsrlimit": limit,
              "prop": "imageinfo", "iiprop": "url|size|extmetadata|mediatype|mime"}
    url = API + "?" + urllib.parse.urlencode(params)
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
    for p in (d.get("query", {}).get("pages") or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata", {})
        lic = re.sub("<[^>]+>", "", (m.get("LicenseShortName") or {}).get("value", ""))
        artist = re.sub("<[^>]+>", "", (m.get("Artist") or {}).get("value", "")).strip()
        yield {"title": p["title"], "license": lic, "artist": artist[:80], "url": ii.get("url"),
               "page": ii.get("descriptionurl"), "size_mb": round(ii.get("size", 0) / 1e6, 1),
               "gov": bool(GOV.search(artist + " " + p["title"]))}


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    for q in argv[1:]:
        print(f"== {q}")
        for r in search(q):
            if "public domain" not in r["license"].lower():
                continue
            tag = "GOV" if r["gov"] else "   "
            print(f"  {tag} {r['size_mb']:5.1f} MB  {r['title'][5:70]:65}  {r['artist'][:40]}")
            print(f"        {r['page']}")


if __name__ == "__main__":
    main(sys.argv)
