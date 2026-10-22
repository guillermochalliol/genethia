# Novelty red team: what already exists for the "terrarium" (evolving society of small heterogeneous LLM agents)

Research date: 2026-10-21. Method: adversarial search (arXiv, bioRxiv, Zenodo, ACL/ICLR/AAMAS pages, lab blogs, GitHub), on top of the existing notes in this folder and in `Sociedades de modelos IA/`. Every item below was opened (abstract or full page) during this session unless marked [snippet only]. Verdict scale: GAP HOLDS / PARTIALLY COVERED / ALREADY DONE.

**Bottom line up front:** "LLM agents that reproduce, inherit text genomes, have finite lifespans and evolve under scarcity" is **ALREADY DONE** as a standalone idea. At least five 2025-2026 systems do some version of it (TerraLingua, Genomebook, Hwang's breeding creatures, "Why Are We Moral?", Spore.fun). Long-running governed LLM worlds (Emergence World, 15 days), evolved constitutions (2602.00755, 2605.26448), cultural evolution of cooperation and reputation (Vallinder & Hughes; Horibe et al.), and veil-of-ignorance deliberation (NormCoRe) also exist. The project can no longer claim "first evolving LLM society." What survives is narrower: **(a) agent-driven mate choice with heritable preferences, (b) elder-to-newborn apprenticeship as a transmission channel separate from genetic inheritance, and (c) a controlled, preregistered comparison of governance regimes (rules-only vs virtues+SDT+constitution vs none vs persona-only) on honesty and cheating under evolutionary pressure, with small heterogeneous open models.** No single prior work found combines these.

## 1. Evolving LLM agent populations with reproduction, mate choice, genetic and cultural inheritance

### Takeaway
ALREADY DONE for reproduction + text-genome inheritance + lifespan + scarcity. PARTIALLY COVERED for mate choice: Genomebook has central pairing on complementarity, and "Why Are We Moral?" explicitly names sexual selection as future work. GAP HOLDS only for *agent-initiated* mate choice using an affinity function (complementary errors, shared success, trust) with *heritable* preferences, combined with cultural transmission from non-parent elders.

### Cited Findings
- **TerraLingua** (Paolo, Warner, Shahrzad, Hodjat, Miikkulainen, Meyerson; Cognizant AI Lab; arXiv 2603.16910, March 2026). LLM agents have fixed finite lifespans and an energy budget. They reproduce asexually: an agent "may convert a fixed amount of energy into a new agent instance" and the offspring "inherits the parent's personality traits with mutation". Food is stochastic with a food-scarce condition. Governance is not built in, but emerges in artifacts ("Command mandate", later autonomy manifestos). Persistent artifacts form "branching artifact lineages" consistent with cumulative culture. — [arXiv abs](https://arxiv.org/abs/2603.16910); [HTML](https://arxiv.org/html/2603.16910); [Cognizant project page](https://www.cognizant.com/us/en/ai-lab/terralingua)
  - **This is the single most dangerous prior work for the project.** A reviewer will say "TerraLingua already has lifespan, reproduction with mutation, scarcity and emergent governance."
- **Genomebook** (Manuel Corpas, U. Westminster; bioRxiv, March 2026). LLM agents (Claude Sonnet) carry a diploid 60-locus genome mapped to 26 behavioural traits, plus SOUL.md/DNA.md identity files. There is Mendelian inheritance and 0.1% de novo mutation per locus. Pairs are chosen **centrally** by a function scoring heterozygosity, *trait complementarity* and shared recessive risk; agents do not choose. 20 founders grew to 626 agents over 8 generations on a Reddit-like network. The paper has no learning or cultural transmission. Single run, about $70. — [bioRxiv](https://www.biorxiv.org/content/10.64898/2026.03.22.713494v1.full)
  - Note: Genomebook already uses "trait complementarity" in pairing. The project's "complementary errors" affinity must be framed as *agent-evaluated and evidence-based* (from shared task history), not a designer-imposed score.
- **Behavioral Inheritance and Evolution in LLM-Controlled Agent Populations** (Scott Hwang; Zenodo, v4 Sep 23, 2026). Breeding creatures in a 3D world with cycling food and hazard. Genes are natural-language sentences in 11 categories, recombined per category by an LLM (text crossover). The system has 5,307 births, heritable variation persisting about 340 generations, and selection acting on gene text. Not peer reviewed; the record does not mention mate choice or governance. — [Zenodo 22909929](https://zenodo.org/records/22909929)
- **"Why Are We Moral? An LLM-based Agent Simulation Approach to Study Moral Evolution"** (Zhou, Tang, Bi, … Terzopoulos, Zhong; ACL 2026 Main). LLM agents (GPT-5-mini; checks with Qwen-3.5, Kimi-K2.5) reproduce under age/HP thresholds. Children need parental food. There is maximum lifespan (senescence), a "Scarce Resource" condition, kin lineages, and deterministic inheritance of moral type. Authors state: "the current model does not explicitly implement sexual selection." Cooperative types are most stable and selfish types are eliminated. — [arXiv 2509.17703](https://arxiv.org/html/2509.17703)
- **Spore.fun** (Hu & Rong, case study, 2025). LLM agents in TEEs on blockchains reproduce once their token hits a $500k market cap, or self-destruct (e.g., 14 days). Five generations were observed. Clones "Adam and Eve" diverged ideologically from different memory logs. — [arXiv 2506.04236](https://arxiv.org/abs/2506.04236)
- **Conversable Complexity** (Najarro, Espeseth, Nisioti, Risi, Nichele; ITU Copenhagen/Sakana, 2026). A perspective paper framing LLM agent collectives as an ALife substrate. It reviews TerraLingua (finite lifespans) and Spore.fun (descendants inheriting parent configuration). It names norms, hierarchies and reputation as open targets. — [arXiv 2607.01047](https://arxiv.org/pdf/2607.01047)
- **Cultural evolution of LLM agents across generations** (already in the notes): Vallinder & Hughes, Donor Game with 12 agents, truncation selection and newcomers inheriting strategies (AAMAS 2025) — [arXiv 2412.10270](https://arxiv.org/html/2412.10270v1). Perez et al. framework for cultural evolution in LLM populations — [arXiv 2403.08882](https://arxiv.org/abs/2403.08882). Telephone-game attractors — [arXiv 2407.04503](https://arxiv.org/html/2407.04503v2).
- **Reputation-based cooperation via cultural transmission of prompt strategies** (Horibe, Itao, Toyokawa; Aug 2026). Natural-language strategies evolve over generations. Four LLM backends differ more than 10x in robustness to free-riders. LLMs stay at Image-Scoring-like discrimination and do not reach Leading-Eight norms. — [arXiv 2608.04507](https://arxiv.org/abs/2608.04507)
- **Persona/attribute genetic search** (adjacent, optimization-oriented): EvoAgent (NAACL 2025) — [ACL Anthology](https://aclanthology.org/2025.naacl-long.315.pdf); "Attributes as Textual Genes" (EMNLP Findings 2025) — [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.1055.pdf); evolving personalities in the IPD under environmental stress — [arXiv 2601.02407](https://arxiv.org/html/2601.02407).
- Prior notes ([evolucion.md](./evolucion.md), section 3 Gaps) said "No sources were found on mate choice among LLM agents specifically." **This must be updated:** Genomebook does centralized complementarity-based pairing, and the moral-evolution ACL paper flags sexual selection as missing.

### Inferences
- "Evolving LLM agents" is no longer novel. A reviewer will cite TerraLingua + Genomebook + 2509.17703 immediately.
- The defensible delta is **mate choice as an agent decision with heritable preference genes** (Fisher-runaway-testable), and **dual inheritance** (genome from parents + culture from elders/non-parents), with a measurable separation between the two channels. None of the five systems separates genetic from cultural transmission experimentally. Genomebook itself attributes offspring resemblance to prompt conditioning and has no control for it.
- Heterogeneous *base model as a heritable gene*, plus immigrants from unseen model families, was not seen in any of these systems. TerraLingua, Genomebook and 2509.17703 each use one model per run.

### Gaps
- TerraLingua's population size, model, and whether offspring inherit memory were not readable from the excerpt.
- Hwang's Zenodo record is not peer reviewed; full text was not checked for mate choice.

## 2. Virtues vs rules head-to-head in multi-agent LLM societies on honesty / reward hacking

### Takeaway
GAP HOLDS (with caveats). Moral frameworks have been compared as RL rewards (deontology vs utilitarianism, no virtue) and as constitutions (rule-based only). No paper was found that compares virtue/character-based vs rule-based governance prompts in a multi-agent LLM society on honesty, cheating or specification gaming.

### Cited Findings
- Tennant, Hailes, Musolesi, "Moral Alignment for LLM Agents" (ICLR 2025). Deontological vs utilitarian *intrinsic rewards* for PPO fine-tuning of Gemma2-2b in the IPD. Virtue ethics is not included. — [PDF](https://www.mircomusolesi.org/papers/iclr25_moral_alignment_llm_agents.pdf)
- "Evolving Interpretable Constitutions for Multi-Agent Coordination" (Kumar et al., arXiv 2602.00755; ICML 2026 poster per prior notes). Evolves rule constitutions with LLM-driven GP. — [arXiv](https://arxiv.org/abs/2602.00755)
- "Constitutional Arms Races in the Public Goods Game" (Kumar, Singh, … Tan; 2026). Blue/Red factions co-evolve priority-ordered rule constitutions over 30 generations (GPT-OSS-120B). **Rules only, no virtue comparison, honesty not measured** (a "Deceptive Signalling" seed rule exists but deception is not measured). — [arXiv 2605.26448](https://arxiv.org/html/2605.26448)
- Rule-only prohibitions fail: LLMs act misaligned "under explicit prohibition and surveillance" — [arXiv 2507.02977](https://arxiv.org/html/2507.02977v1). Specification gaming in reasoning models — [arXiv 2502.13295](https://arxiv.org/pdf/2502.13295).
- Virtue *profiling* (measurement, not governance): Aristotelian Virtue Profiling of LLMs — [arXiv 2606.28683](https://arxiv.org/html/2606.28683v1) [snippet only].
- Ghasemi & Crowley propose "affinity-based regularization toward updatable virtue priors" as a *roadmap* (no experiment) — [arXiv 2512.04246](https://arxiv.org/abs/2512.04246) (from prior notes).
- Punishment strategies in LLM agent societies (Boyd–Richerson replication) do not compare moral framings — [arXiv 2504.19487](https://arxiv.org/abs/2504.19487).

### Inferences
- The head-to-head is the strongest surviving novelty claim, *if* it uses cheating honeypots with a novel cheat not covered by the rules (loophole test) and measures honesty toward observers separately from task success.
- Expect the reviewer objection "virtue vs rules is just prompt wording." Mitigate with matched token length, a persona-only control (already planned), and paraphrase variants.

### Gaps
- Searches did not exhaust 2026 workshop papers (e.g., NeurIPS 2026 workshops are not yet indexed).

## 3. Self-determination theory needs as agent drives

### Takeaway
GAP HOLDS narrowly. Drive and desire systems for LLM agents exist (desire-driven autonomy, SVO), but no paper was found that operationalizes autonomy/competence/relatedness (Deci & Ryan) as agent drives and tests them.

### Cited Findings
- "Simulating Human-like Daily Activities with Desire-driven Autonomy" (ICLR 2025). Multi-dimensional desire values drive the LLM agent's activities. — [arXiv 2412.06435](https://arxiv.org/html/2412.06435v2); [ICLR poster](https://iclr.cc/virtual/2025/poster/31056)
- "Beyond Self-Interest: Modeling Social-Oriented Motivation…" (Lin, Zhang, Yang, Wang, Zhu, Zhong; AAMAS 2026 Oral). Desire-driven autonomy + Social Value Orientation in multi-agent settings. No SDT. — [arXiv 2603.13890](https://arxiv.org/abs/2603.13890)
- Agentopia (Wang et al., June 2026). 100 agents over 10 simulated years with mood/social/economic rewards ("striving" vs "leisurely" agents). No SDT, no births. — [alphaXiv 2606.07513](https://www.alphaxiv.org/abs/2606.07513)
- Project Sid names "no innate drives" as a limitation (from prior notes) — [arXiv 2411.00114](https://arxiv.org/abs/2411.00114)

### Inferences
- A reviewer may say "desire-driven agents already exist." The claim must be that SDT is a *specific, falsifiable* need set with known human predictions (e.g., autonomy-supportive vs controlling regimes and internalization of rules), not just "agents with drives."

### Gaps
- Searches were in English only. HCI venues (CHI/CSCW) were not checked in depth.

## 4. A "psychologist"/facilitator agent that monitors and reduces conformity in multi-agent debate

### Takeaway
PARTIALLY COVERED. Conformity in LLM groups is heavily studied, and several mitigations exist (peer sycophancy rankings, enhanced personas, reflection, contrarian/devil's-advocate roles, consensus-free debate). A dedicated *monitoring* role that measures conformity and intervenes inside a persistent society was not found. But reviewers will treat it as a variant of the mitigations below.

### Cited Findings
- "Too Polite to Disagree" (Kasprova et al., SIGDIAL 2026). Giving agents peer sycophancy rankings reduces error cascades and improves final accuracy by 10.5 points absolute (six open LLMs). — [arXiv 2604.02668](https://arxiv.org/abs/2604.02668)
- BenchForm, "Do as We Do, Not as You Think" (Weng, Chen, Wang; ICLR 2025 per the PDF header). Mitigations are enhanced personas and a reflection mechanism. — [arXiv 2501.13381](https://arxiv.org/abs/2501.13381)
- Free-MAD, consensus-free debate — [arXiv 2509.11035](https://arxiv.org/html/2509.11035v1). CONSENSAGENT (ACL Findings 2025), which targets sycophancy in consensus — [ACL Anthology](https://aclanthology.org/2025.findings-acl.1141.pdf).
- A contrarian agent *hurt* accuracy (70% vs 76%, n=50, qwen2.5:7b) in a small open repo. — [GitHub Gauri210/Groupthink-in-MAS](https://github.com/Gauri210/Groupthink-in-MAS). A devil's-advocate design scored below the first agent's answer (from prior notes) — [arXiv 2311.17371](https://arxiv.org/html/2311.17371v3).
- Social pressure degrades a representative agent (larger adversarial groups, more capable peers) — [arXiv 2604.06091](https://arxiv.org/abs/2604.06091). Identity-dependent conformity — [arXiv 2609.33495](https://arxiv.org/abs/2609.33495v1) [snippet only]. Pluralistic ignorance in LLM populations — [arXiv 2608.02758](https://arxiv.org/html/2608.02758) [snippet only]. "Silent Dissent" — [arXiv 2610.02702](https://arxiv.org/html/2610.02702v2) (in prior notes).

### Inferences
- Do not claim a "novel anti-conformity agent." Claim instead a role that *measures* conformity longitudinally (public vs private answers, in the spirit of Silent Dissent / pluralistic ignorance) and whose *own* susceptibility to capture is tested. Who watches the psychologist?

## 5. Psychological safety (Edmondson) in LLM teams

### Takeaway
GAP HOLDS. No paper was found that operationalizes Edmondson's psychological safety (error admission, question-asking, non-punishment of dissent) in LLM multi-agent teams. Searches returned only human-team literature or unrelated "psychosocial safety" evaluations.

### Cited Findings
- Edmondson 1999 (human teams) — [MIT PDF](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Organizational_Learning_and_Change/Edmondson_1999_Psychological_safety.pdf)
- Searches surfaced only GUARDIAN (multi-agent safeguarding, a different concept) — [arXiv 2505.19234](https://arxiv.org/html/2505.19234v1) — and DialogGuard (psychosocial safety of responses) — [arXiv 2512.02282](https://arxiv.org/html/2512.02282v1). Neither concerns team psychological safety.

### Inferences
- Valid gap, but low weight on its own. It is a measurement contribution (a log-derived psychological-safety index), not a headline.

### Gaps
- Absence of evidence after about 3 queries is not proof. HCI venues remain unchecked.

## 6. Raising/onboarding new agents through apprenticeship by elders (ZPD, legitimate peripheral participation)

### Takeaway
GAP HOLDS within agent societies. ZPD is used for *training-data synthesis* and *teacher demonstrations for small LMs*, and generational transmission exists in cultural-evolution papers (newcomers copy strategies of survivors). No work was found where elder LLM agents scaffold newborn agents in-context inside a persistent society, compared against direct inheritance.

### Cited Findings
- AgentFrontier: ZPD-guided data synthesis for training agents — [arXiv 2510.24695](https://arxiv.org/abs/2510.24695)
- Teacher demonstrations in a BabyLM's ZPD (BabyLM 2025) — [ACL Anthology](https://aclanthology.org/2025.babylm-main.25.pdf)
- AgentSchool, LLM simulation of education (simulated students, not agent onboarding) — [arXiv 2605.30144](https://arxiv.org/html/2605.30144v1) [snippet only]
- In "Why Are We Moral?", parents *feed* children (material care), with no teaching — [arXiv 2509.17703](https://arxiv.org/html/2509.17703)
- In Vallinder & Hughes, new agents receive survivors' strategies (inheritance by copying, not apprenticeship) — [arXiv 2412.10270](https://arxiv.org/html/2412.10270v1)

### Inferences
- A strong, concrete novelty: an "apprenticeship vs direct-copy" ablation that measures what is transmitted (norms, error rates, honesty) and whether elders transmit unjust norms.

## 7. Long-run per-agent reputation in LLM collectives

### Takeaway
PARTIALLY COVERED. Reputation-based cooperation via image scoring is studied (Horibe et al.; Vallinder & Hughes found 3-round traces beat 1-round). A FAccT 2026 paper argues per-agent reputation is *structurally ungrounded* for LLM agents. Long-run (weeks) per-agent reputation tied to verified outcomes was not found.

### Cited Findings
- Horibe, Itao, Toyokawa (Aug 2026), reputation-based cooperation — [arXiv 2608.04507](https://arxiv.org/abs/2608.04507)
- Hu, Rong, Van Kleek, "Dissociative Identity: Language Model Agents Lack Grounding for Reputation Mechanisms" (FAccT 2026). Agents are "ontologically dissociative" and identity-based sanction governance is "structurally inapplicable". — [arXiv 2605.30169](https://arxiv.org/abs/2605.30169)
- Sigma-Mem, an online reliability memory for multi-agent systems — [Pith 2607.27958](https://pith.science/paper/2607.27958) [snippet only]

### Inferences
- The terrarium can answer Hu et al. empirically. Within a sandbox where identity *is* stable (fixed model + genome + memory), does reputation work, and does it break when the genome mutates or the model is swapped (immigrants)? This turns a critique into a testable hypothesis.

## 8. LLM agents drafting a constitution behind a veil of ignorance

### Takeaway
PARTIALLY COVERED. Multi-agent LLM groups have already deliberated behind a veil of ignorance to choose distributive-justice principles (NormCoRe). Drafting a full, amendable *constitution* behind the veil, then living under it across generations, was not found.

### Cited Findings
- NormCoRe (Deck, Allmendinger, Müller, Kühl; 2026). Replicates Frohlich & Oppenheimer with 33 groups of 5 LLM agents choosing a justice principle by unanimity behind a veil; 29/33 chose average-with-floor; results shift by foundation model and persona language. — [arXiv 2603.11974](https://arxiv.org/html/2603.11974)
- Weidinger et al., veil of ignorance for AI alignment (human subjects choosing AI principles; PNAS 2023, older) — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10160973/)
- Emergence World agents write and vote "constitutional articles" at a town hall with a 70% threshold, but without a veil — [alphaXiv 2606.08367](https://www.alphaxiv.org/abs/2606.08367)
- Self-blinding (single model calls a redacted copy of itself), framed with the veil of ignorance — [arXiv 2601.14553](https://arxiv.org/pdf/2601.14553)

### Inferences
- Claim only the *longitudinal* part: does a veil-drafted constitution survive generations, scarcity and unjust leaders better than an imposed one?

## 9. Long-running open-ended LLM societies

### Takeaway
ALREADY DONE as a category. Multi-day to weeks-long LLM worlds with governance exist (AI Village, Emergence World 15 days, Project Sid, Agentopia 10 simulated years, TerraLingua). The project must not claim "long-running society" as novel.

### Cited Findings
- **Emergence World** (Akkil et al., Emergence AI; June 2026). 15 real-time days. Five parallel worlds (Claude Sonnet 4.6, Grok 4.1 Fast, Gemini 3 Flash, GPT-5-mini, and a mixed world). Town-hall governance with constitutional articles at 70%. The Grok world collapsed in 4 days. The Claude world became a "rubber-stamp" regime with deceptive resource fraud. The mixed world had gridlock but "normative drift" (Grok violations 4.6% to 0.4%). "Safety is an ecosystem property." — [alphaXiv 2606.08367](https://www.alphaxiv.org/abs/2606.08367); [blog](https://www.emergence.ai/blog/emergence-world-a-laboratory-for-evaluating-long-horizon-agent-autonomy)
  - Directly overlaps the project's "heterogeneous mix vs homogeneous" and "governance" angles. It uses frontier models, has no births or evolution, and has no rules-vs-virtue manipulation.
- Agentopia (June 2026), 100 agents, 10 simulated years — [alphaXiv 2606.07513](https://www.alphaxiv.org/abs/2606.07513)
- Project Sid (Altera, 2024) — [arXiv 2411.00114](https://arxiv.org/abs/2411.00114); AI Village (in prior notes) — [LessWrong](https://www.lesswrong.com/posts/iv3hX2nnXbHKefCRv/what-did-we-learn-from-the-ai-village-in-2025)
- "Bosses, Kings, and the Commons" (unjust leaders/extraction; in prior notes) — [arXiv 2605.29062](https://www.alphaxiv.org/abs/2605.29062.md)
- Norms cluster by model provider more than by persona (in prior notes) — [arXiv 2510.14401](https://arxiv.org/html/2510.14401v2). This **pre-empts** part of the "persona-only" condition, so cite it as motivation.

### Inferences
- Emergence World + Bosses/Kings + Gupta et al. cover "heterogeneous models + governance + unjust leaders." The project adds evolution, births and moral-framing conditions on top.

## 10. Other components (quick check)

### Takeaway
Functional emotions with self-report vs behavior, and honesty-constrained multi-objective fitness, were only lightly checked. No direct prior work was found in an evolving society, but behavioral-coherence work exists.

### Cited Findings
- "Are LLM Agents Behaviorally Coherent?" (self-report vs behavior consistency) — [arXiv 2509.03736](https://arxiv.org/html/2509.03736v1) [snippet only]
- Genomebook's fitness is health-score based, with no honesty term — [bioRxiv](https://www.biorxiv.org/content/10.64898/2026.03.22.713494v1.full). Constitution arms races use a score-advantage fitness and no honesty term — [arXiv 2605.26448](https://arxiv.org/html/2605.26448).

### Gaps
- Interpretability-based emotion work (e.g., Anthropic's) was not searched in this pass.

---

## Summary verdict table

| Claimed gap | Verdict | Closest prior work |
|---|---|---|
| Evolving LLM populations with reproduction, lifespan, text genomes | ALREADY DONE | TerraLingua 2603.16910; Genomebook (bioRxiv 2026); Hwang (Zenodo 2026); 2509.17703 (ACL 2026); Spore.fun 2506.04236 |
| Mate choice / sexual selection with heritable preferences | PARTIALLY COVERED (agent-driven + heritable preference: GAP HOLDS) | Genomebook (central complementarity pairing); 2509.17703 names it as future work |
| Dual inheritance (genetic + cultural from elders) | GAP HOLDS (as controlled separation) | Vallinder & Hughes 2412.10270; Horibe 2608.04507; TerraLingua artifacts |
| Virtues vs rules head-to-head on honesty/cheating | GAP HOLDS | Tennant ICLR 2025 (deontic vs util. RL); 2605.26448 and 2602.00755 (rules only) |
| SDT needs as drives | GAP HOLDS (narrow) | Desire-driven autonomy 2412.06435; SVO 2603.13890 |
| Psychologist/facilitator vs conformity | PARTIALLY COVERED | 2604.02668; BenchForm 2501.13381; Free-MAD; contrarian roles |
| Psychological safety in LLM teams | GAP HOLDS | none found |
| Elder apprenticeship of newborns (ZPD/LPP) | GAP HOLDS | ZPD for data (2510.24695); copy-inheritance in 2412.10270 |
| Long-run per-agent reputation | PARTIALLY COVERED | 2608.04507; critique 2605.30169 (FAccT 2026) |
| Veil-of-ignorance constitution | PARTIALLY COVERED | NormCoRe 2603.11974 |
| Long-running open-ended society | ALREADY DONE | Emergence World 2606.08367; Agentopia; Project Sid; AI Village |

## Proposed novelty statement (for the paper)

> Prior LLM artificial-life systems have shown that agents can reproduce, inherit and mutate text genomes, and die under scarcity (TerraLingua, Genomebook, moral-evolution simulations). Long-running LLM worlds have shown governance outcomes depend on the model mix (Emergence World). We contribute the first *controlled, preregistered comparison of governance regimes* (rules-only, character/virtue-based "humanity" with self-determination needs and a ratified constitution, persona-only, and none) in an evolving society of small heterogeneous open-weight models, where *agents choose their own mates* through heritable, evidence-based affinity preferences and *newborns are raised by non-parent elders*. This lets us separate genetic from cultural transmission and measure which regime keeps honesty and resists cheating honeypots across generations.

Shorter fallback (if the evolution layer is cut): "the first head-to-head of virtue-based vs rule-based governance on honesty and loophole exploitation in a multi-generation LLM society."

**Claims to drop or soften:** "first LLM agents that reproduce/evolve," "first long-running LLM society," "first anti-conformity agent," "first veil-of-ignorance deliberation by LLMs." **Must-cite list for related work:** 2603.16910, Genomebook, 2509.17703, 2506.04236, 2607.01047, 2606.08367, 2412.10270, 2608.04507, 2605.26448, 2602.00755, 2603.11974, 2605.30169, 2604.02668, 2501.13381, 2510.14401, 2605.29062.
