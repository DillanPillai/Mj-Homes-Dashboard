# Import the pandas library for data manipulation
import pandas as pd

def transform_register_report(file_path: str, skiprows=6) -> pd.DataFrame:
    """
    Transforms a wide-format MSD report CSV file into a normalized long-format DataFrame.

    Args:
        file_path (str): The full path to the cleaned MSD CSV file.
        skiprows (int): Number of rows to skip at the top of the file (default is 6 for MSD format).

    Returns:
        pd.DataFrame: A cleaned, long-format DataFrame with columns:
                      ['register_type', 'month_code', 'count']
    """

    # Load the CSV file, skipping the top metadata/header rows
    df = pd.read_csv(file_path, skiprows=skiprows)

    # Remove any columns that have "Unnamed" in their names (usually empty/excess columns)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Drop rows where all values are NaN (completely empty rows)
    df.dropna(how='all', inplace=True)

    # Convert from wide format (each month as a column) to long format
    # The first column (usually report type) is kept as is; all others are melted into month_code and count
    df_long = pd.melt(
        df,
        id_vars=[df.columns[0]],        # Treat the first column as the identifier (e.g., "Housing Register")
        var_name="month_code",          # New column name for what were previously column headers
        value_name="count"              # New column name for values in the melted columns
    )

    # Rename the first column to a standard name: "register_type"
    df_long.rename(columns={df.columns[0]: "register_type"}, inplace=True)

    # Strip any extra whitespace from register_type values
    df_long["register_type"] = df_long["register_type"].astype(str).str.strip()

    # Convert month_code values to strings (ensures consistency for storage and comparison)
    df_long["month_code"] = df_long["month_code"].astype(str)

    # Convert count values to numeric (int); handle errors by coercing to NaN, then fill NaN with 0
    df_long["count"] = pd.to_numeric(df_long["count"], errors="coerce").fillna(0).astype(int)

    # Return the cleaned and transformed DataFrame
    return df_long
