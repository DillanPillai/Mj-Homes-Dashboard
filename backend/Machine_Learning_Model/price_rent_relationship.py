# backend/Machine_Learning_Model/price_rent_relationship.py
# Purpose: Analyse the relationship between average house prices and market rent.
# Datasets:
#   - backend/Machine_Learning_Model/oneroof_house_price_report_sep_2025.csv
#   - market_rent_timeseries.csv
# Outputs:
#   - Figure 1: Polynomial regression (Price vs Rent)
#   - Figure 2: Price-to-Rent Ratio Over Time
#   - Saved in ./reports for presentation or dashboard use.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score


# ---------------------------------------------------------------------------
# 1. Load and merge datasets
# ---------------------------------------------------------------------------

def load_and_merge_data():
    """
    Load the house price and market rent datasets and merge on time.
    Returns a merged DataFrame with columns:
        Date, NZ_HousePrice, NZ_Rent
    """

    # Load house price data (inside Machine_Learning_Model folder)
    prices = pd.read_csv("backend/Machine_Learning_Model/oneroof_house_price_report_sep_2025.csv")
    prices["Date"] = pd.to_datetime(prices["Date"], dayfirst=True, errors="coerce")
    prices = prices.dropna(subset=["Date"])
    prices = prices[["Date", "NZ"]].rename(columns={"NZ": "NZ_HousePrice"})

    # Load market rent data (in project root)
    rents = pd.read_csv("market_rent_timeseries.csv")
    rents["period"] = pd.to_datetime(rents["period"], format="%Y-%m", errors="coerce")
    rents = rents.dropna(subset=["period"])
    rents = rents.groupby("period")["mean"].mean().reset_index()
    rents = rents.rename(columns={"period": "Date", "mean": "NZ_Rent"})

    # Merge by nearest date (monthly alignment)
    merged = pd.merge_asof(
        prices.sort_values("Date"),
        rents.sort_values("Date"),
        on="Date",
        direction="nearest",
        tolerance=pd.Timedelta("31D")
    )

    merged = merged.dropna(subset=["NZ_HousePrice", "NZ_Rent"]).reset_index(drop=True)
    return merged


# ---------------------------------------------------------------------------
# 2. Train polynomial regression model
# ---------------------------------------------------------------------------

def train_price_rent_model(df):
    """
    Fit a polynomial regression model to predict house prices based on rent.
    """
    X = df[["NZ_Rent"]].values
    y = df["NZ_HousePrice"].values

    # Polynomial regression (degree 2)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)
    y_pred = model.predict(X_poly)

    # Evaluate
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))

    print("\n=== Price–Rent Relationship Model Evaluation ===")
    print(f"R²   : {r2:.4f}")
    print(f"RMSE : {rmse:,.2f}")

    return model, poly, y_pred, r2


# ---------------------------------------------------------------------------
# 3. Visualisations
# ---------------------------------------------------------------------------

def create_visualisations(df, model, poly, y_pred, r2):
    """
    Create and save both regression and ratio trend figures.
    """
    os.makedirs("backend/Machine_Learning_Model/reports", exist_ok=True)

    # === Figure 1: Price vs Rent Polynomial Fit ===
    rent_range = np.linspace(df["NZ_Rent"].min(), df["NZ_Rent"].max(), 200).reshape(-1, 1)
    rent_pred = model.predict(poly.transform(rent_range))

    fig1, ax1 = plt.subplots(figsize=(10, 6))  # wider layout
    ax1.scatter(df["NZ_Rent"], df["NZ_HousePrice"], alpha=0.6, edgecolor="k", label="Data Points")
    ax1.plot(rent_range, rent_pred, "b--", lw=2.5, label="Polynomial Fit (2nd Degree)")

    # --- key formatting changes ---
    ax1.set_xlim(df["NZ_Rent"].min() - 20, df["NZ_Rent"].max() + 20)
    ax1.set_ylim(df["NZ_HousePrice"].min() - 50000, df["NZ_HousePrice"].max() + 50000)
    ax1.ticklabel_format(style='plain', axis='y')

    ax1.set_xlabel("Average Rent ($ per week)", fontsize=11)
    ax1.set_ylabel("Average House Price (NZD $)", fontsize=11)
    ax1.set_title("Figure 1. Price–Rent Relationship — Polynomial Fit Only", fontsize=13, pad=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax1.text(0.03, 0.05,
             "Polynomial regression (blue) reveals a mild non-linear relationship.\n"
             "House prices rise with rent levels up to a point, then stabilise — indicating limited price elasticity.",
             transform=ax1.transAxes, fontsize=9.5, color="dimgray")

    ax1.text(0.83, 0.92, f"R² = {r2:.2f}", transform=ax1.transAxes, fontsize=10, color="dimgray")

    fig1.tight_layout()
    fig1.savefig("backend/Machine_Learning_Model/reports/fig1_price_rent_relationship.png", dpi=200)

    # === Figure 2: Price-to-Rent Ratio Over Time ===
    df["Price_to_Rent_Ratio"] = df["NZ_HousePrice"] / (df["NZ_Rent"] * 52)
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.plot(df["Date"], df["Price_to_Rent_Ratio"], color="purple", lw=2)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Price-to-Rent Ratio (Years of Rent to Buy)")
    ax2.set_title("Figure 2. NZ Price-to-Rent Ratio Over Time")
    ax2.grid(True)
    ax2.text(0.02, 0.02,
             "Note: A higher ratio indicates reduced affordability and lower rental yields.\n"
             "A declining trend suggests stabilisation in house prices relative to rents.",
             transform=ax2.transAxes, fontsize=9, color="dimgray")
    fig2.tight_layout()
    fig2.savefig("backend/Machine_Learning_Model/reports/fig2_price_to_rent_ratio.png", dpi=160)

    plt.show()


# ---------------------------------------------------------------------------
# 4. Run workflow
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df = load_and_merge_data()
    print(df.head())

    model, poly, y_pred, r2 = train_price_rent_model(df)
    create_visualisations(df, model, poly, y_pred, r2)
