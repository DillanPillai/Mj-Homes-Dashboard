
# Python Web Scraper Backend

This is a Python Flask backend that provides API endpoints for the web scraper frontend.

## Setup

1. Create a virtual environment:
```
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the server:
```
python app.py
```

The server will run on http://localhost:5000

## API Endpoints

- POST /api/scrape - Start a new scraping job
- GET /api/jobs - Get all scraping jobs
- GET /api/jobs/:id - Get a specific job
- GET /api/download/:id - Download data from a job
