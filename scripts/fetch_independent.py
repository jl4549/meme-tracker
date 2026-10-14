"""
Find posts that use the sentence but do NOT quote or reply to the Bluesky entry post
(independent copies). Bluesky search only returns one page per query, so we search day by day.

Run from the IS folder:
    python scripts/fetch_independent.py
"""
import json, datetime, os, time, urllib.parse, urllib.request

SEARCH = "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts"
ROOT_RKEY = "3lfor55ezxc2s"


def search(q, since, until):
    url = SEARCH + "?" + urllib.parse.urlencode({"q": q, "sort": "latest", "limit": 100, "since": since, "until": until})
    req = urllib.request.Request(url, headers={"User-Agent": "research-test"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("posts", [])


known = {p["id"] for p in json.load(open("data/quotes_all.json", encoding="utf-8"))}
known |= {p["id"] for p in json.load(open("data/replies_all.json", encoding="utf-8"))}

found = {}
start = datetime.datetime(2025, 1, 1)
days = [(start + datetime.timedelta(days=d)) for d in range(0, 45)]
windows = [(d, d + datetime.timedelta(days=1)) for d in days]
windows.append((datetime.datetime(2025, 2, 15), datetime.datetime(2026, 10, 7)))   # long tail, one big window
for a, b in windows:
    for q in ['"leaked photo of heaven"', '"leaked photo of hell"']:
        try:
            posts = search(q, a.strftime("%Y-%m-%dT00:00:00Z"), b.strftime("%Y-%m-%dT00:00:00Z"))
        except Exception as e:
            print("skip", a.date(), q, e); continue
        for p in posts:
            if p["uri"] in known:
                continue
            rec = p["record"]
            e = p.get("embed") or {}
            quoted = ((e.get("record") or {}).get("record") or e.get("record") or {}).get("uri")
            found[p["uri"]] = {
                "id": p["uri"], "kind": "independent" if not rec.get("reply") and not quoted else
                        "reply-elsewhere" if rec.get("reply") else "quote-elsewhere",
                "url": f"https://bsky.app/profile/{p['author']['handle']}/post/{p['uri'].split('/')[-1]}",
                "author_handle": p["author"]["handle"], "createdAt": rec.get("createdAt"),
                "text": rec.get("text", ""), "langs": rec.get("langs", []),
                "has_image": "image" in e.get("$type", "") or "images" in json.dumps(e.get("media", {})),
                "likeCount": p.get("likeCount", 0), "quoteCount": p.get("quoteCount", 0),
                "replyCount": p.get("replyCount", 0), "repostCount": p.get("repostCount", 0),
            }
        time.sleep(0.2)

out = sorted(found.values(), key=lambda p: p["createdAt"] or "")
json.dump(out, open("data/independent_all.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
from collections import Counter
print("found:", len(out), dict(Counter(p["kind"] for p in out)), "with image:", sum(p["has_image"] for p in out))
print("earliest:", [(p["createdAt"][:16], p["text"][:60]) for p in out[:3]])
