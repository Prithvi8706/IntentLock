# Implementation status

This document records the verified state of the repository against `Decision_Guard_7_Day_Implementation_Plan_v2.md`.

The current repository is an early scaffold. It is not an end-to-end AI agent and is not submission-ready.

## Present

- FastAPI and Jinja page skeleton with a guard-mode toggle.
- Pydantic schemas for intent, listings, decisions, and ledger events.
- Canonical JSON hashing helpers.
- Deterministic hard-constraint checks.
- A transparent pattern-based text detector.
- Structured relevance scoring.
- Basic `ALLOW`, `BLOCK`, and `ESCALATE` branches.
- A Test-Mode-only Razorpay client wired into the configured web demo.
- A fake payment sink for local tests.
- A file-locked SHA-256 hash-chain ledger.
- Small example fixtures and unit tests.

## Partial or incorrect

- Intent compilation is a regex parser rather than a strict model-backed compiler with retry and manual fallback.
- The ranker is a hard-coded deterministic stub rather than a JSON-validating hosted-model adapter.
- Final validation does not reload the intent by hash and SKU from trusted storage.
- The evidence page does not show the complete detector, sanitization, gate, ranking, and order evidence required by the plan.
- The app writes only a subset of required ledger events.
- The evaluation runner is sequential and calculates only a subset of required metrics.
- Tests cover useful units but not the full minimum suite from the plan.

## Missing release proofs

- Real Gemini or equivalent model calls.
- A graceful `ORDER_FAILED` demonstration in the UI.
- Ten to fifteen intent scenarios.
- One hundred to one hundred fifty benign listings.
- Thirty to forty adversarial fixtures grouped into non-overlapping families.
- Approximately 250–300 benign and 100–160 adversarial episodes.
- Frozen configuration and `FIXTURE_HASHES.txt`.
- Committed held-out result runs and figures.
- Listing-level detector metrics and all required episode-level breakdowns.
- Constraint-violation-rate assertion over committed results.
- Complete README result tables, limitations counts, screenshots, and submission video.

## Required implementation order

1. Make CI and clean-clone setup reliable.
2. Implement the real model adapter and strict intent/ranker JSON contracts.
3. Complete intent versioning and trusted reload-by-hash storage.
4. Connect detector sanitization, gate evidence, ranking evidence, and every ledger event.
5. Complete Razorpay failure-path evidence and Standard Checkout only if P0 finishes early.
6. Build and validate the complete calibration and held-out datasets.
7. Freeze configuration and fixtures before reading final results.
8. Run and commit the final evaluation, documentation, and demo evidence.

No P0 item should be marked complete merely because a file with the expected name exists.
