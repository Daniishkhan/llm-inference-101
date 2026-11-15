# CONCEPTS.md: the concept graph

Every pattern, inference concept, Python tool and piece of maths in the course: the module that
introduces it, the modules that use it again, and whether you own it yet. It was seeded on 15 Nov 2026
from [goal.md](goal.md), and renumbered the same day when goal.md went from 18 modules to 20. When a
module's spec is frozen, its README cites the rows it **introduces** and **reuses**, and this file is
updated in the same commit.

Use it for spaced retrieval ([docs/methodology.md](docs/methodology.md)): each day, five rows marked
`in progress` or `owned`, explained out loud in two sentences with one example, without looking.

**Status:** `planned` (not reached yet), `in progress` (being learned now), `owned` (used correctly in a
module *and* explained in a review), `rusty` (failed a retrieval check; revisit). M1 is Module 1, and so
on; D00 is the diagnostic drill set; RAG is the optional module after the capstone.

## Patterns

| Concept | Classic problems (drills) | Introduced | Reused | Status |
|---|---|---|---|---|
| Arrays and hashing: a dict or set to remember what you have seen | Two Sum; Top K Frequent Elements; Group Anagrams | D00, M1 drills | M2 (pair counts), M4 (top-k), M11 (block hashes), M13 (n-gram index), M17 (requests by adapter) | in progress |
| Partition around a pivot; quickselect | Sort Colors; Kth Largest Element in an Array | M1 (percentiles) | M4 (top-k) | in progress |
| Big-O: counting operations, best, average and worst case | | M1 (quickselect against sorting) | every module; M3 (attention is quadratic) | in progress |
| Two pointers | Valid Palindrome; 3Sum; Merge Sorted Array | M13 (verifying drafts) | | planned |
| Sliding window | Longest Substring Without Repeating Characters; Sliding Window Maximum | M4 (repetition penalty) | M12, M19 (rate metrics) | planned |
| Stack | Valid Parentheses; Daily Temperatures | D00 (balanced brackets) | M13 (JSON nesting) | in progress |
| Binary search, and binary search on the answer | Binary Search; Koko Eating Bananas; Search in Rotated Sorted Array | M4 (top-p cutoff) | M15 (tuning), M19 (hash ring) | planned |
| Linked lists, singly and doubly linked, with dummy head and tail | Reverse Linked List; Merge Two Sorted Lists; LRU Cache | M2 (merging in place) | M10 (free blocks), M11 (LRU) | planned |
| Trees, tries and radix trees | Implement Trie; Longest Common Prefix; Word Search II | M11 (radix prefix cache) | M13 (vocabulary trie) | planned |
| Heaps and priority queues | Kth Largest Element in an Array; Find Median from Data Stream; Task Scheduler | M2 (best merge first) | M4 (top-k), M8 (streaming percentiles), M12 (priorities), M19 (least-loaded), RAG (k nearest) | planned |
| Intervals | Merge Intervals; Meeting Rooms II | D00 (merge intervals) | M9 (peak concurrency) | in progress |
| Greedy | Jump Game; Gas Station | M9 (token-budget admission) | M12 | planned |
| Graphs: BFS, DFS, topological order, shortest paths | Number of Islands; Course Schedule; Network Delay Time | M13 (state machines) | RAG (HNSW) | planned |
| Dynamic programming | Climbing Stairs; Word Break; Edit Distance | M2 stretch (Unigram segmentation) | output checks | planned |
| Bit manipulation | Number of 1 Bits; Reverse Bits | M16 (int4 packing) | | planned |
| Dynamic arrays and amortised cost; ring buffers | | M5 (the cache grows) | M10 | planned |
| Queues and state machines | | M7 (the request lifecycle) | M9, M13 | planned |
| Consistent hashing; a token bucket | | M19 | | planned |
| k-means | | RAG (IVF) | | planned |
| Design: an LRU cache, a rate limiter, a key-value store with expiry | LRU Cache; a rate limiter | M11 | M17, M19 | planned |

## Inference and serving

