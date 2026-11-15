# BENCH: Module 2, Tokenizer

Fill this in at M7. Book chapter 6 explains the measurement. You count with your own GPT-2 tokenizer
(M5) and time with your own harness from Module 1 (`time_calls`, then `summarise`).

## The machine

| Date | Machine | Power | Python | tiktoken |
|---|---|---|---|---|
| | MacBook, Apple M5, 24 GB, macOS 26.7.2 | mains | 3.13.18 | 0.14.0 |

## Experiment

**Question.** The same sentence in six languages and scripts: how many GPT-2 tokens does each take?
And on a long text, how much faster is tiktoken than your encoder, and what does `apply_merges_fast`
save over `apply_merges` when the chunks are short?

**Prediction.** Write it before you run anything: numbers and a reason. Commit it on its own
(`M7: prediction`) before you measure.

- the Hindi sentence takes about ___ times as many tokens as the English one, because
- tiktoken is about ___ times faster than your encoder, because
- on short chunks `apply_merges_fast` is ___ (faster, about as fast, slower) than `apply_merges`,
  because

**The sentences.** Each says *The weather is nice today, so we are going to walk to the river*; the
last is a line of Python of about the same length.

| Language | Sentence |
|---|---|
| English | The weather is nice today, so we are going to walk to the river. |
| German | Das Wetter ist heute schön, also gehen wir zu Fuß zum Fluss. |
| Spanish | Hoy hace buen tiempo, así que vamos a caminar hasta el río. |
| Hindi | आज मौसम अच्छा है, इसलिए हम नदी तक पैदल जा रहे हैं। |
| Chinese | 今天天气很好，所以我们要走路去河边。 |
| Python | for day in range(7): print(day, temperatures[day] * 1.8 + 32) |

**Measurement 1: tokens.** With your `load_gpt2()`, or the program (`uv run python -m llm101.tokenizer
"..."`), which prints all three counts.

| Language | Characters | UTF-8 bytes | Tokens | Tokens against English |
|---|---|---|---|---|
| English | | | | 1.0 |
| German | | | | |
| Spanish | | | | |
| Hindi | | | | |
| Chinese | | | | |
| Python | | | | |

**Measurement 2: speed.** The text is the source of Python's `argparse` module
(`inspect.getsource(argparse)`, about 100,000 characters). Time each line at least 20 recorded calls
after 2 warm-up calls.

- The first two lines time the whole text through your `load_gpt2()` tokenizer and through tiktoken.
- The last two time only the merging. Split the text with `pretokenize` once and turn each chunk into
  its byte ids before you start the clock; then one call merges every chunk, with `apply_merges` or
  with `apply_merges_fast`, and the ranks your Tokenizer keeps (it is your class: you know where).

Characters per second is the text's characters divided by the p50 in seconds, for the merging lines too.

| What | n | p50 | p95 | Calls/s | Characters per second |
|---|---|---|---|---|---|
| Your `load_gpt2().encode` | | | | | |
| tiktoken, `encode_ordinary` | | | | | |
| Merging every chunk with `apply_merges` | | | | | |
| Merging every chunk with `apply_merges_fast` | | | | | |

**Explanation.** Two sentences: why the token counts differ as they do, and why the speeds do.

## A long word (optional)

`apply_merges` against `apply_merges_fast` on one chunk of 1,000, 2,000, 4,000 and 8,000 letters with no
space between them: p50 of each. Tabulate them, and say how each one's time grows each time the length
doubles, and why.
