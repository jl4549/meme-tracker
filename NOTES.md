# Project notes

## 2026-10-07: first meme chain demo
**Meme chosen:** "Leaked photo of heaven is going viral on social media", a Bluesky post from Jan 14, 2025
(https://bsky.app/profile/birdrespecter.bsky.social/post/3lfor55ezxc2s). It's a screenshot of an X post with an
image that is very likely AI-generated (not confirmed), framed as a "leaked photo".
Why this one: it touches AI, lost context, a cross-platform move (X → Bluesky), and emotion all at once.

**Data (quote posts only, for now):**
- `scripts/fetch_quotes.py` → `data/quotes_all.json` + `data/images/` (public API, no login)
- 626 posts: original + 564 quotes + 48 quotes-of-quotes + 13 at depth 3. 104 have their own image.
- `scripts/build_chain.py` → `data/chain_data.js` (caption similarity via difflib, image change via perceptual hash)

**First findings (rough, auto-coded):**
- 101 quotes attached a *new* image; **73 kept the caption but swapped the picture**. The caption became a
  template ("Leaked photo of heaven is going viral" + Golden Corral, DashCon ball pit, Pikmin, Warhammer map...).
  This is the reverse of the usual meme (image fixed, text changes).
- Some chains pass the template hand to hand (original → new image → new image → new image, 3 steps).
- Replies mock the image as AI ("heaven looks a lot like shitty AI") and as bad urbanism.
- Idea for Max: once an AI image is called out, people don't stop sharing it. They turn it into a template.

**Viewer:** `chain_viewer.html`. Run `python -m http.server 8000` in this folder, then open
http://localhost:8000/chain_viewer.html

**Simple demo (front end):** `demo.html`, 19 hand-picked versions in 5 acts (claim → questioned →
template → hand to hand → long tail). Picks + kept/added/lost/emotion live in `data/demo_notes.json`
(Claude's DRAFT coding, Charlotte to check). Run `python scripts/make_demo.py` after editing it.
The full viewer `chain_viewer.html` stays as the "backend" and is linked from the demo footer.

**Charlotte's own picks (in progress, Oct 7):** she is choosing 19–20 examples herself. Links go in
`data/my_picks.txt`; `python scripts/fetch_picks.py` saves full details to `data/picks.json`.
First pick is a *reply* ("Counterpoint", 223 likes): the original image recolored red, "heaven" → "Hell",
"Christians" → "Atheists" handwritten over it. It's the first version found that edits the original image itself.
Replies were never collected (440 on the entry post), so collecting them is a to-do.

**Two types (Charlotte's framing, Oct 7):**
- **Type A, picture-based:** works on the original picture/template: edits it (red "hell" recolor), crops it
  (halfpipe zoom), forges its X frame around a new picture, re-uploads it, or argues about it (who took it? is it AI?).
- **Type B, topic-based:** keeps the sentence "leaked photo of heaven is going viral" and brings a new picture.
- A crossover exists: halfpipe zoom (A) → reply "Tony Hawk knew all along" with Skate Heaven (B).
- Replies collected too (`scripts/fetch_replies.py` → 285 replies, 19 with images; Bluesky shows 440, the rest are
  probably deleted or hidden). Most type A edits were in the *replies*, not the quotes.
- `demo.html` now has 25 versions (9 A, 15 B + original), with an Act 0 for the X origin and full post details
  (hover card + "Full post details" in each card). `SHOW_HANDLES` in demo.html hides names for public use.

**Origin (from Daily Dot Jan 16 2025, Know Your Meme Jan 17 2025; dates checked by decoding X post IDs):**
image first seen on X @six_papi, Dec 30 2024 (who made it is unconfirmed); caption added by X @pallnandi,
Jan 12 2025 (reported 6.9–7.1M views); Bluesky entry post Jan 14 2025.

**Oct 7, later: beyond A/B**
- Charlotte: A/B should be *some* of the categories, not the only ones. Proposed 8 lenses (all in demo.html,
  "Other ways to sort"; codes are Claude's draft in `data/demo_notes.json` → `facets`):
  A/B type · how it links · builds on (picture / sentence / X-post frame / another version's joke) ·
  does to the picture (keeps, re-uploads, edits, crops, swaps inside frame, replaces) · stance (plays along,
  makes it personal, calls out AI, questions source, inverts, reframes religion, ...) · heaven becomes
  (real place, game/film world, cozy/cute, hobby/treat, another meme, hell, pun) · when · reach.
- **Correction: the "entry post" was not first.** `scripts/fetch_independent.py` (text search, day by day)
  found the sentence on Bluesky from Jan 13 21:05 UTC, 10.7 h before birdrespecter. Earliest found
  (fernballew) is *already a parody* (caption typed out + a Great Lakes map). A second separate screenshot
  entry (geftokingmongoose, 1,672 likes, 188 quotes) is a whole second tree, not yet collected.
- Link types counted: like 4,591 · repost 430 · quote 625 (61 deeper than 1) · reply 285 (up to 9 deep) ·
  separate posts with no link 129 · posts linking to *another* copy 122 · X screenshots (by eye only).
  Text search misses posts that only carry the sentence inside an image.
- Timeline in demo.html: posts per hour (first 3 days) + per month after, colored by link type,
  with the 27 story versions as markers.

**Oct 14: five research lenses page (`lenses.html`)**
- Charlotte's five lenses, each a row on one shared timeline (first 48 h linear, then compressed):
  information lost by intention · topic drift · relation to the original · AI contribution · professional creation.
- **The earliest Bluesky version (fernballew, Great Lakes map, Jan 13 21:05) is from an account whose bio says
  "Contributor at @theonion".** Bio is current (Oct 2026) and self-described: verify before claiming.
  Other big accounts are writers/podcasters by bio (e.g. the 316k account: WGAE member, podcast host).
  Bios saved to `data/profiles_bio.json` (not in git).
- Lost by *every* version: who made the image and when the X post was made.
- The two versions that call it AI got 4 and 3 likes and were never quoted (lead only, n=2).

**Not done yet / next:**
- Pure reposts (who + followers) and independent re-posts found by search (type ① and ③).
- Hand-code `is_ai_generated`, `emotion`, and `added/kept/lost` for 10–20 key versions.
- Replace simple drift with sentence embeddings + CLIP.
- Find the original X post / image creator.

**Ethics:** `data/` holds public handles and images. Keep it local; don't publish the viewer as is. Ask Max about IRB.

## 2026-10-07 (evening): main focus going forward (Charlotte)
Six questions, each mapped to data we already have or need. This replaces the 5 questions in CLAUDE.md as the main track.

1. **Information missing, by intention.** Which parts of the original (claim, source, AI status, the X frame) get dropped,
   and does that depend on *why* people post (plays along / calls out AI / inverts / personal / promo...)?
   Data: `stance` facet × `kept`/`lost` codes in `data/demo_notes.json`. Needs hand-coding for 20–30 versions.
2. **Topic change.** How far "heaven" drifts (real place → game world → hobby → hell → another meme).
   Data: `heaven becomes` facet + caption/image embedding distance from the original (EmbeddingGemma 2; CLIP baseline).
3. **Timeline.** Are later posts less related to the original? Does emotion/affect, engagement, or stance change with time?
   Data: `createdAt` → hours since the X origin (Jan 12 2025) and since the Bluesky entry; plot drift, likes and stance vs. time.
   We already have timestamps for 625 quotes, 285 replies and 129 independent posts. Watch out: early posts get more exposure, so control for that.
4. **AI contribution.** The image is likely AI (unconfirmed). Track: versions that are AI-made or AI-edited, posts that *call out* AI,
   and whether calling it out changes how it spreads (the "called out → becomes a template" idea).
   Data: `is_ai_generated` (hand-code, null if unsure) + "calls out AI" stance.
5. **Relation to the original.** Direct (quote, reply, repost) vs. indirect (same sentence with no link, links to another copy,
   X screenshot) vs. topic-only. Ties to the Oct 7 feedback point 4 (unlinked memes with the same topic/caption).
   Data: link-type counts already in the notes; embeddings needed for topic-only matches.
6. **Professional meme creation.** Satire outlets and comedians (e.g. The Onion, comedy writers) vs. ordinary users:
   do pros keep more context, change the topic more, get more reach? **To do:** check whether any pro/verified comedy accounts
   appear in our heaven data; if not, pick a pro-made meme as a second case (not chosen yet, nothing verified).

Next: add a `time_since_origin` field and an `is_professional` flag to the data; hand-code `stance`, `kept/lost`, `is_ai_generated`
for 20–30 versions; then one chart per question in demo.html.

## 2026-10-14: direction update (Charlotte)
Full version in the claude.ai project: `claude/research-focus-v3.md` (+ timeline in `claude/weekly-plan.md`).
1. **Conclusion replaces intention** (intention is too subjective). Code each post's one-sentence conclusion and its relation to the
   original's conclusion: same / extends / shifts topic / contradicts / unrelated. Measure with NLI (entail/neutral/contradict) + embeddings; LLM draft + human check, report kappa.
2. **AI = case-based (以点为主), not spread over time.** People interacting with AI (e.g. Grok in threads), AI-made versions, and
   **AI remakes** (an older meme re-created with AI in a new direction; code `ai_remake`).
3. **Account profile / power replaces "professional creator".** Account type (official / brand / media / individual), follower tier, verified, bio.
4. **Two possible outcomes:** A. meme lookup tool (input a meme → story + trace map); B. power map (who shapes a topic, e.g. 2024 politics). May combine: A's map coloured by B's account power.
5. **Process:** outcomes + ~12-meme dataset (heaven = deep case) → pipeline/model → user test with 6–12 Bluesky users (**needs IRB**) → CHI 2027 SRC (due Jan 21 AoE; plan to submit Jan 19).
Also new: `design-space-table.png` (framework figure: rows = evolution over time, columns = platforms/languages).

## 2026-10-21: embedding drift with EmbeddingGemma 2 (CLIP baseline), saved as layers
- `scripts/embed_drift.py` scores posts with **EmbeddingGemma 2** (`google/embeddinggemma-2`, Apache 2.0, text + image in one
  768-d space) and **CLIP ViT-B/32** as the baseline. Drift = 1 − cosine to the entry post. Gemma also gives a joint
  caption+picture drift; both give a caption↔own-picture match.
- **Layers, not overwrites (Charlotte):** the original data and simple scores (`meme_chain.json`, `chain_data.js`) are only read.
  Each model's scores are a separate file: `data/layers/{demo,all}_{gemma,clip}.json/.js`.
  demo.html (27 versions) has a "Drift layer" switch above the versions; chain_viewer.html (all quotes) has a "Drift layer" menu
  that changes the side-panel numbers and the up/down position in the map. Default layer = Original (simple).
- Setup (once): `python -m venv .venv`, then torch + torchvision (CUDA 12.8 wheels), `sentence-transformers[image]`, `transformers` (5.20.2 worked).
  Run: `.venv\Scripts\python scripts\embed_drift.py demo` and `... embed_drift.py all` (about a minute each on the laptop GPU).
- Results, Spearman rank agreement:

  | | demo (27) | all quotes (626) |
  |---|---|---|
  | caption, Gemma vs CLIP | 0.87 | 0.73 |
  | caption, Gemma vs character overlap | 0.87 | 0.63 |
  | picture, Gemma vs CLIP | 0.83 | 0.98 (inflated: most posts show the quoted original, drift 0) → **0.69** on the 101 posts with a new picture |
  | picture, Gemma vs perceptual hash | 0.52 | 0.72 → **0.09** on the 101 new pictures |
  | caption↔picture, Gemma vs CLIP | 0.53 | 0.56 |

  On new pictures, the hash and the models measure different things (pixel layout vs meaning). Character overlap overstates drift
  for short rewordings ("Who took it?": 0.89 vs Gemma 0.19). Median Gemma caption drift: kept 0.00, edited 0.06, new 0.29.
  In the demo set the original caption fits its own picture best under Gemma (0.75; swaps 0.51–0.60); CLIP doesn't separate it.
- Caveats: different scales per model (compare ranks, not raw values). Many pictures are X screenshots with the caption *inside*
  the image, so picture scores may partly read that text. No task prompts used (model card says try with and without).

## 2026-10-28: folder reorganized
Root was getting cluttered with loose PDFs/docx/pptx. Moved, nothing in `data/`, `scripts/`, or the HTML viewers
changed, so nothing breaks:
- `literature/`: the 5 reference PDFs + `specialization/Design Space.pdf` (that folder is gone now).
  Deleted one exact duplicate (`The Time Dimension of Visual Journalism...pdf` = `Aker_2026_...pdf`, same hash).
- `earlier-direction/`: both `Independent_Study_Proposal*.docx` (the two drafts differ — **check with Charlotte
  which is current**) and `Research_Design_Discussion.pptx`.
- `figures/`: `design-space-table.png`, `Leaked Photo of Heaven-screenshot.png`, `Meme_Storyboard_and_Workflow.pdf`
  (her own storyboard, not a reference paper).
- `.gitignore`: screenshots/papers rule was root-only (`/*.png`) and would have stopped ignoring the PNGs once
  moved into `figures/`; changed to `*.png` (any folder) and added `*.doc` to cover the new IRB template file.
- Not moved: `meme_candidates.xlsx`, `IRB consent template - social-behavioral.doc` (both current/active),
  `meme-tracker/` (Obsidian vault, self-contained, left alone).
- `project-docs/*.md` still say `design-space-table.png` "in the IS folder" — those are auto-synced from the
  claude.ai Project, not hand-edited here, so the path note there is stale until the next sync.

## 2026-10-28: research questions fixed to the v3 wording (Charlotte)
Use the wording in `project-docs/research-focus-v3.md` (not the Week 9 meeting agenda version):
- **RQ1 Conclusion drift:** which versions repeat, reuse as a template, comment on, invert, or leave behind the original; what
  information (source, date, AI status, image) is lost; how this relates to link type, timing and who posts it.
  Coded as frame × content (Repeat / Template / Comment / New meme; + Invert, No clear conclusion).
- **RQ2 Roles of AI:** maker, remaker, interpreter, and how each redirects the meme. Case-based.
- **RQ3 Account power:** are conclusions introduced by large or official accounts more often taken up by later versions?
  For now measured as **adoption rate**. Charlotte is still thinking about the broader *power structure* angle
  (who quotes whom / credit vs. attribution / who sets turning points): undecided.
- RQ4 (design) is still only proposed.
Page review against these RQs (no changes made yet): keep the objective parts (link type, timeline, drift layers, chain map);
replace stance/intention with the 2×2 conclusion type; turn kept/added/lost into 6 fixed information units; hide emotion;
lenses.html needs the most work (rows → RQ1 conclusion / content / link, RQ2 AI roles as case cards, RQ3 account power).
**Later Oct 28: lenses.html rebuilt around RQ1–RQ3 (Charlotte: demo ≈ RQ1 + RQ2 expanded; no power map yet; keep the timeline idea).**
- Same shared timeline, rows now grouped under RQ headers:
  RQ1 → What it concludes (2×2) · Where the content goes (heaven becomes) · How it links;
  RQ2 → Where AI appears (only "maker" exists in this meme; remaker/interpreter need other cases);
  RQ3 → Who posts it (follower tiers; bio type in hover). Adoption rate + power map still to come.
- Squares under each picture = 4 information units: X poster visible · claim kept · original image shown · says it is AI.
- **Draft conclusion codes** (Claude, Oct 28) in `data/demo_notes.json` → `facets.conclusion`: Template 15, Comment 8, Invert 2,
  Repeat 1 (the entry post repeats the X post), New meme 1 (Skate Heaven). Also a "Conclusion (RQ1)" button in demo.html.
  Charlotte to check, especially: second entry point (comment vs repeat), halfpipe zoom (comment vs new meme), Skate Heaven.
- To check: the red "Hell" recolor shows "X poster: lost" (from the old KEEP_POSTER list), but its notes say the X screenshot layout was kept.
**Later Oct 28: page review applied (Charlotte: "use your keep/change/drop list").**
- Roles now: **demo.html = RQ1 + RQ2 in detail** (one card per version) · **lenses.html = the time view** (when each kind of change
  happens; RQ1 conclusion + content, RQ2 AI, RQ3 who posts) · **chain_viewer.html = all quotes** (objective layer). Power map: later.
- `data/demo_notes.json`: new `units` per version (6 information units, draft: creator, date, x_frame, claim, image, ai_status;
  1 / 0.5 / 0). demo cards show them as an "Info" row; lenses draws 4 of them (creator and date are lost by all). Replaces the
  hard-coded lists that were in lenses.html.
- demo cards: conclusion tag next to TYPE A/B; emotion label hidden (data kept). Sort buttons "Stance" and "Builds on" removed
  (data kept; replaced by "Conclusion (RQ1)").
- lenses: "How it links" row removed (demo already has the link section + timeline by link type).
- Kept the act structure (A edits / A talks / B…) for now: re-ordering the story by the 2×2 should wait until the conclusion codes are checked.
- Fixed: chain_viewer link text "19-step" → "27-version"; build_chain.py docstring file name.
**Later Oct 28: demo.html reorganised for viewers (Charlotte).**
- Order now: chain at a glance → **Ways to sort** (moved up, opens on "What it concludes" shown as the 2×2: frame kept/changed ×
  content kept/changed, Invert inside Template) → **new chart "Do the words drift, or the picture?"** → timeline →
  **"How a post can link" folded** (click to open) → the cards. Sort buttons carry RQ1/RQ2/RQ3 tags; new "AI's role" (RQ2) sort;
  "Account size" uses the same 4 tiers as lenses.
- Chart: x = caption drift, y = picture drift (follows the drift layer; own layer buttons), dots coloured Template / Comment / other
  (other = labelled). Entry post = ring at (0,0). Table view underneath. Versions with no caption (2) are left out.
- What it shows (EmbeddingGemma 2): Templates top-left (same words, new picture), Comments lower-right (new words, mostly same picture).
  **Caution: partly circular.** The conclusion codes were drafted partly from the same signals (caption kept? new picture?), so the
  separation is expected by construction. It becomes evidence only once the codes are checked by hand (ideally by a second coder, κ).

## 2026-10-28: new feedback on the website (logged in project doc `advisor-feedback.md`)
1. Human evaluation vs. embedding drift: worth doing (also breaks the circularity of the drift chart). Raters outside the team → IRB by Nov 8.
2. A map focused on how each version evolves (step vs. its parent, not only vs. the original).
3. **Next focus:** does the pipeline work for other memes? Hard-coded heaven root in embed_drift.py, fetch_replies.py,
   fetch_independent.py (search phrases), make_demo.py; demo_notes.json is hand-written. Need a per-meme config + LLM-draft coding.
4. Meme-template libraries: known templates help spreading; heaven already has "unbothered. moisturized." (step 12) and a
   4-panel reaction template (step 16). A template could be its own cluster to study.
