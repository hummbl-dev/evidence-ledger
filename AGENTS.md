# AGENTS.md — evidence-ledger

## Project

**evidence-ledger** — Cryptographic Claim-Evidence Provenance Ledger for Auditable AI Reasoning.**.

## Scope

- In scope: Core implementation, documentation, configuration, and tests for evidence-ledger.
- Out of scope: Unreviewed upstream changes, unverified external dependencies, direct pushes to main.

## Governance & Behavioral DNA

This repository adheres to the HUMMBL Agent Fleet governance standards:
- Canonical agent contracts and governance rules derive from `.agents` and `apex-nexus`.
- Agents operating in this repository must follow the Crab Protocol and Bus Protocol where applicable.
- No runtime data or credentials in git: keep history, caches, and auth tokens out of version control.
- Conventional Commits required for all commits (`feat:`, `fix:`, `chore:`, `docs:`, etc.).
- Work must be performed on dedicated branches; direct pushes to `main` without review are prohibited.

## Conventions

- Branch naming: `type/agent/short-desc` (e.g., `chore/agent/governance-baseline`).
- Adhere to the zero-drift policy: keep configuration and contract copies synchronized with canonical definitions.
