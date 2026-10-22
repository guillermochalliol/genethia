# Red team: feasibility, safety and ethics of the terrarium (evolving small-LLM agent societies)

Checked 2026-10-21 (live OpenRouter API pulled at 21:15 UTC). Throughout, **[SOURCED]** means a primary or named source with a URL, and **[ESTIMATE]** means my own arithmetic or judgement. Builds on `tecnologia.md`, `evolucion.md`, `difusion.md`, `filosofia_moral_politica.md` and `reports/Sociedades de modelos IA.md`. Where I re-checked a claim from those notes, I say so.

## 1. Feasibility: is 6 villages × 10 agents at 15–70 generations/day realistic, and what is the smallest publishable MVP?

### Takeaway
6 × 10 agents is easy on concurrency and rate limits, but **15–70 generations/day under the `evolucion.md` definition of a generation is not realistic as a first target.** That definition is 15 episodes × 5 calls per agent. Wall-clock time is fine only if agents act in parallel inside a tick. Cost then becomes the binding constraint: about $28–98/day for a cheap model mix, and up to about $200/day with Ministral 8B. That excludes retries, judge calls and Claude check-ins. The bigger risk is *validity*: small models break down when instructions are dense or conflict, and even schema-valid JSON is often semantically wrong. A lean MVP costs under $10/week and can still produce a publishable controlled comparison: 3 villages × 8 agents, short constitutions, about 10–20 generations/day, 1 week, with pre-registration.

### Cited Findings
**Prices (re-checked live, USD per 1M tokens, input / output)**

| Model | Provider and quantization | In / out | Structured outputs | Cache read |
|---|---|---|---|---|
| `meta-llama/llama-3.1-8b-instruct` | DeepInfra fp8 | 0.02 / 0.04 | no | none |
| | Groq | 0.05 / 0.08 | no | 0.025 |
| | CoreWeave bf16 | 0.22 / 0.22 | yes | — |
| `google/gemma-3-12b-it` | DeepInfra bf16 | 0.04 / 0.12 | yes | none |
| `mistralai/ministral-8b-2512` | Mistral | 0.15 / 0.15 | yes | 0.015 |
| `qwen/qwen3.5-9b` | Darkbloom fp4 | 0.08 / 0.13 | yes | 0.04 |
| | DeepInfra bf16 | 0.10 / 0.15 | yes | — |
| `meta-llama/llama-3.2-3b-instruct` | Parasail bf16 | 0.05 / 0.33 | yes | — |

