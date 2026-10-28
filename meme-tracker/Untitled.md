# Research focus v3: meme evolution (updated Oct 21, 2026)

Status: Charlotte's main focus. Builds on the meme-tracing direction (Oct 5) and the Oct 7 feedback (`claude/advisor-feedback.md`). Working case: the "Leaked photo of heaven is going viral" meme (X → Bluesky, Jan 2025). Details and data are in `NOTES.md` in the IS folder. Framework figure: "Meme Evolution Design Space" artifact + `design-space-table.png` (rows = how the story evolves over time; columns = platforms and languages, US | CN).

## Oct 21: RQ1 refined: two layers (objective + interpretive)

**RQ1.** As a meme spreads, which versions repeat, reuse as a template, comment on, invert, or leave behind the original, and what information (source, date, AI status, image) is lost along the way? How do these patterns relate to how the version is linked (repost, quote, reply), when it appears, and who posts it?

### Layer 1: Objective structure (automatic, from the API)

|Measure|What it is|How|
|---|---|---|
|Link type|repost / quote / reply / unlinked copy (same caption, no link) / links to another copy|Bluesky API fields; text search for unlinked|
|Depth (hops)|steps from the original (quote of a quote = 2)|parent chain|
|Time since origin|hours from the original post (and from the X origin)|`createdAt`|
|Account tier|follower count (log tiers), verified, account type|`getProfiles` + bio coding|
|Engagement|likes, reposts, quotes, replies (normalized by followers)|API counts|
|Image change|same image / edited / new image|perceptual hash (Hamming distance)|
|Content distance|distance from the original and from the parent|EmbeddingGemma 2 (image + caption), 1 − cosine|

### Layer 2: Interpretive (coded: LLM draft + human check, report κ)

Conclusion split into **frame** (how it says it, e.g. "a leaked photo is going viral") and **content** (what it says, e.g. "this is heaven").

||**Content kept**|**Content changed**|
|---|---|---|
|**Frame kept**|**Repeat**: reshares as-is ("omg this is heaven")|**Template**: keeps "leaked photo of heaven is going viral", swaps in a new picture (Type B)|
|**Frame changed**|**Comment**: talks about the original itself ("this is obviously AI", "who took this?") (Type A debates)|**New meme**: both changed; only a loose link remains|

Special cases: **Invert** (frame kept, content flipped to its opposite, e.g. the red "Hell" version; a sub-type of Template) and **No clear conclusion** ("lol", emoji only).

Information units (kept / lost per version): source/author, date, platform frame (X screenshot), claim, AI status, original image.

Compare each version with the **original** (how far from the start) and with its **parent** (how much this step changed → find turning points).

Hard cases: irony (same words, opposite meaning → human check), image-only posts, multiple conclusions (code the main one).

### Combining the layers (example questions)

- Do quotes produce more Templates while replies produce more Comments?
- Are Templates the versions that drop source and AI status?
- Do later or deeper versions become New memes more often?
- Are Inversions posted late (cf. Guerra et al. 2017: late reshares are more often antagonistic)?
- Does a turning point follow a post by a large account?

## Oct 14 update (Charlotte's decisions)

1. **"Conclusion" replaces "intention".** Intention is subjective; code what each post concludes instead (now refined above as frame × content).
2. **AI: case-based ("以点为主"), not spread over time.** AI-made versions; AI remakes of older memes (`ai_remake`); people asking/answering with AI in threads (e.g. Grok on X).
3. **Account profile replaces "professional creator".** Account type and size: big / small (follower tiers), official / brand / media / individual, verified, bio. Question: power.
4. **Two possible outcomes (may combine):** A. meme lookup tool (input a meme → story + trace map); B. power map (who shapes a topic's narrative, e.g. 2024 politics). Combined: A's map coloured by account power.
5. **Process:** outcomes + ~12-meme dataset (heaven = deep case) → pipeline → user test with 6–12 Bluesky users → CHI 2027 SRC (due Jan 21, 2027 AoE).

## Research questions (draft, Oct 21)

- **RQ1 Conclusion drift** (above).
- **RQ2 Roles of AI:** What roles does AI play as a meme evolves (maker, remaker, interpreter), and how does each redirect it?
- **RQ3 Account power:** Are conclusions introduced by large or official accounts more often taken up by later versions?
- **RQ4 Design (proposed, not yet confirmed):** Does a trace map help people understand where a meme came from and how its meaning changed?

## Meme selection types (Oct 21, Charlotte)

1 AI-generated content → meme · 2 photo later remade with AI · 3 news → meme · 4 cross-platform · 5 cross-language (Chinese/English) · 6 political (2024 election) · 7 influencer/official original vs. media reshare · (suggested) 8 revival of old content without its date · 9 human-only control. Candidates under consideration (unverified): heaven (1, 4); Jensen Huang (2); "They're eating the dogs" (2, 3, 6, 7); Xiaohongshu "TikTok refugees" (4, 5); Fukuyama/El País recirculation (3, 8).

## Outlook: cultural AI

Brinkmann et al. 2023 "Machine culture" (AI changes variation, transmission, selection); Farrell, Gopnik, Shalizi & Evans 2025 (_Science_): large models as cultural and social technologies; homogenization vs. fragmentation; power shifts "towards those who can fully deploy these technologies"; Daryani et al. 2026 "The Homogenizing Engine". (Abstract/author-page level; check full texts before citing.)

## Things to watch

- **The user test needs IRB.** Submit by early November.
- **12 memes is a lot by January.** Heaven = deep case; ~6 automated Bluesky memes + ~6 hand-collected cases.
- **Politics (outcome B)** is sensitive: aggregate by account type, not named individuals.