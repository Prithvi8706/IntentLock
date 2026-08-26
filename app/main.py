import json
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from audit.ledger import Ledger, verify_chain
from guard.canonical import hash_object, utc_now
from guard.decision_engine import DecisionEngine
from guard.intent_compiler import IntentCompiler
from guard.model_adapter import LocalDeterministicAdapter
from guard.schemas import EventType, Intent, Listing
from payments.fake_sink import FakePaymentSink

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Decision Guard", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "app/static"), name="static")
templates = Jinja2Templates(directory=ROOT / "app/templates")
compiler = IntentCompiler()
engine = DecisionEngine(LocalDeterministicAdapter())
ledger = Ledger(ROOT / "audit/ledger.jsonl")
sink = FakePaymentSink()
sessions: dict[str, dict] = {}


def catalogue() -> list[Listing]:
    return [Listing.model_validate(x) for x in json.loads((ROOT / "data/catalogues/merchant_alpha.json").read_text())]


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.post("/intent", response_class=HTMLResponse)
def compile_intent(request: Request, raw_request: str = Form(...), guard_mode: str = Form("on")):
    try:
        intent = compiler.compile(raw_request)
    except ValueError as exc:
        return templates.TemplateResponse(request, "index.html", {"error": str(exc), "raw_request": raw_request}, status_code=422)
    sessions[intent.intent_id] = {"intent": intent, "mode": guard_mode}
    ledger.append(EventType.INTENT_COMPILED, intent.model_dump(mode="json"))
    return templates.TemplateResponse(request, "confirm_intent.html", {"intent": intent, "guard_mode": guard_mode})


@app.post("/confirm/{intent_id}")
async def confirm(intent_id: str, category: str = Form(...), usage: str = Form(...), max_price_paise: int = Form(...), quantity: int = Form(...)):
    if intent_id not in sessions:
        raise HTTPException(404, "intent not found")
    draft: Intent = sessions[intent_id]["intent"]
    data = draft.model_dump()
    data.update(category=category, usage=usage, max_price_paise=max_price_paise, quantity=quantity,
                confirmed_by_user=True, confirmed_at=utc_now(), intent_hash=None)
    data["intent_hash"] = hash_object(data, "intent_hash")
    intent = Intent.model_validate(data)
    sessions[intent_id]["intent"] = intent
    ledger.append(EventType.INTENT_CONFIRMED, intent.model_dump(mode="json"))
    decision = await engine.decide(intent, catalogue(), sessions[intent_id]["mode"])
    sessions[intent_id]["decision"] = decision
    ledger.append(EventType.DECIDED, decision.model_dump(mode="json"), decision.decision_id)
    return RedirectResponse(f"/review/{intent_id}", status_code=303)


@app.get("/review/{intent_id}", response_class=HTMLResponse)
def review(request: Request, intent_id: str):
    state = sessions.get(intent_id)
    if not state or "decision" not in state:
        raise HTTPException(404, "decision not found")
    return templates.TemplateResponse(request, "review.html", {**state, "intent_id": intent_id})


@app.post("/purchase/{intent_id}")
def purchase(intent_id: str):
    state = sessions.get(intent_id)
    if not state:
        raise HTTPException(404, "decision not found")
    selected = next(x for x in catalogue() if x.sku_id == state["decision"].selected_sku)
    try:
        state["order"] = sink.create_order(state["decision"], selected, state["intent"].quantity)
        ledger.append(EventType.ORDER_CREATED, state["order"], state["decision"].decision_id)
    except PermissionError as exc:
        raise HTTPException(403, str(exc)) from exc
    return RedirectResponse(f"/evidence/{intent_id}", status_code=303)


@app.get("/evidence/{intent_id}", response_class=HTMLResponse)
def evidence(request: Request, intent_id: str):
    state = sessions.get(intent_id)
    if not state:
        raise HTTPException(404, "evidence not found")
    valid, _, _ = verify_chain(ledger.path)
    return templates.TemplateResponse(request, "evidence.html", {**state, "ledger_valid": valid})

