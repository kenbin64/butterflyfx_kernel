"""Universal SRL and connector utilities.

This module provides a richer Secure Resource Locator (SRL) and a small
set of connector adapter primitives so substrates may be bound to local
or remote data sources (files, databases, HTTP APIs, streaming
endpoints, cloud stores, email, device drivers, etc.). It also exposes
lightweight verification helpers (timestamp, bitcount) and a "Lens"
adapter that projects a substrate into meaningful observed attributes.

Design goals:
- Keep adapters minimal and dependency-free where possible (use stdlib)
- Provide a consistent ConnectorAdapter interface for pluggable
  transports
- Provide verification metadata (timestamp, bitcount) to help verify
  veracity of fetched data
"""

from __future__ import annotations

import hashlib
import sqlite3
import typing as t
from dataclasses import dataclass, field
from datetime import datetime, timezone
from urllib import request as urlrequest
from pathlib import Path

T = t.TypeVar("T")


class ConnectorAdapter:
    """Base class for connector adapters.

    Implementations should override connect/fetch/stream/send/close as
    appropriate for the transport.
    """

    def __init__(self, endpoint: str, *, credentials: t.Optional[dict] = None):
        self.endpoint = endpoint
        self.credentials = credentials or {}
        self.connected = False

    def connect(self) -> bool:
        """Establish connection to the endpoint. Return True on success."""
        self.connected = True
        return self.connected

    def fetch(self, query: t.Optional[str] = None) -> bytes:
        """Fetch a single payload (synchronous). Returns raw bytes."""
        raise NotImplementedError()

    def stream(self, query: t.Optional[str] = None):
        """Return an iterator/generator yielding bytes chunks or messages."""
        raise NotImplementedError()

    def send(self, payload: bytes, *, meta: t.Optional[dict] = None) -> bool:
        """Send payload to the endpoint. Return True on success."""
        raise NotImplementedError()

    def close(self) -> None:
        self.connected = False


class LocalFileAdapter(ConnectorAdapter):
    def fetch(self, query: t.Optional[str] = None) -> bytes:
        path = Path(self.endpoint)
        if not path.exists():
            raise FileNotFoundError(self.endpoint)
        return path.read_bytes()

    def stream(self, query: t.Optional[str] = None):
        path = Path(self.endpoint)
        with path.open("rb") as f:
            for line in f:
                yield line


class HTTPAdapter(ConnectorAdapter):
    def fetch(self, query: t.Optional[str] = None) -> bytes:
        url = self.endpoint
        if query:
            url = f"{self.endpoint}?{query}"
        req = urlrequest.Request(url)
        # simple auth header if provided
        if self.credentials.get("token"):
            req.add_header("Authorization", f"Bearer {self.credentials['token']}")
        with urlrequest.urlopen(req, timeout=10) as resp:
            return resp.read()


class SQLiteAdapter(ConnectorAdapter):
    def __init__(self, endpoint: str, *, credentials: t.Optional[dict] = None):
        super().__init__(endpoint, credentials=credentials)
        self._conn: t.Optional[sqlite3.Connection] = None

    def connect(self) -> bool:
        self._conn = sqlite3.connect(self.endpoint)
        self.connected = True
        return True

    def fetch(self, query: t.Optional[str] = None) -> bytes:
        if not self._conn:
            self.connect()
        cur = self._conn.cursor()
        cur.execute(query or "SELECT name FROM sqlite_master WHERE type='table';")
        rows = cur.fetchall()
        return str(rows).encode("utf-8")

    def close(self) -> None:
        if self._conn:
            self._conn.close()
        self.connected = False


class DummyEmailAdapter(ConnectorAdapter):
    def fetch(self, query: t.Optional[str] = None) -> bytes:
        # Placeholder - in real usage integrate imaplib or similar
        return b"From: example@example.com\nSubject: Test\nBody: hello"


