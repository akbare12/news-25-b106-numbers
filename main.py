#!/usr/bin/env python3
"""Entry point for the make.fun grader (stdlib only).

Copies the pre-rendered entry.png into MAKEFUN_OUTPUT_DIR. No PIL,
no numpy, no third-party imports: the grader image is stdlib-only.
Render first with:  python3 gen.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
os.makedirs(OUT_DIR, exist_ok=True)
DST = os.path.join(OUT_DIR, "entry.png")

shutil.copyfile(SRC, DST)
print("copied", SRC, "->", DST, os.path.getsize(DST), "bytes")
# stdlib only: os + shutil. No PIL / numpy here by design.
