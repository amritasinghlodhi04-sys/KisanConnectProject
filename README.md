# KisanConnect ML API

Machine learning backend for KisanConnect, an Indian farm-to-consumer marketplace.

## Setup

1. Create and activate a Python 3.10+ virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` with:
   ```env
   DATA_GOV_API_KEY=your_api_key_here
   ```
   You can copy it from:
   ```bash
   cp .env.example .env
   ```

## Run

From the **project folder** (`kisanconnect-ml` / this repo):

```bash
cd ~/Desktop/KisanConnectProject   # adjust if your clone path differs
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

`--host 0.0.0.0` listens on all interfaces so `localhost`, `127.0.0.1`, and your LAN IP all work.

Or via Make:

```bash
make setup
make run
```

## Base URL

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

CORS is configured for development: common `localhost` / `127.0.0.1` origins plus a permissive regex for other local or tunneled frontends (`allow_methods` / `allow_headers`: `*`). After changing server code, stop the old `uvicorn` process once (avoid two servers on the same port) so `--reload` can bind cleanly.

### Page won’t open (browser / Swagger)

1. **Confirm the server started** — the terminal must show something like `Uvicorn running on http://0.0.0.0:8000`. If you see `[Errno 48] Address already in use`, another process is using the port:
   ```bash
   lsof -nP -iTCP:8000 -sTCP:LISTEN
   kill <PID>
   ```
2. **Use `http://`, not `https://`** — unless you terminated TLS yourself, use `http://127.0.0.1:8000/docs`.
3. **Open Swagger at** `http://127.0.0.1:8000/docs` — not a `file://` path.
4. **Wrong folder** — if you run `uvicorn` from another directory, Python may import the wrong `main.py` or fail silently; always `cd` into this project first.

## API Endpoints

- `GET /` -> service info
- `GET /health` -> health check
- `POST /ml/price-engine` -> mandi-based fair pricing (live + mock fallback)
- `POST /ml/demand-forecast` -> Prophet-based demand forecast (cached models)
- `POST /ml/reputation-score` -> farmer trust score
- `POST /ml/delivery-match` -> delivery partner ranking
- `POST /ml/carbon-footprint` -> carbon estimate for delivery trips
- `POST /ml/seasonal-calendar` -> crop season context

## Notes

- Price endpoint uses live Data.gov data when available, and falls back to mock prices on failure.
- Demand forecasting uses synthetic historical demand and caches Prophet models to avoid retraining on each request.
- Seasonal calendar currently uses synthetic demand assumptions; in production it should combine real price, supply, and observed demand signals.

## Quick API Test

```bash
make test-api
```

## Automated Test Suite

Run endpoint tests with pytest:

```bash
make test
```