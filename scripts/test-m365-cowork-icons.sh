#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Exercise the dependency-free Cowork PNG parser and the 24-icon fleet gate.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT/scripts"

python3 "$ROOT/scripts/validate_m365_cowork_icons.py"

python3 - <<'PY'
from __future__ import annotations

import struct
import zlib

from validate_m365_cowork_icons import (
    IconValidationError,
    validate_png_bytes,
)

SIGNATURE = b"\x89PNG\r\n\x1a\n"
WIDTH = 3
HEIGHT = 5
ROW_BYTES = WIDTH * 4


def chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = zlib.crc32(payload, zlib.crc32(kind)) & 0xFFFFFFFF
    return (
        struct.pack(">I", len(payload))
        + kind
        + payload
        + struct.pack(">I", checksum)
    )


def paeth(left: int, above: int, upper_left: int) -> int:
    prediction = left + above - upper_left
    distances = (
        abs(prediction - left),
        abs(prediction - above),
        abs(prediction - upper_left),
    )
    return (left, above, upper_left)[distances.index(min(distances))]


def filtered_row(
    row: bytes,
    previous: bytes,
    filter_type: int,
    bytes_per_pixel: int = 4,
) -> bytes:
    encoded = bytearray()
    for index, value in enumerate(row):
        left = (
            row[index - bytes_per_pixel]
            if index >= bytes_per_pixel
            else 0
        )
        above = previous[index]
        upper_left = (
            previous[index - bytes_per_pixel]
            if index >= bytes_per_pixel
            else 0
        )
        predictors = (
            0,
            left,
            above,
            (left + above) // 2,
            paeth(left, above, upper_left),
        )
        encoded.append((value - predictors[filter_type]) & 0xFF)
    return bytes([filter_type]) + bytes(encoded)


def image_rows(*, visible: bool = True) -> list[bytes]:
    rows = []
    for row_index in range(HEIGHT):
        row = bytearray()
        for column in range(WIDTH):
            alpha = 255 if visible and (row_index or column) else 0
            row.extend(
                (
                    20 + row_index,
                    40 + column,
                    60 + row_index + column,
                    alpha,
                ),
            )
        rows.append(bytes(row))
    return rows


def color_rows(first_alpha: int) -> list[bytes]:
    rows = []
    for row_index in range(HEIGHT):
        row = bytearray()
        for column in range(WIDTH):
            alpha = first_alpha if not (row_index or column) else 255
            row.extend((20 + row_index, 40 + column, 60, alpha))
        rows.append(bytes(row))
    return rows


def rgb_color_rows() -> list[bytes]:
    rows = []
    for row_index in range(HEIGHT):
        row = bytearray()
        for column in range(WIDTH):
            row.extend((20 + row_index, 40 + column, 60))
        rows.append(bytes(row))
    return rows


def outline_rows(
    *,
    transparent_background: bool,
    colored_pixel: bool = False,
) -> list[bytes]:
    rows = []
    for row_index in range(HEIGHT):
        row = bytearray()
        for column in range(WIDTH):
            is_origin = not (row_index or column)
            alpha = 0 if transparent_background and is_origin else 255
            rgb = (
                (20, 40, 60)
                if colored_pixel and (row_index, column) == (0, 1)
                else (255, 255, 255)
            )
            row.extend((*rgb, alpha))
        rows.append(bytes(row))
    return rows


def scanlines(
    rows: list[bytes],
    filters: tuple[int, ...] = (0, 1, 2, 3, 4),
    bytes_per_pixel: int = 4,
) -> bytes:
    previous = bytes(WIDTH * bytes_per_pixel)
    encoded = bytearray()
    for row, filter_type in zip(rows, filters, strict=True):
        encoded.extend(
            filtered_row(
                row,
                previous,
                filter_type,
                bytes_per_pixel,
            ),
        )
        previous = row
    return bytes(encoded)


