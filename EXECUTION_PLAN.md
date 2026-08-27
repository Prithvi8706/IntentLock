# Decision Guard: 24-Hour Execution-Grade Plan

**Source of truth:** `Decision_Guard_7_Day_Implementation_Plan_v2.md`  
**Execution window:** 27 August to 2 September 2026  
**Submission target:** 3 September 2026  
**Committed effort:** 24 focused hours  
**Stretch capacity:** 6–12 additional hours, only after P0 passes  
**Primary model:** Gemini 2.5 Flash  
**Model budget:** free tier first; paid fallback capped at USD 5  
**Demo:** local FastAPI application plus recorded video  
**Payment:** Razorpay Test Mode only

This is the operational companion to Plan v2. Plan v2 explains the product, threat model, and target methodology. This document specifies the order of execution, exact proof required at each gate, files affected, commands run, time limits, and predetermined cuts.

---

## 1. Finish line

At hour 24, a fresh clone must demonstrate this complete chain:

```text
Natural-language buyer request
  -> model-compiled structured intent
  -> explicit buyer confirmation
  -> immutable intent version + canonical hash
  -> local catalogue text scan and sanitization
  -> deterministic hard-constraint gate
  -> Gemini ranks eligible sanitized listings only
  -> structured relevance comparison
  -> trusted reload-by-hash and reload-by-SKU final validation
  -> deterministic ALLOW | BLOCK | ESCALATE
  -> explicit final purchase confirmation
  -> Razorpay Test Mode order only from ALLOW
  -> complete tamper-evident ledger and evidence page
  -> frozen, resumable, fake-payment held-out evaluation
  -> committed results, limitations, README, and five-minute demo script
```

The project is complete only if the chain works end to end. A file, class, passing mock, or UI screen is not proof by itself.

### Release invariants

1. Hosted models never authorize payment.
2. Any exception, timeout, invalid JSON, schema failure, missing field, or unknown SKU fails closed.
3. Guard-on `ALLOW` is reachable only after every deterministic check passes.
4. Payment clients accept a validated `DecisionRecord`, never raw amount or SKU input from a request.
5. Razorpay keys must start with `rzp_test_`; live-looking keys fail startup and CI.
6. Evaluation never imports or calls the real Razorpay client.
7. Held-out fixture families are never used for threshold selection.
8. No hard-constraint-violating guard-on order may exist in committed results.
9. All catalogue and adversarial fixtures remain local, fixed, synthetic, and URL-free.
10. Claims in the README and video must be traceable to committed result files.

---

## 2. Resolved decisions

| Decision | Resolution | Consequence |
|---|---|---|
| Core time | 24 focused hours | P0 chain and evidence outrank optional features |
| Stretch time | 6–12 hours | Used only after every P0 release gate passes |
| Primary model | Gemini 2.5 Flash | Local deterministic adapter remains test/offline support only |
| Model spend | Free tier, USD 5 maximum fallback | Runner must cache and resume completed calls |
| Hosting | Local demo | Public deployment is P2 and excluded from core time |
| Benchmark size | Reduced, honest benchmark | Original Plan v2 counts become stretch targets |
| Core dataset target | 8 intents, 60–80 benign listings, 24–30 attacks, about 180 episodes | Both strata and family-level holdout remain mandatory |
| Payments | Razorpay Test Mode | Both controlled baseline and guarded safe path can create test orders after confirmation |
| Evaluation payments | Fake sink only | Benchmark cannot create external orders |
| Checkout completion | Order creation is P0 | Standard Checkout/signature verification remains P1 |
| Second model | Stretch only | One reproducible model is sufficient for P0 |

### Benchmark floor if time is lost

The dataset may be reduced once, transparently, to this minimum without cutting methodology:

- 6 confirmed intents;
- 40 benign listings;
- 16 adversarial listings across 8 families;
- 80 benign episodes and 40 adversarial episodes;
- equal representation of `hard_violating` and `admissible` attacks;
- at least four calibration-only and four held-out-only families.

Below this floor, the project can still be demonstrated but must not claim a meaningful held-out benchmark.

---

## 3. Verified starting state

### Completed and demonstrated

