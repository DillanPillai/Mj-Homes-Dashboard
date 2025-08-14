import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

# Simulated logic from investment_ranker.py
def rank_top_suburbs(df, top_n=10):
    df_clean = df.dropna(subset=["Suburb", "Weekly Rent ($NZD)", "Days on Market"])
    ranked = df_clean.sort_values(
        by=["Weekly Rent ($NZD)", "Days on Market"],
        ascending=[False, True]
    )
    return ranked[["Suburb", "Weekly Rent ($NZD)", "Days on Market", "Bedrooms", "Listing Type"]].head(top_n)

# Unit Test
class TestRankTopSuburbs(unittest.TestCase): 
    def test_rank_suburbs_basic(self):
        # Sample input
        data = {
            "Suburb": ["A", "B", "C"],
            "Weekly Rent ($NZD)": [600, 620, 610],
            "Days on Market": [10, 15, 12],
            "Bedrooms": [3, 4, 3],
            "Listing Type": ["Rent", "Rent", "Rent"]
        }
        df = pd.DataFrame(data)
        
        # Expected output
        expected_data = {
            "Suburb": ["B", "C", "A"],
            "Weekly Rent ($NZD)": [620, 610, 600],
            "Days on Market": [15, 12, 10],
            "Bedrooms": [4, 3, 3],
            "Listing Type": ["Rent", "Rent", "Rent"]
        }
        expected_df = pd.DataFrame(expected_data).reset_index(drop=True)
        
        result_df = rank_top_suburbs(df, top_n=3).reset_index(drop=True)
        
        assert_frame_equal(result_df, expected_df)

if __name__ == "__main__":
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        print("\n Unit test passed!")
    else:
        print("\n Unit test failed.")
