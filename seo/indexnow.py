#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Push every ourword.ai URL to IndexNow (Bing, Yandex, Seznam, Naver share one endpoint).

Waiting to be crawled can take weeks. IndexNow is a submit-side ping: it needs no
account and no OAuth, only a key file served from the domain root, so it is the one
active-discovery lever available to a static site.

Google has no equivalent open endpoint — for Google the path is the sitemap declared in
https://ourword.ai/robots.txt plus a one-off Search Console verification.

Run from the apex repo root:  python seo/indexnow.py [--dry-run]
"""
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

HOST = "ourword.ai"
KEY = "40103483e16da86253413fba25739b49"
ENDPOINT = "https://api.indexnow.org/IndexNow"
SITEMAP_INDEX = "https://%s/sitemap.xml" % HOST
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
BATCH = 10000          # IndexNow's documented per-request ceiling


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ourword-ai-indexnow/1.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def urls_from(sitemap_url):
    """Walk a sitemap or sitemap index and return every <loc> under it."""
    try:
        root = ET.fromstring(fetch(sitemap_url))
    except Exception as e:
        print("  skip %s (%s)" % (sitemap_url, type(e).__name__))
        return []
    tag = root.tag.split("}")[-1]
    if tag == "sitemapindex":
        out = []
        for sm in root.findall("s:sitemap/s:loc", NS):
            out += urls_from(sm.text.strip())
        return out
    return [loc.text.strip() for loc in root.findall("s:url/s:loc", NS) if loc.text]


def submit(urls):
    payload = json.dumps({"host": HOST, "key": KEY,
                          "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
                          "urlList": urls}).encode()
    req = urllib.request.Request(ENDPOINT, data=payload, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read(200).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(300).decode("utf-8", "replace")
    except Exception as e:
        return 0, "%s: %s" % (type(e).__name__, e)


def main():
    dry = "--dry-run" in sys.argv
    urls = sorted(set(urls_from(SITEMAP_INDEX)))
    print("collected %d URLs from %s" % (len(urls), SITEMAP_INDEX))
    if not urls:
        print("nothing to submit"); return 1
    if dry:
        for u in urls[:10]:
            print("  ", u)
        print("  … (dry run, nothing submitted)")
        return 0
    for i in range(0, len(urls), BATCH):
        chunk = urls[i:i + BATCH]
        code, body = submit(chunk)
        print("submitted %d URLs -> HTTP %s %s" % (len(chunk), code, body[:120]))
        # 200 accepted, 202 accepted-pending-key-validation; anything else is worth seeing.
        if code not in (200, 202):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
