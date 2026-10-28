<!-- Synced from claude.ai Project "independent study" (claude/meme-tracing-literature.md). Edit it there; this copy is overwritten on each sync. -->

# Meme tracing: related research (Sep 30, 2026)

Supports `claude/research-direction-v2.md` (relay study). Verification level: **[abstract read]** means Claude read the abstract or summary; **[known + search]** means Claude described it from background knowledge, and a search confirmed the paper exists. Read the originals before citing.

## 1. Tracing memes computationally (from the outside, by pixels)
- **Zannettou et al. (2018). On the Origins of Memes by Means of Fringe Web Communities. IMC '18.** Uses perceptual hashing to track image memes across 4chan /pol/, Reddit, Twitter and Gab, and measures which communities seed which memes. [known + search] https://arxiv.org/abs/1805.12512
- **Moreira et al. (2018). Image Provenance Analysis at Scale. IEEE TIP.** Reconstructs "provenance graphs" (which image was derived from which) and builds datasets from Reddit r/PhotoshopBattles. The dataset is on GitHub and could supply source images or examples. [known + search] https://doi.org/10.1109/tip.2018.2865674 · https://github.com/CVRL/Reddit_Provenance_Datasets
- **Gap for us:** these infer edit chains from the finished images. They cannot see intention, prompts, or who did what. Our relay tool records these from the inside.

## 2. Meme theory
- **Shifman, L. (2014). Memes in Digital Culture. MIT Press.** Defines memes as groups of items that people create with awareness of each other, then circulate, imitate and transform. On this view, memes are multi-author chains by definition. [known + search] https://mitpress.mit.edu/9780262525435/memes-in-digital-culture/

## 3. AI + memes
- **Chang et al. (2024/25). The Meme Is the Message: Generative Memesis and AI Visuals in the 2024 US Presidential Election.** Analyzes 239,526 Instagram images. The meme format, more than AI alone, drives engagement. "Generative memesis": creation (by AI) and curation (by humans) become separate stages. [abstract read] https://arxiv.org/abs/2411.00934
- **Wu et al. (2025). One Does Not Simply Meme Alone: Evaluating Co-Creativity Between LLMs and Humans in the Generation of Humor. IUI '25.** A human–AI meme co-creation study; KTH's press release summarizes it as "AI memes funnier on average, but humans may have the last laugh." [search] https://arxiv.org/abs/2501.11433
- **Synthetic Politics: Prevalence, Spreaders, and Emotional Reception of AI-Generated Political Images on X. HT '25.** [title only] https://dl.acm.org/doi/10.1145/3720553.3746675

## 4. Credit in remix chains
- **Monroy-Hernández, Hill, Gonzalez-Rivero & boyd (2011). Computers Can't Give Credit: How Automatic Attribution Falls Short in an Online Remixing Community. CHI '11.** In Scratch, system-generated attribution was not experienced as real credit; people wanted acknowledgment from other humans. Key for our credit question: can a trace give credit? [known + search] https://dl.acm.org/doi/10.1145/1978942.1979452
- **Fiesler & Bruckman (2014). Remixers' Understandings of Fair Use Online. CSCW '14.** [title only] https://dl.acm.org/doi/10.1145/2531602.2531695

## 5. Showing provenance to viewers
- **Feng, Ritchie, Blumenthal, Parsons & Zhang (2023). Examining the Impact of Provenance-Enabled Media on Trust and Accuracy Perceptions. CSCW '23.** Online experiment, N = 595, US and UK. Provenance lowered trust in deceptive (composite) images. But incomplete provenance made people distrust honest media too, and people conflated the media's credibility with the provenance's credibility. [abstract read] https://arxiv.org/abs/2303.12118
- **C2PA Provenance Labels Increase Trust in News Platforms (ICWSM 2026).** [title only] https://www.christophtrattner.info/pubs/ICWSM2026.pdf

## 6. Method precedent for the relay design
- **Serial reproduction:** Bartlett (1932); Xu & Griffiths; Langlois et al. People pass material along a chain, and the distortions reveal their biases. Our relay swaps memory for intention and AI editing. [known + search] https://cocosci.princeton.edu/tom/papers/memorybias.pdf

## Positioning (one line)
Computational work traces memes from pixels; theory says memes are multi-authored; remix research shows automatic attribution is not credit; provenance studies show that displaying process changes trust. **No one records the process and intention inside a human + AI meme chain that starts from a news photo.**
