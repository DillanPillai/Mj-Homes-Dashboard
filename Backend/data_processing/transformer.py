import pandas as pd

def transform_data(cleaned_data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms cleaned property data for downstream usage like ML or visualization.

    Args:
        cleaned_data (pd.DataFrame): Cleaned DataFrame from cleaner.py

    Returns:
        pd.DataFrame: Transformed and feature-enhanced data
    """
    if cleaned_data.empty:
        raise ValueError("Cleaned data is empty. Check the cleaner output.")

    df = cleaned_data.copy()

    # Convert listing date to useful time features if available
    if 'listing_date' in df.columns and pd.api.types.is_datetime64_any_dtype(df['listing_date']):
        df['listing_year'] = df['listing_date'].dt.year
        df['listing_month'] = df['listing_date'].dt.month
        df['listing_weekday'] = df['listing_date'].dt.dayofweek

    # Example: Add price per square meter if floor_area and rent_price exist
    if 'rent_price' in df.columns and 'floor_area' in df.columns:
        df['price_per_m2'] = df.apply(
            lambda row: row['rent_price'] / row['floor_area']
            if row['floor_area'] > 0 else 0,
            axis=1
        )

    # Encode categories or fill missing with known values
    if 'suburb' in df.columns:
        df['suburb'] = df['suburb'].astype(str).str.title()

    # Create binary feature for luxury homes (e.g., >3 bedrooms and >2 bathrooms)
    if 'bedrooms' in df.columns and 'bathrooms' in df.columns:
        df['is_luxury'] = ((df['bedrooms'] >= 4) & (df['bathrooms'] >= 2)).astype(int)

    # Round float fields for clean display
    float_cols = df.select_dtypes(include='float').columns
    df[float_cols] = df[float_cols].round(2)

    return df
