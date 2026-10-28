<!-- Synced from claude.ai Project "independent study" (claude/weekly-plan.md). Edit it there; this copy is overwritten on each sync. -->

# Weekly plan — Tracing Authorship

Updated: Wednesday, Oct 14, 2026 (Week 8 of the 14-week schedule, Oct 12 – Oct 18)

## Where this week sits

Direction (Oct 5/7): **meme evolution tracing** on Bluesky (automated core) + hand-collected case studies on X, Instagram and Chinese platforms; framed as cultural AI / cultural memes; EmbeddingGemma 2 for embeddings (CLIP baseline). Relay study (`claude/research-direction-v2.md`) is a possible complement. Advisor notes: `claude/advisor-feedback.md`. Focus questions: `claude/research-focus-v3.md`.

**Oct 14:** new design-space map (rows = how the story evolves over time; columns = platforms and languages, US | CN). Published as the "Meme Evolution Design Space" artifact; a PNG of the table is `design-space-table.png` in the IS folder. **Bring it to Max this week.**

**Oct 14 decisions (details in `claude/research-focus-v3.md`):** "conclusion" replaces "intention"; AI studied as case-based interactions (incl. AI remakes), not spread; "account profile / power" replaces "professional creator"; two possible outcomes: **A. meme lookup tool** (input a meme → story + trace map) and **B. power map** (who shapes a topic's narrative, e.g. 2024 politics), possibly combined. Process: outcomes + ~12-meme dataset → model/pipeline → user test with 6–12 Bluesky users → CHI SRC paper.

**Target: CHI 2027 Student Research Competition (SRC), due Thu Jan 21, 2027 AoE (= Fri Jan 22, 7:59 AM New York time). Plan to submit Jan 19.**

**Next week (Week 9, Oct 19–25) is the milestone meeting with Max on study design.**

## Carry-overs from last week (check what is still open)

- Bluesky API access (needs Admin settings -> Capabilities: allow `public.api.bsky.app`, `bsky.social`, `huggingface.co`).
- Coffee-chat email to an industry contact (template from Oct 5).
- Portfolio website (needs CV / old portfolio in the IS folder).
- Ask Max about IRB: public posts **and now the user test** (human participants → IRB needed).

## LITERATURE REVIEW — dedicated time this week

1. **Tue, 1 hr — core meme reading:** Zannettou et al. 2018, Shifman 2014, Chang et al. (Generative Memesis), Wu et al. IUI 2025, Monroy-Hernández et al. CHI 2011. Notes into `claude/meme-tracing-literature.md`.
2. **Thu, 1 hr — in-folder PDFs + library items:** verify the Matich et al. (2026) dimensions; skim Aker (2026). Get Anderson et al. 2014 ("Nasty Effect", DOI 10.1111/jcc4.12009) via Cornell library; the full text couldn't be read online.

Output by Friday: a half-page "what the literature says / the gap we fill" paragraph. **This becomes the Related Work section of the SRC paper.**

## Suggested shape of the week

- **Wed (today):** Design-space map done; Oct 14 decisions recorded.
- **Thu:** Weekly check-in with Max: show the design-space map and the two outcomes; **ask about CHI SRC** (single author, advisor can't be a co-author) and **IRB for the user test**. **Literature block 2.**
- **Fri:** Draft the list of ~12 candidate memes. Try EmbeddingGemma 2 on the heaven chain. Prep a one-page agenda for the Week 9 meeting.

## CHI 2027 SRC timeline (working back from Jan 21)

Facts (checked Oct 14 on chi2027.acm.org): master's students eligible; **single author only, advisor cannot be a co-author**; initial submission up to 5 pages single-column ACM template, not anonymized, excluding references; proof of enrollment = school affiliation document or signed note from a faculty member; if accepted, presenter needs ACM student membership and CHI registration (Pittsburgh, May 10–14, 2027). Notification Feb 18, 2027. One track per submission.

Paper shape: framework (design-space map) + dataset of ~12 memes (heaven = deep case, others lighter) + pipeline/tool (outcome A, with power colouring from B) + user test (6–12 Bluesky users).

**Biggest risk: IRB for the user test.** If approval isn't in by mid-December, the paper reports dataset findings + tool design, and the user test becomes a small pilot or future work.

| When | Research / build | Writing |
|---|---|---|
| **Wk 8** (Oct 12–18) | Decide the two outcomes; draft ~12-meme list | Confirm SRC + ask about IRB with Max |
| **Wk 9** (Oct 19–25) | Milestone meeting: lock outcomes + meme list. Codebook v1: conclusion relation, account type/tier, AI case types (incl. `ai_remake`). **Start IRB application** | One-paragraph research question + contribution |
| **Wk 10** (Oct 26–Nov 1) | Collect data for all memes (reuse heaven scripts). Conclusion coding on heaven: LLM draft + human check, report κ | Paper outline + planned figures |
| **Wk 11** (Nov 2–8) | Pipeline: embeddings (drift) + NLI (conclusion vs. original) + account tiers. **Submit IRB by now** | Draft Related Work |
| **Wk 12** (Nov 9–15) | Tool prototype v0: input a meme → story + trace map, nodes coloured by account power | Draft Method + data/ethics |
| **Wk 13** (Nov 16–22) | Results review with Max (milestone). Prototype v1. Recruit Bluesky users; write test script | Draft dataset findings |
| **Wk 14** (Nov 23–29, Thanksgiving) | IS final presentation. Pilot test with 1–2 people | **Draft v1 to Max** |
| Dec 1–18 | **User tests (6–12 participants, ~45 min each)**, once IRB approves | Notes per session |
| Dec 19–Jan 4 (break, lighter) | Analyze user tests (themes) | v2: add user-test findings; cut to 5 pages; polish figures |
| Jan 5–11 | — | v3: 1–2 peer readers; Max's final read |
| Jan 12–18 | Enrollment proof; PCS account | Final edits, alt text, accessibility check |
| **Tue Jan 19** | — | **Submit (2 days early)**. Hard deadline Thu Jan 21 AoE |

## Standing items

- Weekly 30-min check-in with Max.
- Ethics: public Bluesky data needs care; politics/power map → aggregate by account type, not named individuals. IRB for the user test.
- Milestones: Week 9 (study design, Oct 19–25), Week 13 (results review).
- Jan 21, 2027: CHI SRC submission.
- Spring 2027: AAP showcase (portfolio + live meme-trace installation).
