#!/usr/bin/env python3
"""news-23 b136 numbers-led: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
and refuses an output directory that is empty, a file, or inside the repository.
Verifies the PNG header (IHDR 1024x1024, bit depth 8, colour type 2/6, no interlace),
walks every chunk checking CRCs, requires at least one non-empty IDAT, requires IEND
as the final chunk with no trailing data, and re-reads the output to confirm it is
byte-identical to the source before printing the sha256.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "678d88eb4b72aaba762c07fb0a081244d355ec43a822e51cd6a3add1a4565692"  # entry.png, filled by the builder after the final render


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def check_png(path):
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    if len(data) < 10_000:
        fail("PNG too small")
    if len(data) > 1_048_576:
        fail("PNG over 1 MiB")
    # first chunk must be a 13-byte IHDR: width, height, bit depth, colour type,
    # compression, filter, interlace (layout: 4-byte length + 4-byte type + data + CRC)
    pos = 8
    clen = struct.unpack(">I", data[pos:pos + 4])[0]
    ctype = data[pos + 4:pos + 8]
    if ctype != b"IHDR" or clen != 13:
        fail("first chunk is not a 13-byte IHDR")
    ihdr = data[pos + 8:pos + 8 + 13]
    width, height, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (width, height) != (1024, 1024):
        fail(f"bad dimensions {width}x{height}, expected 1024x1024")
    if depth != 8 or ctype_b not in (2, 6):
        fail(f"bad bit depth {depth} / colour type {ctype_b}")
    if comp != 0 or filt != 0 or inter != 0:
        fail("bad compression/filter/interlace flags")
    stored_crc = struct.unpack(">I", data[pos + 8 + 13:pos + 8 + 13 + 4])[0]
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != stored_crc:
        fail("IHDR CRC mismatch")
    # walk the remaining chunks, checking every CRC; IDAT payload must be non-empty
    pos = pos + 8 + clen + 4
    idat_bytes = 0
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 8 + clen + 4 > len(data):
            fail(f"truncated chunk {ctype!r}")
        chunk_data = data[pos + 8:pos + 8 + clen]
        stored_crc = struct.unpack(">I", data[pos + 8 + clen:pos + 8 + clen + 4])[0]
        if zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF != stored_crc:
            fail(f"CRC mismatch in chunk {ctype!r}")
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_bytes += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if pos + 8 + clen + 4 != len(data):
                fail("trailing data after IEND")
            saw_iend = True
            break
        # next chunk starts after this chunk's data + its 4-byte CRC
        pos = pos + 8 + clen + 4
    if not saw_iend:
        fail("missing IEND chunk")
    if idat_bytes < 1000:
        fail("IDAT payload too small")
    return data


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if os.path.commonpath([out_dir_abs, here]) == here and out_dir_abs != here:
        fail("MAKEFUN_OUTPUT_DIR is inside the repository")
    if out_dir_abs == here:
        fail("MAKEFUN_OUTPUT_DIR is the repository itself")
    data = check_png(src)
    if EXPECTED_SHA256 is not None:
        actual = hashlib.sha256(data).hexdigest()
        if actual != EXPECTED_SHA256:
            fail(f"source sha256 mismatch: {actual} != {EXPECTED_SHA256}")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        fail("output is not byte-identical to the source")
    print("sha256:", hashlib.sha256(written).hexdigest())
    print("wrote", dst, len(written), "bytes")


if __name__ == "__main__":
    main()
