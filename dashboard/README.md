# Brent Oil Dashboard

Interactive dashboard for exploring Brent oil prices, change points, and related geopolitical events.

## Architecture

- Backend: Flask API in `backend/app.py`
- Frontend: React app in `frontend/`
- Data source: CSV files in `../data/`

## Run Locally

### Backend (Terminal 1)

```bash
cd "/Users/naomi/Change Point Analysis and Statistical Modeling of Time Series Data/dashboard/backend"
source ../../venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Backend runs on `http://localhost:5001`.

### Frontend (Terminal 2)

```bash
cd "/Users/naomi/Change Point Analysis and Statistical Modeling of Time Series Data/dashboard/frontend"
npm install
npm start
```

Frontend runs on `http://localhost:3000`.

## API Endpoints

- `GET /api/health`
- `GET /api/prices?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/events?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&type=<event-type>`
- `GET /api/change-points`
- `GET /api/statistics`
- `GET /api/event-correlation`

## Development Notes

- Frontend proxy points to `http://localhost:5001`.
- If the browser is blank, hard refresh (`Cmd+Shift+R`) after frontend compile.
- If `5001` is in use:

```bash
lsof -ti:5001 | xargs kill
```

