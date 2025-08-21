import pandas as pd

def clean_data(raw_data) -> pd.DataFrame:
    """
    Cleans raw scraped property data (either list of dicts or DataFrame).
    
    Args:
        raw_data: The raw data from scraping (list[dict] or pd.DataFrame)

    Returns:
        pd.DataFrame: Cleaned and normalized data.
    """

    # Convert list to DataFrame if needed
    if isinstance(raw_data, list):
        raw_data = pd.DataFrame(raw_data)

    if raw_data.empty:
        raise ValueError("Raw data is empty. Scraper may have failed.")

    df = raw_data.copy()

    # 🔁 Rename known Excel headers to standardized names
    df.rename(columns={
        'Weekly Rent ($NZD)': 'rent_price',
        'Floor Area (m2)': 'floor_area',
        'Suburb': 'suburb',
        'Bedrooms': 'bedrooms',
        'Bathrooms': 'bathrooms'
    }, inplace=True)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Drop rows with too many missing values
    df.dropna(thresh=int(0.7 * len(df.columns)), inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert rent_price to float
    if 'rent_price' in df.columns:
        df['rent_price'] = (
            df['rent_price']
            .astype(str)
            .str.replace(r"[^\d.]", "", regex=True)
            .astype(float)
        )

    # Convert floor area
    if 'floor_area' in df.columns:
        df['floor_area'] = (
            df['floor_area']
            .astype(str)
            .str.replace(r"[^\d.]", "", regex=True)
            .astype(float)
        )

    # Clean numeric fields
    for col in ['bedrooms', 'bathrooms']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Fill missing suburb with 'Unknown'
    if 'suburb' in df.columns:
        df['suburb'] = df['suburb'].fillna('Unknown').astype(str).str.title()

    # Optional: Normalize date field
    if 'listing_date' in df.columns:
        df['listing_date'] = pd.to_datetime(df['listing_date'], errors='coerce')

    # Final cleanup
    df.fillna(0, inplace=True)

    return df


# 🧠 NEW: Used for model training + prediction
def prepare_features(df: pd.DataFrame, valid_suburbs: list[str] = None) -> pd.DataFrame:
    """
    Prepares cleaned, numeric, encoded fields for ML model.
    
    Args:
        df: Raw DataFrame with 'suburb', 'bedrooms', 'bathrooms', 'floor_area'
        valid_suburbs: Optional list of allowed suburb names for validation

    Returns:
        pd.DataFrame: Cleaned and one-hot encoded for ML model
    """
    df = df.copy()

    # Clean suburb values
    df['suburb'] = df['suburb'].astype(str).str.strip().str.title()
    df = df[~df['suburb'].isin(["", "String", "??", "N/A", "Na", "Null", "None", "Unknown"])]

    # Filter to allowed suburbs
    if valid_suburbs is not None:
        df = df[df['suburb'].isin(valid_suburbs)]

    # Convert numeric columns
    numeric_cols = ['bedrooms', 'bathrooms', 'floor_area']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with missing values in key fields
    df = df.dropna(subset=numeric_cols)

    # One-hot encode suburb
    suburb_dummies = pd.get_dummies(df['suburb'], prefix='suburb')
    df = pd.concat([df.drop(columns=['suburb']), suburb_dummies], axis=1)

    return df
