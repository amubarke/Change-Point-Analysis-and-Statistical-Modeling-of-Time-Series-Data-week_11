
from flask import Flask, jsonify
import pandas as pd
from datetime import datetime
from flask_cors import CORS

class DashboardAPI:

    def __init__(self, prices_csv_path, events_csv_path):

        # Initialize Flask app
        self.app = Flask(__name__)
        CORS(self.app)
        # Load datasets
        self.historical_prices = self.load_historical_prices(prices_csv_path)
        self.events = self.load_events(events_csv_path)
        self.change_points = self.load_change_points()

        # Setup routes
        self.setup_routes()

    # Load Brent oil prices from CSV
    def load_historical_prices(self, csv_path):

        df = pd.read_csv(csv_path)

        # Convert Date column (20-May-87 format)
        df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True, errors="coerce")


        # Ensure price is numeric
        df["Price"] = df["Price"].astype(float)

        return df

    # Load events from CSV
    def load_events(self, csv_path):

        df = pd.read_csv(csv_path)

        # Convert Start_Date column
        df["Start_Date"] = pd.to_datetime(df["Start_Date"])

        return df

    # Change point data (sample, replace if needed)
    def load_change_points(self):

        data = {
            "ChangePoint_Index": [4376],
            "Date": [datetime(2004, 8, 5)],
            "Mean_Before": [0.0004],
            "Mean_After": [0.0001],
            "Difference": [-0.0003]
        }

        df = pd.DataFrame(data)

        return df

    # Setup Flask API routes
    def setup_routes(self):

        @self.app.route("/")
        def index():
            return jsonify({"message": "Dashboard API is running."})

        # Prices API
        @self.app.route("/api/historical_prices", methods=["GET"])
        def historical_prices():
            return self.historical_prices.to_json(
                orient="records",
                date_format="iso"
            )

        # Events API
        @self.app.route("/api/events", methods=["GET"])
        def events():
            return self.events.to_json(
                orient="records",
                date_format="iso"
            )

        # Change points API
        @self.app.route("/api/change_points", methods=["GET"])
        def change_points():
            return self.change_points.to_json(
                orient="records",
                date_format="iso"
            )

    # Run Flask app
    def run(self):

        self.app.run(debug=True)


# ============================
# Usage
# ============================

if __name__ == "__main__":

    prices_path = r"E:\Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data-week_11\data\raw\BrentOilPrices.csv"

    events_path = r"E:\Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data-week_11\data\raw\event.csv"

    dashboard_api = DashboardAPI(prices_path, events_path)

    dashboard_api.run()
