#app.py
from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

@app.route("/metrics", methods=["GET"])
def get_metrics():
    metrics_path = os.path.join(os.path.dirname(__file__), "metrics.json")

    if not os.path.exists(metrics_path):
        return jsonify({"error": "Model has not been trained yet."}), 404

    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    return jsonify(metrics), 200

if __name__ == "__main__":
    app.run(debug=True)
