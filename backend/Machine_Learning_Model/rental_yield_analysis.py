# backend/Machine_Learning_Model/rental_yield_analysis.py
# Purpose: Analyse rental yield (return on investment) trends and regional differences.
# Datasets:
#   - backend/Machine_Learning_Model/oneroof_house_price_report_sep_2025.csv
#   - market_rent_timeseries.csv
# Outputs:
#   - Figure 1: Average Rental Yield by Region
#   - Figure 2: Rental Yield Trend Over Time
#   - All plots saved in ./reports for dashboard integration or reporting.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------------------------------------------------------------------
# 1. Load and prepare data
# ---------------------------------------------------------------------------

def load_and_prepare_data():
    """
    Loads house price and rent datasets and prepares them for yield analysis.
    Returns a merged DataFrame with Date, Region, Rent, Price, and Yield (%).
    """

    # Load house price data (national + regional)
    prices = pd.read_csv("backend/Machine_Learning_Model/oneroof_house_price_report_sep_2025.csv")
    prices["Date"] = pd.to_datetime(prices["Date"], dayfirst=True, errors="coerce")
    prices = prices.dropna(subset=["Date"])
    prices = prices[["Date", "NZ", "Auckland", "Wellington"]]

    # Load rent data
    rents = pd.read_csv("market_rent_timeseries.csv")
    rents["period"] = pd.to_datetime(rents["period"], format="%Y-%m", errors="coerce")
    rents = rents.dropna(subset=["period"])
    rents = rents.groupby("period")["mean"].mean().reset_index()
    rents = rents.rename(columns={"period": "Date", "mean": "NZ_Rent"})

    # Merge national data (nearest date)
    merged = pd.merge_asof(
        prices.sort_values("Date"),
        rents.sort_values("Date"),
        on="Date",
        direction="nearest",
        tolerance=pd.Timedelta("31D")
    ).dropna(subset=["NZ_Rent"])

    # Calculate annualised rental yield (%)
    merged["Rental_Yield_NZ"] = (merged["NZ_Rent"] * 52 / merged["NZ"]) * 100
    merged["Rental_Yield_Auckland"] = (merged["NZ_Rent"] * 52 / merged["Auckland"]) * 100
    merged["Rental_Yield_Wellington"] = (merged["NZ_Rent"] * 52 / merged["Wellington"]) * 100

    return merged


# ---------------------------------------------------------------------------
# 2. Regression and summary
# ---------------------------------------------------------------------------

def fit_yield_trend(df):
    """
    Fits a simple linear regression model to see how NZ rental yield changes over time.
    """
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["Rental_Yield_NZ"].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    print("\n=== Rental Yield Trend Model Evaluation ===")
    print(f"R²: {r2:.4f}")
    print(f"Trend Direction: {'Increasing' if model.coef_[0] > 0 else 'Decreasing'} over time")

    return model, y_pred


# ---------------------------------------------------------------------------
# 3. Visualisations
# ---------------------------------------------------------------------------

def create_visualisations(df, y_pred):
    """
    Creates and saves two key figures:
    - Figure 1: Average Rental Yield by Region
    - Figure 2: Yield Trend Over Time
    """
    os.makedirs("backend/Machine_Learning_Model/reports", exist_ok=True)

    # === Figure 1: Average Rental Yield by Region ===
    avg_yields = {
        "New Zealand": df["Rental_Yield_NZ"].mean(),
        "Auckland": df["Rental_Yield_Auckland"].mean(),
        "Wellington": df["Rental_Yield_Wellington"].mean()
    }

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(avg_yields.keys(), avg_yields.values(), color=["#4B8BBE", "#FFD43B", "#306998"], alpha=0.8)
    ax1.set_ylabel("Average Rental Yield (%)")
    ax1.set_title("Figure 1. Average Rental Yield by Region")
    ax1.grid(axis="y", linestyle="--", alpha=0.6)
    for i, val in enumerate(avg_yields.values()):
        ax1.text(i, val + 0.05, f"{val:.2f}%", ha="center", fontsize=9)

    fig1.tight_layout()
    fig1.savefig("backend/Machine_Learning_Model/reports/fig1_rental_yield_regions.png", dpi=200)

    # === Figure 2: Yield Trend Over Time (NZ) ===
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.plot(df["Date"], df["Rental_Yield_NZ"], color="purple", lw=2, label="Observed Yield")
    ax2.plot(df["Date"], y_pred, "r--", lw=2, label="Linear Trend")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Rental Yield (%)")
    ax2.set_title("Figure 2. NZ Rental Yield Trend Over Time")
    ax2.legend()
    ax2.grid(True)
    ax2.text(0.02, 0.02,
             "Note: A declining yield trend indicates house prices rising faster than rents.\n"
             "A stabilising or upward trend suggests improving investment returns.",
             transform=ax2.transAxes, fontsize=9, color="dimgray")

    fig2.tight_layout()
    fig2.savefig("backend/Machine_Learning_Model/reports/fig2_rental_yield_trend.png", dpi=200)

    plt.show()


# ---------------------------------------------------------------------------
# 4. Run workflow
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df = load_and_prepare_data()
    print(df.head())

    model, y_pred = fit_yield_trend(df)
    create_visualisations(df, y_pred)
