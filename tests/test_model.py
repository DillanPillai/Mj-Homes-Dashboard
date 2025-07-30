# tests/test_model.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import json
from model import train_and_evaluate  # Now Python can find model.py


class TestModelEvaluation(unittest.TestCase):
    def setUp(self):
        # Define absolute path to metrics.json relative to project root
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.metrics_path = os.path.join(self.project_root, "metrics.json")

    def test_metrics_output(self):
        metrics = train_and_evaluate()
        self.assertIn("R2", metrics)
        self.assertIn("MAE", metrics)
        self.assertIsInstance(metrics["R2"], float)
        self.assertIsInstance(metrics["MAE"], float)

    def test_metrics_file_saved(self):
        # Ensure metrics.json file is created
        train_and_evaluate()

        print(f"Checking if file exists at: {self.metrics_path}")
        print(f"File exists? {os.path.exists(self.metrics_path)}")
        self.assertTrue(os.path.exists(self.metrics_path))

        with open(self.metrics_path, "r") as f:
            data = json.load(f)
        self.assertIn("R2", data)
        self.assertIn("MAE", data)

    def tearDown(self):
        if os.path.exists(self.metrics_path):
            os.remove(self.metrics_path)


if __name__ == '__main__':
    unittest.main()