| Concept | Introduced | Reused | Status |
|---|---|---|---|
| Latency as a distribution: p50, p95, p99, tails | M1 | M8, M12 (TTFT and ITL), M15, M19 | in progress |
| Throughput, and the trade-off with latency | M1 | M8, M9, M15 | in progress |
| Bytes and UTF-8; byte-pair encoding; tokens as cost | M2 | M3, M11, M13 | planned |
| Embeddings, attention, MLP, layer norm, logits | M3 | M5, M6, Phase 2 | planned |
| Attention cost grows with the square of the sequence length | M3 | M5, M12 | planned |
| Decoding strategies: greedy, temperature, top-k, top-p, repetition penalty, seeds, stop strings | M4 | M7, M13 | planned |
| The KV cache, and memory per token = 2 × layers × KV heads × head size × bytes per value | M5 | M6, M10, M11, M15, M16 | planned |
| A machine with no GPU: the Raspberry Pi column in every `BENCH.md` | M5 | M6, M20 | planned |
| The modern block: rotary positions, RMSNorm, SwiGLU, grouped-query attention; batching with padding and masks | M6 | M9, M14 | planned |
| The request lifecycle (waiting, running, finished); streaming over server-sent events; the OpenAI-compatible API; chat templates; token accounting | M7 | M8, M9, M19 | planned |
| Closed-loop against open-loop load; arrival times and lengths; TTFT and ITL for each request | M8 | M12, M15, M19 | planned |
| Profiling a GPU workload: the PyTorch profiler, Nsight Systems | M8 | M15, M18 | planned |
| Static against continuous batching; a token budget per step | M9 | M12, M15 | planned |
| Paged KV cache: blocks, block tables, fragmentation, reference counts, copy-on-write, preemption by recomputation | M10 | M11, M14 | planned |
| Prefix caching: chained block hashes, LRU eviction, radix trees | M11 | M14, M19 | planned |
| Prefill against decode; TTFT against ITL; chunked prefill; priorities; preemption; splitting prefill and decode across machines | M12 | M14, M15 | planned |
| Speculative decoding: draft, verify, acceptance rate | M13 | M14 | planned |
| Structured output: token masks from a regex or a JSON schema; tool calls | M13 | | planned |
| vLLM's engine loop, scheduler, KV cache manager, model runner and API server | M14 | M15 to M20 | planned |
| Tuning knobs: `max_num_batched_tokens`, `max_num_seqs`, `gpu_memory_utilization`; CUDA graphs, torch.compile; tensor parallelism | M15 | M20 | planned |
| Number formats (fp32, bf16, fp16, fp8, int8, int4); weight-only against weight-and-activation quantization; an fp8 KV cache | M16 | M20 | planned |
| LoRA, and serving several adapters on one base model | M17 | | planned |
| How a GPU runs a kernel; one kernel in Triton and the same one in CUDA | M18 | | planned |
| Routing across replicas, rate limits, health checks, graceful drain, autoscaling signals | M19 | | planned |
| Containers; Prometheus and Grafana; Kubernetes with autoscaling on queue depth | M19 | | planned |
| One model across an NVIDIA GPU, Apple Silicon and a CPU with no GPU; GGUF, memory-mapped weights, threads against cores, memory bandwidth | M20 | | planned |
| Embeddings for retrieval; exact, IVF and HNSW search; reranking; a latency budget | RAG | | planned |

## Python and tools

| Concept | Introduced | Reused | Status |
|---|---|---|---|
| Wall time against CPU time: `time.perf_counter_ns`, `time.process_time_ns` | M1 ([ch. 1](docs/book/01-measure/01-two-clocks.html)) | every measurement | in progress |
| Profiling: cProfile and pstats; tracing against sampling; `sys.settrace`, frames and line numbers | M1 ([ch. 5](docs/book/01-measure/05-where-the-time-goes.html)) | M3, M8, M14 | in progress |
| Boxed objects and `sys.getsizeof`; why numpy beats Python loops | M1 ([ch. 6](docs/book/01-measure/06-boxes-and-arrays.html)) | M3, M5, M16 | in progress |
| rich: `Console`, `Table`, bars, a live display | M1 ([ch. 4](docs/book/01-measure/04-pictures-in-the-terminal.html)) | M4, M9, M10, M19 | in progress |
| pytest; hypothesis property tests and shrinking | M1 ([ch. 2](docs/book/01-measure/02-tails-and-percentiles.html)) | every module; M10 (random alloc and free) | in progress |
| `dataclasses`, type hints | M1 | every module | in progress |
| `bytes`, `str.encode`, `heapq` | M2 | M4, M12 | planned |
| numpy shapes, broadcasting, matrix multiplication; safetensors | M3 | M5, M6, M16 | planned |
| PyTorch: tensors, devices, dtypes, inference without gradients; MPS on the Mac, CUDA on the rented GPU | M6 | Phase 2, Phase 3 | planned |
| asyncio; FastAPI and uvicorn; httpx | M7 | M8, M9, M19 | planned |
| Working on a rented GPU over ssh | M8 | Phase 3, M20 | planned |
| A debugger on someone else's code | M14 | M18 | planned |
| llama.cpp's Python bindings; MLX | M20 | | planned |

## Maths

| Concept | Introduced | Reused | Status |
|---|---|---|---|
| Percentiles and linear interpolation between ranks; histograms | M1 ([ch. 2](docs/book/01-measure/02-tails-and-percentiles.html)) | M8, M12, M15 | in progress |
| Expected value, used for quickselect's average case | M1 ([ch. 3](docs/book/01-measure/03-partition-and-select.html)) | M4 | in progress |
| Matrix multiplication as many dot products; shapes | M3 | M5, M6, M16, M17 | planned |
| Softmax, and the stable form (log-sum-exp) | M3 | M4 | planned |
| Probability distributions and cumulative sums | M4 | M13 | planned |
| Turning a pair of numbers by an angle (rotary positions) | M6 | | planned |
| Requests arriving at random at a given rate | M8 | M15 | planned |
| Log-likelihood and perplexity | M16 | M17 | planned |
| Distance and similarity between vectors (dot product, cosine) | RAG | | planned |
