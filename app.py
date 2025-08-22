#app.py
from flask import Flask, jsonify, render_template_string
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

@app.route("/dashboard", methods=["GET"])
def dashboard():
    metrics_path = os.path.join(os.path.dirname(__file__), "metrics.json")

    if not os.path.exists(metrics_path):
        return "No metrics available", 404

    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    html = f"""
    <html>
      <body>
        <h1>Model Dashboard</h1>
        <p>R²: {metrics['R2']}</p>
        <p>MAE: {metrics['MAE']}</p>
      </body>
    </html>
    """
    return render_template_string(html)
