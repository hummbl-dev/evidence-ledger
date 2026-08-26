"""Tests for authentic Schema v0.1 Claim-Evidence Packet verification."""

import os
from evidence_ledger import EvidenceLedger


def test_claim_packet_schema_v01():
    ledger = EvidenceLedger()
    raw_source = "Anthropic was founded in 2021 by former OpenAI executives."
    packet = ledger.record_claim(
        claim="Anthropic was founded in 2021",
        source_uri="company_profile.txt",
        source_content=raw_source,
    )

    d = packet.to_dict()
    assert d["schemaVersion"] == "0.1"
    assert d["packetStatus"] == "verified"
    assert d["claimEvidenceContract"]["sourceReference"]["contentHash"] is not None
    
    valid, err = ledger.verify_ledger()
    assert valid is True
    assert err is None


def test_tamper_detection():
    ledger = EvidenceLedger()
    ledger.record_claim("Statement A", "srcA", "Source A text")
    ledger.record_claim("Statement B", "srcB", "Source B text")

    # Maliciously mutate claim text
    ledger.packets[0].claimEvidenceContract.claim = "Tampered Statement"
    valid, err = ledger.verify_ledger()
    assert valid is False
    assert "Tampered packet detected" in err


def test_persist_and_reload(tmp_path):
    """Claims persisted to disk survive process restart and verify correctly."""
    db = tmp_path / "ledger.jsonl"
    l1 = EvidenceLedger(persist_path=str(db))
    l1.record_claim("Claim A", "srcA", "Content A")
    l1.record_claim("Claim B", "srcB", "Content B")
    assert db.exists()
    assert len(l1.packets) == 2

    # New instance loads from file
    l2 = EvidenceLedger(persist_path=str(db))
    assert len(l2.packets) == 2
    assert l2._last_hash == l1._last_hash
    valid, err = l2.verify_ledger()
    assert valid is True
    assert err is None
