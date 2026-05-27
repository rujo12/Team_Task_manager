# Backend Setup - Quick Start Commands

## Initial Setup (One-time)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
# Follow prompts to create admin user
```

## Development Commands

```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Start development server
python manage.py runserver

# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Clear database (careful in production!)
python manage.py flush

# Run tests
python manage.py test
```

## API Testing

### Using cURL

```bash
# Signup new user
curl -X POST http://localhost:8000/api/users/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123",
    "password_confirm": "TestPassword123"
  }'

# Login to get JWT tokens
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPassword123"
  }'

# Response example:
# {
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "user": {
#     "id": 1,
#     "username": "testuser",
#     "email": "test@example.com"
#   }
# }

# Get current user (replace TOKEN with access token)
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Using Postman

1. Create new request
2. For authenticated endpoints, add Authorization header:
   - Type: Bearer Token
   - Token: [Your access token from login response]

## Installation Details

### Package Versions

- Django: 6.0.5
- Django REST Framework: 3.17
- SimpleJWT: 5.5
- django-cors-headers: 4.9
- psycopg2-binary: 2.9 (PostgreSQL)
- Gunicorn: 26.0

### What Each Package Does

- **Django**: Web framework
- **DRF**: REST API framework
- **SimpleJWT**: JWT authentication
- **django-cors-headers**: Allows frontend to communicate with backend
- **psycopg2**: PostgreSQL database driver
- **python-decouple**: Load environment variables
- **gunicorn**: Production server

## Environment Variables

See `.env.example` or `.env` for all available variables:

| Variable | Purpose | Example |
|----------|---------|---------|
| DEBUG | Debug mode | True/False |
| SECRET_KEY | Django secret | Random string |
| DATABASE_URL | DB connection | sqlite:///db.sqlite3 |
| ALLOWED_HOSTS | Allowed hosts | localhost,127.0.0.1 |
| CORS_ALLOWED_ORIGINS | Frontend URLs | http://localhost:5173 |

## Common Issues

**Issue**: Import error with apps
- **Solution**: Ensure apps are in INSTALLED_APPS in settings.py

**Issue**: Migration conflicts
- **Solution**: Delete recent migration files and run `makemigrations` again

**Issue**: Database locked
- **Solution**: Delete `db.sqlite3` and run migrations again

**Issue**: PORT already in use
- **Solution**: Use `python manage.py runserver 8001`

## Database Access

### SQLite (Development)
- File location: `backend/db.sqlite3`
- Access via: Any SQLite viewer

### PostgreSQL (Production)
- Connection string in `.env`
- Access via: psql or database GUI

## Admin Interface

Access Django admin:
1. Start server: `python manage.py runserver`
2. Go to: http://localhost:8000/admin
3. Login with superuser credentials

Manage:
- Users
- Projects & Members
- Tasks & History

## IDE Setup

### VSCode

Add to `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

### PyCharm

1. Go to Project settings
2. Select Project Interpreter
3. Click gear → Add Local
4. Select `backend/venv/bin/python`

## Next Steps

1. ✅ Backend initialized
2. ⬜ Create Django apps models and serializers
3. ⬜ Implement API endpoints
4. ⬜ Set up frontend
5. ⬜ Test end-to-end
6. ⬜ Deploy to Railway

## Getting Help

- Django docs: https://docs.djangoproject.com/
- DRF docs: https://www.django-rest-framework.org/
- JWT docs: https://django-rest-framework-simplejwt.readthedocs.io/
