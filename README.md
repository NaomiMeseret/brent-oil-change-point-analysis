# Change Point Analysis and Statistical Modeling of Brent Oil Prices

This project analyzes Brent oil price behavior and links structural breaks to major geopolitical and economic events.  
It combines time-series analysis notebooks with a Flask + React dashboard for exploration.

![Brent Oil Dashboard Screenshot](reports/screenshots/Screenshot%202026-02-17%20at%2010.20.47%20at%20night.png)

## Project Scope

- Analyze Brent oil prices from July 30, 2007 to September 29, 2022
- Map important geopolitical events to price regime shifts
- Build reproducible analysis artifacts and a stakeholder-facing dashboard

## Repository Structure

```text
.
├── data/
│   ├── brent_oil_prices_clean.csv
│   └── geopolitical_events_clean.csv
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_time_series_analysis.ipynb
│   ├── 03_change_point_modeling.ipynb
│   └── 04_dashboard_development.ipynb
├── src/
│   ├── change_point_models.py
│   ├── data_processing.py
│   ├── extract_images.py
│   └── visualization.py
├── dashboard/
│   ├── backend/   # Flask API
│   └── frontend/  # React app
├── reports/
└── requirements.txt
```

## Quick Start

### 1. Install Python dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run notebooks (optional)

```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

### 3. Run the dashboard

Terminal 1 (backend):

```bash
cd "dashboard/backend"
source ../../venv/bin/activate
python3 app.py
```

Terminal 2 (frontend):

```bash
cd "dashboard/frontend"
npm install
npm start
```

Open `http://localhost:3000`.

## Dashboard Services

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5001`
- Health endpoint: `http://localhost:5001/api/health`

## Methods Used

- Exploratory data analysis and descriptive statistics
- Time-series diagnostics (trend/volatility/stationarity)
- Change point modeling (Bayesian workflow in notebooks)
- Event correlation analysis for interpretation

## Notes

- Frontend API proxy is configured to backend port `5001`.
- If port `5001` is already in use:

```bash
lsof -ti:5001 | xargs kill
```
