"""CLI interface for evidence-ledger."""

from __future__ import annotations

import argparse
from .ledger import EvidenceLedger


def main() -> None:
    parser = argparse.ArgumentParser(description="evidence-ledger: Cryptographic Claim Provenance Engine")
    subparsers = parser.add_subparsers(dest="command")

    p_add = subparsers.add_parser("add", help="Anchor a claim with citation evidence")
    p_add.add_argument("claim", help="Claim statement")
    p_add.add_argument("--source", "-s", required=True, help="Source URI or file path")
    p_add.add_argument("--content", "-c", required=True, help="Raw source content to hash")

    subparsers.add_parser("verify", help="Verify ledger cryptographic integrity")

    args = parser.parse_args()
    ledger = EvidenceLedger()

    if args.command == "add":
        packet = ledger.record_claim(
            claim=args.claim,
            source_uri=args.source,
            source_content=args.content,
        )
        print(f"Claim Packet Created: [{packet.claimEvidenceContract.receiptRef.receiptId}]")
        print(f"Source SHA-256: {packet.claimEvidenceContract.sourceReference.contentHash}")
        print(f"Packet Hash: {packet.packetHash}")
    elif args.command == "verify":
        valid, err = ledger.verify_ledger()
        if valid:
            print("Evidence Ledger: 100% Verified Clean!")
        else:
            print(f"Verification FAILED: {err}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
