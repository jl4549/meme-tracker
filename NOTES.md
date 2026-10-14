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