def bitcount(data: bytes) -> int:
    """Return the population count (number of 1-bits) of the SHA-256 digest of data.

    Using the digest reduces dependency on input size while still providing a
    fingerprint suitable for lightweight veracity checks.
    """
    digest = hashlib.sha256(data).digest()
    # count bits
    return sum(bin(b).count("1") for b in digest)


def timestamp_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class SRL:
    """Secure Resource Locator (universal connector) binding a substrate to a source.

    Attributes:
    - substrate: any object that represents the conceptual substrate
    - adapter: ConnectorAdapter instance for I/O
    - last_fetched: timestamp of last fetch
    - last_payload: raw bytes of last fetched value
    - metadata: optional dict with keys like 'query', 'request_id', 'credentials'
    """

    substrate: t.Any
    adapter: ConnectorAdapter
    metadata: dict = field(default_factory=dict)
    last_fetched: t.Optional[str] = None
    last_payload: t.Optional[bytes] = None

    def resolve(self) -> dict:
        """Resolve the substrate to a canonical endpoint and return resolution info."""
        info = {
            "endpoint": getattr(self.adapter, "endpoint", None),
            "adapter": self.adapter.__class__.__name__,
            "substrate": repr(self.substrate),
        }
        info.update(self.metadata)
        return info

    def connect(self) -> bool:
        return self.adapter.connect()

    def fetch(self, query: t.Optional[str] = None) -> bytes:
        payload = self.adapter.fetch(query=query)
        self.last_payload = payload
        self.last_fetched = timestamp_now()
        return payload

    def stream(self, query: t.Optional[str] = None):
        for chunk in self.adapter.stream(query=query):
            self.last_payload = chunk
            self.last_fetched = timestamp_now()
            yield chunk

    def send(self, payload: bytes, *, meta: t.Optional[dict] = None) -> bool:
        return self.adapter.send(payload, meta=meta if meta is not None else self.metadata)

    def verify(self) -> dict:
        """Return verification metadata for the last payload: timestamp and bitcount."""
        if self.last_payload is None:
            return {"ok": False, "reason": "no payload"}
        return {
            "timestamp": self.last_fetched,
            "bitcount": bitcount(self.last_payload),
            "sha256": hashlib.sha256(self.last_payload).hexdigest(),
        }

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"SRL(substrate={self.substrate!r}, adapter={self.adapter!r})"


class LensConnector:
    """A lens-like observer that projects an SRL-substrate binding into attributes.

    The LensConnector is intended to be the bridge between a conceptual
    substrate and a concrete data source: it uses an SRL to fetch/stream
    data, then gleans natural attributes (counts, ranges, fingerprints)
    that are useful for downstream lenses or analytics.
    """

    def __init__(self, srl: SRL):
        self.srl = srl

    def glean(self, *, sample_limit: int = 10) -> dict:
        """Fetch the current payload and return observed attributes.

        Observed attributes include:
        - source metadata (endpoint, adapter)
        - fetch timestamp
        - payload size and bitcount fingerprint
        - simple numeric heuristics: record_count if payload looks like lines
        """
        info = self.srl.resolve()
        try:
            payload = self.srl.fetch(query=self.srl.metadata.get("query"))
        except Exception as e:
            return {"ok": False, "error": str(e), **info}

        size = len(payload)
        bc = bitcount(payload)
        sample_preview = None
        try:
            # try to interpret as UTF-8 text
            text = payload.decode("utf-8")
            lines = text.splitlines()
            record_count = len(lines)
            sample_preview = lines[:sample_limit]
        except Exception:
            record_count = None

        observed = {
            "source": info,
            "fetched_at": self.srl.last_fetched,
            "size_bytes": size,
            "bitcount": bc,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "record_count": record_count,
            "sample_preview": sample_preview,
        }
        return observed


__all__ = [
    "ConnectorAdapter",
    "LocalFileAdapter",
    "HTTPAdapter",
    "SQLiteAdapter",
    "DummyEmailAdapter",
    "SRL",
    "LensConnector",
    "bitcount",
    "timestamp_now",
]
