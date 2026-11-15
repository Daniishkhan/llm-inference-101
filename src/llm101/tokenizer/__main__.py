"""The tokenizer as a program: show where the tokens of a text begin and end.

    uv run python -m llm101.tokenizer "Hello, wörld!"               GPT-2's tokens of a text
    uv run python -m llm101.tokenizer --file notes.txt              the tokens of a file's text
    uv run python -m llm101.tokenizer --train notes.txt "some text" a tokenizer trained on a file

Arguments:

    TEXT              the text to tokenize
    --file PATH       tokenize the text of this file instead (read as UTF-8)
    --train PATH      train a tokenizer on the text of this file (pretokenize it, then train_bpe),
                      and use it instead of GPT-2's
    --vocab-size N    with --train, the size of the vocabulary to train (default 512)

Exactly one of TEXT and --file. With neither, or both, the program stops with argparse's usage
message and exit status 2.

What it prints, in this order:

    1. The text, token by token. Each token is its own bytes, decoded on their own with
       errors="replace", on a background colour that alternates between two, so that you can see
       where one token ends and the next begins. A token that holds part of a character shows "�".
    2. The ids, on one line, separated by single spaces.
    3. One line: "N tokens, C characters, B bytes", where C counts the characters of the text and B
       its UTF-8 bytes.

main is milestone M5.
"""


def main(argv: list[str] | None = None) -> None:
    """Read the arguments (argv, or the command line when argv is None), tokenize the text with
    GPT-2's tokenizer or with one trained by --train, and print the tokens, the ids and the
    count."""
    raise NotImplementedError("TODO(you)")


if __name__ == "__main__":
    main()
