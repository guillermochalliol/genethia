# Low-cost technology stack for a long-running simulation of evolving small-LLM agent societies (as of Oct 2026)

Date checked for all live data (OpenRouter API, PyPI, pricing pages): **2026-10-21 (≈21:04 UTC)**. OpenRouter model/price data was pulled directly from the public API `https://openrouter.ai/api/v1/models` and `https://openrouter.ai/api/v1/models/{id}/endpoints` (469 models listed at that moment). Prices are USD per 1M tokens (input / output). They change often, so check them again before a run.

Project assumptions used below: 50–200 agents in villages of 8–12. Orchestration is Python in Docker on a Minisforum UM880 (Ryzen 7 8845HS, Radeon 780M iGPU, 24 GB RAM). Runs last 1 day and 1 week. The public dashboard is Next.js behind a Cloudflare Tunnel.

---

## 1. Best small open chat models on OpenRouter (3B–12B, multiple families): prices, context, structured output

### Takeaway
The cheapest viable mix runs from about $0.02 to $0.15 per 1M input tokens. Families covered: Meta Llama 3.1 8B, Google Gemma 3 4B/12B, Mistral Ministral 3B/8B (2512), Qwen3.5-9B, IBM Granite 4.2 8B, Microsoft Phi-4 (14B, slightly over range) and Liquid LFM. Mistral's first-party Ministral endpoints are the most "complete": structured outputs, cache-read pricing and `:batch` variants. Structured-output support is set **per provider endpoint**, not per model. The cheapest endpoint for a model often does *not* advertise it.

