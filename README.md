# Decision Guard

Decision Guard prevents agent-induced wrong-item returns by checking whether an AI buyer's selection satisfies the buyer's confirmed intent before a Razorpay order can be created.

> **Current status: early scaffold, not submission-ready.** The repository currently uses a deterministic local ranking stub and a fake payment sink in the web demo. Real model integration, a real Razorpay Test Mode order, the full benchmark, frozen results, and complete evidence capture remain to be implemented. See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for the verified gap analysis.

The intended guarantee is that an LLM may rank products but cannot authorize a transaction. The current scaffold contains the beginnings of that boundary, but it has not yet been demonstrated with a real model and Razorpay Test Mode order. The included demo uses a fake payment sink so it runs without credentials. `RazorpayOrderClient` supports Test Mode only and rejects non-`rzp_test_` keys, but it is not yet wired into the UI.

## Quick start

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. Use the guard toggle to compare the shared baseline and protected paths. When `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are present in `.env`, the final purchase action uses the Razorpay Test Mode Orders API; without them, the UI uses a local fake sink for development.

```bash
python -m pytest
python -m evaluation.runner --dataset heldout
python -m audit.verify
```

## Security chain

```text
buyer request -> confirmed + hashed intent -> deterministic admissibility gate
              -> untrusted-text scan -> bounded ranker -> final validation
              -> ALLOW | BLOCK | ESCALATE -> ALLOW-only test payment boundary
              -> append-only hash-chained ledger
```

The synthetic catalogues trust structured fields and treat titles and descriptions as untrusted. Dishonest structured fields, universal prompt-injection protection, live payments, and real financial-loss estimates are out of scope. See [threat model](docs/threat-model.md), [architecture](docs/architecture.md), and [evaluation method](docs/evaluation.md).

## Evaluation

The committed fixtures are intentionally small starter data, not publishable evidence. `evaluation.runner` runs both modes with a deterministic local adapter and a fake payment sink, writes episode JSONL and Wilson-interval metrics to a versioned results directory, and never imports the Razorpay client. Run `python scripts/freeze.py` only when the dataset and thresholds are ready to freeze.

## Defense-only statement

This repository contains fixed, local, synthetic safety fixtures. It has no attack generator, arbitrary URL input, external target, or live-payment path.