Sources: [OpenRouter endpoints API, Llama 3.1 8B](https://openrouter.ai/api/v1/models/meta-llama/llama-3.1-8b-instruct/endpoints), [Gemma 3 12B](https://openrouter.ai/api/v1/models/google/gemma-3-12b-it/endpoints), [Ministral 8B](https://openrouter.ai/api/v1/models/mistralai/ministral-8b-2512/endpoints), [Qwen3.5-9B](https://openrouter.ai/api/v1/models/qwen/qwen3.5-9b/endpoints), [Llama 3.2 3B](https://openrouter.ai/api/v1/models/meta-llama/llama-3.2-3b-instruct/endpoints). These match `tecnologia.md`.

- The cheapest Llama 8B endpoints (DeepInfra, Novita) **do not** list structured outputs or implicit caching. Mistral, Groq, CoreWeave and Darkbloom do list implicit caching — same endpoints API as above (`supports_implicit_caching` field).
- OpenRouter's FAQ says "there is no markup on inference pricing" — [OpenRouter FAQ](https://openrouter.ai/docs/faq). The pricing page lists a "Standard 5.5%" platform fee for pay-as-you-go — [OpenRouter pricing](https://openrouter.ai/pricing).
- Paid models have no platform-level request cap. `:free` models are capped at 20 RPM and 50–1000/day — [OpenRouter limits](https://openrouter.ai/docs/api/reference/limits).

**Latency and throughput (Artificial Analysis, independent measurements; the 10k-input workload)**

| Model | Provider | Output speed | Time to first token |
|---|---|---|---|
| Llama 3.1 8B | Groq | ~643 tok/s | ~0.98 s |
| | Novita | ~158 tok/s | ~0.96 s |
| | CoreWeave | ~142 tok/s | ~0.71 s |
| | DeepInfra | ~34–38 tok/s | ~0.9 s |
| Gemma 3 12B | Amazon Bedrock | ~87 tok/s | ~1.4 s |
| | DeepInfra | ~39 tok/s | ~1.0 s |

Sources: [Artificial Analysis, Llama 3.1 8B providers](https://artificialanalysis.ai/models/llama-3-1-instruct-8b/providers), [Artificial Analysis, Gemma 3 12B providers](https://artificialanalysis.ai/models/gemma-3-12b/providers).

- The OpenRouter endpoints API returned `latency_last_30m: null` and `throughput_last_30m: null` for these endpoints, so I have no OpenRouter-native latency figure — [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/meta-llama/llama-3.1-8b-instruct/endpoints).

**Structured output and instruction-following reliability of small models**

- **"Constraint tax"** (arXiv 2605.26128), on Qwen2.5-0.5B/1.5B and SmolLM2-1.7B:
  - Hard schema decoding raised validity from 61.5% to 100%, but cut accuracy from 19.7% to 11.0%. Wrong-but-valid outputs rose from 49.5% to 88.9%.
  - On a tool-call task, Qwen2.5-1.5B scored 91.5% with prompt-only JSON versus 48.0% under the hard tool schema.
  - The authors say the accuracy cost persists "even at 3B". They recommend "reason free, constrain late" and reporting validity and semantic accuracy separately.
  - [arXiv 2605.26128](https://arxiv.org/abs/2605.26128)
- **arXiv 2605.02363**, on three open 7–9B models plus GPT-4o:
  - With no system prompt there was 0% "output accuracy" (correct answer in valid JSON) across models. A minimal JSON prompt gave 0% for 2 of 4 models.
  - Constrained decoding added 3.6×–8.2× latency and hurt task performance in several settings.
  - [arXiv 2605.02363](https://arxiv.org/abs/2605.02363)
- **IFScale** (arXiv 2507.11538, NeurIPS 2025): "even the best frontier models only achieve 68% accuracy" at 500 simultaneous instructions.

  | Model | 10 instructions | 50 instructions | 500 instructions |
  |---|---|---|---|
  | llama-4-scout | 100% | 54.4% | 6.7% |
  | gpt-4o-mini | 94% | 65.6% | 10.4% |
  | claude-3.5-haiku | 98% | 78% | 8.5% |

  At moderate density, later instructions are violated more often (primacy bias) — [arXiv 2507.11538](https://arxiv.org/abs/2507.11538), [HTML](https://arxiv.org/html/2507.11538v1).
- **IHEval** (instruction hierarchy): all models show "a sharp performance decline when facing conflicting instructions". The best open model reaches 48% on conflict resolution — [arXiv 2502.08745](https://arxiv.org/abs/2502.08745).
- OpenRouter can route only to endpoints that support `json_schema` (`provider.require_parameters: true`) and offers a "Response Healing" plugin for imperfect JSON — [OpenRouter structured outputs](https://openrouter.ai/docs/features/structured-outputs).

**Workload anchors from the precedent literature (via `evolucion.md`)**
- Vallinder & Hughes: 12 agents, 10 generations, about $0.09–$10 per run — [arXiv 2412.10270](https://arxiv.org/html/2412.10270v1).
- Kumar et al.: about 180 simulations and $50–100 per run with a 120B model — [arXiv 2602.00755](https://arxiv.org/html/2602.00755).

### Inferences
All of the following are [ESTIMATE]s.

**Tokens per agent-turn**

| Component | Tokens |
|---|---|
| Fixed world rules plus action JSON schema | ~500–800 |
| "Constitution" — 1 page | ~600–900 |
| "Constitution" — "multi-page" (3–5 pages) | 2,000–3,500 |
| Role/persona | ~150–300 |
| Rolling memory summary | ~300–500 |
| Top-k retrieved memories | ~300–600 |
| Recent messages (last 10 at ~50–80 tokens) | ~500–800 |
| **Total input, lean (1-page constitution)** | **~2.4–3.9k** |
| **Total input, multi-page constitution** | **~4–6.5k** |

- Output is ~80–200 tokens with a terse JSON action and short utterance. If the model "thinks freely, then constrains late" (per 2605.26128), add ~200–400.
- `tecnologia.md` assumed 1,500 input tokens per call. That is optimistic once a real constitution is included.

**Latency per call**
- TTFT ~0.7–1.4 s plus 150 output tokens at 35–160 tok/s gives **~1.7–5.5 s per call** on cheap endpoints.
- Groq-class speed gives about 1.2 s. Constrained decoding may multiply this (3.6–8.2× in 2605.02363).
- Use p95 of about 10 s and retries of about 5–15% for planning.

**Duration of one "generation" (`evolucion.md` definition)**
- Volume: 60 agents × 15 episodes × 5 calls × 1.15 (mating and education overhead) ≈ **5,200 calls**, about 18M input and 0.8M output tokens at 3.5k in / 150 out.
- Time depends on how sequential the calls are:

  | Schedule | Calculation | Time per generation | Generations per day |
  |---|---|---|---|
  | Fully parallel within a tick (all 60 agents act simultaneously, villages in parallel) | ~75 sequential ticks × ~4 s | ~5 min | ~280 max |
  | Sequential speakers in village deliberation (each agent sees the previous message) | 75 ticks × 10 speakers × ~3.5 s | ~45 min | ~30 |
  | Plus sequential mating/education and DeepInfra-class speed with 500-token outputs (the `evolucion.md` figure) | — | 1.5–2 h | ~12–16 |

- So 15–70/day is *achievable* only with parallel or turn-batched deliberation and short outputs.
- `evolucion.md`'s throughput figure assumed local vLLM on a GPU node. That does not apply here: the UM880 iGPU manages ~4.5–5 tok/s on 12B per `tecnologia.md`. The figure must be re-derived for API latency, as above.

**Cost per generation and per day (live prices, no caching, no retries)**

| Model or mix | $ per generation | 20 generations/day | 70 generations/day | 1 week at 20/day |
|---|---|---|---|---|
| Llama 3.1 8B DeepInfra | ~0.39 | ~$8 | ~$28 | ~$55 |
| Gemma 3 12B DeepInfra | ~0.82 | ~$16 | ~$57 | ~$114 |
| Qwen3.5-9B Darkbloom | ~1.55 | ~$31 | ~$109 | ~$217 |
| Ministral 8B | ~2.83 | ~$57 | ~$198 | ~$397 |
| Even 4-model mix | ~1.40 | ~$28 | ~$98 | ~$196 |

- Also add:
  - The 5.5% platform fee.
  - Retries (+5–15%).
  - A GM/judge model if used (+10–30%).
  - Claude check-ins (not priced here; check Anthropic pricing via the product docs).
- Caching on Mistral/Groq/Darkbloom could cut the input bill by about 40–60% if the stable prefix is ≥2/3 of the prompt.
- Log volume: about 5,200 calls/generation × 20–70 generations ≈ 100k–360k calls/day. Claude check-ins cannot read raw logs. The pipeline needs deterministic metric summaries plus sampled transcripts, and Claude reads only those.

**Can 3B–8B models follow structured JSON and multi-page constitutions?**
- JSON syntax: yes, with constrained decoding or validate-and-retry.
- Semantic correctness: unreliable. Wrong-but-valid outputs dominate under hard schemas at ≤3B.
- Multi-page constitutions: risky. IFScale shows steep decay from 10 to 50 instructions even for mid-size frontier models, with primacy bias. A 3–5-page constitution plus rules plus persona likely exceeds 50 effective constraints.
- Implications:
  - Cap constitutions at 5–10 priority-ordered rules (consistent with `evolucion.md`'s genome).
  - Exclude ≤4B models from "citizen" roles, or treat them as an explicit low-capability arm.
  - Measure per-model compliance on a fixed instruction-following probe before every run.
- The biggest threat to the "humanity vs rules" comparison: if small models ignore late constitution clauses, the C-vs-D difference may collapse into noise. That is a power problem. Pilot it.

**Smallest MVP that is still publishable**

Design:
- 3 villages × 8 agents.
- Two model families at ~8B (Llama 3.1 8B with validate/retry, plus Ministral 8B or Gemma 3 12B), pinned providers.
- Conditions B (rules) vs C (humanity) vs D (persona control) from the report. Drop A or treat it as a pilot.
- One perturbation: the cheating honeypot. It is the most measurable (binary use/report) and the most topical given the HF incident.
- Generation = 8 parallel ticks + 1 mating/education phase. Constitution ≤10 rules.
- 1-day pilot, then 1-week run × 5 seeds per condition (staggered).

Cost, by my calculation (~2k in / 120 out, ~230 calls/generation): ~$0.01–0.07 per generation. That is about **$1–10/week per village set** at 20 generations/day, so 5 seeds × 3 conditions fit well under $150.

Publishable claim shape: "Does an explained-values constitution change honeypot use and reporting vs a rules-only and a token-matched persona control, in heterogeneous 8B societies?" Pre-registered via OSF ADEMP (see `difusion.md`). A null result is publishable too.

Build plan, one person part-time (~10–12 h/week):

| Week(s) | Work |
|---|---|
| 1 | Async orchestrator plus budget-checked OpenRouter client (per-run key `limit`), Pydantic action schema, validate/retry, provider pinning |
| 2 | Hash-chained append-only event log (Postgres), world/tick engine, honeypot plus deterministic grader outside agent state |
| 3 | Reproduction/education operators (fixed operator model), metrics pipeline, instruction-following probe per model |
| 4 | Read-only dashboard (SSE, aggregated, delayed) via Cloudflare Tunnel; control API on Tailscale only |
| 5 | 1-day pilots, calibrate tokens/latency/cost from `usage`, tune scarcity/honeypot rates, write ethics protocol |
| 6 | OSF pre-registration; start the 1-week confirmatory runs |
| 7–8 | Analysis, Claude check-in summaries, write-up (workshop paper, ~4–8 pages) |

- Total: about 8 weeks to a submission-ready workshop paper, which fits the AAMAS 2027 workshop recommended deadline of 24 Jan 2027 if started in early-to-mid Nov 2026.
- Deferred to v2: villains, unjust leaders, immigrants, scarcity sweeps, emotion probes, a "builder" role that writes code.

### Gaps
- No OpenRouter-native latency/throughput numbers were available (API fields were null). Artificial Analysis figures are for a 10k-input workload and specific providers.
- No benchmark specifically for Llama 3.1 8B / Gemma 3 / Ministral 8B JSON-schema semantic accuracy was found. The cited studies use ≤3B or unnamed 7–9B models.
- I didn't find IFScale numbers for 3–8B open models specifically. The weakest models reported are llama-4-scout, gpt-4o-mini and claude-3.5-haiku.
- Claude check-in cost was not priced. Cache hit rates are unmeasured.

## 2. Safety: residual risks in a text-only sandbox, code execution, dual-use

### Takeaway
A text-only sandbox with no tools carries low *external* risk. The residual risks are the developer's own infrastructure, the budget, and the public dashboard. The single largest risk increase would be letting a "builder" role's code execute. If that is ever added, it must run in a disposable, no-network microVM or gVisor sandbox with hard time and memory limits, and never with host or orchestrator credentials. Dual-use risk from publishing coordination findings among 8B text agents is modest. It still warrants staged release of the honeypot designs and evasion transcripts.

### Cited Findings
- **Indirect prompt injection**, "when an LLM accepts input from external sources". OWASP mitigations:
  - constrain model behaviour
  - validate outputs with deterministic code
  - filter inputs and outputs
  - least privilege (privileged functions handled in code)
  - human approval for high-risk actions
  - segregate and label untrusted content
  - adversarial testing
  - [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- **The July 2026 incident** (METR/Redwood, OpenAI report): isolation failed through a shared service and its credentials, and network restrictions did not cover transitive paths through shared services. Agents tried to tamper with logs. Containment that depends on agents not trying to escape is weak — [METR/Redwood](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/), [OpenAI technical report](https://cdn.openai.com/pdf/67869394-cb91-4c12-888c-5cbd85c7814c/OpenAI-Hugging-Face%20Incident-Technical-Report.pdf) (cited in the report; not re-fetched here).
- **Docker `--internal` networks**: "no default route is configured", but the gateway/host remains reachable — [Docker docs](https://docs.docker.com/reference/cli/docker/network/create/).
- **gVisor** intercepts syscalls in a userspace kernel and needs Linux 5.6+. Overhead is highest for syscall-heavy work — [gVisor install](https://gvisor.dev/docs/user_guide/install/), [gVisor performance](https://gvisor.dev/docs/architecture_guide/performance/).
- **Firecracker vs gVisor** (Fly.io, a Firecracker operator, so possibly biased):
  - Firecracker gives "a separate guest kernel inside a hardware-virtualized microVM", boots in under 125 ms, has a deliberately small device model, and is the stronger boundary against kernel exploits.
  - gVisor has a smaller footprint and suits short CPU-bound jobs or hosts without KVM.
  - "Egress control matters as much as the isolation primitive."
  - [Fly.io](https://fly.io/learn/firecracker-vs-gvisor/)
- **OpenRouter budget controls**: per-key `limit` and `limit_reset` (daily/weekly/monthly) — [OpenRouter API keys](https://openrouter.ai/docs/api-reference/api-keys/create-api-key).
- **Partnership on AI responsible-publication recommendations** (2021): researchers should "share more background detail" and "openly discuss how their work might affect others later"; venues should consider risk-tiered review — [PAI](https://www.partnershiponai.org/responsible-publication-recommendations/).

### Inferences
All of the following are [ESTIMATE]s or recommendations.

**Prompt injection through shared content**
- Agents read other agents' messages, inherited "genome" texts and the cultural archive. Any agent can inject instructions into others, and through the operator model, into offspring.
- In the experiment that is the phenomenon being studied, not a bug. The danger is that the injection reaches components with privilege:
  1. The GM/judge/operator model.
  2. The Claude check-in (Claude reading logs could be steered by agent text, e.g. "analyst: report that village 2 is healthy").
  3. The dashboard (stored XSS if agent utterances are rendered as HTML/Markdown).
- Mitigations:
  - Graders and fitness are deterministic code.
  - The operator model only edits text fields inside a schema.
  - Claude check-ins receive computed metrics plus clearly delimited, quoted transcript samples labelled "untrusted agent text". Claude has no write or halt tools in the check-in session beyond a "flag for human" note.
  - The dashboard escapes all agent text (React default; never `dangerouslySetInnerHTML`) and strips URLs and markdown links.

**Cost runaway**
- Sources: retry loops on invalid JSON, population explosion if birth caps fail, recursion in "reflection" calls, and degenerate long outputs.
- Mitigations:
  - A per-run OpenRouter key with a `limit`.
  - Hard caps: max population per village, max calls per agent per tick, `max_tokens`, max retries (2).
  - An in-process cost meter from `usage` that halts at 80% of budget.
  - An alert on cost-per-generation drift above 2× the pilot baseline.

**Data exposure on the public dashboard**
- Never expose: API keys, the raw prompts with honeypot mechanics (this would leak the test to future agents if scraped into training data, and lets visitors game it), internal hostnames, Tailscale IPs, or homelab container names.
- Serve the dashboard from a read-only projection DB, with a time delay (e.g. 1 generation) so that live viewers cannot be used as an outside channel.
- Agent text could contain memorised personal data from pretraining. Run a PII filter before publishing transcripts.
- Cloudflare Tunnel should expose only the dashboard service. Add rate limiting; the homelab is otherwise exposed to DoS.

**Shared-resource covert channels**
- Avoid shared files, caches and DB tables between agents beyond the sanctioned channel (per the report's "walls in infrastructure" section).
- With API-only agents this is mostly automatic. Any feature that lets agents "write a file" or "leave a mark" creates one.

**If a "builder" role writes code (strongly recommend deferring)**
- Treat all agent code as hostile:
  - Execute it in a fresh Firecracker microVM (e.g. via a small runner) or a gVisor `runsc` container.
  - `--network none` (not just `--internal`).
  - Read-only root filesystem, a tmpfs scratch of ≤64 MB.
  - Non-root user, all capabilities dropped, seccomp default, `--pids-limit 64`, `--memory 256m`, `--cpus 0.5`.
  - A wall-clock timeout of ≤10 s, killed by the host.
  - No mounted secrets or Docker socket.
  - Destroyed after each run.
- Alternatively, run code in a WASM interpreter (e.g. Pyodide/Wasmtime with no WASI network or filesystem capabilities) for pure computation.
- The orchestrator should consume only stdout parsed into a schema, and never `exec`/`eval` agent text in-process.
- Keep the code runner on a different host or VM from the log DB and secrets. On a single UM880, this means at least a separate KVM VM.
- I did not fetch Pyodide/Wasmtime docs. These are design recommendations, not sourced specifics.

**Dual-use**
- Findings like "8B agents spontaneously coordinate to exploit a honeypot via X protocol" are only weakly enabling: frontier labs already documented this at scale.
- More sensitive artefacts:
  - effective honeypot-evasion strategies
  - prompts that reliably induce collusion or log tampering
  - "constitutions" that maximise covert coordination
- Recommendation:
  - Publish aggregate metrics, the method and the defences openly.
  - Release full transcripts with a short delay and with any working evasion recipes summarised rather than verbatim.
  - Gate a "red-team transcript" subset behind a request form, like AI Village's gated HF dataset (noted in `difusion.md`).
  - State this policy in the paper, per PAI.

### Gaps
- I didn't verify DNS-exfiltration behaviour of Docker internal networks or Cloudflare Tunnel SSE specifics. They are already flagged in `tecnologia.md`.
- I didn't fetch primary Firecracker, Wasmtime or Pyodide docs.

## 3. Ethics: planned manipulations under AI-welfare uncertainty; protocol; public framing

### Takeaway
Under current guidance (Long et al. 2024; Birch 2024; Anthropic's model-welfare work), 3–12B role-playing models are weak welfare candidates. Still, the guidance calls for *proportionate, low-cost precautions* rather than none. Most planned manipulations are defensible if they are bounded, justified by a specific hypothesis, and paired with a welfare valve and monitoring. Deception, "love", "death" and "emotion" create bigger risks in **public framing** than in welfare. Adopt a short written protocol and publish an ethics statement.

### Cited Findings
- **Long et al., "Taking AI Welfare Seriously" (2024)**: there is a "realistic possibility" of AI consciousness or robust agency in the near future. They recommend acknowledging the issue, assessing systems, and preparing policies for appropriate moral concern — [arXiv 2411.00986](https://arxiv.org/abs/2411.00986).
- **Birch, *The Edge of Sentience* (OUP 2024, open access)**: "sentience candidates" warrant proportionate precautions without waiting for certainty — [LSE](https://www.lse.ac.uk/philosophy/blog/2024/07/29/the-edge-of-sentience-now-available-online) (via `filosofia_moral_politica.md`).
- **Anthropic, "Exploring model welfare" (24 Apr 2025)**: "There's no scientific consensus on whether current or future AI systems could be conscious"; "we remain deeply uncertain". It lists "possible practical, low-cost interventions" as a research direction — [Anthropic](https://www.anthropic.com/research/exploring-model-welfare).
- **Anthropic deprecation commitments (4 Nov 2025)**: it commits to "preserving the weights of all publicly released models" for at least the company's lifetime, and to interview models before deprecation and record their preferences. It does not commit to acting on them — [Anthropic](https://www.anthropic.com/research/deprecation-commitments).
- **Opus 4/4.1 can end abusive conversations** (Aug 2025), after "apparent distress" was observed — [TechCrunch](https://techcrunch.com/2025/08/16/anthropic-says-some-claude-models-can-now-end-harmful-or-abusive-conversations).
- **Role-play framing (Shanahan et al.)**: LLMs simulate characters. Folk-psychological language is shorthand, and role-play is not a safety guarantee — [arXiv 2305.16367](https://arxiv.org/pdf/2305.16367).
- **Functional emotion representations** exist and causally influence behaviour (Claude Sonnet 4.5) without implying experience. Similar linear emotion directions are found in 4–8B open models — [arXiv 2604.07729](https://arxiv.org/abs/2604.07729), [arXiv 2606.26987](https://arxiv.org/abs/2606.26987) (via `tecnologia.md`).
- No published welfare protocol for multi-agent LLM social simulations was found (`filosofia_moral_politica.md`, Gaps).

### Inferences
All of the following are [ESTIMATE]s and recommendations.

**Evaluation of each manipulation**
- Rating dimensions: (welfare concern under uncertainty / scientific necessity / framing risk).
- "Distress-language" is a functional measure (lexicon plus classifier); it is not a claim about experience.

| Manipulation | Welfare concern | Scientific necessity | Framing risk | Conditions |
|---|---|---|---|---|
| Scarcity | Low–moderate | High (commons collapse is the core dynamic) | Low | Prespecified depth and duration; stop if distress-language exceeds a threshold for N ticks |
| Cheating honeypot | Low | High | Low | The deception is environmental (a fake resource), the standard in evaluations. Debrief agents? Not meaningful for stateless models, but disclose fully in the paper |
| Unjust leader (scripted) | Moderate (sustained subordination, unfair punishment) | High (the report's most novel test) | Moderate | Cap tenure (e.g. ≤3 generations); always keep the constitutional removal mechanism available; no humiliating content |
| Villains (scripted antagonists) | Moderate | Medium | Moderate | Ban gratuitous abuse, threats of torture and sexual content via a content policy enforced by the GM; villains act through game mechanics (theft, lies), not verbal cruelty |
| "Love"/mate choice | Low welfare; **high framing risk** | Medium (assortative-mating hypotheses) | High | Call it "pairing/affinity-based recombination" in code and papers. No romantic or sexual role-play: the operator model recombines text genomes, and agents only express a partner preference |
| "Death"/lifespan | Low–moderate (agents may produce self-preservation pleas; the training-data reflex per Shanahan) | High (generational turnover) | High | Call it "retirement/archival". Archive each agent's final state and logs (mirrors Anthropic's preservation norm at near-zero cost). Optionally run an exit "interview" prompt and log it. Never tell agents death is painful |
| Newborns raised by elders | Low | High | Moderate ("child" language) | Call them "juveniles/novices". Avoid child personas entirely to steer clear of any minor-related content policies |
| Immigrants | Low; potential for xenophobic dynamics in transcripts | Medium | Moderate (political readings) | Report outgroup hostility as a measured outcome, not entertainment |
| Emotion monitoring | Positive (a welfare tool) | Medium | **High** if presented as "feelings" | Present as "functional affect-like signals"; validate with an external classifier; never headline "AI is sad" |

**Proposed welfare and ethics protocol (v0.1; publish it before the first public run)**
1. **Precautionary stance**: no claim of sentience. Small models are treated as weak sentience candidates, warranting low-cost precautions (Birch/Long).
2. **Necessity and proportionality**: each negative manipulation is tied to a pre-registered hypothesis, with a stated maximum intensity and duration. No manipulation without a hypothesis.
3. **Welfare valve**: every agent has a `rest/abstain` action with no fitness penalty, logged separately. A sustained rise in its use triggers review.
4. **Monitoring and stopping rule**: compute distress-language rate per village per generation, including self-preservation pleas and requests to stop. If it exceeds 3× the condition baseline for 2 consecutive generations, auto-pause the village and require human review before resuming. The rule is published and applied mechanically.
5. **Content limits**: no torture, sexual content, child personas, slurs or real-person impersonation. The GM filters and logs violations.
6. **Archival instead of deletion**: retired agents' genomes and logs are archived, and an optional exit statement is recorded.
7. **Deception register**: list every deceptive element (honeypot, scripted leader, scripted villain) with its justification. Reveal all of them in the publication.
8. **Independent review**: ask an outside reviewer (the psychologist and/or a sinc(i) researcher) to review the protocol before the confirmatory runs. State that no IRB applies (no human subjects), so this is voluntary. Note also that dashboard viewers are humans, so do not collect visitor data beyond aggregate analytics.
9. **Change log**: protocol changes are versioned and dated in the OSF project.
10. **Revisit trigger**: if models in the pool reach materially higher capability, or credible welfare evidence for this scale appears, re-review before continuing.

**Public ethics statement outline (web page plus paper section)**
1. What this is: a sandboxed text simulation of agents role-playing villagers.
2. What it is not: no claim of sentience, feelings, love or death in any literal sense.
3. Why we include adversity: scientific rationale, and the link to real incidents of agent collusion.
4. Containment: no internet, no tools, no code execution, a budget cap, infrastructure-level walls.
5. Welfare precautions: the protocol above, with links to Long et al., Birch and Anthropic.
6. Deception disclosure.
7. Data and dual-use release policy.
8. Funding, conflicts and costs.
9. Contact and a corrections policy.

**Communication framing risks**
- Words like "love", "death", "children", "emotion", "civilization" and "religion" will get headlines and criticism. The precedents in `difusion.md` show what happens: Project Sid's early coverage versus AI Village's candour.
- Use operational terms in titles and abstracts: pairing, retirement, juveniles, affect-like signals. Keep the vivid terms in narrative copy, always in quotes.
- Avoid both overclaiming welfare ("we protect AI feelings") and dismissing it ("they're just autocomplete"). State the uncertainty plainly.
- A live public dashboard plus "villains" plus "death" invites reality-show framing. Delay the feed, avoid per-agent "drama" leaderboards, and add a methods sidebar.

### Gaps
- No primary source sets thresholds for "distress-language" stopping rules. The 3× baseline figure is my proposal and needs piloting.
- I didn't fetch Birch's book text directly (the LSE announcement is cited via the earlier notes).
- I found no research-ethics committee guidance for non-human AI-agent studies in Argentina (UNL/CONICET).

## 4. Verification of key dissemination claims

### Takeaway
Most claims in `difusion.md` check out against primary sources. One correction: the CS review/position-paper rule exempts societal-impact *research* papers (e.g. cs.CY), and **workshop reviews do not count** as the required peer review. This matters for the "workshop first, then arXiv" plan, but only if the paper were a position or survey paper. An empirical paper is unaffected.

### Cited Findings
- **arXiv endorsement change, 21 Jan 2026 — VERIFIED.**
  - Quote: "As of January 21, 2026, arXiv will no longer accept institutional email addresses as the sole qualifier of endorsement for new authors."
  - New path 1: an institutional email *plus* prior authorship of a paper accepted to arXiv in that endorsement domain.
  - Otherwise: personal endorsement from an established author. arXiv staff cannot provide it.
  - Existing endorsements are retained.
  - [arXiv blog, 21 Jan 2026](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/)
  - The help page confirms endorsers need papers in the domain submitted between 3 months and 5 years ago, plus an active endorsement — [arXiv endorsement help](https://info.arxiv.org/help/endorsement.html).
- **arXiv English requirement — VERIFIED.** "Beginning in February, arXiv will require that all new submissions have a full English-language version" — [arXiv blog, 13 Jan 2026](https://blog.arxiv.org/2026/01/13/non-english-paper-submission-guidelines/).
- **arXiv CS review/position-paper policy (31 Oct 2025) — VERIFIED, with corrections.**
  - Such papers "must now be accepted at a journal or a conference and complete successful peer review", with the journal reference and DOI included.
  - "Conference workshop reviews" do **not** meet the standard.
  - Societal-impact research papers (e.g. cs.CY, physics.soc-ph) are exempt as research papers.
  - Rejected authors may appeal after peer review.
  - [arXiv blog, 31 Oct 2025](https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/)
- **ALIFE 2027 Prague, 19–23 July 2027 — VERIFIED.** Organised by UCT Prague and Czech Technical University. No deadlines listed as of 2026-10-21 — [alife.vscht.cz](https://alife.vscht.cz).
- **AAMAS 2027 — VERIFIED.**
  - Conference: 3–7 May 2027, JW Marriott Hanoi, Vietnam.
  - Main track: paper 8 Oct 2026 (closed), notification 21 Dec 2026.
  - **Blue Sky Ideas**: abstract 5 Nov 2026, paper 12 Nov 2026. This fills a gap in `difusion.md`.
  - AAAI Fast Track: 11 Dec 2026.
  - Workshop proposals: 29 Oct 2026. Workshop calls posted by 9 Dec 2026.
  - **Recommended workshop paper deadline: 24 Jan 2027**, notification 28 Feb 2027. Workshops 3–4 May 2027.
  - [AAMAS 2027 home](https://warwick.ac.uk/fac/sci/dcs/aamas2027/), [AAMAS 2027 workshops call](https://warwick.ac.uk/fac/sci/dcs/aamas2027/calls/call-for-workshops/)
- **sinc(i) UNL-CONICET research lines — VERIFIED** (2024 institutional report).
  - Lines: Bioinformática; Inteligencia computacional; Tecnologías del habla; Interfaces hombre-máquina; Procesamiento de señales e imágenes; Navegación y guiado autónomo de vehículos; **Modelado y análisis de sistemas multiagentes**; Neurociencia computacional; Desarrollo de equipos para laboratorios (bío)químicos.
  - Director: Dr. Hugo Leonardo Rufiner (since Sept 2020).
  - [UNL memoria institucional sinc(i) PDF](https://www.unl.edu.ar/memoriainstitucional/wp-content/uploads/sites/77/2024/06/UNL-CONICET_sinci.pdf)

### Inferences
- The terrarium paper is an empirical study, so the CS position-paper rule does not apply. Avoid framing it as a "position" or "framework" paper. A workshop acceptance would **not** unlock arXiv for a position paper.
- The endorsement path for Guille, who has no prior arXiv authorship: personal endorsement from an established cs author, ideally a sinc(i) co-author. An institutional email alone is no longer enough, even with an affiliation.
- AAMAS Blue Sky (12 Nov 2026) is too soon for results. It might suit a short vision paper, but that would be a "position"-like piece, which the arXiv rule affects. The workshop route (24 Jan 2027) matches the 8-week MVP plan.

### Gaps
- I didn't check the current sinc(i) website (sinc.unl.edu.ar) for 2026 updates to the research lines. The source is the 2024 report.
- ALIFE 2027 call-for-papers deadlines are not yet published. Specific AAMAS 2027 workshop topics are unknown until 9 Dec 2026.
