# Week 11: Change Point Analysis and Brent Oil Price Dashboard

This repository contains **all Week 11 tasks**, focusing on **change point analysis**, **statistical modeling**, and an **interactive dashboard** for Brent crude oil prices. The project combines Python for analysis and Flask APIs with a React frontend for visualization.

---

## Table of Contents

- [Week 11: Change Point Analysis and Brent Oil Price Dashboard](#week-11-change-point-analysis-and-brent-oil-price-dashboard)
  - [Table of Contents](#table-of-contents)
  - [Business Objective](#business-objective)
  - [Tasks Overview](#tasks-overview)
  - [Task 1: Data Exploration and Cleaning](#task-1-data-exploration-and-cleaning)
  - [Task 2: Change Point Analysis \& Statistical Modeling](#task-2-change-point-analysis--statistical-modeling)
    - [Key Steps](#key-steps)
  - [Event Correlation](#event-correlation)
  - [Statistical Modeling](#statistical-modeling)
    - [Insights](#insights)
  - [Task 3: Interactive Dashboard](#task-3-interactive-dashboard)
    - [Key Features](#key-features)
    - [Recommended Libraries](#recommended-libraries)
  - [Backend (Flask API)](#backend-flask-api)
    - [API Endpoints](#api-endpoints)
    - [Running Backend](#running-backend)
    - [Features in Frontend](#features-in-frontend)
    - [Usage](#usage)
    - [Data Sources](#data-sources)
    - [Project Structure](#project-structure)

---

## Business Objective

AlphaCare Insurance Solutions (ACIS) and related stakeholders aim to **analyze historical Brent oil price data** to:  

- Detect **significant shifts** in price trends (change points).  
- Understand **how events** (geopolitical, economic, environmental) affect prices.  
- Enable data-driven **forecasting and strategy optimization**.  

---

## Tasks Overview

| Task | Description |
|------|-------------|
| Task 1 | **Exploratory Data Analysis (EDA)**: Cleaned and visualized historical price and event data. |
| Task 2 | **Change Point Analysis & Statistical Modeling**: Detected price shifts, quantified impacts, and linked to events. |
| Task 3 | **Interactive Dashboard**: Built a React frontend + Flask API backend to visualize price trends, events, and allow filtering. |

---

## Task 1: Data Exploration and Cleaning

- Loaded `BrentOilPrices.csv` and `events.csv` into Pandas DataFrames.  
- Checked **missing values** and **data types**.  
- Converted `Date` fields to datetime objects.  
- Summary statistics:

```text
Price range: $18.45 – $XX  
Number of events: 15  
```
## Task 2: Change Point Analysis & Statistical Modeling

### Key Steps

1. **Data Loading & Cleaning**:  
   - Loaded `BrentOilPrices.csv` and `events.csv`.  
   - Converted date columns to datetime objects.  
   - Checked for missing values and data consistency.

2. **Change Point Detection**:  
   - Detected significant shifts in daily Brent prices using statistical methods.  
   - Example result:

```text
Most probable change point index: 4376
Date: 2004-08-05
Mean log return before change: 0.0004
Mean log return after change: 0.0001
Difference: -0.0003
```

## Event Correlation

Linked change points to major historical events:

- Gulf War (1990)
- Asian Financial Crisis (1997)
- 9/11 Attacks (2001)
- Global Financial Crisis (2008)

Quantified the impact on price changes.

---

## Statistical Modeling

- Built models to compare trends before and after change points.  
- Recorded metrics such as RMSE, volatility, and feature importance.  
- Used SHAP/LIME to evaluate which events had the largest effect.

### Insights

- Geopolitical and economic events strongly influence Brent oil price shifts.  
- Price change magnitudes around events can be quantified for forecasting and risk analysis.

---

## Task 3: Interactive Dashboard

### Key Features

- **Historical Price Trends**: Interactive line chart showing daily Brent prices.  
- **Event Highlights**: Red markers for events; hover to view details.  
- **Filters**: Start and End date selectors for dynamic data views.  
- **Key Indicators**: Display volatility and average price changes around events.  
- **Responsive Design**: Works on desktop, tablet, and mobile.  
- **Drill-down Capability**: Explore trends and events in detail.

### Recommended Libraries

- **Frontend Charts**: Recharts, React Chart.js 2, D3.js  
- **Backend API**: Flask

---

## Backend (Flask API)

### API Endpoints

- `GET /api/historical_prices` → Returns historical Brent price data.  
- `GET /api/events` → Returns all event data.  
- `GET /api/change_points` → Returns detected change points.

### Running Backend

```bash
cd dashboard
python -m venv .venv
# Activate virtual environment:
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py

## API and Frontend

The API runs at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Frontend (React)

### Setup

```bash
cd dashboard_frontend
npm install
npm install recharts
npm start

The dashboard runs at: http://localhost:3000
```
### Features in Frontend

  * Historical trends and event correlation visualization.

  * Event highlight functionality for price spikes/drops.

  * Volatility and average price changes displayed around events.

  * Start and End date filters for dynamic exploration.

### Usage

  -  Open the React dashboard in your browser.
  -  Use Start Date / End Date filters to select a custom time range.
  -  Hover over events to see descriptions and categories.
  -  Analyze historical prices, volatility, and average price changes.
  -  Explore trends with the event highlight functionality.

### Data Sources

   - BrentOilPrices.csv → Daily historical Brent crude oil prices.
   - events.csv → Key geopolitical, economic, and market events.
  

### Project Structure
week_11_project/
```
├── data/raw
│ ├── brent_oil_prices.csv # Historical Brent oil prices
│ ├── events.csv # Key geopolitical & OPEC events
├── src/
│ ├── eda.py # EDA and time series analysis class
│ ├── change_point_model.py # Bayesian Change Point model
├── dashboard/
│ ├── app.py # react dashboard
├── notebooks/
│ ├── change_point.ipynb
│ ├── EDA.ipynb # EDA notebook
│ ├── Task_1.ipynb # Data Analysis workflow,events
├── requirements.txt
├── README.md
```