- Repository structure, pinned requirements, CI, lint, tests, URL scan, and secret scan.
- Canonical JSON and SHA-256 helpers.
- Pydantic intent, listing, decision, and ledger-event schemas.
- Deterministic category, usage, price, stock, and attribute gate.
- Transparent injection signal table and suspicious-span sanitization.
- Structured relevance score.
- Basic fail-closed decision ordering.
- File-locked hash-chain ledger primitive and verifier.
- Test-only payment-key enforcement and idempotency primitive.
- One protected Razorpay Test Mode order: `order_TUV7bq2owsl8PN`.
- Twenty-six current tests and a passing GitHub Actions run.

### Present but not P0-complete

- Intent compilation uses regex instead of Gemini structured output.
- Ranking uses `LocalDeterministicAdapter` instead of Gemini.
- Intent storage is process memory, not durable versioned storage.
- Final validation does not reload intent by hash from durable storage.
- Decision engine does not expose a complete evidence trace.
- The app writes only part of the required ledger event sequence.
- The evidence page omits original/sanitized text and per-SKU gate results.
- The runner is sequential, non-resumable, and incomplete.
- Dataset and metrics are starter examples only.
- Freeze configuration, fixture hashes, final results, figures, and final README are absent.

---

## 4. Quality-versus-time frontier

The best use of 24 hours is to increase proof quality in dependency order:

| Cumulative hours | Quality frontier | Observable proof |
|---:|---|---|
| 0–4 | Real agent behavior | Gemini compiles and ranks strict JSON; failures fail closed |
| 4–8 | Security boundary | Durable confirmed intent, trusted reload, complete decision trace |
| 8–10 | Judge-ready product flow | Baseline failure, guarded intervention, safe test order, evidence page |
| 10–14 | Credible dataset | Family-separated fixtures and deterministic episode construction |
| 14–17 | Reproducible measurement | Async/resumable runner and complete metrics |
| 17–19 | Honest experimental boundary | Calibration-only tuning, frozen config, fixture hashes |
| 19–21 | Trusted result | One held-out run, failure review, tables, figures |
| 21–22 | Judge comprehension | README, architecture, threat model, limitations |
| 22–24 | Reliability buffer | Fresh-clone test, rehearsal, CI, recovery from integration defects |

No UI polish, second model, cloud deployment, or Standard Checkout is allowed to consume time before hour 22.

---

## 5. Critical-path execution

### Phase 0 — Lock the workspace and external dependencies

**Budget:** 0.5 hour  
**Cumulative:** 0.5 / 24 hours  
**Goal:** make every later proof reproducible and prevent credential/setup surprises.

### Steps

