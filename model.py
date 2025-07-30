#model.py
import os
import json

def train_and_evaluate():
    metrics = {"R2": 0.85, "MAE": 2.34}

    project_root = os.path.abspath(os.path.dirname(__file__))
    metrics_path = os.path.join(project_root, "metrics.json")

    print(f"Saving metrics to: {metrics_path}")

    with open(metrics_path, "w") as f:
        json.dump(metrics, f)
        f.flush()
        os.fsync(f.fileno())  # Ensure data is written to disk

    # Check if file exists immediately after writing
    if os.path.exists(metrics_path):
        print("File exists right after saving.")
    else:
        print("File NOT found right after saving!")

    return metrics
