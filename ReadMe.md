# MJ Homes Dashboard

This is the main repository for the MJ Homes Dashboard, a property data analytics and rental price prediction platform built with a FastAPI backend and a future frontend.

---

## Project Structure
```text
Mj-Homes-Dashboard/
│
├──  backend/              FastAPI backend (ML, API endpoints)
│   ├──  main.py           App entry point
│   ├──  requirements.txt  Python dependencies
│   ├──  .gitignore        Ignore rules for backend files
│   └──  README.md         Backend setup and API usage
│
├──  frontend/             Frontend folder
│   ├──  requirements.txt  Typescript dependencies
│   ├──  .gitignore        Ignore rules for frontend files
│   └──  README.md         Frontend setup and API usage
│
└──  README.md             Main project overview (this file)
```

---

## Quick Start

# 1. Clone the repository:
Copy the website URL: https://github.com/DillanPillai/Mj-Homes-Dashboard.git and clone it to your GitHub desktop application. After that, fetch origin from the main folder and open the folder in Visual Studio Code. 

---

## Frontend Setup

Please follow the instructions in:  
[`frontend\dashboard\README.md`](./frontend/dashboard/README.md)

## Frontend Tech Stack

- **Frontend**: TypeScript

---

## Backend Setup

Please follow the instructions in:  
[`backend\README.md`](./backend/README.md)

1. Follow backend setup instructions in `backend/README.md`
2. Access the API documentation at `http://localhost:8000/docs` or `http://127.0.0.1:8000/docs`

## Some API Endpoints

- `POST /predict` - Get rental price predictions
- `POST /upload` - Upload new dataset for model retraining
- `GET /docs` - Interactive API documentation
- `GET /health` - Health check endpoint

## Backend Features

- Model retraining using updated Excel datasets
- Rental price prediction via `/predict`
- Dataset upload and validation
- Swagger docs at `/docs`
- Input logging for audits and debugging

## Tech Stack

- **Backend:** FastAPI, scikit-learn, pandas, Pydantic, Python programming language
- **Environment Management:** `venv`, `.env`, `requirements.txt`
- **Data Format:** Excel (`.xlsx`)

## Notes

- All rental price predictions require a valid suburb name that exists in the uploaded dataset.
- Suburb values are validated dynamically — no hardcoded lists.