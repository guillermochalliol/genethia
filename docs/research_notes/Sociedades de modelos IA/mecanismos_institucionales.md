# Mechanism design for societies of weak/mediocre models: the "institutions"

Scope note: research current as of 21 Oct 2026. Older results are marked [older: year]. arXiv IDs encode posting month (e.g., 2607 = July 2026). Most 2026 items are preprints (not yet peer-reviewed) unless a venue is stated.

## Wisdom-of-crowds theory applied to LLMs, and what breaks independence

### Takeaway
The classical conditions (Condorcet: better-than-chance and independent voters; Hong & Page: diverse search heuristics) are mostly violated by LLM crowds: errors are strongly correlated across models, across samples of one model, and even on prompts with no ground truth, so naive "more voters" yields little. Gains appear only when members have genuinely complementary errors and the aggregator exploits that (learned weights, heterogeneous models, verifier signals).

### Cited Findings
- Hong & Page [older: 2004, PNAS]: a randomly chosen team from a large pool of capable problem solvers can beat a team of the individually best agents, because top performers converge on similar search heuristics; conditions include that no single agent always finds the optimum, that for any non-optimal solution some agent can improve on it, and a sequential group search structure — [Hong & Page 2004, PNAS (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC528939/)
- Critique [older: 2014]: Abigail Thompson (Notices of the AMS) argues the theorem is incorrect as stated, trivial once corrected, requires unlimited clones, and that randomness rather than diversity explains the simulations (maximally "diverse" groups did worse than random ones) — [Thompson 2014, Notices AMS](https://users.wfu.edu/gemmerj/files/S23/FYS/Thompson.pdf)
- Correlated errors across 350+ LLMs: on one leaderboard dataset, when two models are both wrong they give the same wrong answer ~60% of the time; shared provider/architecture increases correlation, and larger, more accurate models have highly correlated errors even across different providers/architectures (ICML 2025) — [Kim, Garg, Peng, Garg 2025](https://arxiv.org/abs/2506.07962v1)
- "Nine judges, two effective votes" (May 2026): a 9-judge panel from 7 model families has Kish effective sample size ~2.0-2.5; mean pairwise error correlation 0.391; panel accuracy 72.0% vs 71.8% best single judge on MNLI; "Condorcet gap" 8-22 points; unanimous panels still err 9.1% (vs ~0.02% expected under independence); Dawid-Skene and accuracy-weighted voting close at most ~11% of the gap; chain-of-thought *increased* correlation (neff 1.94); five judges capture ~90% of attainable independence. Recommends reporting neff and diversifying *how models reason*, not just provider — [Kohli 2026](https://arxiv.org/pdf/2605.29800)
- "Consensus is Not Verification" (Mar 2026, Koyejo group): across 5 open models and 4 benchmarks without external verifiers, no aggregation rule (majority, confidence-weighted, predicted-popularity, Surprisingly Popular) consistently beat single-sample baselines even at 25x inference cost; on MATH the most common wrong answer accounted for 65-87% of wrong responses; models agreed above chance even on random-string prompts (correlation up to 0.35), attributed to shared inductive biases; models predict the crowd far better than the truth; forecasting questions post-cutoff were at chance — [Denisov-Blanch et al. 2026](https://arxiv.org/html/2603.06612)
- Wisdom of LLM crowds on forecasting (Jul 2026): 15 LLMs on 254 Manifold questions; on a 94-question post-cutoff "clean" subset, logistic-regression aggregation (Brier 0.241) and MLP (0.264) beat arithmetic mean (0.313) and every individual model; learned weights tracked how *weakly* a model's errors correlated with the crowd (Spearman +0.482), not individual accuracy (-0.075); 9 of 15 models got negative (contrastive) weights; training-data contamination inflated accuracy by up to +0.26 on pre-cutoff questions; LLM crowd still 1.61-2.64x worse Brier than the human market — [Douven 2026](https://arxiv.org/pdf/2607.18269)
- "Diversity is the Strength of the AI Crowd" (Jun 2026, Mantic, ICML 2026 forecasting workshop): frontier LLMs make highly similar forecasts; Grok 4, only 3rd in solo accuracy, contributed most to the optimal ensemble because least correlated with the frontier cluster; best 5-sample budget was mixed across 4 models; GPT-5 and Gemini 3 Pro were nearly interchangeable (<0.1 BP removal cost). Small test set (113 questions), no CIs — [Aitchison et al. 2026](https://www.alphaxiv.org/abs/2606.29661.md)
- Earlier positive result [older: 2024]: a 12-LLM ensemble on 31 binary questions was not statistically different from 925 human forecasters; models showed acquiescence bias (means well above 50% though outcomes ~even); giving models the human median improved them 17-28% but simple human+machine averaging was better — [Schoenegger, Tuminauskaite, Park, Tetlock 2024](https://arxiv.org/abs/2402.19379)
- Self-MoA [2025, TMLR 2026]: ensembling outputs of only the single best model beat mixed-model Mixture-of-Agents by 6.6% on AlpacaEval 2.0 and 3.8% on average across MMLU/CRUX/MATH, because mixing lowers average quality — quality-diversity trade-off — [Li, Lin, Xia, Jin](https://arxiv.org/abs/2502.00674)

### Inferences
- Independence-breakers in LLM collectives, synthesized from the above: shared pretraining data and inductive biases, same provider/architecture, convergence of strong models (the Hong & Page "best agents look alike" effect appears empirically for LLMs), chain-of-thought homogenizing reasoning, exposure to peers' answers (see debate section), and contamination that makes models "recall" rather than reason.
- Practical design rule: measure error correlation / effective N of the crowd before adding members; a new member's marginal value is its decorrelation, not its standalone accuracy — but only if its quality isn't so low that it drags the average (Self-MoA tension).

### Gaps
- No direct, rigorous test of Surowiecki's four conditions (diversity, independence, decentralization, aggregation) as a framework on LLMs was found; mapping is inferred.
- Did not find a 2025-2026 paper formally testing the Hong & Page theorem with LLM agents.

## Aggregation and weighting mechanisms

### Takeaway
Plain majority vote is a strong, hard-to-beat baseline, but it ignores correlation. Mechanisms that use higher-order information (Optimal Weight, Inverse Surprisingly Popular), latent-variable reliability estimation (Weaver), learned/contrastive weights, and classifiers that decide when to overturn the majority give modest but real gains; signals like Surprisingly Popular and self-reported confidence are unreliable in some unverifiable LLM settings.

### Cited Findings
- Surprisingly Popular [older: 2017, Nature]: respondents answer and predict others' answers; the answer more popular than predicted is chosen; reduced errors 21.3% vs majority vote, 24.2% vs confidence-weighted votes, 22.2% vs highest-average-confidence weighting (on humans) — [MIT News on Prelec, Seung, McCoy 2017](https://news.mit.edu/2017/algorithm-better-wisdom-crowds-0125)
- Beyond Majority Voting (ICML 2026; arXiv Oct 2025, v2 May 2026): two training-free aggregators using first- and second-order information — Optimal Weight (OW) and Inverse Surprising Popularity (ISP) — that account for differences and correlations among models; theoretical guarantees under mild assumptions; consistently beat majority voting on synthetic data, UltraFeedback, MMLU and an ARMMAN healthcare setting — [Ai, Pan, Simchi-Levi, Tambe, Xu](https://arxiv.org/abs/2510.01499); [ICML 2026 poster](https://icml.cc/virtual/2026/poster/63160)
- Counter-evidence: SP and confidence did not reliably separate correct from incorrect LLM answers; Inverse-SP reached 80% on HLE but was at chance elsewhere, so its direction is task-inconsistent — [Denisov-Blanch et al. 2026](https://arxiv.org/html/2603.06612)
- Confidence-weighted voting among diverse LLMs [older: 2023-24, ACL 2024]: ReConcile — different LLMs discuss over rounds, see grouped answers + confidence + "convincing" corrective explanations, final confidence-weighted vote; up to +11.4% over baselines, beats GPT-4 on 3 datasets, +8% on MATH when mixing API, open-source and domain models; authors attribute gains to model diversity — [Chen, Saha, Bansal](https://arxiv.org/abs/2309.13007v3); [ACL Anthology](https://aclanthology.org/2024.acl-long.381)
- Bayesian / latent-variable reliability weighting (Weaver, Stanford Hazy Research/Scaling Intelligence, 2025): combines 30+ weak verifiers (reward models, LM judges) without labels using weak supervision (method-of-moments latent variable model) to estimate each verifier's accuracy from agreement patterns; 87.7% average accuracy, ~1 pt above o3-mini; +11.2 to +27.8 pts over first-sample accuracy; distilled 400M cross-encoder retains up to 98.7% of accuracy at up to 99.97% less verification compute and beats majority vote by 23.2 pts — [Weaver blog](https://hazyresearch.stanford.edu/blog/2025-06-18-weaver); [arXiv 2506.18203](https://arxiv.org/pdf/2506.18203)
- Dawid-Skene and accuracy-weighted voting recovered at most ~11% of the correlation-induced Condorcet gap in LLM judge panels — [Kohli 2026](https://arxiv.org/pdf/2605.29800)
- Learned contrastive weights: a two-model formula σ(p_Gemini Pro − p_Claude Haiku) beat the 15-model mean by 12.9% Brier; logistic regression ~ MLP, implying linear decorrelation, not nonlinear interactions, drives the gain — [Douven 2026](https://arxiv.org/pdf/2607.18269)
- Minority Sentinel (Jun 2026): after 3 cross-vendor agents debate, a LightGBM classifier on a 22-feature "debate fingerprint" decides whether to overturn a 2:1 majority, with threshold set to keep >=95% of correct majorities; minority was right in 25.5% of divergent cases (oracle ceiling +10 pts); net gain +1.71% (81.2% flip precision), positive on all 6 datasets; an LLM-as-judge (GPT-4o) baseline was −1.37% and "always trust minority" −19.16%; key lesson: flip *precision* matters and a non-LLM arbiter avoids shared blind spots — [He et al. 2026](https://arxiv.org/pdf/2606.29270)
- Prediction-market / wagering style mechanisms: "Language Model Mechanisms" — payment rules where agents report in natural language and an LLM picks the outcome; truthful reporting is a best response under strong conditions (LLM as δ-sufficient world model, information over-determination); authors flag the conditions as very strong — [arXiv 2407.07845](https://arxiv.org/abs/2407.07845)
- PolySwarm (Apr 2026): 50 persona LLM agents produce probabilities combined into a confidence-weighted Bayesian consensus merged with market-implied probability; abstract claims better calibration than single models on Polymarket but gives no numbers and no reputation mechanism — [Barot & Borkhatariya 2026](https://arxiv.org/abs/2604.03888)

### Inferences
- A hierarchy of aggregators by strength of evidence: (1) majority vote (robust baseline); (2) correlation-aware weighting (OW/ISP, learned contrastive weights) — modest gains; (3) external grounding (verifiers, execution, tests) — largest gains. Without (3), sophisticated voting mostly reshuffles shared errors.
- "Reputation per agent per domain" can be approximated by Weaver-style unsupervised reliability estimation or by Douven-style learned weights on a held-out track record; the evidence suggests the weight should reward *decorrelation*, not raw accuracy.

### Gaps
- Found no rigorous 2025-2026 study of a running internal prediction market (agents trading with budgets over time, persistent reputation) among LLM agents with quantified accuracy gains; PolySwarm lacks numbers.
- No source found that measures per-domain learned reputation for LLM agents over long horizons.

## Mechanisms that reward dissent or protect minority views

### Takeaway
Unstructured debate among similar models induces conformity (sycophancy toward the modal peer answer) and is, in theory, a martingale: it does not improve expected correctness. Majority voting explains most debate gains. What helps: independent first answers before exposure, heterogeneous members, forced adversarial roles with a separate judge, biasing updates toward correct/verified content, and a non-LLM arbiter that decides when to trust the minority.

### Cited Findings
- Original multiagent debate [older: 2023]: several instances propose and debate over rounds; improved math/strategic reasoning and factuality — [Du, Li, Torralba, Tenenbaum, Mordatch](https://arxiv.org/abs/2305.14325)
- Devil's-advocate debate [older: 2023, EMNLP 2024]: defines Degeneration-of-Thought (self-reflection stops generating new ideas once confident); MAD uses "tit for tat" opposing debaters plus a judge; needs adaptive termination and only modest adversarial intensity; LLM judges may be unfair when debaters are different LLMs — [Liang et al.](https://arxiv.org/abs/2305.19118)
- Debate or Vote (NeurIPS 2025): majority voting alone accounts for most of MAD's gains (e.g., Llama3.1-8B: single 0.620, vote 0.724, best MAD ~0.699); proves debate induces a martingale over belief trajectories, so it doesn't improve expected correctness; biasing updates toward correct responses helps — [Choi, Zhu, Li](https://arxiv.org/html/2508.17536v2)
- Cost of Consensus (Apr 2026): 10 homogeneous 7-8B models, 3 rounds; agents adopted modal peer answer up to 85.5%; correct answers present in the team but lost in voting up to 32.3 pts; debate never beat isolated self-correction (e.g., Ministral GSM-Hard 20.7% vs 48.3%); noise-control rationale injection sometimes beat debate; 2.1-3.4x more tokens; sycophancy 95.4% in a preliminary 32B run. Applies to *unguided homogeneous* debate — [Bertalanič & Fortuna 2026](https://arxiv.org/pdf/2605.00914)
- Can LLM Agents Really Debate? (Nov 2025): on Knight-Knave-Spy puzzles, intrinsic reasoning strength and group diversity dominate; debate order and confidence visibility help little; majority pressure suppresses independent correction; strong teams can overturn wrong consensus — [Wu, Li, Li](https://arxiv.org/abs/2511.07784v1)
- Minority protection via a separate non-LLM arbiter (+1.71% net, vs −1.37% for LLM judge) — [He et al. 2026](https://arxiv.org/pdf/2606.29270)
- Judge/critic separation done right: judge-based *selection* among a diverse team beat MoA-style *synthesis* in all 42 tasks (win rate 0.810 vs 0.179) and beat majority vote (0.810 vs 0.496); derives a selector-quality threshold s* below which diversity hurts; independent-judge re-evaluation cut win rates 53-67% (judge circularity) though ranks held — [Maryanskyy, Budnikov, Kaliyev 2026](https://www.alphaxiv.org/abs/2603.20324.md)

### Inferences
- Institutional analogues: "secret ballot first" (independent answers before seeing peers), "loyal opposition" (assigned devil's advocate), "independent judiciary" (judge of a different family or non-LLM classifier), and "evidence rules" (weight arguments by verifiable steps, per Choi et al.'s biased-update intervention).
- Debate is worth its token cost mainly when members are heterogeneous and stronger than the problem's difficulty; with weak homogeneous members, vote or self-correct instead.

### Gaps
- Limited quantitative evidence on anonymization specifically (hiding which model said what) as a de-biasing intervention; not found in this pass.

## Hierarchy and routing: cascades, small model + verifier, generator-verifier gap, PRMs

### Takeaway
The most reliable way to make weak models beat strong ones is asymmetric: cheap generators sample broadly, and a verifier (tests, execution, PRM, verifier ensemble) selects. Coverage grows log-linearly with samples, but without automatic verification, majority vote and reward models plateau. Routers/cascades save cost rather than raise the ceiling.

### Cited Findings
- FrugalGPT [older: 2023]: learned cascade over LLM APIs matches GPT-4 at up to 98% lower cost or +4% accuracy at same cost — [Chen, Zaharia, Zou](https://arxiv.org/abs/2305.05176)
- RouteLLM (ICLR 2025): routers trained on preference data choose strong vs weak model; >2x cost reduction in some cases without quality loss; routers transfer when the model pair is swapped — [Ong et al.](https://arxiv.org/abs/2406.18665); [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5503a7c69d48a2f86fc00b3dc09de686-Abstract-Conference.html)
- Large Language Monkeys [older: 2024]: coverage scales log-linearly over ~4 orders of magnitude of samples; DeepSeek-Coder-V2 on SWE-bench Lite 15.9% (1 sample) → 56% (250 samples), beating 43% prior SOTA; without automatic verifiers, majority vote and reward models plateau beyond several hundred samples — [Brown et al.](https://arxiv.org/abs/2407.21787)
- Small policy + PRM (2025): with compute-optimal test-time scaling, a 1B model beat a 405B model on MATH-500, a 0.5B beat GPT-4o on MATH-500 and AIME24, a 7B beat o1 and DeepSeek-R1 — [Liu et al. 2025](https://arxiv.org/abs/2502.06703)
- Weaver shrinks the generation-verification gap by ensembling weak verifiers (see aggregation section) — [Weaver](https://hazyresearch.stanford.edu/blog/2025-06-18-weaver)
- Judge selection over diverse generators beats synthesis and voting; selector quality gates whether diversity helps — [Maryanskyy et al. 2026](https://www.alphaxiv.org/abs/2603.20324.md)

### Inferences
- For a "society of mediocre models", the generator role can be crowded and cheap, but the verifier/judge role is the bottleneck institution; invest in it (executable checks first, then ensembles of diverse weak verifiers with Weaver-style reliability estimation).

### Gaps
- Did not retrieve 2026 router/cascade successors with headline numbers; the cascade evidence cited is 2023-2025.

## Collective learning over time

### Takeaway
Societies can improve across rounds when they preserve diversity (separate finetuning per agent), store/distill successful trajectories, or run evolutionary selection against an automated evaluator. The strongest real-world results (AlphaEvolve) depend on objective, machine-checkable fitness.

### Cited Findings
- Multiagent Finetuning (ICLR 2025): a group of models from the same base, each finetuned on its own data from multi-agent interactions, specializes and diversifies; sustains improvement over more rounds than single-agent self-improvement, which hits diminishing returns — [Subramaniam et al.](https://arxiv.org/abs/2501.05707v2); [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1d50221b03ced7152d8750c9d1e66cba-Abstract-Conference.html)
- SiriuS (NeurIPS 2025): experience library of successful multi-agent reasoning trajectories used as training data, plus augmentation that repairs failed trajectories; +2.86% to +21.88% on reasoning and biomedical QA — [Zhao, Yuksekgonul, Wu, Zou](https://arxiv.org/abs/2502.04780v1)
- Evolutionary model merging [older: 2024]: Sakana evolves merges in parameter space and layer/data-flow space without gradient training; EvoLLM-JP (7B, merged from a Japanese LLM + two math LLMs) beat its sources on Japanese MGSM and, on a 9-task Japanese suite, beat all <70B Japanese LLMs and the prior 70B SOTA — [Sakana AI](https://sakana.ai/evolutionary-model-merge/); [arXiv 2403.13187](https://arxiv.org/html/2403.13187v2)
- AlphaEvolve (May 2025, Google DeepMind): evolutionary loop pairing a fast Gemini (breadth of ideas) with a more capable Gemini (depth), scored by automated evaluators; recovered 0.7% of Google's worldwide compute via a Borg heuristic, 23% kernel speedup (~1% training time), 4x4 complex matrix multiplication in 48 multiplications, matched SOTA on ~75% and improved ~20% of 50+ open math problems — [DeepMind blog](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
- Learning from human crowd signals: giving models the human median improved them 17-28% — [Schoenegger et al. 2024](https://arxiv.org/abs/2402.19379)

### Inferences
- AlphaEvolve is effectively a heterogeneous two-tier society (cheap explorer + strong refiner) under an objective "court" (evaluator) with selection pressure — the cleanest existing instance of "institutions" that make the whole exceed its members.
- Multiagent finetuning suggests that diversity must be actively maintained by the training institution; otherwise self-improvement collapses toward a mode.

### Gaps
- Did not retrieve specific 2025-2026 population-based training or self-play "society" papers with numbers beyond those listed; multiagent finetuning numbers not extracted from full text.

## 2025-2026 "constitution"/"governance" frameworks

### Takeaway
Governance framings are emerging but mostly conceptual or pre-registered; empirical evidence on accuracy/amplification is thin.

### Cited Findings
- AgentCity (Apr 2026): "Separation of Power" — agents legislate rules as smart contracts, deterministic software executes, humans adjudicate via an ownership chain linking each agent to a principal; on an EVM layer-2; names the "Logic Monopoly" problem; empirical test is pre-registered (50-1,000 agents in a commons economy), not yet reported — [Ruan & Zhang 2026](https://arxiv.org/abs/2604.07007)

### Inferences
- The separation-of-powers idea maps onto the empirical lessons above: keep generation (legislature/proposers), verification (deterministic execution/tests), and adjudication (independent judge) in different hands to avoid correlated failure.

### Gaps
- No quantitative results yet for AgentCity; other "constitution for agent societies" frameworks were not surveyed in this pass (sibling researcher covers it).
