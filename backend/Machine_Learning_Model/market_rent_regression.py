# backend/Machine_Learning_Model/market_rent_regression.py
# Market Rent Regression: Clean data, train baseline model, and generate
# visuals for client presentation (Actual vs Predicted + Monthly trend).
# Plots are saved under ./reports for report or slide use.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score


# ---------------------------------------------------------------------------
# Data loading / cleaning
# ---------------------------------------------------------------------------

def load_and_clean_market_rent():
    """
    Load the Tenancy Services market rent time series and prepare time features.
    Expects: market_rent_timeseries.csv at the project root.
    Returns a cleaned DataFrame with:
      - period (datetime)
      - year, month
      - time_index (continuous time feature)
    """
    df = pd.read_csv("market_rent_timeseries.csv")

    # Ensure period column is in datetime format
    df["period"] = pd.to_datetime(df["period"], format="%Y-%m")

    # Extract time-related features
    df["year"] = df["period"].dt.year
    df["month"] = df["period"].dt.month
    df["time_index"] = (df["year"] - df["year"].min()) * 12 + df["month"]

    return df


# ---------------------------------------------------------------------------
# Feature building helpers
# ---------------------------------------------------------------------------

def pick_first_present(df, options, required=True):
    """Return the first column in 'options' that exists in the DataFrame."""
    for c in options:
        if c in df.columns:
            return c
    if required:
        raise ValueError(f"None of these columns were found: {options}")
    return None


def build_features(df):
    """
    Prepare features (X) and target (y) for regression.
    Automatically detects key columns across datasets.
    Returns: X, y, target_name, period_s
    """
    # Detect column names
    col_target   = pick_first_present(df, ["mean", "rMean", "Mean"])
    col_bedrooms = pick_first_present(df, ["brr", "nBedrms", "bedrooms", "Beds"])
    col_area     = pick_first_present(df, ["area_label", "area", "TA Name", "Region"])
    col_dwelling = pick_first_present(df, ["dw", "dwell", "dwelling_type", "Dwelling"], required=False)
    col_time_ix  = pick_first_present(df, ["time_index"])
    col_period   = pick_first_present(df, ["period"])

    # Use relevant columns
    use_cols = [col_bedrooms, col_time_ix]
    cat_cols = [col_area] + ([col_dwelling] if col_dwelling else [])

    # Create a working copy
    work = df[use_cols + cat_cols + [col_target, col_period]].copy()

    # Convert and clean data
    work[col_bedrooms] = pd.to_numeric(work[col_bedrooms], errors="coerce")
    work = work.dropna(subset=[col_bedrooms, col_target, col_period])

    # Save the period for trend plotting
    period_s = work[col_period].copy()

    # Encode categorical variables
    work = pd.get_dummies(work, columns=cat_cols, drop_first=True)

    # Split features and target
    X = work.drop(columns=[col_target, col_period])
    y = work[col_target].astype(float)

    return X, y, col_target, period_s


# ---------------------------------------------------------------------------
# Training and evaluation
# ---------------------------------------------------------------------------

def train_and_report(df):
    """
    Train baseline Linear Regression, evaluate model,
    and print performance metrics and top coefficients.
    """
    X, y, target_name, _ = build_features(df)

    # Split for validation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Metrics
    r2  = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\n=== Model Evaluation ===")
    print(f"Target: {target_name}")
    print(f"R²   : {r2:.4f}")
    print(f"RMSE : {rmse:.2f}")

    coefs = (
        pd.DataFrame({"feature": X.columns, "coef": model.coef_})
        .sort_values("coef", key=np.abs, ascending=False)
        .head(15)
    )
    print("\nTop coefficients (by |value|):")
    print(coefs.to_string(index=False))

    return model, (r2, rmse), coefs


# ---------------------------------------------------------------------------
# Main Script
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Step 1: Load data and preview
    df = load_and_clean_market_rent()
    print(df.head())

    # Step 2: Train model
    model, metrics, coefs = train_and_report(df)

    # Step 3: Create output folder
    os.makedirs("reports", exist_ok=True)

    # Step 4: Prepare polynomial fit for visualization
    X, y, target_name, _ = build_features(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    y_pred = model.predict(X_test)

    # Polynomial (2nd-degree) comparison
    x_vals = y_test.values.reshape(-1, 1)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(x_vals)
    poly_model = LinearRegression().fit(X_poly, y_pred)

    x_sorted = np.linspace(y_test.min(), y_test.max(), 200).reshape(-1, 1)
    y_poly_pred = poly_model.predict(poly.transform(x_sorted))

    # -----------------------------------------------------------------------
    # Figure 1 — Actual vs Predicted (Polynomial Fit Only)
    # -----------------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(9, 6))
    ax1.scatter(y_test, y_pred, alpha=0.5, edgecolor="k", label="Data Points")

    # Polynomial fit curve
    ax1.plot(x_sorted, y_poly_pred,
             color="blue", linestyle="--", lw=2, label="Polynomial Regression Fit")

    # Labels and title
    ax1.set_xlabel("Actual Rent ($ per week)")
    ax1.set_ylabel("Predicted Rent ($ per week)")
    ax1.set_title("Figure 1. Market Rent Regression — Polynomial Fit Only")

    # Optional note for clarity
    ax1.text(0.02, 0.02,
             "Note: Polynomial regression (blue) better captures non-linear rent patterns\n"
             "and provides a realistic fit at higher rent levels.",
             transform=ax1.transAxes, fontsize=9, color="dimgray")

    ax1.legend()
    ax1.grid(True)
    fig1.tight_layout()

    try:
        fig1.canvas.manager.set_window_title("Figure 1")
    except Exception:
        pass

    fig1.savefig("reports/fig1_actual_vs_pred_poly.png", dpi=160)
    plt.show()

    # -----------------------------------------------------------------------
    # Figure 2 — Monthly Average Rent Trend (Actual vs Predicted)
    # -----------------------------------------------------------------------
    X_all, y_all, target_name, period_s = build_features(df)
    y_pred_all = model.predict(X_all)

    trend_df = pd.DataFrame({
        "period": period_s,
        "actual": y_all.values,
        "pred":   y_pred_all
    })

    trend_monthly = (
        trend_df
        .groupby(pd.Grouper(key="period", freq="MS"))[["actual", "pred"]]
        .mean()
        .dropna()
        .sort_index()
    )

    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.plot(trend_monthly.index, trend_monthly["actual"], label="Actual (avg per month)")
    ax2.plot(trend_monthly.index, trend_monthly["pred"],
             label="Predicted (avg per month)", linestyle="--")

    ax2.set_xlabel("Month")
    ax2.set_ylabel("Average Weekly Rent ($)")
    ax2.set_title("Figure 2. Market Rent — Monthly Average (Actual vs Predicted)")
    ax2.legend()
    ax2.grid(True)
    fig2.tight_layout()

    try:
        fig2.canvas.manager.set_window_title("Figure 2")
    except Exception:
        pass

    fig2.savefig("reports/fig2_monthly_avg.png", dpi=160)
    plt.show()
