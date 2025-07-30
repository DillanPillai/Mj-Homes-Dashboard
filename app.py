# app.py
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

METRICS_FILE = "metrics.json"

@app.route("/metrics")
def get_metrics():
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r") as f:
            metrics = json.load(f)
        return jsonify(metrics)
    else:
        return jsonify({"error": "Metrics not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