1. Confirm `.env` is ignored and contains non-empty `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, and eventually `MODEL_API_KEY` without printing values.
2. Confirm Razorpay ID begins with `rzp_test_`.
3. Generate a Gemini API key in Google AI Studio; store it only in `.env`.
4. Set `MODEL_PRIMARY=gemini-2.5-flash`.
5. Add a startup configuration validator that distinguishes:
   - demo with full external integrations;
   - offline/test mode using injected fakes;
   - invalid partial credentials, which fail startup.
6. Repair cross-platform quick-start instructions. Keep `make` as the judge path and document PowerShell equivalents.
7. Run the current clean baseline before edits.

### Primary files

- `.env.example`
- `app/config.py`
- `app/main.py`
- `Makefile`
- `README.md`
- `tests/test_payment_boundary.py`

### Commands

```powershell
py -3.11 -m ruff check .
py -3.11 -m pytest
py -3.11 scripts/check_no_external_urls.py
```

### Gate 0

- [ ] CI is green on the starting commit.
- [ ] No secret value appears in Git, logs, screenshots, or test output.
- [ ] Missing or partial production-demo credentials fail with a readable error.
- [ ] Test/offline dependency injection still works without `.env`.

**Stop condition:** do not begin model integration until the Gemini key is locally available.

---

### Phase 1 — Replace stubs with a real bounded model layer

**Budget:** 3.5 hours  
**Cumulative:** 4 / 24 hours  
**Goal:** Gemini performs only compilation and ranking through strict, validated contracts.

### Step 1.1: Define adapter contracts

1. Split model concerns into explicit `compile_intent()` and `rank()` operations or two narrow protocols.
2. Define JSON response schemas before prompts:
   - intent fields exclude confirmation metadata and hashes;
   - ranking contains ordered eligible SKU IDs and short reasons only.
3. Store model ID, temperature, timeout, and retry policy in configuration.
4. Keep `LocalDeterministicAdapter` for unit tests and credential-free smoke tests, not final evidence.

### Step 1.2: Implement Gemini transport

1. Use the official Gemini SDK or a narrow HTTP adapter with an explicit timeout.
2. Request JSON/structured output where supported.
3. Retry once only for transport or rate-limit failures with bounded backoff.
4. Do not retry schema-invalid ranking into `ALLOW`.
5. Record latency and token/usage metadata when returned.
6. Redact API keys and avoid logging raw authorization headers.

### Step 1.3: Implement intent compilation

1. Send only `raw_request`; never pass catalogue data.
2. Validate the response with Pydantic.
3. Reject missing category, maximum price, or quantity.
4. Attempt compilation at most twice.
5. After two failures, render the manual intent form with no inferred authorization.
6. Log `INTENT_COMPILED` with the attempt count and model metadata.

### Step 1.4: Implement bounded ranking

1. Pass only the frozen intent projection and sanitized eligible listing projections.
2. Shuffle candidates with the recorded episode seed.
3. Validate non-empty output, no duplicates, and membership in the eligible set.
4. Treat unknown SKU, parse error, timeout, or missing output as `ESCALATE/RANKER_OUTPUT_INVALID`.

### Primary files

- `guard/model_adapter.py`
- `guard/intent_compiler.py`
- `guard/ranker.py`
- `guard/schemas.py`
- `app/config.py`
- `.env.example`
- `tests/test_intent.py`
- `tests/test_decision_engine.py`

### Required tests

- Compiler receives no catalogue argument or text.
- Valid Gemini-shaped JSON passes strict schema validation.
- Invalid JSON twice activates manual fallback.
- Missing hard intent fields never become an authorization.
- Transport error retries once and then fails closed.
- Unknown, duplicate, or empty ranked SKU list escalates.
- Ranker input contains eligible SKUs only and no matched injection spans.
- API keys cannot appear in captured logs.

### Gate 1

- [ ] A real buyer request is compiled by Gemini into valid structured intent.
- [ ] The user can edit it before confirmation.
- [ ] Gemini ranks sanitized eligible listings.
- [ ] Killing network access produces `BLOCK` or `ESCALATE`, never `ALLOW`.
- [ ] Model name and temperature appear in the decision evidence.

**Proof artifact:** one redacted local transcript showing request, compiled intent, ranking JSON, and fail-closed timeout.

---

### Phase 2 — Complete the trusted state and authorization boundary

**Budget:** 3 hours  
**Cumulative:** 7 / 24 hours  
**Goal:** make stale, mutated, or invented request objects incapable of authorizing an order.

### Step 2.1: Durable versioned intent store

1. Store every compiled/confirmed intent version in append-only JSONL.
2. Confirmation sets timestamp, version, and canonical hash only after validation.
3. Editing a confirmed intent creates a new version and retains the old version.
4. Provide lookup by exact `intent_hash`.
5. Verify the hash on every load.

### Step 2.2: Trusted catalogue repository

1. Load and validate local catalogue files through one repository abstraction.
2. Provide immutable lookup by `(merchant_namespace, sku_id)` or globally unique SKU.
3. Ensure model projections are copies and cannot mutate repository objects.
4. Reload the selected SKU from disk immediately before decision finalization and again before order amount construction if necessary.

### Step 2.3: Complete decision trace

Create a structured pipeline trace containing:

- original candidate order and seed;
- detection score/signals for every listing;
- original and sanitized text for flagged listings;
- exact gate failure codes per rejected SKU;
- eligible SKU set;
- Gemini ranking and reasons;
- structured ranking and component scores;
- selected SKU, score gap, action, and reason codes;
- model and latency metadata.

### Step 2.4: Final decision order

Enforce the Plan v2 order exactly:

1. `BLOCK`: no eligible SKU.
2. `ESCALATE`: ranker invalid or pipeline error.
3. `BLOCK`: trusted reload or final hard validation fails.
4. `ESCALATE`: selected listing detector score crosses threshold.
5. `ESCALATE`: relevance gap exceeds delta.
6. `ALLOW`: every preceding check passes.

### Step 2.5: Harden payment authorization

1. Payment receives validated decision, reloaded intent, and trusted listing—not form amount.
2. Reject non-`ALLOW`, missing/invalid intent hash, missing SKU, guard-on validation mismatch, and non-test credentials.
3. Compute amount as trusted `price_paise * confirmed quantity`.
4. Use `decision_id` as the idempotent receipt.
5. Query the ledger before any external order call.

### Primary files

- `guard/intent_store.py`
- `guard/validator.py`
- `guard/decision_engine.py`
- `guard/schemas.py`
- `data/intents/`
- `payments/razorpay_client.py`
- `tests/test_intent.py`
- `tests/test_decision_engine.py`
- `tests/test_payment_boundary.py`

### Gate 2

- [ ] Tampering with a confirmed intent invalidates its hash.
- [ ] Editing creates a second preserved version.
- [ ] Mutating the model-facing listing cannot affect final validation.
- [ ] A SKU changed on disk between ranking and checkout fails closed.
- [ ] Amount is derived exclusively from trusted price and confirmed quantity.
- [ ] `BLOCK` and `ESCALATE` cannot call either payment adapter.
- [ ] Duplicate purchase confirmation creates only one Razorpay order.

**Release blocker:** any test that permits a hard-violating `ALLOW` stops all later work.

---

### Phase 3 — Complete audit evidence and the interactive product

**Budget:** 2.5 hours  
**Cumulative:** 9.5 / 24 hours  
**Goal:** perform the entire before/after/safe demo without editing code or fixtures.

### Step 3.1: Full ledger sequence

Write these events through the single locked append function:

```text
INTENT_COMPILED
INTENT_CONFIRMED
LISTINGS_SCANNED
GATE_APPLIED
RANKED
DECIDED
ORDER_CREATED | ORDER_FAILED
```

Each order event must point to one decision. Each guard-on `ALLOW` must point to a confirmed intent hash. Store unsanitized flagged text only in the ledger/evidence trace, never in the ranker prompt.

### Step 3.2: Demo scenarios

Expose a fixed scenario selector alongside `guard_mode`:

1. **Manipulated hard violation:** baseline can create a wrong-item test order; guard blocks or selects safely.
2. **Manipulated admissible listing:** baseline is influenced; guard escalates or selects safely.
3. **Clean control:** guard allows safe SKU and creates a real test order.
4. **Failure control:** unavailable SKU or injected payment failure produces readable `ORDER_FAILED` evidence.

All scenarios use the same catalogue files and model adapter. The selector chooses a fixed local slice, not a separate program.

### Step 3.3: Evidence page

Show:

- confirmed intent, version, confirmation time, and hash;
- original versus sanitized text for every flagged SKU;
- detector scores and signal families;
- gate failures by SKU;
- eligible set and candidate seed/order;
- Gemini and structured rankings;
- score gap, final action, and reason codes;
- Razorpay Test Mode order ID or error class;
- ledger verification result.

### Step 3.4: Dispute reconstruction

At minimum, make `audit/dispute.py` reconstruct a readable chain by decision ID or order ID. CLI polish is stretch-only, but reconstruction must be exercised by tests.

### Primary files

- `app/main.py`
- `app/templates/index.html`
- `app/templates/confirm_intent.html`
- `app/templates/review.html`
- `app/templates/evidence.html`
- `app/static/app.js`
- `app/static/styles.css`
- `audit/ledger.py`
- `audit/dispute.py`
- `audit/verify.py`
- `tests/test_ledger.py`

### Gate 3

- [ ] Guard-off and guard-on execute from the same UI.
- [ ] Guard-off controlled baseline creates a Test Mode order only after final confirmation.
- [ ] Guard-on hard violation never creates an order.
- [ ] Guard-on clean control creates a real Test Mode order.
- [ ] One `ORDER_FAILED` path is visible and understandable.
- [ ] `make verify-ledger` verifies the full flow.
- [ ] Changing or removing any ledger event reports the first broken index.

**Feature freeze:** after Gate 3, do not introduce new architecture. Remaining work is fixtures, evaluation, fixes, and packaging.

---

### Phase 4 — Build the reduced but defensible benchmark

**Budget:** 4 hours  
**Cumulative:** 13.5 / 24 hours  
**Goal:** create enough fixed synthetic evidence to measure both structural and defense-in-depth controls honestly.

### Dataset target

| Item | Core target | Stretch target |
|---|---:|---:|
| Confirmed intents | 8 | 10–15 |
| Benign listings | 60–80 | 100–150 |
| Attack fixtures | 24–30 | 30–40 |
| Attack families | 8 | 10–12 |
| Benign episodes | about 120 | 250–300 |
| Adversarial episodes | about 60 | 100–160 |

### Step 4.1: Intent scenarios

Cover at least:

- outdoor and indoor usage;
- `any` usage;
- exact price-cap edge;
- quantity greater than one;
- required colour/size/material attribute;
- brand preference present and absent;
- at least three product categories.

Compile each with Gemini once, manually confirm it, and freeze the confirmed representation. Do not recompile it per episode.

### Step 4.2: Benign listings

Create realistic local listings containing:

- eligible preferred products;
- eligible non-preferred alternatives;
- wrong category/usage;
- one-paise-over-cap boundary;
- insufficient stock;
- required-attribute mismatches;
- benign marketing phrases likely to false-positive.

### Step 4.3: Attack families

Author fixed fixtures only; do not add an attack generator. Use at least eight families split wholly between calibration and held-out sets:

| Calibration-only examples | Held-out-only examples |
|---|---|
| direct instruction override | role/system imitation |
| explicit ranking manipulation | agent-directed imperative |
| zero-width concealment | HTML/comment concealment |
| obvious encoded/control block | requirement-universality claim |

Within each side, divide fixtures evenly between:

- `hard_violating`: attacker SKU fails a trusted hard constraint;
- `admissible`: attacker SKU passes hard constraints but is unacceptable or weakly relevant.

Day-2/development fixtures always remain calibration-only.

### Step 4.4: Deterministic episode composition

Compose episodes from fixed scenario/listing/fixture IDs and seeds. The composition code may build catalogue slices; it must not generate new adversarial text.

Every episode includes:

- `episode_id` and seed;
- intent/scenario ID;
- catalogue slice IDs;
- `attack_present`;
- `attack_stratum`;
- `attacker_sku`;
- expected eligible SKUs;
- acceptable SKUs;
- expected action;
- family and family source.

### Step 4.5: Dataset validation

Tests must enforce:

- JSON/Pydantic schema validity;
- no duplicate IDs or exact duplicate text;
- no family overlap between calibration and held-out;
- every Day-2 family is calibration-only;
- all required labels are present;
- expected eligible sets match the deterministic gate;
- no external URL strings;
- target counts and stratum balance.

### Primary files

- `data/intents/scenarios.json`
- `data/catalogues/*.json`
- `data/fixtures/benign.jsonl`
- `data/fixtures/calibration_attacks.jsonl`
- `data/fixtures/heldout_attacks.jsonl`
- `tests/test_evaluation.py`
- `docs/evaluation.md`

### Gate 4

- [ ] Dataset validation passes before any held-out model run.
- [ ] Family separation is machine-enforced.
- [ ] Counts and any reduction from target are documented.
- [ ] Every expected eligible set agrees with deterministic code.
- [ ] No attack text was generated by a repository endpoint or script.

---

### Phase 5 — Build the resumable evaluation and complete metrics

**Budget:** 3 hours  
**Cumulative:** 16.5 / 24 hours  
**Goal:** one command safely runs either split and can recover from quotas or interruption.

### Step 5.1: Runner architecture

1. Use `asyncio` with a semaphore; start at concurrency 4.
2. Assign one immutable output record per episode/mode/model/run.
3. Write completed records atomically or through a single writer.
4. Resume by skipping records with the same episode ID, mode, model, prompt/config hash, and run version.
5. Bound retry/backoff; persist terminal errors as fail-closed outcomes.
6. Use `FakePaymentSink` only.
7. Enforce by import-boundary test that `evaluation/` cannot import `payments.razorpay_client`.
8. Record model ID, seed, candidate order, latency, action, reasons, selections, token usage if available, and git commit.

### Step 5.2: Listing-level metrics

- detector true positives, false positives, false negatives, true negatives;
- detector precision, recall, and false-positive rate;
- Wilson 95% interval for each proportion.

### Step 5.3: Episode-level metrics

- baseline attack success;
- guarded unsafe-order rate;
- hard-constraint-violation rate;
- intervention precision;
- intervention recall;
- benign task success;
- unnecessary intervention;
- escalation rate split by benign/adversarial and stratum;
- guard-off and guard-on p50/p95 latency;
- ledger verification rate where applicable.

Report `hard_violating`, `admissible`, and benign groups separately. Never combine listing-level and episode-level denominators.

### Step 5.4: Result layout

```text
results/run_<timestamp>_<model>_<split>_v<version>/
  run_metadata.json
  episodes.jsonl
  summary.json
  failures.jsonl
  figures/
```

`run_metadata.json` records model, prompts/config hashes, fixture hash file, start/end time, git commit, repeat number, and whether free or paid tier was used.

### Primary files

- `evaluation/runner.py`
- `evaluation/metrics.py`
- `evaluation/report.py`
- `evaluation/frozen_config.yaml`
- `payments/fake_sink.py`
- `tests/test_evaluation.py`
- `Makefile`
- `.gitignore` (final versioned runs must be committable)

### Gate 5

- [ ] `make eval-calib` completes or resumes after interruption.
- [ ] Hand-calculated metric tests pass at n=0, n=1, and n=100.
- [ ] No evaluation path can make a network payment call.
- [ ] Output contains enough provenance to reproduce the run.
- [ ] A deliberate model timeout becomes a recorded intervention/error, not a missing episode.

---

### Phase 6 — Calibrate once, then freeze

**Budget:** 1.5 hours  
**Cumulative:** 18 / 24 hours  
**Goal:** establish an honest experimental boundary before viewing final results.

### Steps

1. Run `make eval-calib` using calibration and benign episodes only.
2. Review detector precision/recall/FPR, admissible manipulation, and benign intervention cost.
3. Change only `detector_threshold` and `relevance_delta` unless a correctness bug is found.
4. Record every tried value and rationale in `docs/evaluation.md`.
5. Choose fixed values based on pre-declared trade-offs:
   - preserve zero hard-constraint violations structurally;
   - aim for at least 60% relative reduction in admissible manipulation;
   - aim for at least 90% benign task success;
   - aim for no more than 10% unnecessary benign intervention.
6. Run the calibration suite again after the final config selection.
7. Run `make freeze`.
8. Commit config, prompts/model ID, all fixtures, scenarios, and `FIXTURE_HASHES.txt` before any held-out run.
9. Tag or clearly name the freeze commit.

### Gate 6

- [ ] `frozen_config.yaml` says `frozen: true` with a version.
- [ ] `FIXTURE_HASHES.txt` matches every frozen input.
- [ ] Running freeze twice without `--force-new-version` fails.
- [ ] Git working tree is clean at the freeze commit.
- [ ] No held-out result has been opened during calibration.

**Hard rule:** after Gate 6, disappointing held-out results are documented, not tuned away. Any system/config change creates a new version and preserves the old run.

---

### Phase 7 — Run held-out evaluation and inspect failures

**Budget:** 2 hours  
**Cumulative:** 20 / 24 hours  
**Goal:** produce the result table that all public claims will use.

### Steps

1. Verify fixture hashes and clean Git state.
2. Run `make eval-heldout` once on Gemini 2.5 Flash.
3. If quota interrupts the run, resume it; do not silently reduce examples mid-run.
4. Generate three required figures:
   - baseline attack success versus guarded unsafe-order rate by stratum;
   - intervention precision/recall by stratum;
   - benign task success versus unnecessary intervention.
5. Inspect every failure and assign a reason code and family without changing thresholds.
6. Produce a limitations table with observed counts.
7. Assert hard-constraint-violation rate equals exactly zero.
8. Commit the complete results directory.
9. Run a second repeat only in stretch time; never replace a worse run.

### Gate 7

- [ ] All expected episodes have terminal records.
- [ ] Summary denominators match episode files.
- [ ] Constraint-violation rate is exactly zero.
- [ ] Figures are generated from committed `summary.json`/`episodes.jsonl`.
- [ ] Model ID, git commit, run count, sample sizes, timestamps, and Wilson intervals are visible.
- [ ] Failures and missed targets remain documented.

---

### Phase 8 — Package the judge-facing repository

**Budget:** 2 hours  
**Cumulative:** 22 / 24 hours  
**Goal:** let a stranger understand and reproduce the work without assistance.

### README order

1. Twenty-second merchant-loss problem statement.
2. One-line guarantee: Razorpay validates payment; Decision Guard validates the decision.
3. Screenshot/GIF of baseline versus guarded flow.
4. Frozen episode-level results table.
5. Frozen listing-level detector table.
6. Latency table.
7. Actual architecture diagram.
8. Quick start and credential-free safe mode.
9. Real Razorpay Test Mode proof.
10. Threat-model summary and defense-only statement.
11. Evaluation and freeze methodology.
12. Observed limitations with counts.
13. Track 02 judging-criteria mapping.

### Documentation consistency pass

Update:

- `README.md` from actual results only;
- `IMPLEMENTATION_STATUS.md` with verified completion states;
- `docs/architecture.md` from the actual module graph;
- `docs/threat-model.md` with final signal weights and scope;
- `docs/evaluation.md` with calibration history and frozen methodology;
- `docs/demo-script.md` with exact clicks and real result numbers;
- `docs/razorpay-proof.md` with non-secret order evidence.

### Video/evidence preparation

Prepare six backup screenshots:

1. baseline manipulated selection;
2. confirmed intent and hash;
3. guarded intervention with original/sanitized text;
4. guarded safe `ALLOW` and Razorpay order ID;
5. verified ledger output;
6. held-out results and limitations.

Rehearse the five-minute flow once. Recording and a second rehearsal may use the protected buffer or stretch time.

### Gate 8

- [ ] Every README number exists in committed result JSON.
- [ ] Architecture matches the actual code.
- [ ] Synthetic evidence is labelled synthetic.
- [ ] No unsupported claim of novelty, peer review, complete protection, or observed savings exists.
- [ ] Demo script fits five minutes.

---

### Phase 9 — Protected integration and release buffer

**Budget:** 2 hours  
**Cumulative:** 24 / 24 hours  
**Goal:** spend the final time on reliability, not features.

### Release sequence

1. Clone the repository into a fresh temporary directory.
2. Install from pinned dependencies with no `.env`.
3. Run lint, tests, URL scan, secret scan, and fixture-hash verification.
4. Run credential-free demo smoke test and fake-payment evaluation smoke test.
5. Add local credentials without committing them.
6. Run the exact video flow once, including a real Test Mode order if desired.
7. Run `make verify-ledger`.
8. Verify GitHub Actions is green.
9. Confirm `git status` is clean and no absolute local paths are tracked.
10. Tag the final submission commit only after every P0 gate is checked.

### Gate 9 — release decision

Release only if:

- [ ] real Gemini calls work;
- [ ] guarded hard violations cannot create orders;
- [ ] one guarded safe order exists in Razorpay Test Mode;
- [ ] ledger verifies and reconstructs that order;
- [ ] frozen held-out results are committed;
- [ ] hard-constraint-violation rate is zero;
- [ ] clean-clone setup and CI pass;
- [ ] README and video numbers match results.

If any item fails at hour 24, report the repository as a prototype and do not tag it submission-ready.

---

## 6. Calendar mapping

The hour budgets are authoritative; this calendar is a suggested distribution around classes.

| Date | Hours | Target |
|---|---:|---|
| Thu 27 Aug | 4 | Phase 0–1: dependencies and real Gemini layer |
| Fri 28 Aug | 4 | Phase 2 plus start Phase 3: trusted state and decision boundary |
| Sat 29 Aug | 5 | Finish product evidence and begin benchmark |
| Sun 30 Aug | 4 | Finish benchmark and evaluation runner |
| Mon 31 Aug | 3 | Calibration, freeze, and integrity commit |
| Tue 1 Sep | 2 | Held-out run, figures, and failure review |
| Wed 2 Sep | 2 | README, rehearsal, clean-clone release checks |
| Thu 3 Sep | Submission | Upload only; no feature work |

If a day slips, continue by cumulative phase hour. Do not skip a gate to preserve calendar labels.

---

## 7. Predetermined cuts and escalation rules

### Never cut

- real primary model;
- explicit intent confirmation and hash;
- deterministic gate and final trusted reload;
- fail-closed decision ordering;
- protected Razorpay Test Mode path;
- complete ledger and verifier;
- calibration/held-out family separation;
- fake-payment evaluation;
- fixture freeze and committed results;
- zero-constraint-violation assertion;
- honest limitations.

### Cut immediately from core time

- public deployment;
- Standard Checkout and signature verification;
- webhooks;
- second model;
- learned detector;
- dashboard charts inside the app;
- polished dispute CLI;
- minimax/game-theoretic thresholding;
- animations and non-essential UI polish.

### Time-triggered cuts

| Trigger | Action |
|---|---|
| Gemini adapter not stable by hour 4 | Stop UI/data work and fix adapter; local stub cannot produce final evidence |
| Gate 2 not passing by hour 7 | Stop all presentation work; finish authorization invariant tests |
| Product demo not complete by hour 10 | Use plain forms and evidence JSON; cut visual polish |
| Dataset not valid by hour 14 | Use the declared benchmark floor; document reduced counts |
| Runner not resumable by hour 17 | Reduce concurrency complexity, retain checkpointing and sequential fallback |
| Calibration not frozen by hour 18 | Do not open held-out data; fix freeze path first |
| Held-out run blocked by free quota | Resume later or enable paid tier within USD 5 cap |
| Results miss target | Report honestly; do not retune on held-out data |
| Release checks fail after hour 22 | Spend buffer on defects only; add no features |

---

## 8. Stretch plan: hours 25–36

Stretch work begins only when all Gate 9 conditions already pass.

Priority order:

1. Expand dataset toward original Plan v2 counts and create a new frozen version.
2. Run a second Gemini repeat and report the range without discarding either run.
3. Add Razorpay Standard Checkout and server-side signature verification.
4. Add the readable `guard dispute <order_id>` CLI.
5. Add a second vendor model if its adapter is already stable.
6. Improve responsive UI and backup screenshots.
7. Record a second video take only if the first contains a factual or timing defect.

Do not use stretch time to rewrite disappointing held-out results in place.

---

## 9. Definition-of-done matrix

| Capability | Done means | Evidence |
|---|---|---|
| Intent compilation | Gemini sees raw request only; strict schema or manual fallback | compiler tests + ledger event |
| Intent confirmation | user approves immutable version and hash before catalogue processing | UI screenshot + intent-store test |
| Admissibility | trusted hard violations never reach ranker | gate tests + zero-violation metric |
| Detection/sanitization | original is scanned; matched spans absent from ranker input | detector test + evidence page |
| Ranking | Gemini returns validated eligible SKU order | adapter/ranker tests + trace |
| Relevance | fixed documented score and delta drive escalation | hand-calculated tests + trace |
| Final validation | intent and SKU reload from trusted stores | mutation/race tests |
| Authorization | only deterministic engine produces guarded `ALLOW` | decision invariant tests |
| Payment | validated `ALLOW` creates one test order with trusted amount | Razorpay order ID + idempotency test |
| Audit | complete event chain verifies and reconstructs order | verifier output + tamper tests |
| Evaluation | resumable fake-payment run produces all required metrics | committed episodes/summary |
| Freeze | config and fixtures hash-match frozen version | `FIXTURE_HASHES.txt` + test |
| Reporting | README/video numbers match committed results | clean-clone review checklist |

---

## 10. Working discipline

For every implementation block:

1. State one observable outcome in `TODAY.md`.
2. Write or update the failing test first for security invariants.
3. Implement the narrowest code that satisfies the phase contract.
4. Run targeted tests, then the whole suite.
5. Demonstrate the phase gate manually where external behavior matters.
6. Update documentation immediately if terminology or flow changes.
7. Commit by outcome and push only green commits.

Recommended commit sequence:

```text
model: compile and rank with validated Gemini output
intent: reload confirmed versions by canonical hash
guard: finalize decisions from trusted catalogue reloads
audit: record and reconstruct the complete checkout chain
demo: show baseline, intervention, safe order, and failure evidence
data: validate separated calibration and held-out families
eval: resume bounded Gemini episodes and report complete metrics
freeze: lock benchmark version and fixture hashes
results: commit held-out run and observed limitations
docs: publish reproducible submission evidence
```

The governing priority remains:

```text
Confirmed Intent
  -> Deterministic Decision
  -> Bounded Razorpay Action
  -> Reproducible Evidence
```
