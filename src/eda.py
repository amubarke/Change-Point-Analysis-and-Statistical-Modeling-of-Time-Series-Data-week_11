import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller

file_path = pd.read_csv('../data/raw/BrentOilPrices.csv')

class BrentOilAnalyzer:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None


    # =========================
    # DATA LOADING & CLEANING
    # =========================

    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        print("✅ Data loaded successfully")


    def convert_date(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data = self.data.sort_values('Date')
        print("✅ Date converted")


    def clean_data(self):

        self.data = self.data.drop_duplicates()

        self.data['Price'] = pd.to_numeric(
            self.data['Price'],
            errors='coerce'
        )

        self.data = self.data.dropna()

        print("✅ Data cleaned")


    # =========================
    # TABLE METHODS
    # =========================

    def show_head(self, n=5):
        return self.data.head(n)


    def describe_data(self):
        return self.data.describe()


    def missing_values(self):
        return self.data.isnull().sum()


    # =========================
    # VISUALIZATION + TABLES
    # =========================

    def plot_trend(self, preview_rows=5):

        print("📋 Trend Data Preview")
        display(
            self.data[['Date', 'Price']]
            .head(preview_rows)
        )

        plt.figure()
        plt.plot(self.data['Date'], self.data['Price'])
        plt.title("Brent Oil Price Trend")
        plt.xlabel("Year")
        plt.ylabel("Price (USD)")
        plt.show()


    def plot_volatility(self, window=30, preview_rows=5):

        self.data['Volatility'] = (
            self.data['Price']
            .rolling(window)
            .std()
        )

        print(f"📋 Rolling Volatility (Window={window}) Preview")

        display(
            self.data[['Date', 'Volatility']]
            .dropna()
            .head(preview_rows)
        )

        plt.figure()
        plt.plot(self.data['Date'], self.data['Volatility'])
        plt.title(f"Rolling Volatility ({window} Days)")
        plt.xlabel("Year")
        plt.ylabel("Volatility")
        plt.show()


    def plot_distribution(self, preview_rows=10):

        print("📋 Price Distribution Summary")

        display(
            self.data['Price']
            .describe()
            .to_frame()
        )

        plt.figure()
        plt.hist(self.data['Price'], bins=50)
        plt.title("Price Distribution")
        plt.xlabel("Price")
        plt.ylabel("Frequency")
        plt.show()


    def plot_moving_average(self,
                            short=30,
                            long=365,
                            preview_rows=5):

        self.data['MA_Short'] = (
            self.data['Price']
            .rolling(short)
            .mean()
        )

        self.data['MA_Long'] = (
            self.data['Price']
            .rolling(long)
            .mean()
        )

        print("📋 Moving Average Preview")

        display(
            self.data[
                ['Date', 'Price', 'MA_Short', 'MA_Long']
            ]
            .dropna()
            .head(preview_rows)
        )

        plt.figure()

        plt.plot(
            self.data['Date'],
            self.data['Price'],
            label="Price"
        )

        plt.plot(
            self.data['Date'],
            self.data['MA_Short'],
            label=f"{short}-Day MA"
        )

        plt.plot(
            self.data['Date'],
            self.data['MA_Long'],
            label=f"{long}-Day MA"
        )

        plt.title("Moving Averages")
        plt.xlabel("Year")
        plt.ylabel("Price")
        plt.legend()
        plt.show()


    def rolling_stats(self,
                      window=365,
                      preview_rows=5):

        self.data['Roll_Mean'] = (
            self.data['Price']
            .rolling(window)
            .mean()
        )

        self.data['Roll_Var'] = (
            self.data['Price']
            .rolling(window)
            .var()
        )

        print("📋 Rolling Statistics Preview")

        display(
            self.data[
                ['Date', 'Roll_Mean', 'Roll_Var']
            ]
            .dropna()
            .head(preview_rows)
        )

        plt.figure()

        plt.plot(
            self.data['Date'],
            self.data['Roll_Mean'],
            label="Rolling Mean"
        )

        plt.plot(
            self.data['Date'],
            self.data['Roll_Var'],
            label="Rolling Variance"
        )

        plt.title("Rolling Mean & Variance")
        plt.xlabel("Year")
        plt.legend()
        plt.show()


    # =========================
    # STATIONARITY TEST
    # =========================

    def adf_test(self):

        print("📋 ADF Test Input Preview")

        display(
            self.data[['Date', 'Price']]
            .head()
        )

        result = adfuller(self.data['Price'])

        print("\nADF Statistic:", result[0])
        print("p-value:", result[1])

        if result[1] <= 0.05:
            print("✅ Series is Stationary")
        else:
            print("❌ Series is Non-Stationary")
