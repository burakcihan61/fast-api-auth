# FastAPI  Project

FastAPI project with PostgreSQL, Redis, JWT authentication, and modern Python best practices.

## 🚀 Features

- **FastAPI 0.115+** with async/await support
- **PostgreSQL** with SQLAlchemy 2.0 async
- **Redis** for caching
- **JWT Authentication** with access and refresh tokens
- **Pydantic v2** for data validation
- **Alembic** for database migrations
- **Docker & Docker Compose** for containerization
- **Prometheus** metrics
- **Structured logging** with structlog
- **Pre-commit hooks** for code quality
- **Comprehensive testing** with pytest
- **Background tasks** with Celery & Redis

## 📋 Requirements

- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

## 🛠️ Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd fast-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt -r requirements-dev.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit:
- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

### Docker Development

1. **Copy environment file**
```bash
cp .env.example .env
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **View logs**
```bash
docker-compose logs -f api
```

4. **Stop services**
```bash
docker-compose down
```

Services:
- API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- pgAdmin: http://localhost:5050

## 📁 Project Structure

```
fast-api/
├── app/
│   ├── api/              # API endpoints
│   │   ├── deps.py       # Dependencies
│   │   └── v1/           # API version 1
│   ├── core/             # Core functionality
│   │   ├── config.py     # Settings
│   │   ├── database.py   # Database connection
│   │   ├── security.py   # Authentication
│   │   └── cache.py      # Redis cache
│   ├── crud/             # Database operations
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── middleware/       # Custom middleware
│   └── main.py           # Application entry point
├── alembic/              # Database migrations
├── tests/                # Test suite
├── .env.example          # Environment template
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── docker-compose.yml    # Docker configuration
└── README.md
```

## 🔐 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users` - List all users (superuser)
- `GET /api/v1/users/{id}` - Get user by ID (superuser)
- `DELETE /api/v1/users/{id}` - Delete user (superuser)

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 🔧 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Show current revision
alembic current
```

## 🛡️ Rate Limiting

The API implements dynamic rate limiting using `slowapi` and Redis.

- **Anonymous Users**: Limited by IP address (default: 5/minute/endpoint).
- **Authenticated Users**: Limited by User ID (default: 10/minute/endpoint).
- **Premium Users**: Higher limits (default: 20/minute/endpoint).

Configurable via `RATE_LIMIT_PER_MINUTE` in settings.

## 📊 Code Quality

```bash
# Install pre-commit hooks
pre-commit install

# Run linting
ruff check .

# Run formatting
ruff format .

# Run type checking
mypy app
```

## 🐳 Docker Commands

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec api bash

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

## 📝 Environment Variables

Key environment variables (see `.env.example` for full list):

```env
# Application
APP_NAME=MyFastAPIApp
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here

# Database
POSTGRES_SERVER=localhost
POSTGRES_DB=myapp_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 🚀 Deployment

For production deployment, ensure:

1. Set `DEBUG=False`
2. Use strong `SECRET_KEY`
3. Configure HTTPS
4. Set up database backups
5. Enable monitoring and logging
6. Configure rate limiting
7. Review security settings

## 📚 Documentation

- FastAPI docs: https://fastapi.tiangolo.com
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/
- Pydantic v2: https://docs.pydantic.dev/latest/
- Alembic: https://alembic.sqlalchemy.org

## 👷 Background Tasks

The project uses Celery with Redis for asynchronous task management.

### Commands

**Start Celery Worker (Windows):**
```bash
celery -A app.worker worker --loglevel=info -P solo
```

**Start Celery Worker (Linux/macOS):**
```bash
celery -A app.worker worker --loglevel=info
```

**Monitor with Flower:**
```bash
celery -A app.worker flower
```

### Endpoints
- `POST /api/v1/tasks/email` - Trigger async email simulation
- `POST /api/v1/tasks/report` - Trigger async report generation
- `GET /api/v1/tasks/{task_id}` - Check task status and result

---

## 📄 License

MIT License

## 👤 Author

Your Name

---

## 📝 Logging

### Professional Structured Logging System

The project includes a production-ready logging system with:

**Features:**
- **JSON Formatted Logs** - Machine-readable structured logging
- **Correlation IDs** - Track requests across the application
- **Request/Response Tracking** - Automatic HTTP logging
- **Authentication Auditing** - Security event tracking
- **Log Rotation** - Automatic file rotation (10MB per file)
- **Multiple Handlers** - Console, file, and error-specific logs

**Log Files:**
```
logs/
├── app.log       # General application logs (JSON format)
├── error.log     # Error logs only (JSON format)
└── access.log    # HTTP request/response logs (JSON format)
```

**Log Format (Production):**
```json
{
  "timestamp": "2026-01-21T00:42:08",
  "level": "INFO",
  "message": "Request completed: GET /health - 200 (0.042s)",
  "correlation_id": "abc-123",
  "status_code": 200,
  "duration_ms": 42.15
}
```

**Usage Example:**
```python
from app.core.logging import logger

# Basic logging
logger.info("User action completed")

# With structured context
logger.info(
    "User registered",
    extra={
        "event": "user_registration",
        "user_id": 123,
        "username": "johndoe"
    }
)
```

**View Logs:**
```bash
# Live log monitoring
docker-compose logs -f api

# JSON formatted logs
docker-compose logs api | Select-String -Pattern "ERROR"

# Authentication events
docker-compose logs api | Select-String -Pattern "authentication"
```

**Detailed Documentation:** [LOGGING.md](LOGGING.md)

---

For more detailed information, see [rules.md](rules.md)
