#!/usr/bin/env python3
"""make.fun entry for the "Sum up 18 November's world news in one image" bounty.

The program writes the day's news poster to /output/entry.png. It needs no
network and no third-party packages: the poster is shipped in this repository
as entry.png and copied byte for byte, so two runs write identical bytes.
"""
import os
import sys
from pathlib import Path

ENTRY_NAME = "entry.png"
OUTPUT_DIR = Path("/output")
REPO_DIR = Path(__file__).resolve().parent
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def check_payload(payload: bytes) -> str:
    """Return an error message when the poster breaks the gate, else ''."""
    if not payload.startswith(PNG_SIGNATURE):
        return "the poster is not a PNG file"
    if len(payload) > MAX_BYTES:
        return f"the poster is {len(payload)} bytes, over the 1 MiB cap"
    return ""


def main() -> int:
    """Copy the poster from the repository into the output directory."""
    source = REPO_DIR / ENTRY_NAME
    if not source.is_file():
        print(f"error: {source} is missing", file=sys.stderr)
        return 2

    payload = source.read_bytes()
    problem = check_payload(payload)
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 2
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / ENTRY_NAME).write_bytes(payload)
    print(f"wrote {OUTPUT_DIR / ENTRY_NAME} ({len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
