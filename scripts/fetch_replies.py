"""
Fetch every reply (and reply-to-reply) under the original post, download images,
and save data/replies_all.json. Same fields as quotes_all.json, plus kind="reply".

Run from the IS folder:
    python scripts/fetch_replies.py
"""
import json, os, time, urllib.parse, urllib.request

API = "https://public.api.bsky.app/xrpc/"
ROOT = "at://did:plc:qva6zago4agr25tkiu6rbyw6/app.bsky.feed.post/3lfor55ezxc2s"
IMG_DIR = "data/images"


def get(method, **params):
    url = API + method + "?" + urllib.parse.urlencode(params, doseq=True)
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            print("  retry", e); time.sleep(2)
    raise RuntimeError(url)


def images_of(v):
    e = v.get("embed") or {}
    if "images" in e.get("$type", ""):
        return e.get("images", [])
    return (e.get("media") or {}).get("images", [])


def walk(node, depth, out, seen):
    """Depth-first through the thread. Fetch again where the API cut a branch short."""
    for r in node.get("replies", []) or []:
        if r.get("$type", "").endswith("threadViewPost") is False or "post" not in r:
            continue
        v = r["post"]
        if v["uri"] in seen:
            continue
        seen.add(v["uri"])
        out.append((v, node["post"]["uri"], depth))
        if v.get("replyCount", 0) and not r.get("replies"):
            r = get("app.bsky.feed.getPostThread", uri=v["uri"], depth=50, parentHeight=0)["thread"]
        walk(r, depth + 1, out, seen)


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    thread = get("app.bsky.feed.getPostThread", uri=ROOT, depth=50, parentHeight=0)["thread"]
    found = []
    walk(thread, 1, found, set())

    dids = sorted({v["author"]["did"] for v, _, _ in found})
    profiles = {}
    for i in range(0, len(dids), 25):
        for p in get("app.bsky.actor.getProfiles", actors=dids[i:i + 25]).get("profiles", []):
            profiles[p["did"]] = p

    records = []
    for v, parent, depth in found:
        rec, prof = v["record"], profiles.get(v["author"]["did"], {})
        imgs = []
        for k, im in enumerate(images_of(v)):
            path = f"{IMG_DIR}/{v['uri'].split('/')[-1]}_{k}.jpg"
            if not os.path.exists(path):
                try:
                    urllib.request.urlretrieve(im["fullsize"], path)
                except Exception as e:
                    print("  image failed", path, e); path = None
            imgs.append({"local": path, "alt": im.get("alt", ""), "aspect": im.get("aspectRatio")})
        records.append({
            "id": v["uri"], "parent_id": parent, "depth": depth, "kind": "reply",
            "url": f"https://bsky.app/profile/{v['author']['handle']}/post/{v['uri'].split('/')[-1]}",
            "author_handle": v["author"]["handle"], "author_display_name": v["author"].get("displayName", ""),
            "author_did": v["author"]["did"], "author_followers": prof.get("followersCount"),
            "createdAt": rec.get("createdAt"), "text": rec.get("text", ""), "langs": rec.get("langs", []),
            "images": imgs, "has_image": bool(imgs),
            "likeCount": v.get("likeCount", 0), "repostCount": v.get("repostCount", 0),
            "replyCount": v.get("replyCount", 0), "quoteCount": v.get("quoteCount", 0),
        })

    json.dump(records, open("data/replies_all.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"replies: {len(records)}  with images: {sum(r['has_image'] for r in records)}  "
          f"max depth: {max(r['depth'] for r in records)}")


if __name__ == "__main__":
    main()
