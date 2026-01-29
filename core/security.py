# core/security.py
"""
Streaming hashing and verification helpers.

These functions compute SHA-256 digests and bitcounts from iterators of bytes,
so large payloads can be verified without loading them entirely into memory.
"""

from __future__ import annotations
import hashlib
from typing import Iterator


def sha256_stream(chunks: Iterator[bytes]) -> str:
    """
    Compute SHA-256 hex digest from an iterator of byte chunks.
    """
    h = hashlib.sha256()
    for c in chunks:
        h.update(c)
    return h.hexdigest()


def bitcount_of_digest_hex(hex_digest: str) -> int:
    """
    Compute the population count (number of 1-bits) of a hex digest.
    """
    b = bytes.fromhex(hex_digest)
    return sum(bin(x).count("1") for x in b)
