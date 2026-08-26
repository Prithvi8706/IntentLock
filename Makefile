.PHONY: setup demo test lint eval-calib eval-heldout verify-ledger freeze check
setup:
	python -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt
demo:
	python -m uvicorn app.main:app --reload
test:
	python -m pytest
lint:
	python -m ruff check .
eval-calib:
	python -m evaluation.runner --dataset calibration
eval-heldout:
	python -m evaluation.runner --dataset heldout
verify-ledger:
	python -m audit.verify
freeze:
	python scripts/freeze.py
check: lint test
	python scripts/check_no_external_urls.py

