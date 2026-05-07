PYTHON ?= python3
PIP ?= pip3
UVICORN ?= uvicorn
HOST ?= 0.0.0.0
PORT ?= 8000
BASE_URL ?= http://127.0.0.1:$(PORT)

.PHONY: setup run test-api test

setup:
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) main:app --reload --host $(HOST) --port $(PORT)

test-api:
	BASE_URL=$(BASE_URL) bash test_api.sh

test:
	KC_DISABLE_MODEL_PRELOAD=1 $(PYTHON) -m pytest -q
