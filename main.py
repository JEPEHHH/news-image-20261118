#!/usr/bin/env python3
"""Ship the 18 November 2026 news poster to the grader's output folder.

The entry is the picture itself: this program validates the shipped PNG and
places it at /output/entry.png. Nothing here reaches the network, imports a
third-party package, or reads the clock, so repeated runs are byte-identical.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

POSTER = "entry.png"
TARGET_DIR = Path("/output")
SIDE_LIMIT = 1_048_576
MAGIC = b"\x89PNG\r\n\x1a\n"


class PosterError(Exception):
    """Raised when the shipped picture cannot be handed to the grader."""


def png_geometry(blob: bytes) -> tuple[int, int]:
    """Read width and height out of an IHDR chunk without any library."""
    if not blob.startswith(MAGIC):
        raise PosterError("the shipped file is not a PNG (no signature)")
    if len(blob) < 33 or blob[12:16] != b"IHDR":
        raise PosterError("the PNG carries no IHDR header")
    width, height = struct.unpack(">II", blob[16:24])
    if width == 0 or height == 0:
        raise PosterError("the PNG reports a zero side")
    return width, height


def validate(blob: bytes) -> tuple[int, int]:
    """Return the picture's geometry once every intake rule is satisfied."""
    if len(blob) > SIDE_LIMIT:
        raise PosterError(f"the picture is {len(blob)} bytes, past the 1 MiB intake cap")
    width, height = png_geometry(blob)
    if width != height:
        raise PosterError(f"the picture is {width}x{height}; this bounty wants a square")
    return width, height


def locate() -> Path:
    """The poster travels beside this program, so resolve it from __file__."""
    here = Path(__file__).resolve().parent
    candidate = here / POSTER
    if not candidate.is_file():
        raise PosterError(f"no {POSTER} next to the program ({here})")
    return candidate


def deliver(source: Path) -> Path:
    """Copy the picture to the output folder the grader mounts and return it."""
    blob = source.read_bytes()
    width, height = validate(blob)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    destination = TARGET_DIR / POSTER
    destination.write_bytes(blob)
    print(f"{destination}: {width}x{height}, {len(blob)} bytes")
    return destination


def run() -> int:
    try:
        deliver(locate())
    except PosterError as complaint:
        print(f"poster not delivered: {complaint}", file=sys.stderr)
        return 1
    except OSError as complaint:
        print(f"poster not delivered: {complaint}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run())
