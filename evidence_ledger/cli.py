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
    p_add.add_argument("--snippet", "-q", required=True, help="Exact quoted snippet from source")

    subparsers.add_parser("verify", help="Verify ledger cryptographic integrity")

    args = parser.parse_args()
    ledger = EvidenceLedger()

    if args.command == "add":
        entry = ledger.record_claim(
            statement=args.claim,
            source_uri=args.source,
            source_text=args.snippet,
            snippet=args.snippet,
        )
        print(f"Claim Recorded: [{entry.claim_id}]")
        print(f"Hash: {entry.entry_hash}")
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
