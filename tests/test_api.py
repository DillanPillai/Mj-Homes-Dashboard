# tests/test_api.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import json
import os
from app import app  # Now Python can find app.py


class TestMetricsAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Create a dummy metrics file
        self.test_metrics = {"R2": 0.95, "MAE": 1.23}
        with open("metrics.json", "w") as f:
            json.dump(self.test_metrics, f)

    def tearDown(self):
        if os.path.exists("metrics.json"):
            os.remove("metrics.json")

    def test_metrics_endpoint_success(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["R2"], self.test_metrics["R2"])
        self.assertEqual(data["MAE"], self.test_metrics["MAE"])

    def test_metrics_endpoint_missing_file(self):
        # Delete metrics file to simulate untrained model
        os.remove("metrics.json")
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

if __name__ == '__main__':
    unittest.main()