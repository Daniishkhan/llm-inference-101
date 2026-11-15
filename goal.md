# goal.md — LLM inference in Python

**Sun 15 Nov 2026 · Danish.** This file changes only between modules, with one dated line in the
[changelog](#changelog). A new idea goes to [docs/parking-lot.md](docs/parking-lot.md) first. After the
audit of 15 Nov 2026 it holds still until Module 5 is done.

The spine of a self-paced course. I learn data structures and algorithms by building the parts of an inference engine, then I measure and read vLLM, then I serve open models. Python is the base. Kernels come late, in Triton and then CUDA. This replaces the eight-week interview curriculum.

## The goal

By the end I can explain and build every layer of LLM serving: tokenizer, forward pass, sampling, KV cache, batching, paged memory, prefix caching, scheduling, speculative decoding and structured output. Then I can read vLLM's source without getting lost, measure it under load, profile and tune it, quantize and fine-tune models for it, write a GPU kernel, and serve open models behind a router. I can make a model faster and show the numbers: on a rented GPU, on the Mac, and on a Raspberry Pi with no GPU at all.

The proof is public: this repository, four short write-ups with measurements, and one pull request to vLLM or a project beside it.

## Ground rules

- Python first. Kernels come in Module 18: Triton, which is written in Python, then one small kernel in CUDA. Both run only on the rented GPU. Beyond that kernel, C++ is read, not written.
- I type every solution. The tutor writes the problem statements, the tests and the explanations, never solution code. The write-ups and the pull request are mine too.
- One concept at a time: short theory, then a challenge with tests.
- Every module ends with a measurement and five lines in my own words in `log.md`.
- Make it visible early. Use terminal visuals with `rich`: probability bars, block maps, batch animations.
- A module takes about a week at my pace. Move on when "Done when" passes, not when the week ends.
- Twenty modules. With no slips the last one ends in mid April 2027. The checkpoint is the end of week 13, Sat 13 Feb 2027: the core of the engine built, a GPU baseline measured, two write-ups published.

## Setup

- **Python tools:** Python 3.12+, uv, numpy, PyTorch (MPS on the Mac, CUDA on the rented GPU), safetensors, FastAPI with uvicorn, httpx, rich, pytest and hypothesis (property tests). Triton in Module 18. llama.cpp's Python bindings and MLX in Module 20.
- **Models:** GPT-2 small (124M parameters) for Modules 2 to 5. A small modern open model from Module 6 on, for example Qwen3-0.6B, the model nano-vLLM benchmarks with.
- **Hardware:** the MacBook for Phases 1 and 2. A Raspberry Pi 5 beside it from Module 5 on: the machine with no GPU. A GPU rented by the hour from Module 8 on. An AMD GPU or Google's TPU Research Cloud only as a stretch in Module 20.

## Each session

1. **Drill:** one or two classic problems for the module's pattern (table near the end), typed by hand and timed.
2. **Build:** the module's challenge.
3. **Measure:** run the harness from Module 1.
4. **Log:** five lines on what surprised me.

## Each week

- **Saturday's drill is a mock round.** It rotates between a fresh drill, an engine kata (a finished function of mine, typed again cold in 30 to 45 minutes) and, from Phase 2 on, an inference system-design round.
- **From Module 7 on, 30 minutes on one merged pull request** in vLLM, in the area I just built, with three lines in `log.md`.

## Write-ups

Four short pieces in `notes/`, in my own words: numbers first, under 800 words each.

1. After Phase 1.
2. After the GPU baseline in Module 8.
3. After Phase 2.
4. After Phase 3.

---

## Phase 1 — One model, one request (Mac; the Pi from Module 5)

### 1. Measure first
- **Learn:** wall time vs CPU time, profiling (cProfile, a line profiler), why numpy beats Python loops, how big Python objects are.
- **Practise:** arrays and hashing; quickselect, for percentiles.
- **Build:** a benchmark harness to reuse for the rest of the course. It runs a function N times and reports p50, p95, p99 and throughput, with a histogram in the terminal.
- **Done when:** its percentiles match numpy's on random data, and its profile points to the right slow line in a test function.

### 2. Tokenizer
- **Learn:** bytes and UTF-8, byte-pair encoding (BPE), how tokenization changes cost and latency.
- **Practise:** hash maps (pair counts), heaps (best merge first), linked lists (merging in place). Stretch: Unigram segmentation with dynamic programming, which is Word Break with scores.
- **Build:** train BPE on a text file; encode and decode; load GPT-2's merges and reproduce its tokenizer.
- **Done when:** round trips are exact on arbitrary Unicode, and token IDs match GPT-2's tokenizer on the test set.

### 3. Forward pass
- **Learn:** embeddings, attention, MLP, layer norm, logits; numerically stable softmax (log-sum-exp); why attention cost grows with the square of sequence length.
- **Practise:** matrix shapes as arrays; complexity analysis.
- **Build:** GPT-2 small in numpy, loaded from its safetensors file, with greedy generation.
- **Done when:** logits match the reference implementation within tolerance on 20 prompts.

### 4. Sampling
- **Learn:** greedy, temperature, top-k, top-p, repetition penalty, seeds, stop strings.
- **Practise:** heaps and quickselect (top-k); sorting, prefix sums and binary search (top-p); a sliding window with counts (repetition penalty); string matching across token boundaries (stop strings, with Aho–Corasick as a stretch).
- **Build:** a sampler with tests, and a live terminal bar chart of the next-token probabilities.
- **Done when:** the same seed gives the same text, and property tests pass, including top-p mass and stop strings split across tokens.

### 5. KV cache
- **Learn:** what gets recomputed without a cache; memory per token is 2 × layers × KV heads × head size × bytes per value; how dynamic arrays grow.
- **Practise:** dynamic arrays and amortised cost; ring buffers.
- **Build:** add a KV cache to Module 3 and chart tokens per second with and without it.
- **Measure:** on the Mac and on the Raspberry Pi. From here on, a module's numbers have a Pi column wherever its code can run there.
- **Done when:** output is identical with and without the cache, and the speed-up and memory use are measured and explained.

### 6. The modern block, in PyTorch
- **Learn:** PyTorch tensors, devices and dtypes; inference without gradients; what changed since GPT-2: rotary position embeddings, RMSNorm, the SwiGLU feed-forward, grouped-query attention; batching sequences of different lengths with padding and masks.
- **Practise:** matrix shapes with a batch dimension; the KV cache, typed a second time.
- **Build:** port my forward pass and KV cache to PyTorch. Then build the modern block and load Qwen3-0.6B from its safetensors file, with a batched forward pass.
- **Done when:** logits match the reference implementation within tolerance on 20 prompts, alone and in a padded batch, and generation with the cache equals generation without it.
- **Decide at the ritual:** my Module 2 tokenizer on this model's vocabulary, or the reference tokenizer.

## Phase 2 — Many requests: build a mini engine (Mac, PyTorch on MPS; the first rented GPU in Module 8)

### 7. Serving loop
- **Learn:** asyncio, the request lifecycle (waiting, running, finished), streaming over server-sent events, the shape of the OpenAI-compatible API, chat templates, token accounting.
- **Practise:** queues; state machines.
- **Build:** an async server with a subset of `/v1/completions` and `/v1/chat/completions` that streams tokens.
- **Done when:** ten clients streaming at once each get correct, uncorrupted output, and a cancelled request frees its resources.

### 8. Load generator and a first GPU baseline
- **Learn:** closed-loop against open-loop load, where requests arrive on a clock and not when the last one finishes; realistic arrival times and lengths; TTFT and ITL for each request; renting a GPU by the hour; the PyTorch profiler.
- **Practise:** streaming percentiles (Find Median from Data Stream).
- **Build:** a load generator with realistic arrival times and lengths. Point it at my Module 7 server on the Mac, then at real vLLM on a rented GPU. Profile one decode step of my Module 6 model on both machines.
- **Done when:** one command gives the same report for both servers (TTFT, ITL and throughput at p50, p95 and p99), and its numbers agree with vLLM's own benchmark tool on the same run, within a tolerance set at the ritual.

### 9. Continuous batching
- **Learn:** static batching vs adding and removing requests at every step; a token budget per step.
- **Practise:** greedy admission; intervals (peak concurrency is the largest overlap of request lifetimes, which is Meeting Rooms II).
- **Build:** a step-level scheduler, and a terminal animation of batch slots filling and emptying.
- **Done when:** at temperature 0 each request's tokens equal its one-at-a-time tokens; throughput beats static batching on a synthetic workload; and measured peak concurrency matches the interval calculation.

### 10. Paged KV cache
- **Learn:** fixed-size blocks, block tables, fragmentation, reference counts, copy-on-write when one prompt gets several samples, preemption by recomputation.
- **Practise:** linked lists. vLLM keeps free blocks in a doubly linked list with a dummy head and tail, so it can remove a block from the middle in O(1). Build the same.
- **Build:** a block allocator with alloc, free and fork, and a live block map in the terminal. Plug it into Module 9.
- **Done when:** a property test with thousands of random alloc, free and fork steps never leaks a block or frees one twice.
- **Decide at the ritual:** whether pages hold real tensors, with attention reading keys and values through the block table (nano-vLLM does this with flash-attn, which needs CUDA), or the allocator keeps the books beside a contiguous cache.

### 11. Prefix caching
- **Learn:** reusing the KV cache for shared prefixes such as system prompts and chat history.
- **Practise:** hashing (vLLM hashes each full block from its parent block's hash, its tokens and extra keys such as the LoRA ID); LRU, as a hash map plus a doubly linked list; tries and radix trees (SGLang's approach).
- **Build:** both versions, chained block hashes and a radix tree. Compare hit rates on a chat workload that shares a system prompt.
- **Done when:** both versions reuse the same number of tokens on the test workload, and eviction follows LRU.

### 12. Scheduling and chunked prefill
- **Learn:** prefill vs decode; time to first token (TTFT) vs inter-token latency (ITL); chunking long prompts; priorities; preemption. vLLM's scheduler has no separate prefill and decode phases. Each request has tokens computed and tokens still to compute, and every step hands out a token budget. Splitting prefill and decode across machines, as a concept.
- **Practise:** heaps (a priority queue), greedy choices, sliding-window metrics.
- **Build:** decode-first scheduling with chunked prefill and priorities, reporting TTFT and ITL percentiles.
- **Done when:** p95 inter-token latency improves on a mix of long and short prompts, and long prompts still finish.

### 13. Speculative decoding and structured output
- **Learn:** draft, then verify; drafting from n-grams already in the prompt; acceptance rate; constraining output to a regex or a JSON schema with a state machine; tool calls as structured output.
- **Practise:** hashing (an n-gram index), two pointers (verifying drafts), stacks (JSON nesting), graphs (state machines, BFS), tries (over the vocabulary).
- **Build:** n-gram speculative decoding, and a JSON mode built from token masks.
- **Done when:** at temperature 0, speculative decoding gives the same output as normal decoding and reports its speed-up, and constrained output always parses.
- **Decide at the ritual:** one module or two.

## Phase 3 — Real vLLM (GPU)

### 14. Read nano-vLLM, then vLLM
- **Learn:** nano-vLLM first (about 1,200 lines of Python). It needs CUDA and Python below 3.13, so it runs on the rented GPU in its own environment. Then vLLM's engine loop, scheduler, KV cache manager, model runner and API server.
- **Practise:** reading code; tracing with a debugger.
- **Build:** trace one request end to end, and write a one-page map in my own words that matches each piece to my Phase 2 engine. Choose the pull request that ends Phase 3.
- **Done when:** the map is committed, and I can answer the tutor's "where does this happen?" quiz from memory.

### 15. Tuning and profiling
- **Learn:** vLLM's benchmark tools; `max_num_batched_tokens`, `max_num_seqs` and `gpu_memory_utilization`; what CUDA graphs and torch.compile remove; profiling a GPU workload with the PyTorch profiler and Nsight Systems; tensor parallelism and all-reduce at the level of concepts; splitting prefill and decode across machines, again as a concept.
- **Practise:** binary search on the answer, for the largest load that meets a latency target (Koko Eating Bananas).
- **Build:** a tuning report with charts, driven by the Module 8 load generator.
- **Done when:** the report gives the highest request rate that meets a p95 latency target, and explains why, with a profile of one decode step as evidence.

### 16. Quantization
- **Learn:** fp32, bf16, fp16, fp8, int8 and int4; quantizing weights only vs weights and activations; an fp8 KV cache; checking quality.
- **Practise:** bit manipulation, by packing and unpacking int4 in numpy.
- **Build:** serve one model at three precisions, measuring speed, memory and quality (perplexity plus a small task set).
- **Done when:** one table shows the trade-off, and my int4 packing round-trips exactly.

### 17. Fine-tuning and multi-LoRA serving
- **Learn:** LoRA; fine-tuning a small model for one task; serving several adapters on one base model.
- **Practise:** hashing and bucketing (grouping requests by adapter); LRU (an adapter cache).
- **Build:** train a LoRA, evaluate it on held-out data, then serve the base model with four adapters at once.
- **Done when:** the adapter beats the base model on held-out data, and the latency cost of 1 vs 4 adapters is measured.

### 18. Kernels: Triton, then CUDA
- **Learn:** how a GPU runs a kernel; Triton, which is written in Python; the same kernel in CUDA; finding my way in a C++ and CUDA codebase. Triton runs only on Linux with an NVIDIA or AMD GPU, so this module lives on the rented GPU.
- **Practise:** reading code; careful measurement.
- **Build:** read the Triton kernel inside nano-vLLM, which writes keys and values into the cache. Write one fused kernel in Triton, a softmax or RMSNorm. Write the same kernel in CUDA and call it from Python. Compare both with PyTorch.
- **Done when:** both kernels match PyTorch's output within tolerance, and the timing differences are measured and explained with a profile.
- **Decide at the ritual:** the details, from Triton's documentation as it stands then.

**Phase 3 is done when** one pull request of mine to vLLM, or to a project beside it such as llm-compressor, GuideLLM or production-stack, has been through a maintainer's review. Merged is the aim.

## Phase 4 — Serving open models for real

### 19. The front door, deployed
- **Learn:** routing across replicas, rate limits, health checks, graceful drain, autoscaling signals (queue depth, KV cache use), metrics; containers; Prometheus and Grafana, fed by the metrics vLLM already exports; Kubernetes at the size of one small cluster.
- **Practise:** consistent hashing (a sorted ring plus binary search), heaps (least-loaded replica), a token bucket, sliding windows.
- **Build:** a router in front of two or more replicas (vLLM or my engine) that routes by prefix, with a terminal dashboard. Then the deployment lab: the replicas in containers, their metrics on a dashboard, and autoscaling on queue depth.
- **Done when:** routing by prefix beats round-robin on cache hit rate and p95 latency, and the same setup runs from containers with its metrics on a dashboard.
- **Decide at the ritual:** how large the Kubernetes part is.

### 20. One model, three machines, four runtimes
- **Learn:** what changes across an NVIDIA GPU, Apple Silicon and a CPU with no GPU; GGUF and llama.cpp's quantization formats; memory-mapped weights; threads against cores; memory bandwidth; MLX; vLLM's backends for AMD (ROCm) and Google TPU, at the level of concepts.
- **Practise:** nothing new; careful measurement.
- **Build:** run one model on the rented GPU, the Mac and the Raspberry Pi, through four runtimes where each one runs: my engine, llama.cpp's Python bindings, MLX and vLLM. Produce a table of speed, memory, cost per million tokens, and whether the outputs agree. Stretch: an AMD GPU or a TPU, if I can get one.
- **Done when:** one script and a README reproduce the table.

## Capstone

The repository has been public since day one, so the capstone is the write-up of record: the engine, the router and the three-machine report as one piece, in my own words, with the pull request linked.

## Optional, after the capstone

### RAG serving
- **Learn:** embeddings; vector search (exact, IVF, HNSW); reranking; an end-to-end latency budget; caching.
- **Practise:** heaps (k nearest), k-means, graph search (HNSW is greedy search on a graph).
- **Build:** a RAG pipeline with my own top-k search, both exact and IVF, served behind the router.
- **Done when:** recall@k against a library is reported, along with p50 and p95 latency for each stage.

---

## Classic problems by pattern (names only, for the drills)

| Pattern | Problems | Where it shows up |
|---|---|---|
| Arrays and hashing | Two Sum; Top K Frequent Elements; Group Anagrams | BPE pair counts (2), top-k (4), block hashes (11) |
| Two pointers | Valid Palindrome; 3Sum; Merge Sorted Array | verifying drafts (13) |
| Sliding window | Longest Substring Without Repeating Characters; Sliding Window Maximum | repetition penalty (4), rate metrics (12, 19) |
| Stack | Valid Parentheses; Daily Temperatures | JSON nesting (13) |
| Binary search | Binary Search; Koko Eating Bananas; Search in Rotated Sorted Array | top-p cutoff (4), tuning (15), hash ring (19) |
| Linked lists | Reverse Linked List; Merge Two Sorted Lists; LRU Cache | free blocks (10), LRU eviction (11) |
| Trees and tries | Implement Trie; Longest Common Prefix; Word Search II | radix prefix cache (11), vocabulary trie (13) |
| Heaps | Kth Largest Element in an Array; Find Median from Data Stream; Task Scheduler | top-k (4), priorities (12), percentiles (1, 8), least-loaded routing (19) |
| Intervals | Merge Intervals; Meeting Rooms II | peak concurrency (9) |
| Greedy | Jump Game; Gas Station | token-budget admission (9, 12) |
| Graphs | Number of Islands; Course Schedule; Network Delay Time | state machines (13), HNSW (the optional RAG module) |
| Dynamic programming | Climbing Stairs; Word Break; Edit Distance | Unigram segmentation (2), output checks |
| Bit manipulation | Number of 1 Bits; Reverse Bits | int4 packing (16) |
| Design | LRU Cache; a rate limiter; a key-value store with expiry | 11, 19 |

## Reading (names only)

- **Phase 1:** Attention Is All You Need (2017); the GPT-2 paper (2019); RoFormer (2021), on rotary position embeddings.
- **Phase 2:** Orca (2022), on continuous batching; the vLLM paper on PagedAttention (2023); SGLang and RadixAttention (2024); Sarathi-Serve (2024), on chunked prefill; DistServe (2024), on splitting prefill and decode across machines; Fast Inference from Transformers via Speculative Decoding (2023); Efficient Guided Generation for Large Language Models (2023).
- **Phase 3:** vLLM's design docs (architecture, automatic prefix caching); nano-vLLM; FlashAttention (2022); GPTQ (2022); AWQ (2023); LoRA (2021); S-LoRA (2023); Triton's tutorials.
- **Phase 4:** the documentation of llama.cpp and MLX.
- **Optional (RAG):** HNSW (2016).

## Links

- nano-vLLM: https://github.com/GeeeekExplorer/nano-vllm
- vLLM prefix caching design: https://docs.vllm.ai/en/stable/design/prefix_caching/
- vLLM KV cache utilities (free block queue, block hashing): https://docs.vllm.ai/en/stable/api/vllm/v1/core/kv_cache_utils/
- vLLM scheduler: https://docs.vllm.ai/en/stable/api/vllm/v1/core/sched/scheduler/
- vLLM chunked prefill: https://docs.vllm.ai/en/stable/configuration/optimization/
- Triton's tutorials (fused softmax, layer norm): https://triton-lang.org/main/getting-started/tutorials/index.html
- TPU Research Cloud, for the stretch in Module 20: https://sites.research.google/trc/about/

---

## Changelog

- 2026-11-15: written; replaces the eight-week interview curriculum in `../interview-prep`, which
  stays private. The method comes from `../cpp-101` (paused).
- 2026-11-15, after an audit the same day: twenty modules instead of eighteen. New are 6 (the modern block,
  in PyTorch), 8 (a load generator and a first GPU baseline, the first half of the old 13) and 18
  (kernels: Triton, then CUDA, from the old optional line). The old 6 is now 7; the old 7 to 15 are 9
  to 17; the old 16 is 19 and gains a deployment lab; the old 18 is 20 and runs on a GPU, the Mac and a
  Raspberry Pi; the old 17 (RAG) is optional. The pull request ends Phase 3 instead of being optional,
  four short write-ups replace the single one, and "Done when" changed in 9, 14, 15 and 19. Ground rule 1
  and the goal are reworded. This file now holds still until Module 5 is done.
