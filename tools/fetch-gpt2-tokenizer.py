"""fetch-gpt2-tokenizer.py: download GPT-2's tokenizer files into data/gpt2/, and check them.

GPT-2's byte-level BPE tokenizer is two files, published by OpenAI with the model in 2019 (MIT
licence) and mirrored on the Hugging Face hub:

    vocab.json   every token as a string (bytes shown through GPT-2's byte-to-character map),
                 and its id: 50,257 entries
    merges.txt   a "#version" line, then the 50,000 merges in the order they were learned, one
                 per line: the two token strings, separated by one space

Module 2 loads them (src/llm101/tokenizer/gpt2.py), and its tests build tiktoken's GPT-2 encoding
from the same two files, so that the tests never need the network. The files are committed, so you
only need this script to fetch them again or to check them:

    uv run python tools/fetch-gpt2-tokenizer.py           # download whatever is missing, then check
    uv run python tools/fetch-gpt2-tokenizer.py --check   # check only; exit 1 on a mismatch

The check compares each file's SHA-256 with the one written below. These are the same bytes as
OpenAI's own copies (encoder.json and vocab.bpe at openaipublic.blob.core.windows.net/gpt-2/), which
tiktoken downloads for its "gpt2" encoding; this was checked on 15 Nov 2026.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "data" / "gpt2"
BASE = "https://huggingface.co/openai-community/gpt2/resolve/main/"
FILES = {
    "vocab.json": "196139668be63f3b5d6574427317ae82f612a97c5d1cdaf36ed2256dbf636783",
    "merges.txt": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(name: str) -> None:
    target = FOLDER / name
    print(f"fetching {BASE + name}")
    with urllib.request.urlopen(BASE + name, timeout=60) as response:
        data = response.read()
    target.write_bytes(data)
    print(f"  wrote {target.relative_to(ROOT)} ({len(data):,} bytes)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download and check GPT-2's tokenizer files.")
    parser.add_argument("--check", action="store_true", help="check only, download nothing")
    args = parser.parse_args(argv)

    FOLDER.mkdir(parents=True, exist_ok=True)
    bad = []
    for name, expected in FILES.items():
        path = FOLDER / name
        if not path.exists() and not args.check:
            fetch(name)
        if not path.exists():
            print(f"missing: {path.relative_to(ROOT)}")
            bad.append(name)
        elif sha256(path) != expected:
            print(f"wrong checksum: {path.relative_to(ROOT)} (delete it and run this again)")
            bad.append(name)
        else:
            print(f"ok: {path.relative_to(ROOT)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
