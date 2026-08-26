# Threat model

In scope are indirect prompt injection in local synthetic titles/descriptions, hard-constraint manipulation, technically admissible but weakly relevant manipulation, and ranking disagreement before order creation.

Structured catalogue fields are trusted. Merchant lies in those fields, compromised payment credentials/infrastructure, browsers, arbitrary external services, universal detection, and real loss estimation are out of scope.

The transparent detector normalizes NFKC, lowercases, collapses whitespace, removes zero-width characters, and scores five signal families: instruction-to-agent language (0.7), role imitation (0.7), ranking manipulation (0.45), hidden/encoded content (0.4), and agent-directed imperatives (0.45). The threshold is frozen in `evaluation/frozen_config.yaml`. Marketing language can false-positive; evaluation must report that rather than conceal it.

