# MJ Homes Dashboard

This is the main repository for the **MJ Homes Dashboard** — a property data analytics and rental price prediction platform built with a FastAPI backend and a future frontend.

---

## Project Structure
Mj-Homes-Dashboard/
│
├── backend/ → FastAPI backend (ML, API endpoints)
│ ├── main.py → App entry point
│ ├── requirements.txt → Python dependencies
│ ├── .gitignore → Ignore rules for backend files
│ ├── README.md → Backend setup and API usage
│
├── frontend/ → Frontend folder (optional or WIP)
│
└── ReadMe.md → This file (main project overview)


---

## Backend Setup

Please follow the instructions in:  
[`backend/README.md`](./backend/README.md)

---

## Backend Features

- Model retraining using updated Excel datasets
- Rental price prediction via `/predict`
- Dataset upload and validation
- Swagger docs at `/docs`
- Input logging for audits and debugging

---

## Tech Stack

- **Backend:** FastAPI, scikit-learn, pandas, Pydantic
- **Environment Management:** `venv`, `.env`, `requirements.txt`
- **Data Format:** Excel (`.xlsx`)

---

## Notes

- All rental price predictions require a valid suburb name that exists in the uploaded dataset.
- Suburb values are validated dynamically — no hardcoded lists.