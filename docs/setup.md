# Setup: this Mac, the first time, and what arrives later

## This machine (checked Sun 15 Nov 2026)

| | |
|---|---|
| Machine | MacBook, Apple M5: 4 performance cores and 6 efficiency cores, 24 GB of memory, 765 GB free |
| OS | macOS 26.7.2 |
| uv | 0.13.7 |
| Python | 3.13.18 (installed with mise). The project pins 3.13 in `.python-version`; Homebrew's 3.14 and 3.15 are also installed and unused here |
| In `.venv` | numpy 2.5.4, rich 15.0.0; for development pytest 9.2.0, hypothesis 6.170.15, ruff 0.17.5 |
| git, gh | git 2.56.0; gh 2.103.3, signed in as `Daniishkhan` |
| Editor | Zed, with edit predictions and completion off for this project (`.zed/settings.json`) |

## The other two machines

| | |
|---|---|
| The Raspberry Pi | A Pi 5 with 4 GB of memory or less: four CPU cores and no GPU. It joins in Module 5. GPT-2 small is about 0.5 GB of weights, so your numpy engine fits. Its exact model, memory and operating system are recorded here at Module 5's ritual |
| The rented GPU | By the hour, from Module 8 on. The card, its memory, the image and the hourly price are recorded here the first time you rent one |

A number without its machine and date is not evidence, and from Module 5 on there is more than one
machine.

## The first time

```sh
cd ~/Desktop/projects/llm-inference-101
uv sync                            # creates .venv with Python 3.13 and the dependencies
tools/install-hooks.sh             # the pre-commit hook
uv run pytest tests/m01            # red on day one: that is the starting line
uv run python tools/serve-book.py  # the book at http://localhost:8767
```

Open the folder in Zed (`zed .` once the CLI is installed from Zed's menu, or File, Open). Zed finds
`.venv` by itself, so imports of `llm101` and numpy resolve.

## Five-minute check, when something feels off

```sh
uv run python -c "import llm101, numpy, rich; print('ok')"
uv run ruff check . && uv run ruff format --check .
uv run python tools/book-check.py
```

## Measuring on this Mac

macOS decides which cores a Python process runs on, and the M5 has two kinds. So for numbers you want
to compare: plug in the power cable, close anything heavy, run each measurement at least three times,
and report the median with the date and the machine. A number without its machine and date is not
evidence. Each module's `BENCH.md` has columns for this.

## What arrives when

Dependencies arrive with the module that needs them, so that nothing is installed for weeks before it
is used. Claude adds them in that module's spec ritual.

| When | What | Why |
|---|---|---|
| Now | numpy, rich; pytest, hypothesis, ruff | Module 1, and the book's examples |
| Module 2 | tiktoken (development only) | The oracle that your tokenizer's ids are checked against |
| Module 2 | GPT-2's `vocab.json` and `merges.txt` (about 1.5 MB), fetched by a tools script | The merges your tokenizer loads |
| Module 3 | safetensors, huggingface_hub | Loading GPT-2's weights |
| Module 3 | GPT-2 small's `model.safetensors` (about 550 MB) into `models/`, which git ignores | The weights |
| Module 3 | torch and transformers (development only; torch from the CPU index on CI) | Reference logits that your numpy model is checked against |
| Module 5 | The Raspberry Pi: uv, Python 3.13 and a clone of this repository, reached over ssh | The machine with no GPU. Its numbers get their own column in `BENCH.md` from here on |
| Module 6 | torch as a dependency of your own code; Qwen3-0.6B (about 1.5 GB) | The modern block, in PyTorch on the Mac's GPU (MPS) |
| Module 7 | fastapi, uvicorn, httpx | The serving loop and its clients |
| Module 8 | A GPU rented by the hour, with vLLM on it | The first GPU baseline |
| Module 14 | nano-vLLM in its own environment on the rented GPU | It needs CUDA and Python below 3.13, and this project pins 3.13 |
| Module 18 | Triton and the CUDA toolkit, on the rented GPU | Triton runs only on Linux with an NVIDIA or AMD GPU |
| Module 20 | llama.cpp's Python bindings; MLX | One model on the GPU, the Mac and the Pi |
| Module 20, stretch | An AMD GPU by the hour; Google's TPU Research Cloud | Only if you can get one |

**The TPU Research Cloud gives access to researchers, by application** (goal.md, Links). It is a
stretch goal of Module 20. If you want that row in the table, apply at the start of Phase 3 and plan the
run around the dates it gives.
