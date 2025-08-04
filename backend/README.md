# 🏠 MJ Home API (Backend)

This is the backend server for MJ Homes — a property analytics and rental prediction platform.  
It provides endpoints for scraping data, processing listings, uploading datasets, retraining the ML model, and predicting rental prices using FastAPI.

---

## Requirements

- Python 3.10+
- Node.js (for `npm run dev` command)
- `venv` or another virtual environment tool
- `MockData.xlsx` placed at: `backend/data_processing/MockData.xlsx`

---

## Setup Instructions

```bash
# 1. Navigate to the backend folder
cd backend

# 2. Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the backend server
npm run dev
# (or) manually:
# uvicorn main:app --reload
