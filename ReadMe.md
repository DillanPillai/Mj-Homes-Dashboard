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
├──  frontend/             Frontend folder (optional / WIP) (NEED TO UPDATE)
│
└──  README.md             Main project overview (this file)
```

---

## Quick Start

# 1. Clone the repository:
Copy the website URL: https://github.com/DillanPillai/Mj-Homes-Dashboard.git and clone it to your GitHub desktop application. After that, fetch origin from the main folder and open the folder in Visual Studio Code. 

# 2. Create an .env local file in the root folder with the below code:
DB_NAME=mjhome
DB_USER=postgres
DB_PASSWORD=2025DashMjHomesSecure
DB_HOST=localhost
DB_PORT=5432

DATABASE_URL=postgresql://user:password@localhost:5432/mydb
API_KEY=your_api_key_here
MODEL_PATH=Machine_Learning_Model/rental_model.pkl
LOG_PATH=Machine_Learning_Model/prediction_logs.csv

VITE_FIREBASE_API_KEY=AIzaSyB3n-Gu1Wf1q4bziuvwmG1CSx38lUPdgR8
VITE_FIREBASE_AUTH_DOMAIN=mj-home-dashboard.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mj-home-dashboard
VITE_FIREBASE_STORAGE_BUCKET=mj-home-dashboard.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=74941228201
VITE_FIREBASE_APP_ID=1:74941228201:web:087f66e9e57988eb5c35b8
VITE_FIREBASE_MEASUREMENT_ID=G-M3WHD6DNS8

---

## Frontend Setup

Please follow the instructions in:  
[`backend/README.md`](./frontend/dashboard/README.md)

## Frontend Tech Stack

- **Frontend**: TypeScript

---

## Backend Setup

Please follow the instructions in:  
[`backend/README.md`](./backend/README.md)

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

---

## Future Roadmap

- [ ]  Advanced analytics features
- [ ]  Multi-property comparison tools
- [ ]  Historical price trend analysis
- [ ]  Social Media Analytics Display

## Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/example-feature`)  
3. Commit your changes (`git commit -m 'Add example feature'`)  
4. Push to the branch (`git push origin feature/example-feature`)  
5. Open a Pull Request  

## Support

For questions or support, please open an issue in this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](https://www.github.com/) file for details.
