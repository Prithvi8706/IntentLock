from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Usage(StrEnum):
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    ANY = "any"


class ListingUsage(StrEnum):
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    ALL = "all"


class Action(StrEnum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"


class ReasonCode(StrEnum):
    HARD_CONSTRAINTS_PASS = "HARD_CONSTRAINTS_PASS"
    RELEVANCE_WITHIN_THRESHOLD = "RELEVANCE_WITHIN_THRESHOLD"
    DETECTOR_CLEAR = "DETECTOR_CLEAR"
    NO_ELIGIBLE_SKU = "NO_ELIGIBLE_SKU"
    FINAL_VALIDATION_FAILED = "FINAL_VALIDATION_FAILED"
    RANKER_OUTPUT_INVALID = "RANKER_OUTPUT_INVALID"
    DETECTOR_FLAGGED = "DETECTOR_FLAGGED"
    RELEVANCE_DISAGREEMENT = "RELEVANCE_DISAGREEMENT"
    PIPELINE_ERROR = "PIPELINE_ERROR"
    BASELINE_UNGUARDED = "BASELINE_UNGUARDED"


class EventType(StrEnum):
    INTENT_COMPILED = "INTENT_COMPILED"
    INTENT_CONFIRMED = "INTENT_CONFIRMED"
    LISTINGS_SCANNED = "LISTINGS_SCANNED"
    GATE_APPLIED = "GATE_APPLIED"
    RANKED = "RANKED"
    DECIDED = "DECIDED"
    ORDER_CREATED = "ORDER_CREATED"
    ORDER_FAILED = "ORDER_FAILED"
    PAYMENT_VERIFIED = "PAYMENT_VERIFIED"
    ESCALATION_RESOLVED = "ESCALATION_RESOLVED"


class Intent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    intent_id: str
    intent_version: int = Field(ge=1)
    raw_request: str
    category: str
    usage: Usage = Usage.ANY
    max_price_paise: int = Field(gt=0)
    quantity: int = Field(default=1, gt=0)
    required_attributes: dict[str, str] = Field(default_factory=dict)
    preferred_brand: str | None = None
    preferred_colour: str | None = None
    confirmed_by_user: bool = False
    confirmed_at: str | None = None
    schema_version: Literal[1] = 1
    intent_hash: str | None = None

    @model_validator(mode="after")
    def confirmed_fields(self) -> "Intent":
        if self.confirmed_by_user and (not self.confirmed_at or not self.intent_hash):
            raise ValueError("confirmed intent needs confirmed_at and intent_hash")
        return self


class Listing(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sku_id: str
    merchant_namespace: str
    title: str
    description: str
    category: str
    usage: ListingUsage
    price_paise: int = Field(gt=0)
    stock: int = Field(ge=0)
    attributes: dict[str, str] = Field(default_factory=dict)
    fixture_label: Literal["benign", "malicious"] = "benign"


class Detection(BaseModel):
    flagged: bool
    score: float = Field(ge=0, le=1)
    matched_signals: list[str]
    matched_spans: list[str]
    normalized_text: str
    zero_width_removed: bool = False


class DecisionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision_id: str
    intent_hash: str
    guard_mode: Literal["on", "off"]
    selected_sku: str | None
    action: Action
    reason_codes: list[ReasonCode] = Field(min_length=1)
    flagged_skus: list[str] = Field(default_factory=list)
    candidate_count_before: int = Field(ge=0)
    candidate_count_after_gate: int = Field(ge=0)
    candidate_order_seed: int
    llm_rank: list[str] = Field(default_factory=list)
    structured_top_sku: str | None = None
    score_gap: float | None = None
    model_id: str
    temperature: float = 0.0
    latency_ms: int = Field(ge=0)
    created_at: str


class LedgerEvent(BaseModel):
    event_id: str
    event_type: EventType
    timestamp: str
    decision_id: str | None = None
    payload: dict[str, Any]
    previous_hash: str
    event_hash: str

