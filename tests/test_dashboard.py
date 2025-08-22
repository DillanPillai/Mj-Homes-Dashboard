# tests/test_dashboard.py
import sys
import os
import json
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Create dummy metrics file
        self.test_metrics = {"R2": 0.91, "MAE": 1.11}
        with open("metrics.json", "w") as f:
            json.dump(self.test_metrics, f)

    def tearDown(self):
        if os.path.exists("metrics.json"):
            os.remove("metrics.json")

    def test_dashboard_displays_metrics(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn(f"R²: {self.test_metrics['R2']}", html)
        self.assertIn(f"MAE: {self.test_metrics['MAE']}", html)

    def test_dashboard_missing_file(self):
        os.remove("metrics.json")
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 404)
        self.assertIn("No metrics available", response.data.decode("utf-8"))

if __name__ == "__main__":
    unittest.main()
