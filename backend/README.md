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

# Follow this link:
https://docs.google.com/document/d/1xEVb7UzcwDebs0dvD-32FPjdkqJnDXUPjX5GE6Z7PPA/edit?tab=t.0

Copy the local files in the root, frontend and backend folder before following the steps in the document or below:

## Backend Setup

# 1. Create a local .env file in the backend folder with the below code:
DATABASE_URL=sqlite:///./temp.db
API_KEY=your_api_key_here
MODEL_PATH=Machine_Learning_Model/rental_model.pkl
LOG_PATH=Machine_Learning_Model/prediction_logs.csv
DEFAULT_PROVIDER=mock
ENABLE_INGEST_SCHEDULER=false
JWT_SECRET=please_change_me_in_prod
JWT_ALGO=HS256
JWT_EXPIRE_MIN=60

# 2. Navigate to the backend folder
cd backend

# 3. Create and activate your virtual environment (only once)
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
.\venv\Scripts\activate

# 3. Install dependencies (only once)
pip install --upgrade pip
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Start the FastAPI server
npm run dev



# NOTE: Input the above if you’re entering the backend for the first time. After that, you can enter without it as many times as you wish later, as shown below: 

# 1. Navigate to the backend folder
cd backend

# 4. Start the FastAPI server
npm run dev


## Modular Data Pipeline

The backend includes a modular pipeline that separates **ingestion**, **validation**, **transformation**, and **storage** into distinct components.  

### Endpoints
- **POST /ingest/file** → Validation only (no DB writes).  
  Returns per-row issues, a summary, and a CSV report path if validation fails.  
- **POST /ingest/pipeline** → Full pipeline (ingest → validate → transform → store).  
  Returns stage counts, pipeline duration, and the path to a CSV issues report.  
  Use `replace_table=true` if you want to wipe and reload the `properties` table.

### Adding a New Loader
To support a new data source (e.g., a new CSV format, Excel sheet, or API):
1. Implement a new reader function that outputs a Pandas DataFrame.
2. Normalize the column names to match existing schema fields (`address`, `suburb`, `bedrooms`, `bathrooms`, `floor_area`, `rent_weekly`).
3. Call the pipeline orchestrator (`pipeline_main.run`) with your DataFrame.
4. No changes are required to validation, transformation, or storage.

Reports from pipeline runs are saved under:  
`backend/Machine_Learning_Model/reports/`