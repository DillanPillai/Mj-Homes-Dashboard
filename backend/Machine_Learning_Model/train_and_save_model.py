import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load Excel data
df = pd.read_excel('./backend/data_processing/MockData.xlsx')

# Rename columns to match what the model expects
df.rename(columns={
    'Bedrooms': 'bedrooms',
    'Bathrooms': 'bathrooms',
    'Suburb': 'suburb',
    'Weekly Rent ($NZD)': 'rent_price'
}, inplace=True)

# Drop rows with missing essential values
df.dropna(subset=['bedrooms', 'bathrooms', 'rent_price', 'suburb'], inplace=True)

# Assign dummy value for floor_area (since it's not in your file)
df['floor_area'] = 100  # Placeholder value — improve later with estimation

# One-hot encode categorical suburb
df = pd.get_dummies(df, columns=['suburb'], drop_first=True)

# Define input features and target
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
print(f"Model trained. MSE: {mse:.2f}")

# Save trained model
joblib.dump(model, './backend/Machine_Learning_Model/rental_model.pkl')
print("Model saved to './backend/Machine_Learning_Model/rental_model.pkl'")