def png(
    raw: bytes,
    *,
    width: int = WIDTH,
    height: int = HEIGHT,
    bit_depth: int = 8,
    color_type: int = 6,
    interlace: int = 0,
) -> bytes:
    header = struct.pack(
        ">IIBBBBB",
        width,
        height,
        bit_depth,
        color_type,
        0,
        0,
        interlace,
    )
    return png_with_idat(header, zlib.compress(raw))


def png_with_idat(header: bytes, compressed: bytes) -> bytes:
    """Build a PNG around caller-supplied IHDR and compressed IDAT bytes."""
    return (
        SIGNATURE
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )


def expect_failure(
    label: str,
    data: bytes,
    fragment: str,
    *,
    icon_kind: str | None = None,
) -> None:
    try:
        validate_png_bytes(
            data,
            (WIDTH, HEIGHT),
            label,
            icon_kind=icon_kind,
        )
    except IconValidationError as error:
        if fragment not in str(error):
            raise AssertionError(
                f"{label}: expected {fragment!r}, got {error!s}",
            ) from error
    else:
        raise AssertionError(f"{label}: malformed PNG was accepted")


valid_raw = scanlines(image_rows())
valid = png(valid_raw)
validate_png_bytes(valid, (WIDTH, HEIGHT), "all-filter-types")
validate_png_bytes(
    png(scanlines(color_rows(255))),
    (WIDTH, HEIGHT),
    "valid-color",
    icon_kind="color",
)
validate_png_bytes(
    png(
        scanlines(rgb_color_rows(), bytes_per_pixel=3),
        color_type=2,
    ),
    (WIDTH, HEIGHT),
    "valid-rgb-color",
    icon_kind="color",
)
validate_png_bytes(
    png(scanlines(outline_rows(transparent_background=True))),
    (WIDTH, HEIGHT),
    "valid-outline",
    icon_kind="outline",
)

bad_crc = bytearray(valid)
idat_offset = valid.index(b"IDAT")
bad_crc[idat_offset + 5] ^= 1
expect_failure("crc", bytes(bad_crc), "CRC mismatch")
expect_failure("signature", b"not-png", "signature")
expect_failure("dimensions", png(valid_raw, width=WIDTH + 1), "dimensions")
expect_failure("bit-depth", png(valid_raw, bit_depth=16), "8-bit RGB or RGBA")
expect_failure("color-type", png(valid_raw, color_type=0), "8-bit RGB or RGBA")
expect_failure("interlace", png(valid_raw, interlace=1), "no interlace")
expect_failure(
    "short-decode",
    png(valid_raw[: ROW_BYTES + 1]),
    "decoded data length",
)

bad_filter = bytes([5]) + valid_raw[1:]
expect_failure("filter", png(bad_filter), "filter type 5")
expect_failure(
    "transparent",
    png(scanlines(image_rows(visible=False))),
    "visible pixel",
)
expect_failure(
    "transparent-color-pixel",
    png(scanlines(color_rows(0))),
    "alpha 255",
    icon_kind="color",
)
expect_failure(
    "partial-color-pixel",
    png(scanlines(color_rows(128))),
    "alpha 255",
    icon_kind="color",
)
expect_failure(
    "opaque-outline-background",
    png(scanlines(outline_rows(transparent_background=False))),
    "transparent pixel",
    icon_kind="outline",
)
expect_failure(
    "colored-outline-pixel",
    png(
        scanlines(
            outline_rows(
                transparent_background=True,
                colored_pixel=True,
            ),
        ),
    ),
    "pure white",
    icon_kind="outline",
)
expect_failure(
    "rgb-outline",
    png(
        scanlines(rgb_color_rows(), bytes_per_pixel=3),
        color_type=2,
    ),
    "outline IHDR must declare 8-bit RGBA",
    icon_kind="outline",
)
expect_failure("trailing", valid + b"x", "trailing data")
expect_failure("missing-iend", valid[:-12], "missing IEND")

valid_header = struct.pack(
    ">IIBBBBB",
    WIDTH,
    HEIGHT,
    8,
    6,
    0,
    0,
    0,
)
compressed = zlib.compress(valid_raw)
known_plte = (
    SIGNATURE
    + chunk(b"IHDR", valid_header)
    + chunk(b"PLTE", b"\x00\x00\x00")
    + chunk(b"IDAT", compressed)
    + chunk(b"IEND", b"")
)
validate_png_bytes(known_plte, (WIDTH, HEIGHT), "known-critical-plte")

