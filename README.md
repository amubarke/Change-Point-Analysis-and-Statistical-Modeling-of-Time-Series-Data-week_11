# Week 11: Change Point Analysis and Statistical Modeling of Brent Oil Prices

## Project Overview
This project focuses on analyzing historical Brent oil prices (1987–2022) to detect structural changes and associate them with major geopolitical events, OPEC decisions, and economic shocks. Using Bayesian Change Point modeling with PyMC, we identify key shifts in price regimes and quantify their impacts.  

An interactive dashboard (Streamlit) provides visualization of price trends, volatility, and forecasted change points for stakeholders.

---

## Business Objective
- Understand how major events impact Brent oil prices.  
- Quantify event-driven price changes and volatility regimes.  
- Provide actionable insights to investors, policymakers, and energy companies.  

---

## Tasks Covered (Week 11)
1. **Task 1: Laying the Foundation**
   - Defined the analysis workflow from raw data to actionable insights.  
   - Compiled a structured dataset of key events affecting oil prices (15+ events).  
   - Documented assumptions and limitations.  

2. **Exploratory Data Analysis (EDA)**
   - Loaded Brent oil price dataset (`brent_oil_prices.csv`).  
   - Cleaned and processed data.  
   - Performed statistical summaries, trend analysis, volatility calculations, and moving averages.  
   - Tested stationarity (ADF test).  
   - Placeholder for visualizations (trend, volatility, distribution, moving averages, rolling statistics).  

3. **Next Steps**
   - Build the Bayesian Change Point Model with PyMC:
     - Define switch points and regime parameters (before/after).  
     - Fit MCMC sampler and interpret posterior distributions.  
     - Associate detected change points with historical events.  
     - Quantify impacts for each major change point.  
   - Optional Extensions:
     - Incorporate macroeconomic variables (GDP, inflation, exchange rates).  
     - Explore advanced models (VAR, Markov-Switching).  
   - Develop an interactive dashboard to visualize trends, volatility, and change points.

---

## Project Structure
week_11_project/
├── data/raw
│ ├── brent_oil_prices.csv # Historical Brent oil prices
│ ├── events.csv # Key geopolitical & OPEC events
├── src/
│ ├── eda.py # EDA and time series analysis class
│ ├── change_point_model.py # Bayesian Change Point model
├── dashboard/
│ ├── app.py # Streamlit dashboard
├── notebooks/
│ ├── EDA.ipynb # EDA notebook
│ ├── Task_1.ipynb # Data Analysis workflow,events
├── requirements.txt
├── README.md
---
