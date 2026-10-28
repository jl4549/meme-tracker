# CLAUDE.md — Charlotte's Independent Study: Meme Tracing

## Latest project state (auto-synced daily from the claude.ai Project)
The newest plans, decisions and advisor feedback live in `project-docs/` and are refreshed every morning. They are newer than the Oct 5 notes below; when they disagree, follow `project-docs/`.
@project-docs/INDEX.md


Context for Claude Code, carried over from a Cowork session (Sep 29 – Oct 5, 2026).

## Who / what
- Charlotte Lyu, MS Design Tech student at Cornell Tech, Fall 2026. Independent study advisor: Max Kreminski.
- She is a designer who wants to **build**. This project is also her lead portfolio piece, for a Spring 2027 AAP showcase with recruiters.
- Explain technical steps plainly. She is learning to code with you, so keep things small and runnable, and show her how to run each step.

## Research direction (current, Oct 5)
**Tracing how a meme evolves ("updates") as it spreads.** Not news-focused per se. As memes circulate, people share them without knowing the story behind them. Questions:
1. At which step is the original information first lost? What survives?
2. Do influencers make the spread explode?
3. Does the framing or trend of the same topic drift?
4. How does AI contribute (AI-generated or AI-edited versions)?
5. How do people's emotions change along the chain?

Method idea: Bluesky API (AT Protocol) for posts, quotes and reposts, plus embeddings to measure drift from the original: text (sentence embeddings) and images (CLIP).

The earlier "relay study" (designers edit a photo in a chain, logging each step and intent) is a possible complement for the "why", not the main track. **Max hasn't approved the new direction yet.**

## This week's to-do (in order)
1. **Build a small demo that traces ONE meme.**
   - Start with hand-collected data: 10–20 versions in `data/meme_chain.json`.
   - Use API-shaped fields so real data can drop in later:
     `{id, parent_id, author_handle, author_followers, createdAt, text, image_path_or_url, is_ai_generated (bool|null), quoteCount, repostCount, likeCount, added, kept, lost, emotion}`
   - The view is a simple web page (single HTML file is fine): original → versions as a tree or timeline. Clicking a step shows what was added, kept and lost, the drift score, and who spread it.
   - Candidate memes: *All Eyes on Rafah* (AI image, huge spread, analyzed in Matich et al.); the Jensen Huang AI videos (real dance → AI "confronting Dwarkesh" → AI moonwalk; X only, so screenshots); or ideally an image meme that lives on Bluesky with many quote posts.
2. **Connect to the Bluesky public API** (`https://public.api.bsky.app/xrpc/`, no auth needed for reads):
   - `com.atproto.identity.resolveHandle?handle=...` → DID
   - `app.bsky.feed.getAuthorFeed?actor=...` → find the post URI
   - `app.bsky.feed.getQuotes?uri=...` (paginate with `cursor`), `app.bsky.feed.getRepostedBy`, `app.bsky.feed.getPostThread`
   - `app.bsky.actor.getProfiles?actors=...` → follower counts (influencer flag)
   - Test post: @timhowles.bsky.social (DID `did:plc:2m3hmdeyeykqhdfr6qyllvpl`), Sep 27, 2025, sharing a 2022 El País Fukuyama interview (322 quotes, 206 reposts). It's a link post, not an image meme, but good for testing the pipeline. Note: the 2022 article was recirculated in 2025 with no visible date, which is an example of context loss.
   - Then embeddings: e.g. `sentence-transformers` (all-MiniLM-L6-v2) for text; CLIP (open_clip) for images. Drift = 1 − cosine similarity to the original.
   - Note: the Cowork cloud sandbox couldn't reach Bluesky (network policy). Running locally should work. If not, tell her.
3. Prepare notes and the demo for the weekly check-in with Max (Thursday). Ask him about IRB for public Bluesky data.
4. Also this week: a coffee-chat email to an industry person; start a portfolio website (she will add her CV or old portfolio to this folder).

## Ethics
Public does not mean consented (cf. the 2024 backlash against a scraped dataset of one million Bluesky posts). Store only what's needed, don't republish handles in public outputs without thought, and confirm IRB needs with Max.

## Files in this folder
Reorganized Oct 28, 2026: papers into `literature/`, the outdated proposal into `earlier-direction/`, visual deliverables into `figures/`. Nothing in `data/`, `scripts/` or the HTML viewers moved.

- `earlier-direction/Independent_Study_Proposal*.docx`: original proposal ("Tracing Authorship": sequence of AI edits vs. perceived photo authenticity). Now outdated in direction. Two different drafts exist (not duplicates) — unclear which is final; check with Charlotte before treating either as canonical.
- `earlier-direction/Research_Design_Discussion.pptx`: earlier design deck.
- `figures/design-space-table.png`: the "Meme Evolution Design Space" framework figure (rows = evolution over time, columns = platforms/languages).
- `figures/Leaked Photo of Heaven-screenshot.png`: screenshot of the deep-case meme's entry post.
- `figures/Meme_Storyboard_and_Workflow.pdf`: Charlotte's own storyboard of the news→meme information-loss idea and the heaven meme's branching (Oct 9), not a literature reference.
- `literature/Draftmarks.pdf`: Siddiqui et al., CHI 2026. Skeuomorphic process traces for human–AI writing (masking tape = AI insert, eraser crumb = prompt, residual glue = discarded AI text). Different readers need different trace detail. **Visual inspiration for the trace view.**
- `literature/matich-et-al-2026-...pdf`: Matich, Richardson & Burgess, *Media, Culture & Society* 48(6). Compares *90 Miles* and *All Eyes on Rafah*. An automated summary claimed authenticity works on four dimensions (provenance, symbolism, moral fidelity, affect). **UNVERIFIED: check the exact terms in this PDF before using them.**
- `literature/Aker_2026_Time_Dimension_of_Visual_Journalism.pdf`, `literature/martinez_generative_2025.pdf`, `literature/AI_Provenance_CHI_2026___Sep_10_Deadline.pdf`, `literature/Design Space.pdf`: other references or materials. Read them before relying on them.
- `IRB consent template - social-behavioral.doc`: current IRB materials (application due Nov 8, see `project-docs/weekly-plan-week10.md`).

## Key related work (for positioning)
- Zannettou et al. 2018 (IMC): tracks image memes across communities with perceptual hashing.
- Moreira et al. 2018 (IEEE TIP): image provenance graphs; Reddit PhotoshopBattles dataset (github.com/CVRL/Reddit_Provenance_Datasets).
- Shifman 2014, *Memes in Digital Culture*: memes are multi-author by definition.
- Chang et al. (arXiv 2411.00934): "generative memesis". AI generates, humans curate; meme format drives engagement more than AI; AI faces look happier and less angry.
- Wu et al. IUI 2025: human+AI meme captions are no better than human-only; AI-only is best on average, but humans make the very best; AI use lowers felt ownership.
- Chen et al. HT '25: ~12% of 2024 election political images on X were AI; 10% of users spread 80% of them.
- Monroy-Hernández et al. CHI 2011: automatic attribution ≠ credit (Scratch remixing).
- Feng et al. CSCW 2023: provenance info lowers trust in fakes, but incomplete provenance makes people distrust honest media too.
- **Gap:** existing work traces memes from the outside (pixels, finished posts). No one shows step by step what was kept, added and lost, or the role of AI and intention, in a way people can explore.

## Working style
- Small steps; get something visible early. Show her the commands to run.
- Never invent data or citations. Mark anything unverified.
- Keep the project notes up to date in `NOTES.md` (decisions, what worked, next steps).
