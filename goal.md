# goal.md — LLM inference in Python

**Sun 15 Nov 2026 · Danish.** This file changes only between modules, with one dated line in the
[changelog](#changelog). A new idea goes to [docs/parking-lot.md](docs/parking-lot.md) first.

The spine of a self-paced course. I learn data structures and algorithms by building the parts of an inference engine, then I read vLLM, then I serve open models. It's Python all the way. This replaces the eight-week interview curriculum.

## The goal

By the end I can explain and build every layer of LLM serving: tokenizer, forward pass, sampling, KV cache, batching, paged memory, prefix caching, scheduling, speculative decoding and structured output. Then I can read vLLM's source without getting lost, tune it, quantize and fine-tune models for it, and serve open models behind a router, with retrieval (RAG), on more than one kind of hardware.

## Ground rules

- Python only. Kernels appear once, at the end, through Triton, which is written in Python.
- I type every solution. The tutor writes the problem statements, the tests and the explanations, never solution code.
- One concept at a time: short theory, then a challenge with tests.
- Every module ends with a measurement and five lines in my own words in `log.md`.
- Make it visible early. Use terminal visuals with `rich`: probability bars, block maps, batch animations.
- A module takes about a week at my pace. Move on when "Done when" passes, not when the week ends.

## Setup

- **Python tools:** Python 3.12+, uv, numpy, PyTorch (MPS on the Mac), safetensors, FastAPI with uvicorn, httpx, rich, pytest and hypothesis (property tests).
- **Models:** GPT-2 small (124M parameters) for Phase 1. A small modern open model from Phase 2 on, for example Qwen3-0.6B, the model nano-vLLM benchmarks with.
- **Hardware:** the MacBook for Phases 1 and 2. A GPU rented by the hour, or a free notebook GPU, for Phases 3 and 4. Google's TPU Research Cloud for the TPU run in Module 18.

## Each session

1. **Drill:** one or two classic problems for the module's pattern (table near the end), typed by hand and timed.
2. **Build:** the module's challenge.
3. **Measure:** run the harness from Module 1.
4. **Log:** five lines on what surprised me.

---

## Phase 1 — One model, one request (Mac)

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
- **Done when:** output is identical with and without the cache, and the speed-up and memory use are measured and explained.

## Phase 2 — Many requests: build a mini engine (Mac; PyTorch on MPS is fine)

### 6. Serving loop
- **Learn:** asyncio, the request lifecycle (waiting, running, finished), streaming over server-sent events, the shape of the OpenAI-compatible API.
- **Practise:** queues; state machines.
- **Build:** an async server with a subset of `/v1/completions` and `/v1/chat/completions` that streams tokens.
- **Done when:** ten clients streaming at once each get correct, uncorrupted output, and a cancelled request frees its resources.

### 7. Continuous batching
- **Learn:** static batching vs adding and removing requests at every step; a token budget per step.
- **Practise:** greedy admission; intervals (peak concurrency is the largest overlap of request lifetimes, which is Meeting Rooms II).
- **Build:** a step-level scheduler, and a terminal animation of batch slots filling and emptying.
- **Done when:** throughput beats static batching on a synthetic workload, and measured peak concurrency matches the interval calculation.

### 8. Paged KV cache
- **Learn:** fixed-size blocks, block tables, fragmentation, reference counts, copy-on-write when one prompt gets several samples, preemption by recomputation.
- **Practise:** linked lists. vLLM keeps free blocks in a doubly linked list with a dummy head and tail, so it can remove a block from the middle in O(1). Build the same.
- **Build:** a block allocator with alloc, free and fork, and a live block map in the terminal. Plug it into Module 7.
- **Done when:** a property test with thousands of random alloc, free and fork steps never leaks a block or frees one twice.

### 9. Prefix caching
- **Learn:** reusing the KV cache for shared prefixes such as system prompts and chat history.
- **Practise:** hashing (vLLM hashes each full block from its parent block's hash, its tokens and extra keys such as the LoRA ID); LRU, as a hash map plus a doubly linked list; tries and radix trees (SGLang's approach).
- **Build:** both versions, chained block hashes and a radix tree. Compare hit rates on a chat workload that shares a system prompt.
- **Done when:** both versions reuse the same number of tokens on the test workload, and eviction follows LRU.

### 10. Scheduling and chunked prefill
- **Learn:** prefill vs decode; time to first token (TTFT) vs inter-token latency (ITL); chunking long prompts; priorities; preemption. vLLM's scheduler has no separate prefill and decode phases. Each request has tokens computed and tokens still to compute, and every step hands out a token budget.
- **Practise:** heaps (a priority queue), greedy choices, sliding-window metrics.
- **Build:** decode-first scheduling with chunked prefill and priorities, reporting TTFT and ITL percentiles.
- **Done when:** p95 inter-token latency improves on a mix of long and short prompts, and long prompts still finish.

### 11. Speculative decoding and structured output
- **Learn:** draft, then verify; drafting from n-grams already in the prompt; acceptance rate; constraining output to a regex or a JSON schema with a state machine.
- **Practise:** hashing (an n-gram index), two pointers (verifying drafts), stacks (JSON nesting), graphs (state machines, BFS), tries (over the vocabulary).
- **Build:** n-gram speculative decoding, and a JSON mode built from token masks.
- **Done when:** at temperature 0, speculative decoding gives the same output as normal decoding and reports its speed-up, and constrained output always parses.

## Phase 3 — Real vLLM (GPU)

### 12. Read nano-vLLM, then vLLM
- **Learn:** nano-vLLM first (about 1,200 lines of Python). Then vLLM's engine loop, scheduler, KV cache manager, model runner and API server.
- **Practise:** reading code; tracing with a debugger.
- **Build:** trace one request end to end, and write a one-page map in my own words that matches each piece to my Phase 2 engine.
- **Done when:** I can answer the tutor's "where does this happen?" quiz from memory.

### 13. Performance and tuning
- **Learn:** vLLM's benchmark tools; `max_num_batched_tokens`, `max_num_seqs` and `gpu_memory_utilization`; what CUDA graphs and torch.compile remove; tensor parallelism and all-reduce at the level of concepts.
- **Practise:** binary search on the answer, for the largest load that meets a latency target (Koko Eating Bananas); streaming percentiles.
- **Build:** a load generator with realistic arrival times and lengths, and a tuning report with charts.
- **Done when:** the report gives the highest request rate that meets a p95 latency target, and explains why.

### 14. Quantization
- **Learn:** fp32, bf16, fp16, fp8, int8 and int4; quantizing weights only vs weights and activations; an fp8 KV cache; checking quality.
- **Practise:** bit manipulation, by packing and unpacking int4 in numpy.
- **Build:** serve one model at three precisions, measuring speed, memory and quality (perplexity plus a small task set).
- **Done when:** one table shows the trade-off, and my int4 packing round-trips exactly.

### 15. Fine-tuning and multi-LoRA serving
- **Learn:** LoRA; fine-tuning a small model for one task; serving several adapters on one base model.
- **Practise:** hashing and bucketing (grouping requests by adapter); LRU (an adapter cache).
- **Build:** train a LoRA, evaluate it on held-out data, then serve the base model with four adapters at once.
- **Done when:** the adapter beats the base model on held-out data, and the latency cost of 1 vs 4 adapters is measured.

Optional: one small pull request to vLLM, such as docs, a test or a small fix.

## Phase 4 — Serving open models for real

### 16. The front door
- **Learn:** routing across replicas, rate limits, health checks, graceful drain, autoscaling signals (queue depth, KV cache use), metrics.
- **Practise:** consistent hashing (a sorted ring plus binary search), heaps (least-loaded replica), a token bucket, sliding windows.
- **Build:** a router in front of two or more replicas (vLLM or my engine) that routes by prefix, with a terminal dashboard.
- **Done when:** routing by prefix beats round-robin on cache hit rate and p95 latency.

### 17. RAG serving
- **Learn:** embeddings; vector search (exact, IVF, HNSW); reranking; an end-to-end latency budget; caching.
- **Practise:** heaps (k nearest), k-means, graph search (HNSW is greedy search on a graph).
- **Build:** a RAG pipeline with my own top-k search, both exact and IVF, served behind the router.
- **Done when:** recall@k against a library is reported, along with p50 and p95 latency for each stage.

### 18. Other hardware
- **Learn:** what changes across NVIDIA, AMD (ROCm), Google TPU, Apple Silicon and CPU; vLLM's hardware backends; MLX or llama.cpp's Python bindings on the Mac.
- **Practise:** nothing new; careful measurement.
- **Build:** run one model on four kinds of hardware and produce a table of cost per million tokens and latency. Optional: write one Triton kernel, a fused softmax or RMSNorm, and compare it with PyTorch.
- **Done when:** one script and a README reproduce the table.

## Capstone

Publish one repo with the Phase 2 engine, the router, the RAG pipeline and the hardware report, plus a write-up in my own words.

---

## Classic problems by pattern (names only, for the drills)

| Pattern | Problems | Where it shows up |
|---|---|---|
| Arrays and hashing | Two Sum; Top K Frequent Elements; Group Anagrams | BPE pair counts (2), top-k (4), block hashes (9) |
| Two pointers | Valid Palindrome; 3Sum; Merge Sorted Array | verifying drafts (11) |
| Sliding window | Longest Substring Without Repeating Characters; Sliding Window Maximum | repetition penalty (4), rate metrics (10, 16) |
| Stack | Valid Parentheses; Daily Temperatures | JSON nesting (11) |
| Binary search | Binary Search; Koko Eating Bananas; Search in Rotated Sorted Array | top-p cutoff (4), tuning (13), hash ring (16) |
| Linked lists | Reverse Linked List; Merge Two Sorted Lists; LRU Cache | free blocks (8), LRU eviction (9) |
| Trees and tries | Implement Trie; Longest Common Prefix; Word Search II | radix prefix cache (9), vocabulary trie (11) |
| Heaps | Kth Largest Element in an Array; Find Median from Data Stream; Task Scheduler | top-k (4), priorities (10), percentiles (1, 13), least-loaded routing (16) |
| Intervals | Merge Intervals; Meeting Rooms II | peak concurrency (7) |
| Greedy | Jump Game; Gas Station | token-budget admission (7, 10) |
| Graphs | Number of Islands; Course Schedule; Network Delay Time | state machines (11), HNSW (17) |
| Dynamic programming | Climbing Stairs; Word Break; Edit Distance | Unigram segmentation (2), output checks |
| Bit manipulation | Number of 1 Bits; Reverse Bits | int4 packing (14) |
| Design | LRU Cache; a rate limiter; a key-value store with expiry | 9, 16 |

## Reading (names only)

- **Phase 1:** Attention Is All You Need (2017); the GPT-2 paper (2019).
- **Phase 2:** Orca (2022), on continuous batching; the vLLM paper on PagedAttention (2023); SGLang and RadixAttention (2024); Sarathi-Serve (2024), on chunked prefill; Fast Inference from Transformers via Speculative Decoding (2023); Efficient Guided Generation for Large Language Models (2023).
- **Phase 3:** vLLM's design docs (architecture, automatic prefix caching); nano-vLLM; FlashAttention (2022); GPTQ (2022); AWQ (2023); LoRA (2021); S-LoRA (2023).
- **Phase 4:** DistServe (2024), on splitting prefill and decode across machines; HNSW (2016).

## Links

- nano-vLLM: https://github.com/GeeeekExplorer/nano-vllm
- vLLM prefix caching design: https://docs.vllm.ai/en/stable/design/prefix_caching/
- vLLM KV cache utilities (free block queue, block hashing): https://docs.vllm.ai/en/stable/api/vllm/v1/core/kv_cache_utils/
- vLLM scheduler: https://docs.vllm.ai/en/stable/api/vllm/v1/core/sched/scheduler/
- vLLM chunked prefill: https://docs.vllm.ai/en/stable/configuration/optimization/
- TPU Research Cloud: https://sites.research.google/trc/about/

---

## Changelog

- 2026-11-15: written; replaces the eight-week interview curriculum in `../interview-prep`, which
  stays private. The method comes from `../cpp-101` (paused).
