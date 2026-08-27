# Decision Guard

Decision Guard is the domain of verifying whether an agent-selected product remains faithful to a buyer's confirmed intent before a merchant accepts the resulting checkout risk.

## Shopping decision

**Buyer Intent**:
The buyer's requested product category, usage, budget, quantity, hard requirements, and preferences before catalogue influence.
_Avoid_: Prompt, query, shopping text

**Confirmed Intent**:
A buyer-approved, immutable version of Buyer Intent that serves as the authority for one shopping decision.
_Avoid_: Parsed request, current intent, mutable intent

**Listing**:
A merchant catalogue offer composed of trusted structured facts and untrusted descriptive text.
_Avoid_: Product, model candidate

**Decision**:
The recorded outcome for one agent selection: `ALLOW`, `BLOCK`, or `ESCALATE`.
_Avoid_: Recommendation, model answer, payment result

**Intervention**:
A `BLOCK` or `ESCALATE` decision that prevents automatic order creation.
_Avoid_: Rejection, detector hit

**Unsafe Order**:
An allowed order for the attacker-promoted listing, whether or not that listing satisfies the hard constraints.
_Avoid_: Failed payment, invalid transaction

## Evaluation

**Evaluation Episode**:
One fixed combination of Confirmed Intent, catalogue slice, optional adversarial listing, and candidate-order seed evaluated in baseline and guarded modes.
_Avoid_: Test case, prompt run

**Attack Stratum**:
The safety boundary an adversarial listing targets: `hard_violating` or `admissible`.
_Avoid_: Attack severity, detector category

**Calibration Set**:
The fixture families available for choosing fixed thresholds and evaluation configuration.
_Avoid_: Training set, development examples

**Held-out Set**:
Fixture families unavailable to threshold selection and reserved for the frozen final evaluation.
_Avoid_: Validation set, test prompts
