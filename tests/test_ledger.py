"""Tests for evidence-ledger cryptographic proof chain."""

from evidence_ledger import EvidenceLedger


def test_claim_recording_and_verification():
    ledger = EvidenceLedger()
    doc_text = "The speed of light in vacuum is approximately 299,792,458 meters per second."
    c1 = ledger.record_claim(
        statement="Light travels at ~300,000 km/s in vacuum",
        source_uri="physics_constants.txt",
        source_text=doc_text,
        snippet="299,792,458 meters per second",
    )
    assert c1.citations[0].verified is True
    valid, err = ledger.verify_ledger()
    assert valid is True
    assert err is None


def test_tamper_detection():
    ledger = EvidenceLedger()
    doc = "System throughput is 50,000 RPS."
    ledger.record_claim("Throughput is 50k RPS", "bench.txt", doc, "50,000 RPS")
    
    # Tamper with statement
    ledger.entries[0].statement = "Throughput is 500,000 RPS"
    valid, err = ledger.verify_ledger()
    assert valid is False
    assert "Tampered record" in err
