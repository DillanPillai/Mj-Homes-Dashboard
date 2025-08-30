# MJ Homes Dashboard

This is the main repository for the MJ Homes Dashboard, a property data analytics and rental price prediction platform built with a FastAPI backend and a future frontend.

---

## Project Structure
```text
Mj-Homes-Dashboard/
│
├──  backend/             FastAPI backend (ML, API endpoints)
│   ├── 📄 main.py           App entry point
│   ├── 📄 requirements.txt  Python dependencies
│   ├── 📄 .gitignore        Ignore rules for backend files
│   └── 📄 README.md         Backend setup and API usage
│
├──  frontend/             Frontend folder (optional / WIP) (NEED TO UPDATE)
│
└──  ReadMe.md             Main project overview (this file)
```

---

##  Backend Setup

Please follow the instructions in:  
[`backend/README.md`](./backend/README.md)


## Backend Features

- Model retraining using updated Excel datasets
- Rental price prediction via `/predict`
- Dataset upload and validation
- Swagger docs at `/docs`
- Input logging for audits and debugging


## Tech Stack

- **Backend:** FastAPI, scikit-learn, pandas, Pydantic
- **Environment Management:** `venv`, `.env`, `requirements.txt`
- **Data Format:** Excel (`.xlsx`)


## Notes

- All rental price predictions require a valid suburb name that exists in the uploaded dataset.
- Suburb values are validated dynamically — no hardcoded lists.

---

##  Frontend Setup

Please follow the instructions in:  
[`backend/README.md`](./frontend/dashboard/README.md)

## Frontend Tech Stack

- **Frontend**: TypeScript, Python

---

## Quick Start

1. Clone the repository:
    
    ```bash
    git clone https://github.com/yourusername/mj-homes-dashboard.git
    cd mj-homes-dashboard
    ```

2. Follow backend setup instructions in `backend/README.md`
3. Access the API documentation at `http://127.0.0.1:8000/docs` or `http://localhost:8000/docs` 

## API Endpoints

- `POST /predict` - Get rental price predictions
- `POST /upload` - Upload new dataset for model retraining
- `GET /docs` - Interactive API documentation
- `GET /health` - Health check endpoint

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
