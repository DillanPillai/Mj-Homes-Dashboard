import os
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

def _pick_dataset_path() -> Path | None:
    data_dir = Path("data_processing")
    xlsx = data_dir / "MockData.xlsx"
    csvp = data_dir / "MockData.csv"
    if xlsx.exists() and csvp.exists():
        return xlsx if xlsx.stat().st_mtime >= csvp.stat().st_mtime else csvp
    if xlsx.exists():
        return xlsx
    if csvp.exists():
        return csvp
    return None

src = _pick_dataset_path()
if not src:
    raise SystemExit("No MockData.xlsx or MockData.csv found in data_processing/")

df = pd.read_excel(src) if src.suffix.lower() == ".xlsx" else pd.read_csv(src)

# Rename columns as used in training
df = df.rename(columns={
    "Bedrooms": "bedrooms",
    "Bathrooms": "bathrooms",
    "Suburb": "suburb",
    "Weekly Rent ($NZD)": "rent_price",
})

# Basic cleaning
df = df.dropna(subset=["bedrooms", "bathrooms", "rent_price", "suburb"]).copy()
if "floor_area" not in df.columns:
    df["floor_area"] = 100

# One-hot suburbs
df = pd.get_dummies(df, columns=["suburb"])

X = df[["bedrooms", "bathrooms", "floor_area"] + [c for c in df.columns if c.startswith("suburb_")]]
y = df["rent_price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
mse = mean_squared_error(y_test, model.predict(X_test))
print(f"Model trained. MSE: {mse:.2f} (source: {src.name})")

model_path = os.path.join("Machine_Learning_Model", "rental_model.pkl")
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
