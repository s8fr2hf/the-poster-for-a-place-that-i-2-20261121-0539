#!/usr/bin/env python3
"""Luminara travel poster entry.

Writes the poster image to /output/entry.png. The poster itself is the file
entry.png next to this script; this program copies it to the output
directory. Pure standard library, no network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(dst, "rb") as f:
        head = f.read(len(PNG_MAGIC))
        ihdr = f.read(25)
    if head != PNG_MAGIC:
        print("error: output is not a PNG", file=sys.stderr)
        return 1
    # IHDR: 4-byte length, "IHDR", then width and height as big-endian u32.
    width = int.from_bytes(ihdr[8:12], "big")
    height = int.from_bytes(ihdr[12:16], "big")
    if (width, height) != (1024, 1024):
        print(f"error: expected 1024x1024, got {width}x{height}", file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes", f"{width}x{height}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
