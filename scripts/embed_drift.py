"""
Drift scores from embeddings, saved as separate LAYERS. The original data files are only read, never changed.

Main model:  EmbeddingGemma 2 (google/embeddinggemma-2). Text and images go into ONE 768-d space,
             so we also get a joint caption+picture score and a caption-vs-picture score.
Baseline:    CLIP ViT-B/32 (sentence-transformers/clip-ViT-B-32), also text+image in one space.

Two sets of posts:
  demo   the 27 versions in demo.html          reads data/meme_chain.json
  all    the original + every quote post       reads data/chain_data.js (chain_viewer.html)

Output, one file per model per set (the .js copy is what the web pages load):
  data/layers/<set>_gemma.json/.js    data/layers/<set>_clip.json/.js
  rows: {rkey: {text, image, joint, cap_img}}

drift = 1 - cosine similarity to the original (the entry post, rkey 3lfor55ezxc2s)
  text    caption only (posts with no caption get none)
  image   the picture a reader sees (own picture, or the one it quotes/replies to)
  joint   caption + picture in one embedding (EmbeddingGemma 2 only)
  cap_img how well the caption matches its own picture (cosine, higher = closer). Only compare
          within one model: CLIP and Gemma cosines live on different scales.

Run from the IS folder, with the project venv (first run downloads ~1.5 GB of weights):
    .venv\\Scripts\\python scripts\\embed_drift.py demo
    .venv\\Scripts\\python scripts\\embed_drift.py all
"""
import json, os, sys
import numpy as np
import torch
from PIL import Image
from sentence_transformers import SentenceTransformer

ROOT = "3lfor55ezxc2s"
MODELS = {
    "gemma": {"name": "google/embeddinggemma-2", "label": "EmbeddingGemma 2", "joint": True},
    "clip": {"name": "sentence-transformers/clip-ViT-B-32", "label": "CLIP ViT-B/32 (baseline)", "joint": False},
}
OUT_DIR = "data/layers"

rk = lambda uri: uri.split("/")[-1]


def load_posts(which):
    """[(rkey, caption, picture path or None, old text drift, old image drift)] for one set."""
    if which == "demo":
        steps = json.load(open("data/meme_chain.json", encoding="utf-8"))["steps"]
        return [(rk(s["id"]), s["text"], s["image_path_or_url"], s["text_drift"], s["image_drift"]) for s in steps]
    src = open("data/chain_data.js", encoding="utf-8").read()
    posts = json.loads(src[src.index("["):src.rindex("]") + 1])
    return [(rk(p["id"]), p["text"], p["eff_image"],
             None if p["depth"] == 0 else 1 - (0 if p["caption_status"] == "none" else p["text_sim_root"]),
             p["img_dist_root"]) for p in posts]


def cos(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def spearman(x, y):
    """Rank correlation, ignoring pairs where either value is missing."""
    pairs = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pairs) < 3:
        return None, len(pairs)
    r = lambda v: np.argsort(np.argsort(v)).astype(float)
    a, b = map(np.array, zip(*pairs))
    return round(float(np.corrcoef(r(a), r(b))[0, 1]), 2), len(pairs)


def embed_all(posts, model, joint):
    """Return {rkey: {"text": vec|None, "image": vec|None, "joint": vec|None}} for one model."""
    texts = [t.strip() for _, t, _, _, _ in posts]
    paths = sorted({p for _, _, p, _, _ in posts if p})          # many posts share the quoted picture
    imgs = {p: Image.open(p).convert("RGB") for p in paths}

    t_idx = [i for i, t in enumerate(texts) if t]
    t_vec = dict(zip(t_idx, model.encode([texts[i] for i in t_idx], batch_size=16, show_progress_bar=True)))
    i_vec = dict(zip(paths, model.encode([{"image": imgs[p]} for p in paths], batch_size=4, show_progress_bar=True)))

    out = {}
    for i, (key, _, path, _, _) in enumerate(posts):
        out[key] = {"text": t_vec.get(i), "image": i_vec.get(path), "joint": None}
    if joint:
        j_in = [{k: v for k, v in (("text", texts[i]), ("image", imgs.get(p[2]))) if v} for i, p in enumerate(posts)]
        for (key, *_), v in zip(posts, model.encode(j_in, batch_size=4, show_progress_bar=True)):
            out[key]["joint"] = v
    return out


def scores(vecs, joint):
    root = vecs[ROOT]
    res = {}
    for key, v in vecs.items():
        d = lambda k: None if v[k] is None or root[k] is None else round(max(0.0, 1 - cos(v[k], root[k])), 3)
        row = {"text": d("text"), "image": d("image"),
               "cap_img": None if v["text"] is None or v["image"] is None else round(cos(v["text"], v["image"]), 3)}
        if joint:
            row["joint"] = d("joint")
        res[key] = row
    return res


def save_layer(which, key, rows):
    m = MODELS[key]
    layer = {"set": which, "model": m["name"], "label": m["label"], "root": ROOT,
             "note": "drift = 1 - cosine to the original; cap_img = cosine caption vs own picture", "rows": rows}
    os.makedirs(OUT_DIR, exist_ok=True)
    base = f"{OUT_DIR}/{which}_{key}"
    json.dump(layer, open(base + ".json", "w", encoding="utf-8"), indent=1)
    with open(base + ".js", "w", encoding="utf-8") as f:
        f.write(f"// generated by scripts/embed_drift.py {which}\n"
                f"(window.DRIFT_LAYERS = window.DRIFT_LAYERS || {{}})[{json.dumps(key)}] = {json.dumps(layer)};\n")
    print("saved", base + ".json/.js")


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "demo"
    assert which in ("demo", "all"), "use: embed_drift.py demo | all"
    posts = load_posts(which)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # float16 gives NaN/garbage with EmbeddingGemma 2 (model card), so bf16 on GPU or fp32 on CPU
    dtype = torch.bfloat16 if device == "cuda" and torch.cuda.is_bf16_supported() else torch.float32
    print(f"{which}: {len(posts)} posts, {len({p[2] for p in posts if p[2]})} distinct pictures · {device} {dtype}")

    res = {}
    for key, m in MODELS.items():
        kw = {"model_kwargs": {"torch_dtype": dtype}, "config_kwargs": {"audio_config": None}} if key == "gemma" else {}
        model = SentenceTransformer(m["name"], device=device, **kw)   # gemma: text + image, no audio encoder
        res[key] = scores(embed_all(posts, model, m["joint"]), m["joint"])
        save_layer(which, key, res[key])
        del model
        torch.cuda.empty_cache()

    # ---- how well the layers agree ----
    col = lambda m, k: [res[m][p[0]][k] if p[0] != ROOT else None for p in posts]
    old_t, old_i = [p[3] for p in posts], [p[4] for p in posts]
    print("\nSpearman rank agreement (rho, n):")
    print("  caption  gemma vs clip:", spearman(col("gemma", "text"), col("clip", "text")),
          "| gemma vs original (character overlap):", spearman(col("gemma", "text"), old_t),
          "| clip vs original:", spearman(col("clip", "text"), old_t))
    print("  picture  gemma vs clip:", spearman(col("gemma", "image"), col("clip", "image")),
          "| gemma vs original (perceptual hash):", spearman(col("gemma", "image"), old_i),
          "| clip vs original:", spearman(col("clip", "image"), old_i))
    print("  cap~pic  gemma vs clip:", spearman(col("gemma", "cap_img"), col("clip", "cap_img")))


if __name__ == "__main__":
    main()
