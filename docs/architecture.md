# Architecture

```mermaid
flowchart LR
  A[Buyer request] --> B[Intent compiler]
  B --> C[Explicit confirmation]
  C --> D[Canonical hash]
  D --> E[Admissibility gate]
  F[Local catalogue] --> G[Text detector + sanitizer]
  F --> E
  E --> H[Bounded ranker]
  G --> H
  H --> I[Structured relevance]
  I --> J[Final reload + validation]
  J --> K{Decision engine}
  K -->|ALLOW only| L[Test payment adapter]
  K -->|BLOCK / ESCALATE| M[Evidence UI]
  C --> N[Hash-chain ledger]
  K --> N
  L --> N
```

`guard/` owns authorization logic. `payments/` receives a validated decision rather than raw price/SKU input. `audit/` records tamper-evident events. `evaluation/` uses only `FakePaymentSink`.

