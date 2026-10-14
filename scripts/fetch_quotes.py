"""
Fetch every quote post of one Bluesky post (and quotes of those quotes),
download the images, and save everything to data/.

Run from the IS folder:
    python scripts/fetch_quotes.py https://bsky.app/profile/birdrespecter.bsky.social/post/3lfor55ezxc2s

No login or API key needed: it only reads public data.
"""
import json, os, sys, time, urllib.parse, urllib.request

API = "https://public.api.bsky.app/xrpc/"
MAX_DEPTH = 3          # 1 = quotes of the original, 2 = quotes of quotes, ...
OUT_DIR = "data"
IMG_DIR = os.path.join(OUT_DIR, "images")


def get(method, **params):
    url = API + method + "?" + urllib.parse.urlencode(params, doseq=True)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            print("  retry", method, e)
            time.sleep(2)
    raise RuntimeError("failed: " + url)


def link_to_uri(link):
    # https://bsky.app/profile/<handle>/post/<rkey>  ->  at://<did>/app.bsky.feed.post/<rkey>
    parts = link.rstrip("/").split("/")
    handle, rkey = parts[-3], parts[-1]
    did = handle if handle.startswith("did:") else get("com.atproto.identity.resolveHandle", handle=handle)["did"]
    return f"at://{did}/app.bsky.feed.post/{rkey}"


def images_of(post):
    """Return the images a post itself attaches (not the images of the post it quotes)."""
    e = post.get("embed") or {}
    t = e.get("$type", "")
    if t.startswith("app.bsky.embed.images"):
        return e.get("images", [])
    if t.startswith("app.bsky.embed.recordWithMedia"):
        return (e.get("media") or {}).get("images", [])
    return []


def has_video(post):
    e = post.get("embed") or {}
    return "video" in e.get("$type", "") or "video" in (e.get("media") or {}).get("$type", "")


def all_quotes(uri):
    out, cursor = [], None
    while True:
        params = {"uri": uri, "limit": 100}
        if cursor:
            params["cursor"] = cursor
        d = get("app.bsky.feed.getQuotes", **params)
        out += d.get("posts", [])
        cursor = d.get("cursor")
        if not cursor or not d.get("posts"):
            return out
        time.sleep(0.3)


def links_of(post):
    """Links written in the post text, plus a link card if the post has one."""
    out = []
    for f in post["record"].get("facets", []) or []:
        for feat in f.get("features", []):
            if feat.get("uri"):
                out.append(feat["uri"])
    e = post.get("embed") or {}
    ext = e.get("external") or (e.get("media") or {}).get("external")
    if ext:
        out.append(ext.get("uri"))
    return out


def to_record(post, parent_id, depth):
    imgs = images_of(post)
    return {
        "cid": post.get("cid"),
        "author_display_name": post["author"].get("displayName", ""),
        "langs": post["record"].get("langs", []),
        "labels": [l.get("val") for l in post.get("labels", [])],
        "links": links_of(post),
        "indexedAt": post.get("indexedAt"),
        "bookmarkCount": post.get("bookmarkCount"),
        "id": post["uri"],
        "parent_id": parent_id,
        "depth": depth,
        "url": "https://bsky.app/profile/{}/post/{}".format(post["author"]["handle"], post["uri"].split("/")[-1]),
        "author_handle": post["author"]["handle"],
        "author_did": post["author"]["did"],
        "author_followers": None,          # filled in below
        "createdAt": post["record"].get("createdAt"),
        "text": post["record"].get("text", ""),
        "images": [{"thumb": i.get("thumb"), "full": i.get("fullsize"), "alt": i.get("alt", ""), "local": None,
                    "aspect": i.get("aspectRatio")} for i in imgs],
        "has_image": bool(imgs),
        "has_video": has_video(post),
        "is_ai_generated": None,           # to code by hand later
        "quoteCount": post.get("quoteCount", 0),
        "repostCount": post.get("repostCount", 0),
        "likeCount": post.get("likeCount", 0),
        "replyCount": post.get("replyCount", 0),
        "added": None, "kept": None, "lost": None, "emotion": None,   # to code by hand later
    }


def main(link):
    os.makedirs(IMG_DIR, exist_ok=True)
    root_uri = link_to_uri(link)
    root = get("app.bsky.feed.getPosts", uris=root_uri)["posts"][0]
    records = [to_record(root, None, 0)]

    # Walk the quote tree level by level
    frontier = [root]
    for depth in range(1, MAX_DEPTH + 1):
        nxt = []
        for parent in frontier:
            if parent.get("quoteCount", 0) == 0:
                continue
            qs = all_quotes(parent["uri"])
            print(f"depth {depth}: {len(qs):>4} quotes of {parent['uri'].split('/')[-1]}")
            for q in qs:
                records.append(to_record(q, parent["uri"], depth))
                nxt.append(q)
        frontier = nxt

    # Follower counts (25 profiles per request)
    dids = sorted({r["author_did"] for r in records})
    profiles = {}
    for i in range(0, len(dids), 25):
        for p in get("app.bsky.actor.getProfiles", actors=dids[i:i + 25]).get("profiles", []):
            profiles[p["did"]] = p
    for r in records:
        p = profiles.get(r["author_did"], {})
        r["author_followers"] = p.get("followersCount")
        r["author_following"] = p.get("followsCount")
        r["author_posts"] = p.get("postsCount")
        r["author_joined"] = p.get("createdAt")
    fetched = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for r in records:
        r["fetchedAt"] = fetched       # counts are as of this moment

    # Download images (full size)
    for r in records:
        for k, img in enumerate(r["images"]):
            name = "{}_{}.jpg".format(r["id"].split("/")[-1], k)
            path = os.path.join(IMG_DIR, name)
            if not os.path.exists(path):
                try:
                    urllib.request.urlretrieve(img["full"] or img["thumb"], path)
                except Exception as e:
                    print("  image failed", name, e)
                    continue
            img["local"] = path.replace("\\", "/")

    with open(os.path.join(OUT_DIR, "quotes_all.json"), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    with_img = [r for r in records if r["has_image"]]
    print("\nDone.")
    print(f"  total posts (original + quotes): {len(records)}")
    print(f"  with images:                     {len(with_img)}")
    print(f"  with video:                      {sum(r['has_video'] for r in records)}")
    print(f"  by depth: " + ", ".join(f"{d}={sum(r['depth'] == d for r in records)}" for d in range(MAX_DEPTH + 1)))
    print(f"  saved: {OUT_DIR}/quotes_all.json and {IMG_DIR}/")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         "https://bsky.app/profile/birdrespecter.bsky.social/post/3lfor55ezxc2s")
