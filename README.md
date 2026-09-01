# FINARCH AI

Financial decision support for answering “what should I do with my money now?” It produces a transparent financial twin, risk lens, ranked actions, and Monte Carlo outcomes. It is educational software—not personalised regulated investment, tax, or credit advice.

## Run locally

Backend (Python 3.10+):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Set-Location backend
uvicorn app.main:app --reload
```

Frontend (Node 18+), in another terminal:

```powershell
Set-Location frontend
npm install
npm run dev
```

Open `http://localhost:5173`; API documentation is at `http://localhost:8000/docs`.

## API

- `PUT /api/v1/profile` persists the supplied financial profile in the local SQLite store.
- `POST /api/v1/analysis` calculates net worth, cash flow, emergency cover, allocation, health score, risk, and ten ranked actions.
- `POST /api/v1/simulate` runs 500 Monte Carlo paths for baseline, market-drop, inflation-rise, or salary-increase scenarios.
- `GET /api/v1/market` exposes a clearly labelled mock market-data fallback.

The implementation deliberately keeps market values mocked until a licensed data provider is configured. Planning calculations explain their inputs and do not invent account or market data.
