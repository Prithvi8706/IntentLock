# Decision Guard

Decision Guard prevents agent-induced wrong-item returns by checking whether an AI buyer's selection satisfies the buyer's confirmed intent before a Razorpay order can be created.

An LLM may rank products, but it cannot authorize a transaction. Only the deterministic decision engine can produce `ALLOW`; the payment boundary rejects every other outcome. The included demo uses a fake payment sink by default so it runs without credentials. `RazorpayOrderClient` supports Test Mode only and rejects non-`rzp_test_` keys.

## Quick start

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. Use the guard toggle to compare the shared baseline and protected paths.

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

