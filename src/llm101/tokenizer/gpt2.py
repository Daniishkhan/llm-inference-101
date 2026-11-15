"""GPT-2's tokenizer, loaded from its two files.

Milestone M5. The tests compare your ids with tiktoken's, which they build from the same two files,
and they read this file: it may not import tiktoken.

GPT-2's files are in data/gpt2/ (tools/fetch-gpt2-tokenizer.py fetches and checks them):

    vocab.json   a JSON object from each token, written as a string, to its id: 50,257 entries
    merges.txt   a first line "#version: 0.2", then one merge per line, in the order they were
                 learned: the two token strings, separated by one space

Both files write a token's bytes through bytes_to_unicode: each byte is shown as one printable
character, so that a token with a space or a newline in it can sit in a text file. "Ġworld" is
" world": Ġ (U+0120) stands for the space byte.
"""

from pathlib import Path

from llm101.tokenizer.bpe import Tokenizer

DATA = Path(__file__).resolve().parents[3] / "data" / "gpt2"
VOCAB_PATH = DATA / "vocab.json"
MERGES_PATH = DATA / "merges.txt"


def bytes_to_unicode() -> dict[int, str]:
    """GPT-2's map from each of the 256 byte values to one printable character, all different.

    - A byte whose character is printable and not a space keeps it: the bytes from 33 ("!") to 126
      ("~"), from 161 ("¡") to 172 ("¬") and from 174 ("®") to 255 ("ÿ") map to chr(b). That is 188
      bytes.
    - The other 68 bytes (0 to 32, 127 to 160, and 173) map, in rising order of the byte, to the
      characters chr(256), chr(257), chr(258), and so on.

        bytes_to_unicode()[ord("A")]  ->  "A"
        bytes_to_unicode()[0]         ->  "Ā"       chr(256): byte 0 is the first byte left over
        bytes_to_unicode()[32]        ->  "Ġ"       chr(288): the space
        bytes_to_unicode()[10]        ->  "Ċ"       chr(266): the newline
    """
    raise NotImplementedError("TODO(you)")


def load_gpt2(vocab_path: Path = VOCAB_PATH, merges_path: Path = MERGES_PATH) -> Tokenizer:
    """GPT-2's tokenizer, built from vocab.json and merges.txt: a Tokenizer from bpe.py.

    - byte_ids: the id that vocab.json gives to the one-character token for each byte, through
      bytes_to_unicode. Byte 33, "!", has id 0.
    - merges: one pair per line of merges.txt after the first, in order. Each line names two tokens,
      and the pair is their two ids from vocab.json. Merge r makes the token 256 + r, and vocab.json
      agrees: the token whose string is the two strings joined has that id.
    - special_tokens: {"<|endoftext|>": 50256}, the one token of vocab.json that no merge makes.

        tokenizer = load_gpt2()
        tokenizer.encode("Hello world")   ->  [15496, 995]
        tokenizer.decode([15496, 995])    ->  "Hello world"

    Read both files as UTF-8. The last line of merges.txt ends with a newline, so the file splits
    into one empty string after the last merge; that is not a merge.
    """
    raise NotImplementedError("TODO(you)")
