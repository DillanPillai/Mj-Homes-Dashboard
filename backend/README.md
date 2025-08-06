# MJ Home API (Backend)

This is the backend server for **MJ Homes**, a property analytics and rental prediction platform.

It exposes RESTful endpoints using **FastAPI** for:
- Uploading new datasets and retraining the rental price prediction model
- Predicting rent from listing data
- Viewing processed property data
- Running the full data pipeline
- Scraping listings (planned or optional)


## Requirements

- Python 3.10+
- Node.js (for `npm run dev` startup)
- `venv` or another virtual environment tool
- A dataset file `MockData.xlsx` located at:  
  `backend/data_processing/MockData.xlsx`



## Backend Setup
# 1. Navigate to the backend folder
cd backend

# 2. Create and activate your virtual environment (only once)
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the FastAPI server
npm run dev