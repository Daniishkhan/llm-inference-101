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
| Module 6 | fastapi, uvicorn, httpx | The serving loop and its clients |
| Phase 2 | Qwen3-0.6B (about 1.5 GB); PyTorch on the Mac's GPU (MPS) | The modern open model of goal.md |
| Phase 3 | A GPU rented by the hour, or a free notebook GPU; vLLM | Real vLLM |
| Module 18 | Google's TPU Research Cloud, an AMD GPU by the hour | Other hardware |

**The TPU Research Cloud gives access by application** (goal.md, Links). Apply at the start of Phase 3,
so that the grant is there by Module 18, and plan the TPU run around the dates it gives.
