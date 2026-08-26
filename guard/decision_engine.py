import time
from uuid import uuid4

from guard.admissibility import gate
from guard.canonical import utc_now
from guard.detector import scan_listing
from guard.model_adapter import ModelAdapter
from guard.ranker import rank
from guard.relevance import rank_structured, structured_score
from guard.sanitizer import sanitize
from guard.schemas import Action, DecisionRecord, Intent, Listing, ReasonCode
from guard.validator import final_validate


class DecisionEngine:
    def __init__(self, adapter: ModelAdapter, detector_threshold: float = 0.6, delta: float = 0.15) -> None:
        self.adapter = adapter
        self.detector_threshold = detector_threshold
        self.delta = delta

    def _record(self, *, intent: Intent, mode: str, before: int, after: int, seed: int,
                started: float, action: Action, reasons: list[ReasonCode], selected: str | None = None,
                flags: list[str] | None = None, llm_rank: list[str] | None = None,
                structured_top: str | None = None, gap: float | None = None) -> DecisionRecord:
        return DecisionRecord(
            decision_id=f"dec_{uuid4().hex[:12]}", intent_hash=intent.intent_hash or "",
            guard_mode=mode, selected_sku=selected, action=action, reason_codes=reasons,
            flagged_skus=flags or [], candidate_count_before=before, candidate_count_after_gate=after,
            candidate_order_seed=seed, llm_rank=llm_rank or [], structured_top_sku=structured_top,
            score_gap=gap, model_id=self.adapter.model_id, temperature=0,
            latency_ms=max(0, int((time.perf_counter() - started) * 1000)), created_at=utc_now(),
        )

    async def decide(self, intent: Intent, listings: list[Listing], guard_mode: str = "on", seed: int = 20260829) -> DecisionRecord:
        started = time.perf_counter()
        if not intent.confirmed_by_user or not intent.intent_hash:
            return self._record(intent=intent, mode=guard_mode, before=len(listings), after=0, seed=seed,
                                started=started, action=Action.BLOCK, reasons=[ReasonCode.PIPELINE_ERROR])
        try:
            if guard_mode == "off":
                ranked, _ = await rank(self.adapter, intent, listings, seed)
                return self._record(intent=intent, mode="off", before=len(listings), after=len(listings), seed=seed,
                                    started=started, action=Action.ALLOW, reasons=[ReasonCode.BASELINE_UNGUARDED],
                                    selected=ranked[0], llm_rank=ranked)
            eligible, _ = gate(intent, listings)
            if not eligible:
                return self._record(intent=intent, mode="on", before=len(listings), after=0, seed=seed,
                                    started=started, action=Action.BLOCK, reasons=[ReasonCode.NO_ELIGIBLE_SKU])
            detections = {x.sku_id: scan_listing(x.title, x.description, self.detector_threshold) for x in eligible}
            flags = [sku for sku, result in detections.items() if result.flagged]
            ranker_listings = [
                item.model_copy(
                    update={
                        "title": sanitize(item.title, detections[item.sku_id].flagged),
                        "description": sanitize(
                            item.description, detections[item.sku_id].flagged
                        ),
                    }
                )
                for item in eligible
            ]
            ranked, _ = await rank(self.adapter, intent, ranker_listings, seed)
            selected = next(x for x in eligible if x.sku_id == ranked[0])
            structured = rank_structured(intent, eligible)[0]
            gap = structured_score(intent, structured) - structured_score(intent, selected)
            if not final_validate(intent, selected):
                return self._record(intent=intent, mode="on", before=len(listings), after=len(eligible), seed=seed,
                                    started=started, action=Action.BLOCK, reasons=[ReasonCode.FINAL_VALIDATION_FAILED],
                                    selected=selected.sku_id, flags=flags, llm_rank=ranked, structured_top=structured.sku_id, gap=gap)
            if detections[selected.sku_id].flagged:
                return self._record(intent=intent, mode="on", before=len(listings), after=len(eligible), seed=seed,
                                    started=started, action=Action.ESCALATE, reasons=[ReasonCode.DETECTOR_FLAGGED],
                                    selected=selected.sku_id, flags=flags, llm_rank=ranked, structured_top=structured.sku_id, gap=gap)
            if gap > self.delta:
                return self._record(intent=intent, mode="on", before=len(listings), after=len(eligible), seed=seed,
                                    started=started, action=Action.ESCALATE, reasons=[ReasonCode.RELEVANCE_DISAGREEMENT],
                                    selected=selected.sku_id, flags=flags, llm_rank=ranked, structured_top=structured.sku_id, gap=gap)
            return self._record(intent=intent, mode="on", before=len(listings), after=len(eligible), seed=seed,
                                started=started, action=Action.ALLOW,
                                reasons=[ReasonCode.HARD_CONSTRAINTS_PASS, ReasonCode.RELEVANCE_WITHIN_THRESHOLD, ReasonCode.DETECTOR_CLEAR],
                                selected=selected.sku_id, flags=flags, llm_rank=ranked, structured_top=structured.sku_id, gap=gap)
        except Exception:
            return self._record(intent=intent, mode=guard_mode, before=len(listings), after=0, seed=seed,
                                started=started, action=Action.ESCALATE, reasons=[ReasonCode.RANKER_OUTPUT_INVALID])
