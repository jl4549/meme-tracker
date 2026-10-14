"""
Fetch full details for every link in data/my_picks.txt (quotes, replies or plain posts),
download their images, and save data/picks.json.

Run from the IS folder:
    python scripts/fetch_picks.py
"""
import json, os, urllib.parse, urllib.request

API = "https://public.api.bsky.app/xrpc/"
IMG_DIR = "data/images"


def get(method, **params):
    url = API + method + "?" + urllib.parse.urlencode(params, doseq=True)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def link_to_uri(link):
    parts = link.strip().rstrip("/").split("/")
    handle, rkey = parts[-3], parts[-1]
    did = handle if handle.startswith("did:") else get("com.atproto.identity.resolveHandle", handle=handle)["did"]
    return f"at://{did}/app.bsky.feed.post/{rkey}"


def images_of(view):
    e = view.get("embed") or {}
    if "images" in e.get("$type", ""):
        return e.get("images", [])
    return (e.get("media") or {}).get("images", [])


def quoted_uri(view):
    e = view.get("embed") or {}
    rec = e.get("record") or {}
    rec = rec.get("record", rec)          # recordWithMedia nests one level deeper
    return rec.get("uri")


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    picks = []
    for line in open("data/my_picks.txt", encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        link, _, note = (x.strip() for x in line.partition("|"))
        picks.append((link, note))

    out = []
    for n, (link, note) in enumerate(picks, 1):
        uri = link_to_uri(link)
        v = get("app.bsky.feed.getPosts", uris=uri)["posts"][0]
        rec = v["record"]
        prof = get("app.bsky.actor.getProfile", actor=v["author"]["did"])
        reply_parent = (rec.get("reply") or {}).get("parent", {}).get("uri")
        quote_parent = quoted_uri(v)
        imgs = []
        for k, im in enumerate(images_of(v)):
            path = f"{IMG_DIR}/{uri.split('/')[-1]}_{k}.jpg"
            if not os.path.exists(path):
                urllib.request.urlretrieve(im["fullsize"], path)
            imgs.append({"local": path, "alt": im.get("alt", ""), "aspect": im.get("aspectRatio")})
        out.append({
            "order": n, "link": link, "my_note": note,
            "uri": uri, "cid": v.get("cid"),
            "kind": "reply" if reply_parent else "quote" if quote_parent else "post",
            "parent_uri": reply_parent or quote_parent,
            "author_handle": v["author"]["handle"], "author_display_name": v["author"].get("displayName", ""),
            "author_did": v["author"]["did"],
            "author_followers": prof.get("followersCount"), "author_following": prof.get("followsCount"),
            "author_posts": prof.get("postsCount"), "author_joined": prof.get("createdAt"),
            "createdAt": rec.get("createdAt"), "text": rec.get("text", ""), "langs": rec.get("langs", []),
            "images": imgs,
            "likeCount": v.get("likeCount"), "repostCount": v.get("repostCount"),
            "replyCount": v.get("replyCount"), "quoteCount": v.get("quoteCount"),
            "labels": [l.get("val") for l in v.get("labels", [])],
        })
        print(f"{n:>2}. {out[-1]['kind']:<5} @{out[-1]['author_handle']}  ♥{out[-1]['likeCount']}  {out[-1]['text'][:60]!r}")

    json.dump(out, open("data/picks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n{len(out)} posts saved to data/picks.json")


if __name__ == "__main__":
    main()
