
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from datetime import datetime
import json
import io
import pickle

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# In-memory storage for scraping results (would use a database in production)
scraping_jobs = [
    {
        "id": 1,
        "url": "https://example.com",
        "date": "2025-05-11",
        "status": "completed",
        "records": 128,
        "scriptType": "python",
        "location": "New York",
        "price": 500000,
        "interest": "high"
    },
    {
        "id": 2, 
        "url": "https://news.example.com/tech",
        "date": "2025-05-10",
        "status": "completed",
        "records": 64,
        "scriptType": "r",
        "location": "San Francisco",
        "price": 750000,
        "interest": "medium"
    },
    {
        "id": 3,
        "url": "https://store.example.com",
        "date": "2025-05-09",
        "status": "failed",
        "records": 0,
        "scriptType": "python",
        "location": "Chicago",
        "price": 350000,
        "interest": "low"
    }
]

with open('rent_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    # ... keep existing code
    pass

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    # You could add filtering here based on request parameters
    return jsonify(scraping_jobs), 200

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = next((job for job in scraping_jobs if job["id"] == job_id), None)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job), 200

@app.route('/api/download/<int:job_id>', methods=['GET'])
def download_job_data(job_id):
    format_type = request.args.get('format', 'csv')
    
    job = next((job for job in scraping_jobs if job["id"] == job_id), None)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    # Generate mock data based on the job
    mock_data = generate_mock_data(job)
    
    # Handle different format types
    if format_type == 'csv':
        return create_csv_response(mock_data, job_id)
    elif format_type == 'sql':
        # Mock SQL export response
        return jsonify({"message": f"Data for job {job_id} exported to SQL database", "format": "sql"}), 200
    elif format_type == 'r':
        # Mock R export response
        return jsonify({"message": f"Data for job {job_id} prepared for R analysis", "format": "r"}), 200
    elif format_type == 'powerbi':
        # Mock Power BI export response
        return jsonify({"message": f"Data for job {job_id} exported for Power BI", "format": "powerbi"}), 200
    else:
        return jsonify({"error": "Unsupported format type"}), 400

@app.route('/predict_rent', methods=['POST'])
def predict_rent():
    data = request.json
    df = pd.DataFrame([data])
    pred = model.predict(df)[0]
    return jsonify({'predicted_rent': round(pred, 2)})

def create_csv_response(data, job_id):
    """Create a CSV response from the provided data"""
    df = pd.DataFrame(data)
    
    # Create a string buffer
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    # In a real app, we would return the file for download
    # For this mock implementation, we'll return a success message
    return jsonify({"message": f"CSV data for job {job_id} generated successfully", "format": "csv"}), 200

def generate_mock_data(job):
    """Generate mock data based on job information"""
    num_records = job["records"]
    data = []
    
    for i in range(num_records):
        data.append({
            "id": i + 1,
            "title": f"Item {i+1}",
            "url": f"{job['url']}/item-{i+1}",
            "price": round(job["price"] * (0.5 + i/num_records), 2),
            "location": job["location"],
            "category": "Category " + str((i % 5) + 1),
            "interest_level": job["interest"],
            "timestamp": job["date"]
        })
    
    return data

def perform_scrape(url):
    # ... keep existing code
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
