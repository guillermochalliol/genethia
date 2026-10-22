# Novelty gaps and the compliance opportunity: a society of small heterogeneous models for US financial-marketing review

Research date: 2026-10-21. Items dated before 2026 are marked [older].

## Q1. Do existing multi-agent frameworks use heterogeneous small models with formal roles, voting, reputation and audit logs?

### Takeaway
The mainstream frameworks let you give each agent a different model. None of them ships voting, longitudinal reputation, rewarded dissent or tamper-evident deliberation logs as built-in primitives. The closest governance design (AgentCity, April 2026) is a preregistered proposal with no results yet, and it does not commit to heterogeneous models.

### Cited Findings
- CrewAI: each agent has its own `llm` parameter, so heterogeneous models per agent are supported. The agents docs describe no voting or reputation features. Logging is limited to `verbose` output and a `step_callback` hook, with no dedicated audit log — [CrewAI docs](https://docs.crewai.com/en/concepts/agents)
- AutoGen is "in maintenance mode. It will not receive new features or enhancements" and is now community-managed. Microsoft points new users to Microsoft Agent Framework, which it calls "the enterprise-ready successor to AutoGen" — [AutoGen GitHub README](https://github.com/microsoft/autogen)
- AgentCity (Ruan and Zhang, NetX Foundation, arXiv 2604.07007, 8 April 2026) proposes a separation of powers:
  - Agents legislate by proposing and voting on rules. Voting needs 60% participation and aggregates ordinal rankings with Copeland/Minimax.
  - Software executes; humans adjudicate.
  - Reputation is an exponential moving average starting at 0.5, with a reward multiplier bounded at 0.75–1.25.
  - Logging is append-only and anchored by Merkle roots, and a check detects voting blocs.
  - Results are "currently in progress"; only an n=5 pilot has run.
  - Multi-provider model diversity appears only as a mitigation, and the primary model is "TBD."
  — [arXiv 2604.07007](https://arxiv.org/pdf/2604.07007)
- Together AI's Mixture-of-Agents (MoA) layers several open-source LLMs as proposers and aggregators. It scored 65.1% on AlpacaEval 2.0 versus 57.5% for GPT-4 Omni, under Apache-2.0 [older, 2024]. It is ensemble aggregation, not role- or governance-based deliberation — [togethercomputer/MoA GitHub](https://github.com/togethercomputer/moa)
- Sakana AI's TreeQuest / Multi-LLM AB-MCTS (July 2025, Apache-2.0) combines o4-mini, Gemini 2.5 Pro and DeepSeek-R1. It solved over 30% of 120 ARC-AGI-2 test problems, beating any single model, and some problems were solved only when one model corrected another's failed attempt [older, 2025; frontier models, not small ones] — [VentureBeat](https://venturebeat.com/ai/sakana-ais-treequest-deploy-multi-model-teams-that-outperform-individual-llms-by-30)

### Inferences
- Heterogeneous models per agent is already a commodity: CrewAI, LangGraph and MAF all allow it. Novelty cannot rest on "different models." It has to come from the institutional layer: roles with authority, voting rules, reputation that persists across cases, incentives for dissent, and a deliberation record that can be audited.
- AutoGen being frozen and AgentCity having no results point to an open space for a working, evaluated governance layer.

### Gaps
- I did not verify LangGraph, MetaGPT, CAMEL, AgentVerse, ChatDev or Microsoft Agent Framework docs directly for voting or audit features. I found no source saying they have them, but absence is not confirmed.
- I found no open-source framework that ships rewarded dissent as a feature.

## Q2. Research on societies of small or specialized models: do they beat larger single models?

### Takeaway
The evidence is mixed and depends heavily on the task. Heterogeneous model mixes and weight-space collaboration among 7B experts show real gains. Several careful 2025–2026 studies, however, find that plain majority voting captures most of the benefit and that debate among small models can even hurt. Mechanisms against conformity are an active research topic.

### Cited Findings
- **"Debate or Vote"** (Choi, Zhu and Li, UW-Madison, NeurIPS 2025): "Majority Voting accounts for most of the performance gains" in multi-agent debate (average over seven benchmarks).
  - Qwen2.5-7B: single agent 0.7205, best debate variant 0.7377, majority vote 0.7691.
  - Llama3.1-8B: 0.6203 / 0.6990 / 0.7242.
  - Theory: debate forms a martingale, so expected correctness does not rise across rounds. Debate variants guided by the majority vote reach about 0.75–0.76.
  — [arXiv 2508.17536](https://arxiv.org/pdf/2508.17536)
- **SLMJury** (Laddha, Pradhan and Srivastava, 2026 preprint) tested 16 small models (0.6B–14B) from the Llama 3.x, Qwen 2.5/3 and Phi-4 families as judges.
  - Phi-4-mini (3.8B) reached 88.22% judge accuracy, against 89.55% for Phi-4 (14B).
  - A three-judge majority vote added only 0.06 points over the best single judge.
  - Multi-agent debate lowered accuracy in every configuration tested (best debate 87.04% vs 87.81% for its strongest member).
  - Their conclusion: "no single SLM dominates."
  — [arXiv 2606.07810](https://arxiv.org/pdf/2606.07810)
- **Diversity of Thought** (Hegazy, Oct 2024, revised Jan 2025) [older]: a debate among different medium-capacity models (Gemini-Pro, Mixtral 8x7B, PaLM 2-M) reached 91% on GSM8K after 4 rounds, versus 82% for three copies of Gemini-Pro. It reports beating GPT-4 and 94% on ASDiv — [arXiv 2410.12853](https://arxiv.org/abs/2410.12853v1)
- **Cultural-alignment debate** (Ki et al., ACL 2025) [older]: debate among 7–9B open models reached accuracy comparable to a 27B model on NormAd-ETI and improved cultural group parity. It covered 7 open models in 21 combinations — [AI Weekly summary](https://aiweekly.co/alerts/small-llms-match-27b-model-via-multi-agent-cultural-debate) / [ACL Anthology](https://aclanthology.org/2025.acl-long.1210/)
- **Model Swarms** (Feng et al., Google / UW, ICML 2025) [older]: 10 Gemma-7B LoRA experts run a particle-swarm search in weight space. They gain up to 21.0% over 12 composition baselines and 13.3% on average across 9 datasets, with as few as 200 examples — [arXiv 2410.11163](https://arxiv.org/html/2410.11163v2); [PMLR](https://proceedings.mlr.press/v267/feng25o.html)
- **SambaNova Composition of Experts** [older, 2024]: Samba-CoE has 150 Llama2-7B-derived experts plus a router, more than 1T parameters in total. The paper claims that compositions of small models "can match or exceed" monolithic LLMs but credits accuracy claims to prior work. Its own results are efficiency numbers: 3.7x speedup vs DGX H100 and up to 19x smaller footprint — [arXiv 2405.07518](https://arxiv.org/html/2405.07518v2)
- An August 2026 arXiv paper (2608.03648) targets "blind conformity" in multi-agent debate by regulating debate relationships. I could not extract its content because the PDF had no machine-readable text, so only the title is confirmed — [arXiv 2608.03648](https://arxiv.org/pdf/2608.03648)

### Inferences
- At the 3–8B scale, a naive "everyone debates" design is unlikely to beat majority voting on accuracy. The project's value should come from:
  - real model heterogeneity (Diversity of Thought, Ki et al.);
  - structure that resists conformity, such as rewarded dissent or an adversarial role;
  - the audit record.
  Raw accuracy from debate alone is not the selling point.
- A credible evaluation must include majority vote and best-single-small-model baselines, or reviewers will cite Choi et al. and SLMJury.
- SLMJury's finding that Phi-4-mini comes close to 14B models supports low-compute feasibility for judge and reviewer roles.

### Gaps
- I found no study of reputation-weighted voting across heterogeneous small models on regulatory or compliance tasks.
- I found no direct comparison of a 3–8B society against a frontier single model on legal or compliance review.

## Q3. Where are the real gaps?

### Takeaway
Four areas are under-explored: governance and institution design that has actually been tested, reputation that persists across cases, dissent mechanisms that work against conformity, and deliberation logs as an auditable product artifact. Each lines up with what regulators now say they expect.

### Cited Findings
- **Auditable Agents** (Nian et al., USC FORTIS Lab, arXiv 2604.05485, April 2026):
  - Delegation context and inter-agent handoffs are "often missing or weakly represented" in logs.
  - Tracing responsibility across multi-agent delegation chains is "largely open."
  - Only two surveyed approaches provide tamper-evident records.
  - Open problems include cross-framework event capture (OP3) and cross-party audit aggregation (OP6).
  — [arXiv 2604.05485](https://arxiv.org/pdf/2604.05485)
- AgentCity's governance design (voting, reputation, Merkle-anchored logs) has no empirical results yet — [arXiv 2604.07007](https://arxiv.org/pdf/2604.07007)
- Majority voting dominates debate, and debate can degrade small-model judges, so mechanisms that make dissent informative remain unsolved — [arXiv 2508.17536](https://arxiv.org/pdf/2508.17536); [arXiv 2606.07810](https://arxiv.org/pdf/2606.07810)
- FINRA's 2026 report says multi-step agent chains "may be difficult to reconstruct, complicating auditability." It expects firms to track "agent actions and decisions" and "which model version was used and when" — [Debevoise summary of FINRA 2026 Report](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)

### Inferences
- The most defensible novelty claim is "a governed, auditable deliberation record across heterogeneous models." The record would show:
  - each model's verdict and its version;
  - dissent, and how it was resolved;
  - reputation weights;
  - the reviewer's sign-off.
  This covers FINRA's reconstruction concern, the responsibility-chain gap Nian et al. describe, and the missing empirical work on governance in one design.
- Longitudinal reputation is a second gap: tracking which model's flags human reviewers later upheld, by rule category (e.g., Reg Z trigger terms vs UDAAP impressions). I found no prior work on this.

### Gaps
- I did not find a systematic survey of reputation systems for LLM agents. Older multi-agent-system literature on reputation exists but was not reviewed.

## Q4. AI-assisted marketing compliance in US financial services: rules, vendors, pricing, regulator guidance

### Takeaway
The rules are concrete enough to encode as checks: FINRA 2210, Reg Z §1026.24 trigger terms and "fixed" rules, and UDAAP. The vendor field is active and funded: Saifr (Fidelity), Red Oak, PerformLine, Hadrius, which raised $27M in July 2026 with marketing review still on its roadmap, and Luthor (YC F24). None of these vendors publishes prices. Regulators increasingly expect prompt and output logs and reconstructable agent decisions, which favors an auditable multi-model design.

### Cited Findings: regulations
- **FINRA Rule 2210:**
  - Communications must be "fair and balanced" and must not be "false, exaggerated, unwarranted, promissory or misleading."
  - A registered principal must approve each retail communication before use.
  - Records are kept under SEA Rule 17a-4(b) and must include the approving principal's name and approval date.
  — [FINRA Rule 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210)
- **Reg Z §1026.24 (closed-end credit advertising):**
  - Rates must be stated as APR.
  - Trigger terms require full disclosures (downpayment, repayment terms, APR). Triggers are the downpayment, the number of payments or repayment period, the payment amount, and the finance charge. Triggers can be implied, e.g., "80 percent financing" implies a 20% downpayment.
  - For dwelling-secured credit, misuse of "fixed" is prohibited, as are misleading comparisons, false government-endorsement claims, debt-elimination claims and the term "counselor."
  — [CFPB Reg Z §1026.24](https://www.consumerfinance.gov/rules-policy/regulations/1026/24/)
- **CFPB guidance withdrawal:** on 12 May 2025 the CFPB withdrew 67 guidance documents, including the abusive-practices policy statement. States are expected to fill enforcement gaps [older, 2025] — [Cooley](https://www.cooley.com/news/insight/2025/2025-05-15-cfpb-withdraws-guidance-documents-in-shift-from-nonbinding-policymaking)
  - Whether the August 2022 digital-marketer interpretive rule was among the 67 could not be confirmed from the sources I fetched.

### Cited Findings: regulator guidance on AI
- FINRA's 2026 Annual Regulatory Oversight Report (published around December 2025) expects firms to:
  - store "prompt and output logs for accountability and troubleshooting";
  - track model versions;
  - review prompts and outputs over time with a human in the loop;
  - track agent actions and decisions;
  - keep AI descriptions in marketing accurate and not overstated (AI-washing).
  — [Debevoise](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued); [Global Relay](https://www.globalrelay.com/?p=47924)
- The report also says GenAI and chatbot communications with investors should be retained for recordkeeping, and that firms should assess how third-party vendors use GenAI — [Global Relay](https://www.globalrelay.com/?p=47924)

### Cited Findings: vendors (verified on their own sites where possible)
- **SaifrReview (Fidelity-founded):**
  - Banking product covers Reg E, Reg Z, Reg DD and UDAAP, including misleading impressions and omissions. Products include cards, auto loans, mortgages, home equity and other consumer lending.
  - Flags carry regulation-specific citations and explanations.
  - Delivered through a workflow tool, add-ins and an API.
  - Licensed per user or enterprise, with no public prices.
  — [Saifr banking](https://saifr.ai/saifrreview-banking)
  - Securities product covers FINRA 2210, SEC Rule 482 and the SEC Marketing Rule. It scans text, images and video and suggests disclosures. Partners listed are Microsoft Azure AI catalog, ServiceNow, Adobe and Superhuman. Its page does not mention an audit trail — [SaifrReview](https://saifr.ai/saifrreview)
- **Red Oak:**
  - AI Review module launched 7 January 2025 [older] on its advertising-review rules engine. It needs no model training and is configured through prompts and rules.
  - Red Oak reports more than 1,800 firms as customers.
  - The suite includes 17a-4/WORM-compliant solutions; the page does not say the AI module's outputs are covered.
  — [Red Oak news](https://www.redoak.com/resources/news/red-oak-compliance-launches-ai-review-module-to-accelerate-advertising-review/)
- **PerformLine (mortgage and lending):**
  - Covers TILA, RESPA, HMDA, Fair Housing, ECOA and UDAAP.
  - Offers pre-publication review, web monitoring (including discovering unknown loan-officer vanity URLs and landing pages), social monitoring, NMLS detection and an "AI Response Monitor."
  - Customer quote from Benchmark Mortgage: compliant items approved "in less than five minutes with no human intervention."
  — [PerformLine mortgage](https://performline.com/industry/mortgage/)
- **Hadrius:**
  - Raised $27M seed plus Series A, led by CRV with YC participating, on 14 July 2026.
  - Claims more than 500 financial-institution customers.
  - "AI-first review & approval of marketing materials" is planned for the end of 2026, so it is not yet shipped.
  — [PR Newswire via StreetInsider](https://www.streetinsider.com/PRNewswire/Hadrius+Raises+%2427+Million+to+Build+Agentic+Compliance+Infrastructure/26766129.html)
- **Luthor (YC F24, 3 employees):**
  - Reviews regulated marketing against policies, regulations and approved sources before publication, and logs results for audit.
  - Targets RIAs and broker-dealers, banks and credit unions, mortgage lenders and marketing agencies.
  - Lists agencies among its live customers.
  — [YC profile](https://www.ycombinator.com/companies/luthor)

### Inferences
- The space is crowded at the enterprise end (Saifr, Red Oak, PerformLine) and attracting venture capital (Hadrius, Luthor). The project should therefore not pitch "AI marketing review" on its own. Possible differentiation:
  1. a multi-model deliberation record with model versions, dissent and the human sign-off, built to match FINRA's log and reconstruction expectations;
  2. low cost and self-hosting through small open models, so client data stays private;
  3. a fintech and lending focus (Reg Z triggers, UDAAP, landing pages) for small lenders and the agencies serving them.
- Luthor listing agencies as customers and PerformLine scanning landing pages both suggest an agency-side wedge. An agency that builds fintech landing pages could run pre-publication review before sending work to the client's compliance team.
- Most vendors center on FINRA and SEC (Saifr securities, Red Oak). Coverage of consumer lending and Reg Z appears in Saifr banking and PerformLine, so it is not unclaimed, but there are fewer players there.

### Gaps
- **Pricing:** none of the vendors publishes prices (Saifr: contact sales; Red Oak, PerformLine, Hadrius and Luthor: none found). I found no reliable third-party pricing data.
- **Theta Lake** was not researched within the tool budget.
- **FTC and fair-lending (ECOA/Reg B) advertising guidance specific to AI** was not researched.
- **SEC AI guidance:** I did not fetch SEC-specific AI recordkeeping guidance; the FINRA guidance above comes from law-firm and vendor summaries, not the FINRA report PDF itself.
- **2022 CFPB digital-marketer interpretive rule:** whether it was withdrawn in May 2025 is unconfirmed; check 90 Fed. Reg. 20,084.
