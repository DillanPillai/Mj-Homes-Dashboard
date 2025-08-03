import unittest
import pandas as pd
from validate_properties import validate_data

class TestValidateProperties(unittest.TestCase):

    def test_missing_values(self):
        # Data with missing values in Suburb and Rent
        df = pd.DataFrame({
            "Suburb": ["Papakura", None],
            "Weekly Rent ($NZD)": [650, None],
            "Days on Market": [12, None],
            "Bedrooms": [3, 2],
            "Listing Type": ["Rent", "Rent"]
        })

        issues = validate_data(df)

        self.assertIn("Suburb", issues)
        self.assertIn("Weekly Rent ($NZD)", issues)
        self.assertIn("Days on Market", issues)
        self.assertNotIn("Bedrooms", issues)  # No missing values in Bedrooms

    def test_no_issues(self):
        # Clean data
        df = pd.DataFrame({
            "Suburb": ["A", "B"],
            "Weekly Rent ($NZD)": [600, 620],
            "Days on Market": [10, 12],
            "Bedrooms": [2, 3],
            "Listing Type": ["Rent", "Rent"]
        })

        issues = validate_data(df)

        self.assertEqual(len(issues), 0)

if __name__ == "__main__":
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        print("\n Unit test passed!")
    else:
        print("\n Unit test failed.")
