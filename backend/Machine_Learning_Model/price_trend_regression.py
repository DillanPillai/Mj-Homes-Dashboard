# backend/Machine_Learning_Model/price_trend_regression.py
# Purpose: Analyse NZ house price growth trends using polynomial regression.
# Dataset: oneroof_house_price_report_sep_2025.csv
# Outputs:
#   - Figure 1: Polynomial House Price Trend (NZ)
#   - Figure 2: Regional Comparison (NZ, Auckland, Wellington)
# All plots are saved to ./reports for presentation and dashboard use.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

# ---------------------------------------------------------------------------
# 1. Load and prepare the dataset
# ---------------------------------------------------------------------------

def load_and_prepare_prices():
    """
    Load and clean house price data.
    Adds a continuous time index for regression.
    Expects columns: Date, NZ, Auckland, Wellington.
    """
    df = pd.read_csv("backend/Machine_Learning_Model/oneroof_house_price_report_sep_2025.csv")


    # Ensure Date is in datetime format
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    # Add continuous numeric time index (for regression)
    df["time_index"] = np.arange(len(df))

    return df


# ---------------------------------------------------------------------------
# 2. Train polynomial regression model
# ---------------------------------------------------------------------------

def train_polynomial_model(df):
    """
    Fit a 2nd-degree polynomial regression model on NZ average prices.
    Returns the model, transformer, and predicted values.
    """
    X = df[["time_index"]].values
    y = df["NZ"].values

    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)

    y_pred = model.predict(X_poly)

    # Evaluate model performance
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))

    print("\n=== Model Performance Summary ===")
    print(f"Polynomial Regression (deg=2) -> R²: {r2:.4f}, RMSE: {rmse:.2f}")

    return model, poly, y_pred


# ---------------------------------------------------------------------------
# 3. Generate and save visualisations
# ---------------------------------------------------------------------------

def create_visualisations(df, y_pred_poly):
    """
    Creates and saves:
    - Figure 1: Polynomial Trend for NZ House Prices
    - Figure 2: Regional Comparison (NZ, Auckland, Wellington)
    """
    os.makedirs("reports", exist_ok=True)

    # === Figure 1: Polynomial Price Trend ===
    fig1, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(df["Date"], df["NZ"], "o", alpha=0.5, markersize=4, label="Actual Prices")
    ax1.plot(df["Date"], y_pred_poly, "b--", lw=2, label="Polynomial Fit (2nd Degree)")

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Average House Price ($)")
    ax1.set_title("Figure 1. NZ House Price Trend — Polynomial Fit Only")
    ax1.legend()
    ax1.grid(True)

    # Caption note for clarity
    ax1.text(0.02, 0.02,
             "Note: The polynomial curve captures the non-linear trend in NZ house prices,\n"
             "highlighting the rapid growth between 2020–2022 and the stabilisation post-2023.",
             transform=ax1.transAxes, fontsize=9, color="dimgray")

    fig1.tight_layout()
    fig1.savefig("reports/fig1_price_trend_poly.png", dpi=160)
    plt.show()

    # === Figure 2: Regional Comparison ===
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    for region in ["NZ", "Auckland", "Wellington"]:
        if region in df.columns:
            ax2.plot(df["Date"], df[region], label=region)

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Average House Price ($)")
    ax2.set_title("Figure 2. Regional House Price Comparison — NZ vs Major Cities")
    ax2.legend()
    ax2.grid(True)
    fig2.tight_layout()
    fig2.savefig("reports/fig2_regional_comparison.png", dpi=160)
    plt.show()


# ---------------------------------------------------------------------------
# 4. Run workflow
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df = load_and_prepare_prices()
    print(df.head())

    model, poly, y_pred_poly = train_polynomial_model(df)
    create_visualisations(df, y_pred_poly)
