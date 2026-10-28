# Meme Tracker

Tracing how a meme changes as it spreads: what each version keeps, adds and loses, where AI comes in, and whose accounts steer it.

Independent study by Charlotte Lyu, MS Design Technology, Cornell Tech (Fall 2026). Advisor: Max Kreminski.

**Deep case:** the "Leaked photo of heaven is going viral on social media" meme. A likely AI-made image travelled from X to Bluesky in January 2025, then was quoted and replied to hundreds of times, mostly as a template ("leaked photo of heaven" + a new picture).

## Research questions

- **RQ1 Conclusion drift.** Which versions repeat, reuse as a template, comment on, invert, or leave behind the original, and what information (source, date, AI status, image) is lost along the way? How does this relate to how a version links (quote, reply, repost), when it appears, and who posts it?
- **RQ2 Roles of AI.** What roles does AI play as a meme evolves (maker, remaker, interpreter), and how does each redirect it?
- **RQ3 Account power.** Are conclusions introduced by large or official accounts more often taken up by later versions? (Measured first as adoption rate; a power map is planned.)

Details and the codebook: [`project-docs/research-focus-v3.md`](project-docs/research-focus-v3.md). Running log of decisions and findings: [`NOTES.md`](NOTES.md).

## The three views

All three pages share a **Story · Timeline · All quotes** switch at the top.

| View | File | What it shows |
|---|---|---|
| **Story** | `demo.html` | 27 hand-picked versions, step by step (RQ1 + RQ2). Sort them by conclusion (frame × content), picture change, where "heaven" goes, timing, AI's role or account size; a chart of caption drift vs. picture drift; switchable drift layers. |
| **Timeline** | `lenses.html` | The same 27 versions on one shared timeline, one row per question, grouped by RQ1–RQ3: *when* each kind of change happens. |
| **All quotes** | `chain_viewer.html` | The entry post and all 625 collected quote posts on one map: time × depth, with each post's chain and drift scores. |

## Run it locally

The pages are **not hosted online**: they run on your own computer. They also read data files that are **not in this repo** (see [Data and ethics](#data-and-ethics)), so on a new computer build the data first (below).

1. Open a terminal in this folder and start the local server:

   ```bash
   python scripts/serve.py
   ```

2. Wait for the line `Serving this folder at http://localhost:8000/demo.html`.
3. Open **http://localhost:8000/demo.html** in your browser. Use the switch at the top for the other two views.
4. Keep the terminal open while you browse. `Ctrl+C` in it stops the server.

**The page won't open?** The server isn't running: do step 1 again. If it says "Port 8000 is already in use", a server is already running in another terminal; use that one, or stop it with `Ctrl+C` first.

(`serve.py` is like `python -m http.server`, but it stops the browser from showing old cached copies.)

## Data pipeline

Python 3.12. Run from this folder, in order:

| Step | Command | Output |
|---|---|---|
| 1. Quote posts + images | `python scripts/fetch_quotes.py` | `data/quotes_all.json`, `data/images/` |
| 2. Replies | `python scripts/fetch_replies.py` | `data/replies_all.json` |
| 3. Unlinked copies (text search) | `python scripts/fetch_independent.py` | `data/independent_all.json` |
| 4. Hand picks (links in `data/my_picks.txt`) | `python scripts/fetch_picks.py` | `data/picks.json` |
| 5. Data for All quotes | `python scripts/build_chain.py` | `data/chain_data.js` |
| 6. Data for Story + Timeline | `python scripts/make_demo.py` | `data/meme_chain.json/.js` |
| 7. Embedding drift layers (optional) | `.venv\Scripts\python scripts\embed_drift.py demo` and `... all` | `data/layers/` |

Steps 1–4 use the public Bluesky API (`public.api.bsky.app`, no login).

**Hand coding** lives in [`data/demo_notes.json`](data/demo_notes.json): which versions appear in the Story, kept / added / lost, conclusion (RQ1), information units and other facets. Edit it, then re-run step 6 and refresh the page.

**Drift layers (step 7)** compare each version with the entry post (drift = 1 − cosine similarity), with [EmbeddingGemma 2](https://huggingface.co/google/embeddinggemma-2) (caption and picture in one shared space) and CLIP ViT-B/32 as the baseline. The original simple scores (character overlap, perceptual hash) are kept as their own layer. Step 7 needs a separate environment with PyTorch:

```bash
python -m venv .venv
```
```bash
.venv\Scripts\python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```
```bash
.venv\Scripts\python -m pip install "sentence-transformers[image]" transformers
```

## Status

Work in progress. The conclusion codes and information units in `data/demo_notes.json` are a **first draft** (LLM-assisted) and still need a human check and a second coder (κ). Treat the patterns in the pages as leads, not findings, until then.

## Data and ethics

Public does not mean consented. This repo holds code and hand coding only. Collected posts, images, profile bios, screenshots and model scores stay local (see `.gitignore`) and are rebuilt with the scripts above.

- Handles are shown in the pages for research use; set `SHOW_HANDLES = false` in `demo.html` and `lenses.html` before sharing anything publicly.
- Some authors have asked Bluesky not to show their posts outside the app; public outputs should respect that.
- An IRB application for the study is being prepared.

## Folder

```
demo.html, lenses.html, chain_viewer.html   the three views
nav.js                                      shared view switch
scripts/                                    data pipeline + local server
data/demo_notes.json, data/my_picks.txt     hand coding and picks (everything else in data/ stays local)
NOTES.md                                    project log
project-docs/                               plans, research focus, advisor feedback (synced from the claude.ai project)
meme-tracker/                               Obsidian notes
```
