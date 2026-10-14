"""
Combine the hand-picked steps in data/demo_notes.json with the collected data
(quote posts, replies and Charlotte's picks) and write data/meme_chain.json
(+ data/meme_chain.js for demo.html).

Run from the IS folder (after fetch_quotes.py, fetch_replies.py, fetch_picks.py):
    python scripts/make_demo.py
"""
import json, os, sys, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from build_chain import dhash, hdist, text_sim, SAME_IMAGE

notes = json.load(open("data/demo_notes.json", encoding="utf-8"))
rk = lambda uri: uri.split("/")[-1] if uri else None

# ---- one pool of every post we know about, keyed by rkey ----
pool = {}
for p in json.load(open("data/quotes_all.json", encoding="utf-8")):
    pool[rk(p["id"])] = dict(p, kind="quote" if p["depth"] else "root")
if os.path.exists("data/replies_all.json"):
    for p in json.load(open("data/replies_all.json", encoding="utf-8")):
        pool.setdefault(rk(p["id"]), p)
if os.path.exists("data/picks.json"):
    for p in json.load(open("data/picks.json", encoding="utf-8")):
        base = pool.setdefault(rk(p["uri"]), {"id": p["uri"], "url": p["link"]})
        base.update({k: v for k, v in p.items() if v not in (None, "") and k not in ("link", "uri", "order")})
        base.setdefault("parent_id", p["parent_uri"])
        base["kind"] = p["kind"]
for p in pool.values():
    p.setdefault("parent_id", p.get("parent_uri"))

root = pool["3lfor55ezxc2s"]
root_hash = dhash(root["images"][0]["local"])


def own_image(p):
    return p["images"][0]["local"] if p.get("images") and p["images"][0].get("local") else None


def eff_image(p):
    """The picture a reader sees: the post's own, or the one it quotes/replies to."""
    while p is not None:
        if own_image(p):
            return own_image(p)
        p = pool.get(rk(p.get("parent_id")))
    return None


# ---- fill in profile numbers that replies don't carry ----
need = sorted({p["author_did"] for p in pool.values()
               if any(rk(p["id"]) == s["rkey"] for s in notes["steps"]) and p.get("author_following") is None})
for i in range(0, len(need), 25):
    url = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles?" + urllib.parse.urlencode({"actors": need[i:i + 25]}, doseq=True)
    for prof in json.load(urllib.request.urlopen(url, timeout=30)).get("profiles", []):
        for p in pool.values():
            if p.get("author_did") == prof["did"]:
                p.update(author_followers=prof.get("followersCount"), author_following=prof.get("followsCount"),
                         author_posts=prof.get("postsCount"), author_joined=prof.get("createdAt"),
                         author_display_name=p.get("author_display_name") or prof.get("displayName", ""))

steps = []
for n in notes["steps"]:
    p = pool[n["rkey"]]
    parent = pool.get(rk(p.get("parent_id")))
    eff = eff_image(p)
    own = own_image(p)

    if p is root:
        image_status = "original"
    elif not own:
        image_status = "inherited"
    else:
        d = hdist(dhash(own), dhash(eff_image(parent))) if parent and eff_image(parent) else 1.0
        image_status = "same" if d < SAME_IMAGE else "new"
    sim = text_sim(p.get("text", ""), root["text"])
    caption_status = ("original" if p is root else "none" if not p.get("text", "").strip()
                      else "kept" if sim >= 0.9 else "edited" if sim >= 0.6 else "new")

    steps.append({
        "id": p["id"], "parent_id": p.get("parent_id"), "kind": p.get("kind", "quote"),
        "author_handle": p["author_handle"], "author_followers": p.get("author_followers"),
        "createdAt": p["createdAt"], "text": p.get("text", ""),
        "image_path_or_url": eff, "own_image": bool(own),
        "image_alt": p["images"][0]["alt"] if p.get("images") else "",
        "is_ai_generated": n.get("is_ai_generated"),
        "quoteCount": p.get("quoteCount", 0), "repostCount": p.get("repostCount", 0), "likeCount": p.get("likeCount", 0),
        "added": n["added"], "kept": n["kept"], "lost": n["lost"], "emotion": n["emotion"],
        "act": n["act"], "type": n.get("type") or next(a["type"] for a in notes["acts"] if a["id"] == n["act"]),
        "facets": n.get("facets", {}),
        "title": n["title"], "note": n.get("note", ""), "ai_note": n.get("ai_note", ""),
        "picked_by": n.get("picked_by", ""), "image_change": n.get("image_change"),
        "depth": p.get("depth", 1), "url": p["url"],
        "image_status": image_status, "caption_status": caption_status,
        "text_drift": None if p is root else round(1 - (0 if caption_status == "none" else sim), 2),
        "image_drift": None if p is root or not eff else hdist(dhash(eff), root_hash),
        "coded_by": "draft",
        "details": {
            "display_name": p.get("author_display_name", ""), "did": p.get("author_did"),
            "following": p.get("author_following"), "posts": p.get("author_posts"), "joined": p.get("author_joined"),
            "langs": p.get("langs", []), "labels": p.get("labels", []), "links": p.get("links", []),
            "replyCount": p.get("replyCount"),
            "images": [{"local": i.get("local"), "alt": i.get("alt", ""), "aspect": i.get("aspect")} for i in p.get("images", [])],
            "uri": p["id"], "cid": p.get("cid"),
            "parent": None if not parent else {"url": parent["url"], "handle": parent["author_handle"],
                                               "text": parent.get("text", ""), "createdAt": parent["createdAt"]},
        },
    })

