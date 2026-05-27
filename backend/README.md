# Team Task Manager Backend

Django REST API for Team Task Manager with JWT authentication and role-based access.

## Stack

- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL-ready configuration (`DATABASE_URL`)
- WhiteNoise static serving
- Gunicorn + Procfile (Railway ready)

## Apps

- `users` - auth and profile
- `projects` - projects and members
- `tasks` - tasks and status tracking
- `dashboard` - aggregate metrics API

## API Endpoints

### Authentication
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

## RBAC

- `ADMIN`: create projects, add members, create/assign tasks
- `MEMBER`: view assigned tasks, update own assigned task status

## Setup

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

## Environment

Copy `.env.example` to `.env` and update values.

Important variables:
- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `JWT_SECRET_KEY`

## Tests

```bash
python manage.py test
```

## Railway Deployment

- `Procfile` includes:
  - release: migrate + collectstatic
  - web: gunicorn
- Uses env-driven production settings in `config/settings.py`.
