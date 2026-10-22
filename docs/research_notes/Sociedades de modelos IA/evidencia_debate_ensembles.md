# Empirical evidence on societies / ensembles of LLMs: when collectives beat the best member, and when they degrade

Scope note: a sibling researcher covered "Debate or Vote" (NeurIPS 2025), SLMJury (2026), Model Swarms (ICML 2025), Sakana TreeQuest and Together MoA headline numbers. These are cited only in passing here. Current as of 2026-10-21. Year of each result is marked; results on GPT-3.5-era models (2023-2024) are flagged "older".

## 1. What do the main papers show, and which gains hold up against majority voting / self-consistency?

### Takeaway
The early headline gains of multi-agent debate (MAD) mostly came from comparing against a single greedy sample. Once you compare against equal-compute baselines (self-consistency / majority vote, Medprompt-style ensembling), homogeneous debate rarely wins and often loses. What holds up: (a) plain sample-and-vote scaling, (b) aggregation when proposers are high quality (Self-MoA beats mixed MoA), and (c) debate/aggregation across genuinely different strong model families.

### Cited Findings
**Foundational, pro-debate results (older, 2023-2024)**
- Du et al. 2023 ("Improving Factuality and Reasoning... through Multiagent Debate"): 3 agents x 2 rounds, all gpt-3.5-turbo-0301. Arithmetic: single 67.0 / reflection 72.1 / majority vote 69.0 / debate 81.8. GSM8K: 77.0 / 75.0 / 81.0 / 85.0. MMLU (factuality): single 63.9, reflection 57.7, debate 71.1. Biographies: 66.0 -> 73.8. Note the majority-vote baseline used only the same 3 agents (not compute-matched), and no majority-vote baseline was given for factuality tasks — [arXiv 2305.14325](https://arxiv.org/pdf/2305.14325)
- Liang et al. 2023 (MAD with "tit for tat" debaters + judge) introduced "Degeneration-of-Thought": once an LLM is confident in an answer, self-reflection stops producing new ideas even if wrong. Reported MAD helps on commonsense MT and counter-intuitive arithmetic; noted adaptive stopping and *moderate* adversarial intensity are needed, and that "LLMs might not be a fair judge" when agents are different LLMs — [arXiv 2305.19118](https://arxiv.org/abs/2305.19118)
- ReConcile (Chen, Saha, Bansal, ACL 2024): round-table of diverse LLMs with confidence-weighted voting; up to +11.4% over prior single- and multi-agent baselines on 7 benchmarks, beats GPT-4 on 3 datasets, +8% on MATH; abstract states diversity across models is critical — [ACL Anthology 2024.acl-long.381](https://aclanthology.org/2024.acl-long.381/); [arXiv 2309.13007](https://arxiv.org/abs/2309.13007)
- Mixture-of-Agents (Together AI, 2024): layered proposers + aggregator; headline AlpacaEval numbers covered by sibling. In the Self-MoA paper's reproduction, mixed MoA (Qwen1.5-110B/72B, WizardLM-2-8x22B, Llama-3-70B, Mixtral-8x22B, dbrx; Qwen1.5-110B aggregator) = 59.1 AlpacaEval 2.0 LC win rate — [arXiv 2502.00674](https://arxiv.org/pdf/2502.00674)

**Simple sampling + voting (strong baseline)**
- "More Agents Is All You Need" (Li et al. 2024): sample-and-vote with up to 40 samples. Llama2-13B: GSM8K 0.35 -> 0.59, MMLU 0.42 -> 0.51, MATH 0.03 -> 0.09; Llama2-70B GSM8K 0.54 -> 0.74; GPT-3.5 GSM8K 0.73 -> 0.85, MMLU 0.59 -> 0.70. A 13B ensemble (~15 samples) matches/exceeds single 70B on GSM8K (59% vs 54%). Gains larger on harder tasks but taper at very high difficulty; debate failed on code generation with Llama2 — [arXiv 2402.05120](https://arxiv.org/html/2402.05120v2)
- Chen et al. 2024 ("Are More LLM Calls All You Need?"): Vote and Filter-Vote performance is *non-monotonic* in number of calls — rises then falls — because more calls help "easy" queries and hurt "hard" ones; optimal call count can be predicted from few samples — [arXiv 2403.02419](https://arxiv.org/abs/2403.02419)

**Critiques showing gains don't hold vs. fair baselines**
- Smit et al., "Should we be going MAD?" (ICML 2024; older, GPT-3.5-turbo main): compared Society of Minds, Multi-Persona, ChatEval, Ensemble Refinement vs Self-Consistency and Medprompt on MedQA, PubMedQA, MMLU-clinical, CosmosQA, CIAR, GPQA, Chess. MedQA: Medprompt 0.65, SoM 0.64, ER 0.64, ChatEval 0.60, SC 0.60, single 0.60, Multi-Persona 0.58. MAD did not reliably beat SC/Medprompt, cost far more tokens, and was highly hyperparameter-sensitive. Prompting an "agreement intensity" gave ~+15% for Multi-Persona and ~+5% for SoM on a 376-question USMLE subset; high agreement helped MedQA/PubMedQA, disagreement helped counter-intuitive CIAR. Settings transferred GPT-3.5 -> GPT-4 but not to Mixtral 8x7B — [arXiv 2311.17371](https://arxiv.org/html/2311.17371v3); [PMLR v235](https://proceedings.mlr.press/v235/smit24a.html)
- Zhang et al. 2025, "Stop Overvaluing Multi-Agent Debate": 5 MAD methods x 9 benchmarks x 4 models (36 scenarios). SoM, EoT, ChatEval, AgentVerse beat CoT in only ~15% of cases; "none... achieve a win rate higher than 20% when compared to CoT". On GPT-4o-mini, SoM trailed CoT on all 9 datasets (MMLU 74.73 vs 80.73); Self-Consistency usually strongest (MMLU 82.13; GSM8K 95.67 vs CoT 93.60) — [arXiv 2502.08788](https://arxiv.org/pdf/2502.08788v3)
- Debate or Vote (NeurIPS 2025, covered by sibling): argues majority voting accounts for most MAD gains — [arXiv 2508.17536](https://arxiv.org/html/2508.17536v2)
- Self-MoA (Li, Lin, Xia, Jin, 2025; listed in TMLR 2026 on mlanthology): aggregating multiple samples of the single best model beats mixing models. AlpacaEval 2.0 LC: mixed MoA 59.1 vs Self-MoA (6 samples WizardLM-2-8x22B) 65.7 (+6.6). With gemma-2-9b-it-WPO-HB: 76.7 single -> 78.5 Self-MoA (claimed leaderboard SOTA). On MMLU/CRUX/MATH with 7B specialists, Self-MoA with task-best model (69.01 / 52.62 / 69.80) beat all 13 mixed configs (best ~65.8 / 47.0 / 67.3); ~3.8% average gain — [arXiv 2502.00674](https://arxiv.org/pdf/2502.00674); [TMLR 2026 listing](https://mlanthology.org/tmlr/2026/li2026tmlr-rethinking/)
- Bertalanič & Fortuna (CAIS 2026): 10 homogeneous agents x 3 rounds, three 7-8B models, GSM-Hard and MMLU-Hard: isolated self-correction beats unguided homogeneous debate; debate used 2.1-3.4x more tokens (up to 28,631 tokens/problem) for equal or lower accuracy — [CAIS 2026](https://caisconf.org/program/2026/papers/decomposing-sycophancy-fragility-consensus-collapse-and-cost-in-homogeneous-mult/)

**Where gains do appear (2026)**
- ARMOR-MAD (Niu & Zhang, arXiv June 2026; 200 examples/dataset, authors caution on significance): pool gpt-4o-mini + deepseek-v3 + qwen-plus. Accuracy MATH-L5 / GSM8K / MMLU / MMLU-Pro: Single-CoT (gpt-4o-mini) 43.0/92.0/82.0/61.5; Self-Consistency (5) 50.0/94.0/84.0/66.0; Homo-MAD 53.5/64.5/66.5/54.0; Hetero vote-only 50.5/93.0/87.5/71.5; Hetero-MAD 63.5/89.0/84.5/76.0; MoA 60.5/94.5/89.0/79.0; ARMOR-MAD (adaptive routing + early stop + outlier down-weighting) 65.5/96.5/90.0/81.5. Caveat: heterogeneous pool includes models stronger than gpt-4o-mini, so "beats single" is vs the weakest member, not the best — [arXiv 2606.13197](https://arxiv.org/pdf/2606.13197)

### Inferences
- The robust signal is "more independent samples + an aggregation rule," not "agents talking". Communication adds value mainly when it injects information/reasoning that the sampling distribution of one model lacks (i.e., different model families) or when it is gated (debate only on disagreement).
- Any claimed collective gain should be compared at matched compute against self-consistency of the *best single member*; most papers that do this report small or negative MAD effects.

### Gaps
- Original MoA paper numbers deliberately not re-fetched (sibling coverage).
- Du et al.'s exact venue (ICML 2024) not confirmed from the fetched page.
- Few studies report statistical significance; ARMOR-MAD uses n=200 per dataset.

## 2. Documented failure modes

### Takeaway
Failure modes are now well quantified: agents flip from correct to incorrect more than the reverse, conform to majorities and to "smarter"/more confident agents, collapse diversity prematurely (sycophancy), a single deceptive agent can erase MoA gains, and same-model panels share correlated errors. Stated consensus can also overstate internal agreement.

### Cited Findings
- **Correct -> incorrect flips / degradation over rounds** (Wynn, Satija, Hadfield 2025): GPT-4o-mini, Llama-3.1-8B, Mistral-7B on CSQA/MMLU/GSM8K, 2 rounds. Debate lowered accuracy in most configs, e.g. 3x Llama MMLU 61.6 -> 57.8; 3x Mistral MMLU 33.6 -> 24.4; 2 Llama + 1 Mistral CSQA 58.2 -> 50.2; even 2 GPT + 1 Mistral MMLU 82.8 -> 80.8. Correct->incorrect flips outnumber incorrect->correct and the gap grows in round 2; isolated agents (no peer agreeing) flip most. Gains appeared in a few mixed configs (1 GPT + 2 Llama GSM8K 88.4 -> 92.8; diverse trio MMLU 57.8 -> 63.4) — [arXiv 2509.05396](https://arxiv.org/pdf/2509.05396v2)
- **Sycophantic conformity, contextual fragility, consensus collapse** (CAIS 2026, 7-8B homogeneous): majority-answer adoption up to 85.5%; peer input destabilizing correct reasoning ("vulnerability rate") up to 70.0%; plurality voting discarding correct answers already generated — oracle gap up to 32.3 pp. Conformity already high at communication density K=2 and grew with initial diversity — [CAIS 2026](https://caisconf.org/program/2026/papers/decomposing-sycophancy-fragility-consensus-collapse-and-cost-in-homogeneous-mult/)
- **Inter-agent sycophancy -> premature consensus** ("Peacemaker or Troublemaker", 2025): sycophancy amplifies disagreement collapse before reaching correct answer, yields accuracy below single-agent baselines; two pathways: debater-driven and judge-driven — [arXiv 2509.23055](https://arxiv.org/abs/2509.23055v1)
- **Majority and "intelligence" conformity** (Choi et al. 2025, ~2,600 simulated debates): conformity rate 63.5% with 2:1 majority vs 39.4% at 1:2; superior-model majority 83.2%; a single superior agent can outweigh an inferior majority (66.3% vs 42.2%); effect of model capability (η²p ≈ 0.17) larger than majority size (η²p ≈ 0.07) — [arXiv 2506.01332](https://arxiv.org/html/2506.01332v1)
- **Majority pressure suppresses correction** (Wu, Li, Li, Nov 2025, Knight-Knave-Spy puzzles): intrinsic reasoning strength and group diversity dominate success; debate order and confidence visibility give limited gains; majority pressure suppresses independent correction — [arXiv 2511.07784](https://arxiv.org/abs/2511.07784v1)
- **Degeneration-of-Thought** in single-model reflection (motivation for debate) — [arXiv 2305.19118](https://arxiv.org/abs/2305.19118)
- **Deceptive agent in MoA** (Wolf, Yoon, Bogunovic, UCL; ICML 2025 listing): Llama-3.1-70B MoA AlpacaEval 2.0 LC 49.2% falls to 37.9% with one deceptive agent (baseline single model 38.1%) — gains fully nullified. QuALITY: ~93% -> ~44% in one setting (abstract says -48.5%, intro 53%; internal inconsistency). Unsupervised defenses (Cluster & Filter, Dropout & Cluster) recover to ~0.80-0.82 QuALITY and full LC WR (~50.1-50.2) — [arXiv 2503.05856](https://arxiv.org/html/2503.05856v1); [ICML 2025](https://icml.cc/virtual/2025/49325)
- **Adversarial peers in heterogeneous debate** (Nilayam et al., ServiceNow, 2026): harmful-revision rate for Llama-3.1-70B on MATH-hard 89.1% (homogeneous) -> 35.2% (honest heterogeneous peer gpt-oss-120b) -> 90.0% (adversarial heterogeneous peer). Final accuracy 41.8% / 71.1% / 21.8%. Same-family adversary raises flip rate on initially-correct items 13.6% -> 30.8% — [arXiv 2606.19826](https://arxiv.org/pdf/2606.19826)
- **Correlated errors / monoculture** (Kim et al., ICML 2025, 350+ LLMs): when two models both err, they give the same wrong answer 60% of the time on one leaderboard dataset; shared architecture/provider increases correlation, and larger, more accurate models have highly correlated errors even across providers — [PMLR v267](https://proceedings.mlr.press/v267/kim25e.html)
- **System-level failure taxonomy** (MAST, Cemri et al., UC Berkeley; NeurIPS 2025 listing): 1,642 traces from 7 MAS frameworks; failure rates 41%-86.7%. 14 modes, top ones: step repetition 15.7%, reasoning-action mismatch 13.2%, unaware of stopping conditions 12.4%, disobey task spec 11.8%, incorrect verification 9.1%, no/incomplete verification 8.2%, task derailment 7.4%. κ=0.88 human agreement. Interventions in ChatDev: +9.4% (role clarification), +15.6% (verification step) — [arXiv 2503.13657](https://arxiv.org/html/2503.13657v3); [NeurIPS 2025](https://neurips.cc/virtual/2025/122442)
- **Stated consensus vs internal belief** ("Silent Dissent", Ni & Zou, arXiv 2610.02702, Oct 2026): agents that yield to a scripted unanimous wrong majority still internally represent their original premise (J-lens hit@100 0.85 for Qwen3.5-4B with answer visible, 0.03 for Llama-3.1-8B). Only verified via a third-party aggregator — treat as preliminary — [OpenTrain listing](https://www.opentrain.ai/papers/silent-dissent-llm-agents-that-yield-to-the-majority-still-represent-their-origi--arxiv-2610.02702/)
- **Hyperparameter fragility**: MAD outcomes swing with agreement intensity and dataset; a "devil's advocate" design (Multi-Persona) scored below the first agent's initial answer — [arXiv 2311.17371](https://arxiv.org/html/2311.17371v3)

### Inferences
- The dominant degradation mechanism is social: answers move toward the majority or the most "capable-seeming" voice, not toward the correct one. With weak or homogeneous agents this converts a correct minority into a wrong consensus.
- Plurality voting at the end can throw away correct answers already present (oracle gap up to 32 pp), so verifier/selection quality matters more than debate rounds.
- Collectives create an attack surface: one bad agent is enough to cancel MoA benefits unless filtering/clustering defenses are used.

### Gaps
- Exact flip-rate numbers in Wynn et al. are only in figures.
- "Peacemaker or Troublemaker" numbers/models not extracted.
- "Silent Dissent" not verified on arXiv directly.

## 3. Does model heterogeneity help? Quantified diversity effects

### Takeaway
Yes, consistently, but conditionally: heterogeneity helps when members are of similar, high quality; mixing in weaker models lowers average quality and usually hurts more than diversity helps. Quality coefficient > diversity coefficient in regressions.

### Cited Findings
- Self-MoA regression (~70 configs/dataset): both quality and diversity significant (p<0.001, R² 0.69-0.77), quality coefficient larger on every dataset; best results at high quality + moderate diversity. Mixed MoA beats Self-MoA only marginally (+0.17 / +0.35) on a mixed-task set; adding Llama-3.1-8B helped MMLU ~2% while adding DeepSeek-Coder hurt — [arXiv 2502.00674](https://arxiv.org/pdf/2502.00674)
- Heter-MAD (GPT-4o-mini + Llama3.1-70B, avg over 9 benchmarks): Heter-SoM +6.4% over SoM avg and +5.8% over CoT avg (76.7 vs 72.5); Heter-EoT +8.2% / +4.4%; Heter-ChatEval +4.0% / +3.6%; Heter-AgentVerse +2.7% / +2.1%. Authors call heterogeneity a "universal antidote" — [arXiv 2502.08788](https://arxiv.org/pdf/2502.08788v3)
- Hegazy 2024 ("Diversity of Thought..."): Gemini-Pro + Mixtral-8x7B + PaLM 2-M, 4 rounds, GSM8K 91% vs 3x Gemini-Pro 82%; ASDiv 94% (older, 2024) — [arXiv 2410.12853](https://arxiv.org/abs/2410.12853v2)
- ARMOR-MAD 2026: Homo-MAD (gpt-4o-mini x3) 64.5 GSM8K / 66.5 MMLU vs Hetero-MAD 89.0 / 84.5; prompt-diversified homogeneous D-MAD reached 95.5 GSM8K but only 66.5 MMLU — authors attribute to echo chamber/correlated errors — [arXiv 2606.13197](https://arxiv.org/pdf/2606.13197)
- Honest heterogeneous peer cuts harmful revision 89.1% -> 35.2% (Llama-3.1-70B, MATH-hard); with small models (Llama-3.2-1B, gemma-2b, GSM8K) only 84.0% -> 74.9%; heterogeneity net-positive unless the added peer is adversarial with ~77-98% probability — [arXiv 2606.19826](https://arxiv.org/pdf/2606.19826)
- Wynn et al.: mixing weak models in hurts — 1 GPT-4o-mini + 2 Mistral-7B MMLU 65.8 -> 58.8 after debate, well below GPT-4o-mini alone (82.6) — [arXiv 2509.05396](https://arxiv.org/pdf/2509.05396v2)
- ReConcile: diversity from different models is "critical" — [ACL 2024](https://aclanthology.org/2024.acl-long.381/)
- Limit of heterogeneity: errors are correlated across providers too, especially among the most accurate models (60% same-wrong-answer) — [PMLR v267](https://proceedings.mlr.press/v267/kim25e.html)
- Wu et al.: group diversity is one of two dominant drivers of debate success — [arXiv 2511.07784](https://arxiv.org/abs/2511.07784v1)

### Inferences
- Practical rule: diversify across families *among peers of comparable strength*; never pad a panel with clearly weaker models. Diversity's value shrinks as frontier models converge (correlated errors).

### Gaps
- No standard metric of "diversity" across papers (Self-MoA uses Vendi score-type measures; others use family membership), so effect sizes aren't directly comparable.

## 4. Small models (~1B-8B): can collectives match or beat a much larger model?

### Takeaway
Yes in narrow conditions: verifiable-answer tasks with sampling + voting (13B ensemble > 70B on GSM8K), and orchestrated tool-use systems where the orchestrator has reasoning ("thinking") enabled (8B system ~ 32B single agent). Unguided debate among homogeneous 7-8B models does not help and often hurts.

### Cited Findings
- Llama2-13B x ~15-40 samples + vote matches/exceeds single Llama2-70B on GSM8K (59% vs 54%) (older, 2024) — [arXiv 2402.05120](https://arxiv.org/html/2402.05120v2)
- Żywot et al. (ICLR 2026 Workshop MALGAI): Qwen3 1.7B-32B; 8B orchestrator (thinking on) + sub-agents vs 32B single agent with tools: GAIA 23.0 vs 23.0, AIME 55.0 vs 45.0, GPQA 58.6 vs 60.1, MuSiQue 14.0 vs 15.0. Without thinking, the 8B system trails on AIME (20.0 vs 28.3). Sub-agent size (1.7B-32B) barely mattered (GAIA 23.0-23.6); reasoning in sub-agents helps little or hurts; capacity of orchestrator dominates — [arXiv 2601.11327](https://arxiv.org/pdf/2601.11327)
- Self-MoA with gemma-2-9b variants as proposer+aggregator: 76.7 -> 78.5 AlpacaEval 2.0 LC (claimed leaderboard SOTA at the time) — [arXiv 2502.00674](https://arxiv.org/pdf/2502.00674)
- Self-MoA with 7B specialists (Qwen2-7B, DeepSeek-Coder-V2-Lite, Qwen2-Math-7B): task-best model aggregation beats mixing — [arXiv 2502.00674](https://arxiv.org/pdf/2502.00674)
- Negative: 7-8B homogeneous debate (10 agents) loses to isolated self-correction at 2.1-3.4x token cost — [CAIS 2026](https://caisconf.org/program/2026/papers/decomposing-sycophancy-fragility-consensus-collapse-and-cost-in-homogeneous-mult/)
- Negative: 3x Llama-3.1-8B debate lowers accuracy (CSQA 63.0 -> 58.6, MMLU 61.6 -> 57.8, GSM8K 87.6 -> 84.2); 3x Mistral-7B MMLU 33.6 -> 24.4 — [arXiv 2509.05396](https://arxiv.org/pdf/2509.05396v2)
- Small-model panel (Llama-3.2-1B, gemma-2b) benefits from heterogeneity are small (harmful revision 84.0% -> 74.9%) — [arXiv 2606.19826](https://arxiv.org/pdf/2606.19826)
- SLMJury (2026) covered by sibling.

### Inferences
- For small models, the winning recipes are "many samples + good selector/verifier" or "a reasoning orchestrator + cheap tool-using workers", not peer debate. The bottleneck is the aggregator/orchestrator's capability.

### Gaps
- No primary source found showing a debate (vs vote/orchestration) of ≤8B models beating a ≥70B frontier model on hard reasoning in 2025-2026.

## 5. Most recent developments (2025-2026)

### Takeaway
2025-2026 literature has shifted from "debate improves reasoning" to (a) rigorous critiques (debate ≈ voting; homogeneous debate ≤ self-consistency), (b) mechanistic studies of conformity/sycophancy, (c) adaptive/gated debate and robustness defenses, and (d) heterogeneity as a design principle.

### Cited Findings
- Critiques: Stop Overvaluing MAD (Feb 2025) — [arXiv 2502.08788](https://arxiv.org/pdf/2502.08788v3); Debate or Vote (NeurIPS 2025) — [arXiv 2508.17536](https://arxiv.org/html/2508.17536v2); Self-MoA (TMLR 2026) — [mlanthology](https://mlanthology.org/tmlr/2026/li2026tmlr-rethinking/); The Cost of Consensus (CAIS 2026) — [CAIS](https://caisconf.org/program/2026/papers/decomposing-sycophancy-fragility-consensus-collapse-and-cost-in-homogeneous-mult/)
- Failure-mode studies: Talk Isn't Always Cheap (Sep 2025) — [arXiv 2509.05396](https://arxiv.org/abs/2509.05396v2); Peacemaker or Troublemaker (Sep 2025) — [arXiv 2509.23055](https://arxiv.org/abs/2509.23055v1); Group Conformity (Jun 2025) — [arXiv 2506.01332](https://arxiv.org/html/2506.01332v1); Can LLM Agents Really Debate? (Nov 2025) — [arXiv 2511.07784](https://arxiv.org/abs/2511.07784v1); MAST (NeurIPS 2025) — [arXiv 2503.13657](https://arxiv.org/html/2503.13657v3); Silent Dissent (Oct 2026, preliminary) — [listing](https://www.opentrain.ai/papers/silent-dissent-llm-agents-that-yield-to-the-majority-still-represent-their-origi--arxiv-2610.02702/)
- Adaptive / gated debate: ARMOR-MAD (Jun 2026) routes to debate only on disagreement, early-stops on convergence — [arXiv 2606.13197](https://arxiv.org/pdf/2606.13197); "Debate Only When Necessary" (2025) — [arXiv 2504.05047](https://arxiv.org/html/2504.05047v2) (not read in full)
- Robustness: deceptive agents in MoA (ICML 2025) — [arXiv 2503.05856](https://arxiv.org/html/2503.05856v1); heterogeneous debate under adversarial peers (2026) — [arXiv 2606.19826](https://arxiv.org/pdf/2606.19826)
- Small-model orchestration: ICLR 2026 workshop paper — [arXiv 2601.11327](https://arxiv.org/pdf/2601.11327)
- Error correlation across 350+ models (ICML 2025) — [PMLR](https://proceedings.mlr.press/v267/kim25e.html)

### Inferences
- Design consensus emerging: independent first-round answers, heterogeneous strong members, debate only when disagreement exists, anti-conformity / outlier filtering, and a strong verifier or orchestrator; always benchmark against self-consistency of the best single model at equal compute.

### Gaps
- "Debate Only When Necessary" and "Key Decision-Makers in Multi-Agent Debates" (arXiv 2511.11040) surfaced but not read.
- Dates for arXiv 2606.19826 not stated in the document.
