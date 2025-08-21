import unittest
from property_filter import properties, filter_properties

class TestPropertyFilter(unittest.TestCase):

    def test_filter_by_location(self):
        result = filter_properties(properties, location="Auckland")
        self.assertTrue(all(p["location"] == "Auckland" for p in result))
        self.assertEqual(len(result), 2)

    def test_filter_by_price(self):
        result = filter_properties(properties, max_price=700000)
        self.assertTrue(all(p["price"] <= 700000 for p in result))
        self.assertEqual(len(result), 2)

    def test_filter_by_interest(self):
        result = filter_properties(properties, interest="Medium")
        self.assertTrue(all(p["interest"] == "Medium" for p in result))
        self.assertEqual(len(result), 2)

    def test_filter_by_keyword(self):
        result = filter_properties(properties, keyword="pool")
        self.assertTrue(all("pool" in p["description"].lower() for p in result))
        self.assertEqual(len(result), 2)

    def test_combined_filters(self):
        result = filter_properties(properties, location="Auckland", max_price=1200000, interest="Medium", keyword="pool")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 4)

    def test_no_filters(self):
        result = filter_properties(properties)
        self.assertEqual(len(result), len(properties))

if __name__ == "__main__":
    unittest.main()
