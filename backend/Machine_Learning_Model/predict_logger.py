import csv
import os
from datetime import datetime

# File where predictions will be saved
LOG_FILE = os.path.join(os.path.dirname(__file__), "prediction_logs.csv")

def log_prediction(input_data: dict, prediction: float, user_id: str = "anonymous"):
    """
    Logs prediction input, result, timestamp, and user ID to a CSV file.
    """
    timestamp = datetime.now().isoformat()

    # Create one full row for logging
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        **input_data,
        "prediction": prediction
    }

    # Check if log file already exists
    file_exists = os.path.isfile(LOG_FILE)

    # Open log file and write row
    with open(LOG_FILE, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=log_entry.keys())

        # Write header only once (if file is new)
        if not file_exists:
            writer.writeheader()

        # Write the actual row
        writer.writerow(log_entry)
