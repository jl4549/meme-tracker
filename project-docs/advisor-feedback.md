<!-- Synced from claude.ai Project "independent study" (claude/advisor-feedback.md). Edit it there; this copy is overwritten on each sync. -->

# Advisor feedback log: Tracing Authorship / meme tracing

## Oct 7, 2026 (Week 7)

Feedback on the meme-evolution-tracing direction.

### 1. Future direction: cultural AI and cultural memes
- Frame the work around **cultural AI / cultural memes**: memes as cultural artifacts, and AI's role in making and spreading them.
- Look at **what people are interested in**: which topics, formats and emotions make a meme get picked up and remixed. Interest becomes a research question, alongside "what gets lost."
- Possible measures: engagement (likes, reposts, quotes) per version vs. its drift from the original; topic clusters that attract the most remixing.

### 2. Model: EmbeddingGemma 2 (in place of / alongside CLIP)
- Link: https://huggingface.co/google/embeddinggemma-2
- Checked Oct 7: open multimodal embedding model from Google DeepMind. Inputs: **text, images, video, audio**, alone or mixed in one input. 740M parameters. 768-dim embeddings (can be cut to 512/256/128). 100+ languages. Apache 2.0, ungated.
- Why it fits: **one model and one shared vector space for image + caption**, instead of CLIP (images) plus a separate sentence model (text). It also handles video memes and multilingual captions, which helps with point 3.
- To do: test on the demo meme chain. Embed each version (image + caption together) and plot its similarity to the original. Compare with CLIP as a baseline. Confirm Chinese caption quality, since the model card gives no Chinese-specific numbers.

### 3. Multi-platform data: X/Twitter, Instagram, and Chinese memes
- Extend beyond Bluesky: **X/Twitter, Instagram**, and possibly **Chinese platforms** (e.g. Weibo, Xiaohongshu, Bilibili, Douyin).
- Advisor flagged **likely technical difficulties** (可能有一些技术难题):
  - X: paid/closed API; automated reading is blocked. Screenshots or a small hand-collected set for now.
  - Instagram: Meta API covers only business/creator accounts you manage; public scraping is restricted.
  - Chinese platforms: login walls, anti-scraping, no open API, and network access from outside China. Hand collection is likely the only realistic route at first.
- Suggested approach: keep **Bluesky as the automated core**; add other platforms as small, hand-collected **case studies** for cross-platform and cross-cultural comparison (e.g. the same meme in English vs. Chinese contexts).
- Ethics/IRB: confirm what's allowed for each platform's public data.

### 4. Broader scope: memes not directly linked to the original post
- Currently the chain is built from direct links (quotes, reposts, replies). Future work can include memes that are **not directly connected** but share:
  - the **same topic**,
  - the **same caption / text template**, or
  - the **same image/meme but a different intention** (e.g. irony, a political stance, an ad).
- This needs **similarity search** rather than following links: embed a large pool of posts (EmbeddingGemma 2) and find near neighbours by image, caption or topic. It ties in with Zannettou et al. 2018 (meme clustering across communities) and Shifman 2014 (memes as groups of related texts).
- "Same meme, different intention" also links back to the relay study's intention labels. Intention could be coded by hand or with an LLM, then compared across versions.

### Next steps from this feedback
- [ ] Swap/add EmbeddingGemma 2 in the demo pipeline; CLIP stays as the baseline.
- [ ] Add an "interest" layer to the trace (engagement per version).
- [ ] Pick 1 Chinese meme example and hand-collect a few versions as a feasibility test.
- [ ] Draft a "related but unlinked" retrieval step (topic / caption / image similarity) as a future-work section.
