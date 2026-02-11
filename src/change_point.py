# brent_change_point_v2.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
import os

class BrentChangePointAnalyzer:
    """
    Bayesian Change Point Analysis for Brent Oil Prices
    Includes EDA tables, visualizations, Bayesian modeling, and result interpretation
    """

    REQUIRED_COLUMNS = ['Date', 'Price']

    def __init__(self, file_path, event_data=None):
        """
        Initialize with CSV file path and optional events DataFrame
        """
        self.file_path = file_path
        self.event_data = event_data
        self.data = None
        self.log_returns = None
        self.model = None
        self.trace = None

    # ----------------------------
    # Data Loading & Validation
    # ----------------------------
    def load_data(self):
        """Load CSV data and validate required columns"""
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")

            self.data = pd.read_csv(self.file_path)
            missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in self.data.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")

            if self.data[self.REQUIRED_COLUMNS].isnull().any().any():
                print("⚠ Warning: Missing values detected in data")

            print(f"✅ Data loaded successfully: {self.data.shape[0]} rows, {self.data.shape[1]} columns")

        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.data = None

    def convert_date(self):
        """Convert Date column to datetime and sort"""
        try:
            assert self.data is not None, "Data not loaded"
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            self.data = self.data.sort_values('Date').reset_index(drop=True)
            print("✅ Date column converted and data sorted")
        except Exception as e:
            print(f"❌ Error converting date: {e}")

    def compute_log_returns(self):
        """Compute log returns for stationarity analysis"""
        try:
            assert 'Price' in self.data.columns, "Price column missing"
            self.data['LogReturn'] = np.log(self.data['Price']).diff()
            self.log_returns = self.data['LogReturn'].dropna().reset_index(drop=True)
            print("✅ Log returns computed")
        except Exception as e:
            print(f"❌ Error computing log returns: {e}")

    # ----------------------------
    # Exploratory Data Analysis
    # ----------------------------
    def show_table(self, cols=None, n=5):
        """Display top rows as a table before plotting"""
        try:
            if self.data is None:
                raise ValueError("Data not loaded")
            display_df = self.data[cols] if cols else self.data
            print(display_df.head(n))
        except Exception as e:
            print(f"❌ Error showing table: {e}")

    def plot_price_series(self):
        """Plot Brent oil price time series"""
        try:
            self.show_table(cols=['Date', 'Price'], n=10)  # show first 10 rows as table
            plt.figure(figsize=(12,5))
            plt.plot(self.data['Date'], self.data['Price'], color='blue')
            plt.title("Brent Oil Price Over Time")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.show()
        except Exception as e:
            print(f"❌ Error plotting price series: {e}")

    def plot_log_returns(self):
        """Plot log returns time series"""
        try:
            self.show_table(cols=['Date', 'LogReturn'], n=10)
            plt.figure(figsize=(12,5))
            plt.plot(self.data['Date'][1:], self.log_returns, color='red')
            plt.title("Log Returns of Brent Oil Price")
            plt.xlabel("Date")
            plt.ylabel("Log Return")
            plt.show()
        except Exception as e:
            print(f"❌ Error plotting log returns: {e}")

    # ----------------------------
    # Bayesian Change Point Model
    # ----------------------------
    def build_change_point_model(self):
        """Define Bayesian model with one change point"""
        try:
            assert self.log_returns is not None, "Log returns not computed"
            y = self.log_returns.values
            n = len(y)

            with pm.Model() as model:
                # Switch point tau (discrete uniform)
                tau = pm.DiscreteUniform("tau", lower=0, upper=n-1)

                # Means before and after change
                mu1 = pm.Normal("mu1", mu=np.mean(y), sigma=np.std(y))
                mu2 = pm.Normal("mu2", mu=np.mean(y), sigma=np.std(y))

                # Shared standard deviation
                sigma = pm.HalfNormal("sigma", sigma=np.std(y))

                # Switch function
                mu = pm.math.switch(tau >= np.arange(n), mu2, mu1)

                # Likelihood
                obs = pm.Normal("obs", mu=mu, sigma=sigma, observed=y)

                self.model = model

            print("✅ Bayesian Change Point model built")
        except Exception as e:
            print(f"❌ Error building model: {e}")

    def run_sampler(self, tune=500, draws=1000, chains=2, target_accept=0.9):
        """
        Run MCMC sampling with configurable speed/quality"""

        try:
           assert self.model is not None, "Model not built"

           with self.model:
                self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                target_accept=target_accept,
                return_inferencedata=True
            )

           print(f"✅ Sampling completed: {draws} draws, {tune} tuning steps, {chains} chains")

        except Exception as e:
           print(f"❌ Error during sampling: {e}")

    # ----------------------------
    # Post-Processing & Visualization
    # ----------------------------
    def plot_trace(self):
        """Plot trace for all parameters"""
        try:
            az.plot_trace(self.trace)
            plt.show()
        except Exception as e:
            print(f"❌ Error plotting trace: {e}")

    def plot_posterior_tau(self):
        """Plot posterior of change point tau"""
        try:
            az.plot_posterior(self.trace, var_names=["tau"])
            plt.title("Posterior Distribution of Change Point (tau)")
            plt.show()
        except Exception as e:
            print(f"❌ Error plotting posterior tau: {e}")

    def summarize_change_point(self):
        """Summarize change point index, date, and mu1/mu2"""
        try:
            tau_post = self.trace.posterior['tau'].values.flatten()
            tau_mean = int(np.mean(tau_post))
            change_date = self.data['Date'].iloc[tau_mean + 1]  # offset for log returns
            mu1_mean = self.trace.posterior['mu1'].values.mean()
            mu2_mean = self.trace.posterior['mu2'].values.mean()

            print(f"🔹 Most probable change point index: {tau_mean}")
            print(f"🔹 Corresponding date: {change_date}")
            print(f"🔹 Mean log return before change: {mu1_mean:.4f}")
            print(f"🔹 Mean log return after change: {mu2_mean:.4f}")
            print(f"🔹 Difference: {mu2_mean - mu1_mean:.4f}")

            return change_date, mu1_mean, mu2_mean
        except Exception as e:
            print(f"❌ Error summarizing change point: {e}")
            return None, None, None
