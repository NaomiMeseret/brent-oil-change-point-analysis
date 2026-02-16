# Change Point Analysis and Statistical Modeling of Brent Oil Prices

## Project Overview

This project analyzes how major political and economic events affect Brent oil prices using Bayesian change point detection methods. The analysis focuses on identifying structural breaks in oil price data and associating them with significant geopolitical events.

## Business Context

- **Company**: Birhan Energies - Energy sector consultancy
- **Objective**: Quantify impact of political decisions, conflicts, sanctions and OPEC policy changes on Brent oil prices
- **Time Period**: July 30, 2007 - September 29, 2022 (price data), 1990-2022 (events data)
- **Stakeholders**: Investors, policymakers, energy companies

## Key Questions

1. Which events have significantly impacted Brent oil prices over the past decades?
2. How can we quantify the magnitude of these effects using statistical methods?
3. What insights can guide investment strategies, policy development and operational planning?

## Project Structure

```
├── data/
│   ├── brent_oil_prices_clean.csv     # Cleaned historical Brent oil price data (2007-2022)
│   └── geopolitical_events_clean.csv  # Compiled major events dataset (1990-2022)
├── notebooks/
│   ├── 01_data_exploration.ipynb      # Initial data analysis
│   ├── 02_time_series_analysis.ipynb   # Trend, stationarity, volatility
│   ├── 03_change_point_modeling.ipynb # Bayesian change point detection
│   └── 04_dashboard_development.ipynb # Interactive dashboard
├── src/
│   ├── data_processing.py               # Data cleaning and preparation
│   ├── change_point_models.py            # PyMC Bayesian models
│   ├── visualization.py                  # Plotting and dashboard utilities
│   └── extract_images.py                # Image extraction from notebooks
├── reports/
│   ├── interim_report_task1.md          # Task 1 findings and analysis plan
│   ├── assumptions_and_limitations.md    # Methodological considerations
│   ├── data_analysis_workflow.md       # Analysis workflow documentation
│   └── images/                         # Extracted visualizations
│       ├── notebook_cell_9_output_0.png  # Time series visualization
│       └── notebook_cell_11_output_0.png # Data exploration dashboard
├── requirements.txt                     # Python dependencies


## Methodology
1. **Data Preparation**: Load and clean historical price data 
2. **Event Compilation**: Research and structure major geopolitical/economic events 
3. **Initial EDA**: Conduct exploratory data analysis with visualizations 
4. **Time Series Analysis**: Investigate trend, stationarity, and volatility patterns (upcoming)
5. **Bayesian Change Point Detection**: Implement PyMC models to identify structural breaks (upcoming)
6. **Causal Analysis**: Correlate detected change points with major events (upcoming)
7. **Dashboard Development**: Create interactive visualization tool (upcoming)
8. **Reporting**: Generate comprehensive insights for stakeholders (upcoming)

## Current Status: Task 1 Complete 
- **Data Acquisition**: Successfully loaded 3,766 Brent oil price observations (2007-2022)
- **Event Catalog**: Compiled 27 major geopolitical/economic events (1990-2022)
- **Initial Analysis**: Completed EDA with statistical findings and visualizations
- **Documentation**: Created interim report with analysis plan and methodology
- **Project Structure**: Established organized file structure with proper documentation

## Key Findings So Far
- **Price Range**: $19.33 to $146.08 per barrel (mean: $78.14 ± $25.95)
- **Distribution Characteristics**: Positive skewness, fat-tailed behavior, volatility clustering
- **Event Impact**: 21 out of 27 events classified as high-impact
- **Most Frequent Event Types**: Military Conflict (6), OPEC Policy (6), Economic Crisis (2)

## Key Concepts
- **Change Point Models**: Identify structural breaks in time series data
- **Bayesian Inference**: Update probability estimates as new evidence arrives
- **Monte Carlo Markov Chain**: Sampling method for Bayesian inference
- **Correlation vs Causation**: Critical distinction in time series analysis

## Installation and Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run data exploration: `jupyter notebook notebooks/01_data_exploration.ipynb`

## Next Steps
- **Time Series Analysis**: Stationarity testing, volatility modeling, trend decomposition
- **Bayesian Modeling**: Implement PyMC change point detection algorithms
- **Event Correlation**: Analyze temporal relationships between events and price changes
- **Policy Analysis**: Evaluate effectiveness of policy interventions

## Contributing
This project follows a structured approach to time series analysis with emphasis on reproducible research and clear documentation.
```