# ---- every collected post on one timeline: [minutes after the big entry post, kind] ----
t_root = root["createdAt"]
def mins(iso):
    from datetime import datetime
    f = lambda x: datetime.fromisoformat(x.replace("Z", "+00:00"))
    return round((f(iso) - f(t_root)).total_seconds() / 60, 1)
timeline = [[mins(p["createdAt"]), "quote" if p.get("kind") == "quote" else "reply"]
            for p in pool.values() if p.get("kind") in ("quote", "reply") and p.get("createdAt")]
indep = json.load(open("data/independent_all.json", encoding="utf-8")) if os.path.exists("data/independent_all.json") else []
timeline += [[mins(p["createdAt"]), "independent" if p["kind"] == "independent" else "other-entry"] for p in indep if p.get("createdAt")]
timeline.sort()

links = {
    "likes": root.get("likeCount"), "reposts": root.get("repostCount"),
    "quotes_listed": root.get("quoteCount"), "replies_listed": root.get("replyCount"),
    "quotes": sum(1 for p in pool.values() if p.get("kind") == "quote"),
    "quote_max_depth": max(p.get("depth", 0) for p in pool.values() if p.get("kind") == "quote"),
    "replies": sum(1 for p in pool.values() if p.get("kind") == "reply"),
    "reply_max_depth": max((p.get("depth", 0) for p in pool.values() if p.get("kind") == "reply"), default=0),
    "quotes_deep": sum(1 for p in pool.values() if p.get("kind") == "quote" and p.get("depth", 0) >= 2),
    "replies_deep": sum(1 for p in pool.values() if p.get("kind") == "reply" and p.get("depth", 0) >= 2),
    "independent": sum(1 for p in indep if p["kind"] == "independent"),
    "other_entry": sum(1 for p in indep if p["kind"] != "independent"),
}

out = {"acts": notes["acts"], "origin": notes.get("origin", []), "root_created": root["createdAt"],
       "facets": notes.get("facets", []), "timeline": timeline, "links": links,
       "total_quotes": sum(1 for p in pool.values() if p.get("kind") == "quote"),
       "total_replies": sum(1 for p in pool.values() if p.get("kind") == "reply"),
       "steps": steps}
json.dump(out, open("data/meme_chain.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
with open("data/meme_chain.js", "w", encoding="utf-8") as f:
    f.write("// generated by scripts/make_demo.py\nwindow.MEME = " + json.dumps(out, ensure_ascii=False) + ";\n")
print(f"{len(steps)} steps -> data/meme_chain.json, data/meme_chain.js")
for i, s in enumerate(steps, 1):
    print(f"{i:>2} act{s['act']} {s['type']:<4} {s['kind']:<5} img:{s['image_status']:<9} cap:{s['caption_status']:<7} {s['title']}")
