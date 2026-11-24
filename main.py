#!/usr/bin/env python3
"""Two Lines to Your Past Self.

Writes exactly two lines to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output):
line one warns my past self about one specific moment, in a single
sentence; line two says in one sentence why that moment mattered and
what changed because of it. Gate: UTF-8 text, 1-280 characters.

Pure standard library, deterministic: the same two lines every run.
"""

import os
import sys

LINE_ONE = "Don't slide your phone into the taxi door pocket at 11:47 p.m. on the last night of the trip."
LINE_TWO = "It held the only photos of your grandmother laughing, and the taxi was already gone by the time you remembered."


def build_text() -> str:
    """Return the entry: exactly two lines, each exactly one sentence."""
    return LINE_ONE + "\n" + LINE_TWO + "\n"


def self_check(text: str) -> None:
    """Enforce the gate before writing: 2 lines, 1 sentence each, 1-280 chars."""
    if not (1 <= len(text) <= 280):
        raise ValueError(f"entry must be 1-280 chars, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        raise ValueError(f"entry must be exactly 2 lines, got {len(lines)}")
    for i, line in enumerate(lines, 1):
        # One sentence: a single terminal period. Abbreviations such as
        # "p.m." carry periods that are not sentence ends, so fold them
        # away before counting.
        folded = line.replace("p.m.", "pm").replace("a.m.", "am")
        if folded.count(".") != 1 or not line.endswith("."):
            raise ValueError(f"line {i} must be exactly one sentence: {line!r}")


def main() -> int:
    text = build_text()
    self_check(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Re-read and verify the bytes on disk are exactly what we built.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != text.encode("utf-8"):
        raise ValueError("entry.txt on disk differs from the built text")
    print(f"wrote {len(raw)} bytes to {path}")
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
