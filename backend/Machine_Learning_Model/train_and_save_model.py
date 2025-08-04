import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

# Load Excel data
file_path = os.path.join("data_processing", "MockData.xlsx")
df = pd.read_excel(file_path)

# Rename columns
df.rename(columns={
    'Bedrooms': 'bedrooms',
    'Bathrooms': 'bathrooms',
    'Suburb': 'suburb',
    'Weekly Rent ($NZD)': 'rent_price'
}, inplace=True)

# Drop missing rows
df.dropna(subset=['bedrooms', 'bathrooms', 'rent_price', 'suburb'], inplace=True)

# Assign default floor area
df['floor_area'] = 100

# One-hot encode suburb
df = pd.get_dummies(df, columns=['suburb'], drop_first=True)

# Features and target
X = df[['bedrooms', 'bathrooms', 'floor_area'] + [col for col in df.columns if col.startswith('suburb_')]]
y = df['rent_price']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"✅ Model trained. MSE: {mse:.2f}")

# Save model
model_path = os.path.join("Machine_Learning_Model", "rental_model.pkl")
joblib.dump(model, model_path)
print(f"✅ Model saved to {model_path}")