unknown_critical = (
    SIGNATURE
    + chunk(b"IHDR", valid_header)
    + chunk(b"ABCD", b"crc-valid-unknown-critical")
    + chunk(b"IDAT", compressed)
    + chunk(b"IEND", b"")
)
expect_failure(
    "unknown-critical",
    unknown_critical,
    "unsupported critical PNG chunk ABCD",
)

valid_unknown_ancillary = (
    SIGNATURE
    + chunk(b"IHDR", valid_header)
    + chunk(b"abCd", b"crc-valid-ancillary")
    + chunk(b"IDAT", compressed)
    + chunk(b"IEND", b"")
)
validate_png_bytes(
    valid_unknown_ancillary,
    (WIDTH, HEIGHT),
    "valid-unknown-ancillary",
)

rgb_header = struct.pack(
    ">IIBBBBB",
    WIDTH,
    HEIGHT,
    8,
    2,
    0,
    0,
    0,
)
rgb_compressed = zlib.compress(
    scanlines(rgb_color_rows(), bytes_per_pixel=3),
)
rgb_transparency = (
    SIGNATURE
    + chunk(b"IHDR", rgb_header)
    + chunk(b"tRNS", b"\x00\x14\x00\x28\x00\x3c")
    + chunk(b"IDAT", rgb_compressed)
    + chunk(b"IEND", b"")
)
expect_failure(
    "rgb-transparency",
    rgb_transparency,
    "tRNS transparency is not allowed",
    icon_kind="color",
)

invalid_reserved_type = (
    SIGNATURE
    + chunk(b"IHDR", valid_header)
    + chunk(b"abcd", b"crc-valid-invalid-reserved-bit")
    + chunk(b"IDAT", compressed)
    + chunk(b"IEND", b"")
)
expect_failure(
    "invalid-reserved-type",
    invalid_reserved_type,
    "reserved third byte must be uppercase",
)

invalid_nonletter_type = (
    SIGNATURE
    + chunk(b"IHDR", valid_header)
    + chunk(b"ab1D", b"crc-valid-nonletter-type")
    + chunk(b"IDAT", compressed)
    + chunk(b"IEND", b"")
)
expect_failure(
    "invalid-nonletter-type",
    invalid_nonletter_type,
    "exactly four ASCII letters",
)

invalid_nonascii_type = (
    SIGNATURE
    + chunk(b"IHDR", valid_header)
    + chunk(b"a\x80cD", b"crc-valid-nonascii-type")
    + chunk(b"IDAT", compressed)
    + chunk(b"IEND", b"")
)
expect_failure(
    "invalid-nonascii-type",
    invalid_nonascii_type,
    "exactly four ASCII letters",
)

expect_failure(
    "zlib-trailing",
    png_with_idat(valid_header, compressed + zlib.compress(b"x")),
    "trailing compressed data",
)
expect_failure(
    "zlib-incomplete",
    png_with_idat(valid_header, compressed[:-2]),
    "incomplete",
)

bomb_compressor = zlib.compressobj(level=9)
bomb_block = bytes(1024 * 1024)
bomb_parts = [
    bomb_compressor.compress(bomb_block)
    for _ in range(64)
]
bomb_parts.append(bomb_compressor.flush())
compressed_bomb = b"".join(bomb_parts)
expect_failure(
    "compressed-bomb",
    png_with_idat(valid_header, compressed_bomb),
    "output budget",
)

header = valid[: valid.index(b"IDAT") - 4]
split = len(compressed) // 2
noncontiguous = (
    header
    + chunk(b"IDAT", compressed[:split])
    + chunk(b"tEXt", b"gap")
    + chunk(b"IDAT", compressed[split:])
    + chunk(b"IEND", b"")
)
expect_failure("noncontiguous", noncontiguous, "contiguous")

print("m365 Cowork PNG parser fixtures: OK")
PY
