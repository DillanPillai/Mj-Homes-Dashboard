# backend/Machine_Learning_Model/market_rent_regression.py
# Market Rent linear regression: clean data, train baseline model, and produce
# client-ready visuals (Actual vs Predicted scatter + Monthly trend).
# Plots are also saved to ./reports for easy use in slides.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# ---------------------------------------------------------------------------
# Data loading / cleaning
# ---------------------------------------------------------------------------

def load_and_clean_market_rent():
    """
    Load the Tenancy Services market rent time series and create time features.
    Assumes CSV is at the project root as: market_rent_timeseries.csv
    Returns a tidy DataFrame with:
      - period (datetime)
      - year, month (ints)
      - time_index (months since start; useful as a continuous time proxy)
    """
    df = pd.read_csv("market_rent_timeseries.csv")

    # Ensure period is proper datetime (e.g., '2025-06' -> 2025-06-01)
    df["period"] = pd.to_datetime(df["period"], format="%Y-%m")

    # Basic time features
    df["year"] = df["period"].dt.year
    df["month"] = df["period"].dt.month
    df["time_index"] = (df["year"] - df["year"].min()) * 12 + df["month"]

    return df


# ---------------------------------------------------------------------------
# Feature building helpers
# ---------------------------------------------------------------------------

def pick_first_present(df, options, required=True):
    """
    Return the first column name from 'options' that exists in df.columns.
    If 'required' and none match, raise an error.
    """
    for c in options:
        if c in df.columns:
            return c
    if required:
        raise ValueError(f"None of these columns were found: {options}")
    return None


def build_features(df):
    """
    Prepare features (X) and target (y) for regression and return:
      X, y, target_name, period_s

    - Detects actual column names (handles header variants across datasets).
    - Uses bedrooms + time_index + one-hot dummies for area and dwelling type.
    - Returns a period Series aligned with X/y for monthly trend plotting.
    """
    # Detect columns seen across your files/screenshots
    col_target   = pick_first_present(df, ["mean", "rMean", "Mean"])
    col_bedrooms = pick_first_present(df, ["brr", "nBedrms", "bedrooms", "Beds"])
    col_area     = pick_first_present(df, ["area_label", "area", "TA Name", "Region"])
    col_dwelling = pick_first_present(df, ["dw", "dwell", "dwelling_type", "Dwelling"], required=False)
    col_time_ix  = pick_first_present(df, ["time_index"])
    col_period   = pick_first_present(df, ["period"])  # datetime set above

    # Base numeric + categorical features
    use_cols = [col_bedrooms, col_time_ix]
    cat_cols = [col_area] + ([col_dwelling] if col_dwelling else [])

    # Work on a minimal copy
    work = df[use_cols + cat_cols + [col_target, col_period]].copy()

    # Coerce bedrooms to numeric and drop rows missing key fields
    work[col_bedrooms] = pd.to_numeric(work[col_bedrooms], errors="coerce")
    work = work.dropna(subset=[col_bedrooms, col_target, col_period])

    # Save aligned period before encoding
    period_s = work[col_period].copy()

    # One-hot encode categoricals
    work = pd.get_dummies(work, columns=cat_cols, drop_first=True)

    # Split into features and target
    X = work.drop(columns=[col_target, col_period])
    y = work[col_target].astype(float)

    return X, y, col_target, period_s


# ---------------------------------------------------------------------------
# Training / reporting
# ---------------------------------------------------------------------------

def train_and_report(df):
    """
    Train a baseline Linear Regression, evaluate on a test split,
    and print key metrics and top coefficients.
    RMSE is computed as sqrt(MSE) for compatibility with all sklearn versions.
    """
    X, y, target_name, _ = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2  = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print("\n=== Model evaluation ===")
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
# Script entry point (single run block)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 1) Load and show a small preview (keep this single head print)
    df = load_and_clean_market_rent()
    print(df.head())

    # 2) Train baseline model and report metrics
    model, metrics, coefs = train_and_report(df)

    # Create folder for saving plots
    os.makedirs("reports", exist_ok=True)

        # 3) Scatter: Actual vs Predicted (Figure 1) + Polynomial Comparison
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression

    X, y, target_name, _ = build_features(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    y_pred = model.predict(X_test)

    # === Polynomial fit for comparison (2nd-degree) ===
    x_vals = y_test.values.reshape(-1, 1)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(x_vals)
    poly_model = LinearRegression().fit(X_poly, y_pred)

    # Smooth curve for plotting
    x_sorted = np.linspace(y_test.min(), y_test.max(), 200).reshape(-1, 1)
    y_poly_pred = poly_model.predict(poly.transform(x_sorted))

    # === Plot ===
    fig1, ax1 = plt.subplots(figsize=(9, 6))
    ax1.scatter(y_test, y_pred, alpha=0.5, edgecolor="k", label="Data Points")

    lo, hi = float(y_test.min()), float(y_test.max())
    ax1.plot([lo, hi], [lo, hi], "r--", lw=2, label="Linear Fit")
    ax1.plot(x_sorted, y_poly_pred,
             color="blue", linestyle="--", lw=2, label="Polynomial Fit (2nd Degree)")

    ax1.set_xlabel("Actual Rent ($ per week)")
    ax1.set_ylabel("Predicted Rent ($ per week)")
    ax1.set_title("Figure 1. Market Rent Regression — Linear vs Polynomial Fit")
    ax1.text(0.02, 0.02,
             "Note: Polynomial curve (blue) captures non-linear rent trend\n"
             "at higher price ranges ($800+ per week).",
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

# 4) Monthly Average Trend (Figure 2)
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
ax2.plot(trend_monthly.index, trend_monthly["pred"],   label="Predicted (avg per month)", linestyle="--")

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
