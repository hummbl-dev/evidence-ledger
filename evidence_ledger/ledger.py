"""Cryptographic Claim-Evidence Provenance Ledger."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class EvidenceCitation:
    source_uri: str
    content_hash: str
    snippet: str
    verified: bool = True


@dataclass
class ClaimEntry:
    claim_id: str
    statement: str
    citations: List[EvidenceCitation]
    timestamp: float
    prev_hash: str
    entry_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "statement": self.statement,
            "citations": [asdict(c) for c in self.citations],
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "entry_hash": self.entry_hash,
        }


class EvidenceLedger:
    """Tamper-evident append-only claim verification provenance ledger."""

    def __init__(self, log_path: Optional[str] = None) -> None:
        self.log_path = log_path
        self.entries: List[ClaimEntry] = []
        self._last_hash = "0" * 64

    def record_claim(self, statement: str, source_uri: str, source_text: str, snippet: str) -> ClaimEntry:
        """Record a factual claim anchored by a SHA-256 source content hash."""
        content_hash = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
        citation = EvidenceCitation(
            source_uri=source_uri,
            content_hash=content_hash,
            snippet=snippet,
            verified=snippet in source_text,
        )

        now = time.time()
        claim_id = f"clm_{hashlib.sha256(f'{statement}:{now}'.encode()).hexdigest()[:12]}"
        
        # Chained hash
        payload_repr = f"{claim_id}:{statement}:{content_hash}:{now:.6f}:{self._last_hash}"
        entry_hash = hashlib.sha256(payload_repr.encode("utf-8")).hexdigest()

        entry = ClaimEntry(
            claim_id=claim_id,
            statement=statement,
            citations=[citation],
            timestamp=now,
            prev_hash=self._last_hash,
            entry_hash=entry_hash,
        )

        self._last_hash = entry_hash
        self.entries.append(entry)

        if self.log_path:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")

        return entry

    def verify_ledger(self) -> Tuple[bool, Optional[str]]:
        """Verify hash chain integrity and citation validity across all claims."""
        expected_prev = "0" * 64
        for entry in self.entries:
            if entry.prev_hash != expected_prev:
                return False, f"Broken chain at claim {entry.claim_id}: prev_hash mismatch"
            
            c_hash = entry.citations[0].content_hash if entry.citations else ""
            payload_repr = f"{entry.claim_id}:{entry.statement}:{c_hash}:{entry.timestamp:.6f}:{entry.prev_hash}"
            calculated = hashlib.sha256(payload_repr.encode("utf-8")).hexdigest()
            if entry.entry_hash != calculated:
                return False, f"Tampered record at claim {entry.claim_id}: hash mismatch"
            
            expected_prev = entry.entry_hash

        return True, None
