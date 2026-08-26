import hashlib
import json
from datetime import UTC, datetime
from typing import Any


def canonical_json(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha256_hex(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def hash_object(obj: dict[str, Any], excluded_field: str) -> str:
    return sha256_hex(canonical_json({k: v for k, v in obj.items() if k != excluded_field}))


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")

