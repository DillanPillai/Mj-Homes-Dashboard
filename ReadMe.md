---

## Backend Setup - MJ Home API

### Requirements
- Python 3.10 or above
- Virtual environment tool (e.g. `venv`)
- Node.js (for frontend or npm tasks)

---

### Backend Setup

```bash
# 1. Navigate to backend folder
cd backend

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # on Windows

# 3. Install requirements
pip install -r requirements.txt

# 4. Start the backend server
npm run dev
```

---

### API Docs

After running the server, open:

- http://127.0.0.1:8000/docs
- http://localhost:8000/docs

---

### Environment Variables

To use secrets or config, add a `.env` file like:

```
DATABASE_URL=your_database_url
API_KEY=your_api_key_here
```