### Cited Findings
All figures below come from the OpenRouter API on 2026-10-21. "SO" means the endpoint lists `structured_outputs` in `supported_parameters`. "Cache" is the listed `input_cache_read` price. Sources: [OpenRouter models API](https://openrouter.ai/api/v1/models); per-model endpoint API, e.g. [ministral-8b endpoints](https://openrouter.ai/api/v1/models/mistralai/ministral-8b-2512/endpoints).

| Model ID (family) | Context | Cheapest listed $/M in / out | Cache read $/M | Structured outputs |
|---|---|---|---|---|
| `meta-llama/llama-3.1-8b-instruct` (Llama) | 131,072 | DeepInfra 0.02 / 0.04 (fp8); Novita 0.02/0.05 (16k ctx); Groq 0.05/0.08 | Groq 0.025 | Only CoreWeave endpoint (0.22/0.22, bf16) lists SO |
| `meta-llama/llama-3.2-3b-instruct` (Llama) | 131,072 | Parasail 0.05 / 0.33 | none | Parasail SO |
| `google/gemma-3-4b-it` (Gemma) | 131,072 | Parasail 0.04 / 0.05 (bf16) | Parasail 0.02 | yes (model-level) |
| `google/gemma-3-12b-it` (Gemma) | 131,072 | DeepInfra 0.04 / 0.12 (bf16) | NextBit 0.05 (int4) | DeepInfra SO |
| `mistralai/ministral-3b-2512` (Mistral) | 131,072 | Mistral 0.10 / 0.10 | 0.01 | SO |
| `mistralai/ministral-8b-2512` (Mistral) | 262,144 | Mistral 0.15 / 0.15 | 0.015 | SO, `response_format`, tools |
| `mistralai/ministral-8b-2512:batch` | 262,144 | 0.075 / 0.075 | 0.0075 | SO |
| `mistralai/ministral-14b-2512` (Mistral, above range) | 262,144 | 0.20 / 0.20 | 0.02 | SO |
| `qwen/qwen3.5-9b` (Qwen) | 262,144 | Darkbloom 0.08 / 0.13 (fp4); SiliconFlow 0.10 (fp8); DeepInfra/Parasail 0.10 (bf16); Together 0.17 | Darkbloom 0.04 | yes (model-level) |
| `qwen/qwen-2.5-7b-instruct` (Qwen, older) | 32,768 | 0.10 / 0.20 | none | yes |
| `ibm-granite/granite-4.2-8b` (Granite) | 131,072 | DeepInfra 0.06 / 0.25; CoreWeave 0.10 / 0.15 | DeepInfra 0.015; CoreWeave 0.05 | Only CoreWeave lists SO |
| `ibm-granite/granite-4.0-h-micro` (Granite, ~3B class) | 131,000 | 0.017 / 0.112 | none | not listed |
| `microsoft/phi-4` (Phi, 14B) | 16,384 | DeepInfra 0.056 / 0.112 | none | SO |
| `liquid/lfm-2.5-2.6b:free` (Liquid) | 65,536 | free | n/a | SO |
| `liquid/lfm-2.5-24b-a2b` (Liquid MoE, 2B active) | 128,000 | 0.05 / 0.70 | 0.025 | SO |
| `nvidia/nemotron-3-nano-30b-a3b` (NVIDIA MoE, 3B active) | 262,144 | 0.06 / 0.24 | none | SO |
| `google/gemma-4-26b-a4b-it` (Gemma 4 MoE, 4B active) | 262,144 | 0.076 / 0.255 (also a `:free` variant) | 0.0425 | SO (paid only) |
| `mistralai/mistral-small-24b-instruct-2501` (above range) | 32,768 | 0.05 / 0.08 | none | SO |

- Small Gemma 4 dense models (E2B/E4B) and Phi-4-mini did **not** appear in the OpenRouter catalogue on 2026-10-21. Gemma 4 is present only as 26B-A4B and 31B — [OpenRouter models API](https://openrouter.ai/api/v1/models).
- To get structured output: send `response_format: {type: "json_schema", json_schema: {name, strict: true, schema}}`. Support is "determined per endpoint, not per model." Set `provider.require_parameters: true` so requests only route to endpoints that support it. A "Response Healing" plugin can repair imperfect JSON on non-streaming `json_schema` requests — [OpenRouter structured outputs docs](https://openrouter.ai/docs/features/structured-outputs).
- Paid models have "no platform-level request cap." `:free` models are capped at 20 RPM and 50/day, or 1000/day once ≥$10 of credits has been purchased — [OpenRouter limits](https://openrouter.ai/docs/api/reference/limits).
- Cheap embeddings for memory retrieval exist on OpenRouter: `qwen/qwen3-embedding-8b` at $0.01/M, `baai/bge-m3` at $0.01/M, `sentence-transformers/all-minilm-l6-v2` at $0.005/M — [OpenRouter embeddings models API](https://openrouter.ai/api/v1/embeddings/models).

### Inferences
- A sensible "multi-family village" roster at ≤$0.15/M input: Llama 3.1 8B, Gemma 3 4B or 12B, Ministral 8B 2512, Qwen3.5-9B and Granite 4.2 8B, with Ministral 3B / Granite micro / LFM 2.6B as "small-brain" agents.
- Pin providers per model with `provider.order` / `provider.only` and `require_parameters`. Otherwise one agent may silently hop between fp4, fp8 and bf16 endpoints that behave differently. That is a confound for any "personality" or emotion measurement.
- Llama 3.1 8B and Granite 4.2 8B are cheapest on endpoints without advertised SO. Either pay the CoreWeave price or use plain JSON prompting plus validation and retry (Pydantic).

### Gaps
- I did not check whether Qwen3.5-9B produces "thinking" tokens by default on OpenRouter. If it does, output cost rises, so test it and set reasoning off.
- No independent benchmark of JSON-schema adherence for these specific small models was found in this session.

---

## 2. Cost reduction: prompt caching, batching, short contexts, structured outputs

### Takeaway
On OpenRouter, caching for open small models depends on the endpoint. Mistral's first-party endpoints price cache reads at 0.1× input. Qwen3.5-9B (Darkbloom), Gemma 3 4B (Parasail) and Llama 8B (Groq) price them at 0.5×. Granite on DeepInfra prices them at 0.25×. Many cheap endpoints show no cache price at all. The Batch API gives about 50% off but only for models with `:batch` variants (among small ones, essentially Ministral 8B and Mistral Small). It has a 24h window, so it suits offline steps (nightly reflection or summarisation), not the live loop. The biggest lever is keeping the per-call prompt short and stable.

### Cited Findings
- "Most providers automatically enable prompt caching." Anthropic and Alibaba need explicit `cache_control`. Cache hits show up in `usage.prompt_tokens_details.cached_tokens` and `cache_write_tokens`, and in a `cache_discount` field — [OpenRouter prompt caching](https://openrouter.ai/docs/features/prompt-caching).
- The caching doc's provider table does not mention DeepInfra, Parasail or Mistral by name. Per-endpoint cache prices therefore come from the endpoints API: Ministral 8B 0.015 vs 0.15 input; Qwen3.5-9B Darkbloom 0.04 vs 0.08; Gemma 3 4B Parasail 0.02 vs 0.04; Granite 4.2 DeepInfra 0.015 vs 0.06 — [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/qwen/qwen3.5-9b/endpoints).
- Batch API: `POST /api/v1/batches` with inline `requests` (no JSONL upload). It is "typically billed at 50%", `completion_window` must be `24h`, results are kept 30 days, and one batch uses a single model and provider — [OpenRouter Batch quickstart](https://openrouter.ai/docs/batch-quickstart).
- Batch variants seen: `mistralai/ministral-8b-2512:batch` 0.075/0.075, `mistralai/mistral-small-2603:batch` 0.075/0.30, `openai/gpt-oss-20b:batch` 0.024/0.112 — [OpenRouter models API](https://openrouter.ai/api/v1/models).
- Within a batch, a cache written by one request may not be visible to other requests in the same batch. Warming the cache with one sync request first improves hit rates — [OpenRouter prompt caching](https://openrouter.ai/docs/features/prompt-caching).
- Routing can sort by price with a throughput floor: `sort: {by: "price"}` plus `preferred_min_throughput`. Switching slug variants mid-session breaks sticky routing, which hurts cache reuse — [OpenRouter latency & performance](https://openrouter.ai/docs/guides/best-practices/latency-and-performance).

### Inferences
- Put the stable content (world rules, persona, schema) at the start of the prompt and the volatile content (latest observations) at the end, so prefix caching can work where it is offered.
- Memory summarisation: keep a rolling summary of about 300–500 tokens per agent plus the top-k retrieved memories via cheap embeddings ($0.005–0.01/M). Don't send the full history. Run summarisation and reflection as nightly `:batch` jobs on Ministral 8B at half price.
- Use structured outputs with terse enum fields (action, target_id, short utterance). Cap `max_tokens` at around 120–200 to bound output spend.

### Gaps
- None of the docs say how long caches stay alive on DeepInfra, Parasail or Mistral, or what minimum prefix length triggers caching for small models. Measure it from `cached_tokens`.

---

## 3. Orchestration: plain asyncio vs frameworks; Concordia; AgentSociety; Project Sid / PIANO

### Takeaway
For a custom, cost-capped society simulation, the recommended base is **plain asyncio (or anyio) plus a small custom tick or event loop**. Use `httpx`/`openai` SDK async clients, a semaphore per provider, Pydantic schemas and FastAPI for the control API. **Concordia** (Google DeepMind) is the strongest off-the-shelf conceptual base. It provides a Game Master (GM) that simulates the environment and resolves actions, plus component-based agents. Use it as a design reference, or adopt it if you accept its abstractions and its embedder requirement. LangGraph, Microsoft Agent Framework and CrewAI are built for task-oriented agent workflows. Ray is overkill on a single 24 GB box. AgentSociety is oriented to urban simulation. Project Sid's PIANO has no released code.

### Cited Findings
- **Concordia**: "a library for building and running generative agent-based models" using a tabletop RPG structure. "A special entity called the Game Master (GM) simulates the environment in which player entities interact." Core concepts are Entities, Components and the Engine, plus `prefabs` ("pre-assembled recipes for common agents and Game Masters"). "Any LLM API that supports sampling text should work." "You must also provide a text embedder for associative memory." License: Apache-2.0. Citation: Vezhnevets et al. 2023, arXiv:2312.03664 — [Concordia GitHub](https://github.com/google-deepmind/concordia), [README](https://raw.githubusercontent.com/google-deepmind/concordia/main/README.md).
- Concordia on PyPI: `gdm-concordia` 2.4.0, released 2026-03-06, requires Python ≥3.12. Extras: amazon, google, groq, huggingface, langchain, mistralai, ollama, openai, together, vllm — [PyPI gdm-concordia](https://pypi.org/project/gdm-concordia/).
- **AgentSociety** (Tsinghua FIB lab): "a large-scale social simulator built on large model agents". It "simulates urban spaces… transportation, infrastructure, and public resources" and uses Ray for distribution. Docs say AgentSociety 2 (`agentsociety2`) is now recommended for new projects; PyPI `agentsociety` 1.5.7 dates from 2026-03-20 — [AgentSociety docs](https://agentsociety.readthedocs.io/en/latest/), [arXiv 2502.08691](https://arxiv.org/html/2502.08691v1).
- **Project Sid / PIANO** (Altera): PIANO = "Parallel Information Aggregation via Neural Orchestration", for coherent multi-stream real-time agents. The GitHub repo holds only the technical report, a visual abstract and a BibTeX entry, with no source code — [project-sid README](https://raw.githubusercontent.com/altera-al/project-sid/main/README.md), [arXiv 2411.00114](https://arxiv.org/abs/2411.00114).
- **LangGraph**: "a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents", with durable execution and persistence. PyPI 1.2.16, 2026-10-16 — [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/overview), [PyPI](https://pypi.org/pypi/langgraph/json).
- **Microsoft Agent Framework**: successor to AutoGen and Semantic Kernel, with agents plus graph-based workflows, in .NET, Python and Go (Go is preview). The docs advise: "if you can write a function to handle the task, do that instead". PyPI `agent-framework` 1.22.0, 2026-10-15 — [MS Learn](https://learn.microsoft.com/en-us/agent-framework/overview/), [PyPI](https://pypi.org/pypi/agent-framework/json).
- CrewAI 1.15.28 (2026-10-14, Python <3.14) and Ray 2.59.0 (2026-10-02) are current on PyPI — [PyPI crewai](https://pypi.org/pypi/crewai/json), [PyPI ray](https://pypi.org/pypi/ray/json).

### Inferences
- Concordia's GM pattern fits "villages" well: one GM per village resolves conflicts and world state, and a global GM handles inter-village events. Its associative memory needs embeddings (cheap via OpenRouter, see section 1). Risks: GM calls add LLM spend per step; it is Python ≥3.12 only; and its abstractions may fight custom logging and budget hooks. A pragmatic path is to borrow Concordia's GM/component ideas, or wrap its `language_model` interface with your own budget-checked, logged client.
- Ray adds operational weight with little gain at 200 agents. The workload is I/O-bound API calls, which asyncio handles easily.

### Gaps
- I couldn't verify Concordia's latest commit date or its exact list of language-model wrapper files (GitHub API access was blocked and the tree page is robots-disallowed).
- I couldn't fetch AgentSociety 2 details.

---

## 4. Logging: tamper-evident append-only options and storage size

### Takeaway
Simplest robust choice: **Postgres (or SQLite in WAL mode) with an append-only `events` table and a per-row SHA-256 hash chain** (`row_hash = H(prev_hash || canonical_json(row))`). Only the logger service role can write. Periodically export the chain head outside the box, for example to GCS or a public dashboard. **immudb** gives built-in tamper evidence but adds a component; its Python SDK was last released in 2024. Event sourcing (all state derived from the log) composes naturally with either.

### Cited Findings
- Postgres hash-chain pattern: insert-only rows with `prev_hash` and `row_hash`. Serialise "get last hash + insert" with an advisory lock or locked head row to prevent forks. Use stable serialisation (watch JSON key order). Run a verifier that flags `BROKEN_LINK` / `HASH_MISMATCH`, and keep periodic chain-head snapshots. Limitation: "a privileged or compromised account may still alter rows". Hashing makes edits detectable, not impossible — [AppMaster: tamper-evident audit trails in PostgreSQL](https://appmaster.io/blog/tamper-evident-audit-trails-postgresql).
- immudb: an immutable database (KV, SQL and document modes) under Apache 2.0. Changes to history "would be noticed by clients" — [immudb docs](https://docs.immudb.io/master/). The Python client `immudb-py` is at 1.5.0, last released 2024-07-29 — [PyPI immudb-py](https://pypi.org/pypi/immudb-py/json).
- SQLite WAL: concurrent readers with a single writer ("there can only be one writer at a time"). With `synchronous=NORMAL`, transactions "are no longer durable" across power loss — [SQLite WAL](https://sqlite.org/wal.html).

### Inferences
- Agents can't touch the logs if the log DB is reachable only by the orchestrator process and not by any agent tool. LLM agents only emit text that the orchestrator parses; they never get DB credentials. Run the DB in a separate container with an `INSERT`-only role for the orchestrator (`REVOKE UPDATE, DELETE`). Anchor the chain head hourly, for example by posting it to the dashboard or a GCS bucket with object retention, so tampering that rewrites the whole chain is still detectable.
- Use `synchronous=FULL` (or Postgres) if no log event may ever be lost after a power cut.
- Storage estimate (my arithmetic, not sourced): about 2–8 KB per call (prompt hash + response + metadata, with full prompts stored deduplicated). At 144k calls/day (100 agents, one call per agent per minute) that is roughly 0.3–1.2 GB/day, or 2–8 GB/week, before compression. Text usually compresses well with zstd, but no ratio was measured.

### Gaps
- I didn't fetch immudb's internal mechanism (Merkle tree, verified reads) from the primary docs in this session.

---

## 5. Isolation, secrets and budget guards

### Takeaway
Put the agent-runner container on a Docker `--internal` network with no default route. Give it a single egress path through a forward proxy (Squid/tinyproxy/Envoy) that allowlists only `openrouter.ai` (plus `integrate.api.nvidia.com` for dev). Optionally run the container under gVisor (`runsc`), which has acceptable overhead for an I/O-light orchestrator. Spending is enforced at the provider with a dedicated OpenRouter key that has `limit` and `limit_reset`, plus an in-process budget meter and a kill switch.

### Cited Findings
- Docker `--internal`: "Containers on an internal network may communicate between each other, but not with any other network, as no default route is configured and firewall rules are set up to drop all traffic to or from other networks." The gateway or host stays reachable — [docker network create](https://docs.docker.com/reference/cli/docker/network/create/).
- Squid egress-filtering patterns are documented by Qovery and cloud.gov — [Qovery Squid egress](https://www.qovery.com/docs/getting-started/guides/advanced-tutorials/egress-filtering-squid-proxy), [cloud-gov space-egress-examples](https://github.com/cloud-gov/space-egress-examples).
- gVisor: installed via apt (`runsc`) and registered with `runsc install`, then `docker run --runtime=runsc`. It needs Linux 5.6+ — [gVisor install](https://gvisor.dev/docs/user_guide/install/). Overhead is highest for syscall-heavy and small-request workloads. The network stack "is less CPU efficient", and Systrap is the recommended platform — [gVisor performance guide](https://gvisor.dev/docs/architecture_guide/performance/).
- OpenRouter per-key budget: `POST /keys` with `limit` (USD) and `limit_reset` (`daily`/`weekly`/`monthly`). "Resets happen automatically at midnight UTC" — [OpenRouter create API key](https://openrouter.ai/docs/api-reference/api-keys/create-api-key). `GET /api/v1/key` returns `limit_remaining`, `usage_daily` and `usage_weekly` for live polling — [OpenRouter limits](https://openrouter.ai/docs/api/reference/limits).
- NVIDIA build.nvidia.com free endpoints are "for prototyping, research, development, and testing". Production ("activity serving real end-users") requires NVIDIA AI Enterprise. Rate limits vary by model — [NVIDIA NIM FAQ (forum, posted by TomNVIDIA)](https://forums.developer.nvidia.com/t/nvidia-nim-faq/300317). Users widely report a 40 RPM default (community, unofficial) — [NVIDIA forum thread](https://forums.developer.nvidia.com/t/request-for-nvidia-build-api-rate-limit-increase-40-rpm-200-rpm/377433).

### Inferences
- Secrets: mount the OpenRouter key as a Docker secret or file into the proxy, or into the orchestrator only. Keys never enter prompts. Use a separate key per run so the `limit` is the hard ceiling.
- Kill switch, in three layers:
  1. The orchestrator checks a cumulative cost counter (from each response's `usage`/cost) before each tick and stops at a threshold.
  2. A FastAPI `/halt` endpoint, reachable only via Tailscale.
  3. The provider-side key limit as a backstop. Disabling or deleting the key via the API is the last resort.
- A 40 RPM NVIDIA free tier can't sustain 100+ agents in real time. Use it only for small-village dev runs. A public live dashboard may itself count as "serving end-users", so keep NVIDIA out of the public runs.

### Gaps
- I didn't verify whether Docker's `--internal` plus a proxy container leaves DNS exfiltration paths open. Run the proxy as the only resolver and test it.

---

## 6. Interpretability feasibility: reading emotion-like activations in small open models

### Takeaway
It is feasible scientifically: published work finds linear emotion directions in 124M–8B open models. It is **not** practical on the UM880's iGPU for anything beyond small offline probes, because measured 780M speeds for a 12B Q4 model are about 4.5–5 tok/s. TransformerLens and nnsight also run in PyTorch, not llama.cpp. The realistic path is to replay logged agent conversations offline through an HF model with nnsight or TransformerLens on a rented 24 GB GPU (RunPod A5000 at $0.27/h, RTX 3090 at $0.50/h) or on Modal's $30/month free credits.

### Cited Findings
- Jeong (2026), "Extracting and Steering Emotion Representations in Small Language Models": 9 models across 5 families (GPT-2, Gemma, Qwen, Llama, Mistral), 100M–10B, 20 emotions. Emotion representations peak around 50% depth. Steering effects were "surgical", "repetitive collapse" or "explosive", varying by architecture. An external classifier confirmed 37/40 steering scenarios — [arXiv 2604.04064](https://arxiv.org/abs/2604.04064).
- van der Ben et al. (2026), "Where Do Models Find Happiness? Emotion Vectors in Open-Source LLMs": Apertus-8B-Instruct and Gemma-4-E4B-it. Peak PC1–valence correlations were r=0.76 and r=0.83, close to the r=0.81 reported for Claude Sonnet 4.5. Code and data are released — [arXiv 2606.26987](https://arxiv.org/abs/2606.26987).
- Sofroniew et al., "Emotion Concepts and their Function in a Large Language Model" (Claude Sonnet 4.5): emotion representations causally influence behaviour ("functional emotions"), without implying subjective experience — [arXiv 2604.07729](https://arxiv.org/abs/2604.07729).
- Tools: nnsight supports "local execution on any PyTorch model" plus remote NDIF execution (`remote=True`), and the site lists a vLLM section. PyPI nnsight 0.8.1 is from 2026-10-20 — [nnsight.net](https://nnsight.net/), [PyPI](https://pypi.org/pypi/nnsight/json). TransformerLens 4.2.0 (2026-10-10) lists adapters for llama, qwen3/qwen3_5 and gemma1–gemma4 (TransformerBridge) — [TransformerLens docs](https://transformerlensorg.github.io/TransformerLens/), [PyPI](https://pypi.org/pypi/transformer-lens/json). The `steering-vectors` package is at 0.12.2 (2025-02) and `repeng` at 0.4.0 (2024-12) — [PyPI steering-vectors](https://pypi.org/pypi/steering-vectors/json), [PyPI repeng](https://pypi.org/pypi/repeng/json).
- 780M measured speed, Gemma 4 12B QAT Q4_0 on a Ryzen 7 PRO 8700GE with 780M, single-channel DDR5:

  | Setup | Prefill (tok/s) | Generation (tok/s) |
  |---|---|---|
  | Ollama, ROCm | 54 | 4.5 |
  | llama.cpp, Vulkan RADV | 39 | 4.7 |
  | llama.cpp, CPU 8 threads | 14 | 5.3 |

  Gemma 4 E4B on CPU generated 12.3 tok/s, and Gemma 4 26B-A4B MoE 13–14 tok/s. ROCm needed `HSA_OVERRIDE_GFX_VERSION=11.0.2` — [k8s.it blog, 2026-06-07](https://www.k8s.it/posts/running-a-local-llm-on-amd-radeon-780m-gfx1103-rocm-and-the-gpu-that-wasnt-supposed-to-work/).
- The same 780M numbers were posted for a Ryzen 7 7840HS / 780M (32 GB DDR5-4800). A UM790 Pro reply showed Qwen3.6-35B-A3B Q8_0 on Vulkan at pp512 325 t/s and tg128 20.5 t/s, but that reply doesn't name the GPU — [llama.cpp discussion #27519](https://github.com/ggml-org/llama.cpp/discussions/27519). A known issue: HIP builds crash on gfx1103 because it is missing from rocBLAS TensileLibrary — [llama.cpp issue #20839](https://github.com/ggml-org/llama.cpp/issues/20839).
- GPU rental, checked 2026-10-21:

  | Provider | GPU | Price |
  |---|---|---|
  | RunPod pods | RTX A5000 | $0.27/h |
  | RunPod pods | RTX 3090 | $0.50/h |
  | RunPod pods | L4 | $0.59/h |
  | RunPod pods | RTX 4090 | $0.89/h |
  | RunPod pods | A100 80GB | $1.79/h |
  | RunPod pods | H100 PCIe | $2.89/h |
  | RunPod serverless | 24 GB class | $0.69/h |
  | Modal | T4 | ≈$0.59/h ($0.000164/s) |
  | Modal | L4 | ≈$0.80/h ($0.000222/s) |
  | Modal | A100 80GB | ≈$2.50/h |

  Modal's Starter plan includes $30/month of free credits — [RunPod pricing](https://www.runpod.io/pricing), [Modal pricing](https://modal.com/pricing). Vast.ai prices are live and market-driven, and the page text showed no figures — [Vast.ai pricing](https://vast.ai/pricing).

### Inferences
- An 8B model in bf16 needs about 16 GB for weights. On the 24 GB UM880 that leaves little headroom next to the orchestrator and DB, and CPU PyTorch speed would be very slow (no sourced number). Locally, use ≤4B models (for example Gemma-family E4B-class or Qwen 3–4B) for probe development only.
- A cost-effective workflow:
  1. Log the exact prompts and outputs (already required).
  2. Rent an A5000 or 3090 for a few hours.
  3. Replay conversations through the same open-weight model with nnsight, record mid-layer activations, and project them onto emotion vectors built with the papers' methods.
  4. Push the scores back into the dashboard as a delayed "affect" layer.

  For example, 4 hours on an A5000 costs about $1.08.
- Caveat for the write-up: OpenRouter endpoints serve quantised weights (fp4/fp8/bf16 vary), so offline activations come from a sibling of the served model, not the identical one.

### Gaps
- No sourced throughput figure for PyTorch/TransformerLens on CPU or 780M for 3–8B models.
- I didn't verify llama.cpp control-vector support in this session.

---

## 7. Dashboard / visualisation and public read-only exposure

### Takeaway
Recommended: Next.js plus **Server-Sent Events** (one-way, read-only, simplest through proxies) from a FastAPI read-model service. Use **Sigma.js + graphology** (WebGL) for the live relationship graph, and Cytoscape.js (dagre/breadthfirst layouts) or D3 for lineage trees. Expose it publicly via Cloudflare Tunnel, with the control API kept on Tailscale only.

### Cited Findings
- Sigma.js is "a WebGL-powered JavaScript library for interactive graph visualization, built on graphology". Layouts, metrics and community detection come from graphology's standard library, and it works with React — [sigmajs.org](https://www.sigmajs.org/).
- Cytoscape.js is a pure-JS graph library under the MIT license, with Dagre, Breadthfirst, ELK, CoSE and other layouts — [js.cytoscape.org](https://js.cytoscape.org/).
- "WebSockets are supported on all Cloudflare plans." There is an idle timeout, so use a heartbeat — [Cloudflare WebSockets](https://developers.cloudflare.com/network/websockets/).

### Inferences
- The dashboard backend should read from a separate read-only replica, or a materialised projection of the event log. The public site then has no path to write or halt anything.
- Use an SSE heartbeat every 15–30 s to survive Cloudflare idle timeouts. Push aggregated deltas (edges changed, metrics) at most once per second instead of every event.

### Gaps
- I didn't confirm Cloudflare's behaviour with long-lived SSE through Tunnel (buffering or timeout specifics) from primary docs.

---

## 8. Rough cost model for 1-day and 1-week runs

### Takeaway
At 100 agents, one call per agent per minute (about 1,500 input and 150 output tokens per call), the cost is roughly **$5–36/day**, or about **$35–250/week**, depending on the model mix. A slower cadence (one call per agent every 5 minutes) or caching cuts this by 3–5×. All of this is arithmetic on the prices in section 1, checked 2026-10-21.

### Cited Findings
- Input prices come from section 1 — [OpenRouter models API](https://openrouter.ai/api/v1/models):
  - Llama 3.1 8B (DeepInfra) 0.02/0.04
  - Gemma 3 4B 0.04/0.05
  - Granite 4.2 8B 0.06/0.25
  - Qwen3.5-9B 0.08/0.13
  - Ministral 8B 0.15/0.15 (0.015 cached; batch 0.075)

### Inferences
These are my calculations, not sourced figures.
- Volume: 100 agents × 1,440 calls/day = 144,000 calls/day, which is 216M input and 21.6M output tokens per day.

| Model | $/day (no cache) | $/week |
|---|---|---|
| Llama 3.1 8B (DeepInfra) | 4.32 + 0.86 = **$5.2** | ~$36 |
| Gemma 3 4B | 8.64 + 1.08 = **$9.7** | ~$68 |
| Granite 4.2 8B | 12.96 + 5.40 = **$18.4** | ~$129 |
| Qwen3.5-9B | 17.28 + 2.81 = **$20.1** | ~$141 |
| Ministral 8B | 32.4 + 3.24 = **$35.6** | ~$250 |
| Ministral 8B with 2/3 of prompt cached | 72×0.15 + 144×0.015 = 10.8 + 2.16 + 3.24 ≈ **$16.2** | ~$113 |
| Even mix of the five models (no cache) | ≈ **$18** | ≈ **$125** |

- Scaling:
  - 200 agents doubles everything.
  - 50 agents halves it.
  - One call per agent every 5 minutes divides it by 5. A 100-agent, 1-week run on the even mix then costs about $25.
- Add GM/narrator calls (for example one per village per tick ≈ +10% at 100 agents in villages of 10) and nightly batch reflection (small).
- Add optional GPU replay for interpretability: about $1–5 per study session.
- The home server's electricity is not included.
- Recommended guardrails:
  - 1-day pilot: key `limit` $10, `limit_reset` none, in-app halt at $8.
  - 1-week run: key `limit` $25/day with `limit_reset: daily`, plus a total stop at around $150.

### Gaps
- The tokens-per-call assumptions (1,500 in / 150 out) are not measured. Run a 1-hour pilot and read `usage` to calibrate.
- Cache hit rates for small-model endpoints are unknown until measured.
