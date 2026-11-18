#!/usr/bin/env python3
"""Entry for make.fun news-image-20261117: "The World in One Day".

Copies the entry image (entry.png, a newspaper front page summing up
Tuesday 17 November 2026) to /output/entry.png. Standard library only,
no network, deterministic: the same bytes are written on every run.

Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
SRC = HERE / "entry.png"
DST = OUT_DIR / "entry.png"

# The contest gate: a whole PNG, at most 1 MiB and 1024 x 1024 px.
# Refuse to write anything that is not a valid PNG within those limits.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576

data = SRC.read_bytes()
if not data.startswith(PNG_MAGIC):
    sys.exit("entry.png is not a PNG file")
if len(data) > MAX_BYTES:
    sys.exit(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
width = int.from_bytes(data[16:20], "big")
height = int.from_bytes(data[20:24], "big")
if width > 1024 or height > 1024:
    sys.exit(f"entry.png is {width}x{height}, over the 1024x1024 limit")

OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, DST)
print(f"wrote {DST} ({width}x{height}, {len(data)} bytes, "
      f"sha256 {hashlib.sha256(data).hexdigest()[:16]}...)")
