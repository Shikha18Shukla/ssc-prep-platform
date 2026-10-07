# SSC Prep Platform

A production-ready competitive exam preparation platform for SSC (Staff Selection Commission) exams.

## Project Structure

```
ssc-prep-platform/
├── frontend/          # React + TypeScript + Vite
├── backend/           # Python + FastAPI
├── database/          # Database migrations and schemas
├── docs/              # Project documentation
├── question-bank/     # Question data and imports
├── .gitignore
└── README.md
```

## Tech Stack

### Frontend

- React with TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- React Router (routing)

### Backend

- Python with FastAPI
- SQLAlchemy (ORM)
- JWT Authentication
- PostgreSQL (database)

## Getting Started

### Prerequisites

- Node.js (v18 or later)
- Python (3.11 or later)
- PostgreSQL (15 or later)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server runs at `http://localhost:5173`.

### Backend

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env  # Then edit .env with your settings
uvicorn app.main:app --reload
```

The API server runs at `http://localhost:8000`.
API docs are available at `http://localhost:8000/api/docs`.

## License

Private — All rights reserved.
