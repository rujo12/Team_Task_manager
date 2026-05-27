# Team Task Manager

Full-stack Team Task Manager with Django REST backend and React frontend.

## Tech Stack

### Backend
- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL-ready settings
- Railway-ready deployment config

### Frontend
- React + Vite
- Tailwind CSS
- Axios
- React Router
- Vercel-ready SPA config

## Repository Structure

```text
ethara_ai_assignment/
├── backend/
└── frontend/
```

## Backend API Routes

### Auth
- `POST /api/auth/signup/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`

### Projects
- `GET /api/projects/`
- `POST /api/projects/`
- `POST /api/projects/<id>/add-member/`

### Tasks
- `GET /api/tasks/`
- `POST /api/tasks/`
- `PATCH /api/tasks/<id>/status/`

### Dashboard
- `GET /api/dashboard/`

## RBAC Rules

### ADMIN
- Create projects
- Add project members
- Create and assign tasks
- Update task status

### MEMBER
- View assigned tasks
- Update own assigned task status

## Local Setup

### 1) Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs on `http://127.0.0.1:8000`.

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`.

## Environment Variables

### Backend (`backend/.env`)
Use `backend/.env.example` as reference.

### Frontend (`frontend/.env`)
Use `frontend/.env.example`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Production Deployment

### Backend (Railway)
- Uses `Procfile` for release + web commands
- Gunicorn config: `backend/gunicorn.conf.py`
- Static file handling via WhiteNoise
- PostgreSQL via `DATABASE_URL`

### Frontend (Vercel)
- `frontend/vercel.json` configured for SPA rewrites
- Set `VITE_API_BASE_URL` in Vercel environment

## Validation Commands

### Backend
```bash
cd backend
python manage.py test
```

### Frontend
```bash
cd frontend
npm run lint
npm run build
```
