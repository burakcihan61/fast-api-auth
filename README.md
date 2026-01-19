# FastAPI Authentication & User Management

> Professional FastAPI boilerplate with JWT authentication, PostgreSQL, Redis, and comprehensive security features.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-00a889.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg?style=flat&logo=redis&logoColor=white)](https://redis.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Teknoloji Stack](#-teknoloji-stack)
- [Başlangıç](#-başlangıç)
- [Proje Yapısı](#-proje-yapısı)
- [API Endpoints](#-api-endpoints)
- [Veritabanı](#-veritabanı)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## ✨ Özellikler

### 🔐 Authentication & Security

- ✅ **JWT Authentication** - Access & Refresh tokens
- ✅ **Token Blacklist** - Redis-based logout mechanism
- ✅ **Password Hashing** - bcrypt with configurable cost
- ✅ **Password Validation** - Strong password requirements
- ✅ **OAuth2 Compatible** - Standard OAuth2 password flow
- ✅ **Role-Based Access Control** - User/Superuser permissions
- ✅ **CORS Configuration** - Configurable allowed origins
- ✅ **Rate Limiting Ready** - Prepared for production rate limiting

### 🗃️ Database & Caching

- ✅ **PostgreSQL 16** - Advanced SQL database
- ✅ **SQLAlchemy 2.0** - Modern async ORM
- ✅ **Alembic Migrations** - Database version control
- ✅ **Redis Cache** - Fast data caching & session management
- ✅ **Connection Pooling** - Optimized database connections

### 🎯 API Features

- ✅ **RESTful API Design** - Industry best practices
- ✅ **Pydantic v2 Validation** - Robust request/response validation
- ✅ **Auto-generated Docs** - Swagger UI & ReDoc
- ✅ **Standardized Responses** - Consistent API response format
- ✅ **Error Handling** - Global exception middleware
- ✅ **Pagination Support** - Built-in pagination for list endpoints

### 🛠️ Development Tools

- ✅ **Docker Support** - Full containerization
- ✅ **Hot Reload** - Auto-restart in development
- ✅ **Code Quality** - Ruff linting & formatting
- ✅ **Type Checking** - mypy static type analysis
- ✅ **Pre-commit Hooks** - Automated code checks
- ✅ **GitHub Actions** - CI/CD pipeline ready

### 📊 Monitoring & Logging

- ✅ **Prometheus Metrics** - Ready for production monitoring
- ✅ **Structured Logging** - JSON formatted logs
- ✅ **Health Check Endpoint** - Service health monitoring
- ✅ **Sentry Integration Ready** - Error tracking support

---

## 🚀 Teknoloji Stack

| Kategori | Teknoloji | Versiyon |
|----------|-----------|----------|
| **Framework** | FastAPI | 0.115.0+ |
| **Language** | Python | 3.11+ |
| **Database** | PostgreSQL | 16 |
| **Cache** | Redis | 7 |
| **ORM** | SQLAlchemy | 2.0.30+ |
| **Validation** | Pydantic | 2.8.0+ |
| **Migration** | Alembic | 1.13.0+ |
| **Authentication** | python-jose | 3.3.0+ |
| **Password** | passlib | 1.7.4+ |
| **Testing** | Pytest | 8.0.0+ |
| **Linting** | Ruff | 0.3.0+ |
| **Type Check** | mypy | 1.9.0+ |

---

## 🎯 Başlangıç

### Gereksinimler

- **Python 3.11+**
- **Docker & Docker Compose** (önerilen)
- **PostgreSQL 16** (Docker kullanmıyorsanız)
- **Redis 7** (Docker kullanmıyorsanız)

### 🐳 Docker ile Kurulum (Önerilen)

```bash
# 1. Repository'yi klonlayın
git clone https://github.com/burakcihan61/fast-api-auth.git
cd fast-api-auth

# 2. Environment dosyasını oluşturun
cp .env.example .env

# 3. (Opsiyonel) .env dosyasını düzenleyin
# SECRET_KEY, database credentials vb.

# 4. Docker container'ları başlatın
docker-compose up -d

# 5. Veritabanı migration'ı
docker-compose exec api alembic upgrade head

# 6. (Opsiyonel) Admin kullanıcı oluşturun
docker-compose exec api python scripts/create_superuser.py
```

**API Hazır!** 🎉
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- pgAdmin: http://localhost:5050

### 💻 Manuel Kurulum

```bash
# 1. Virtual environment oluşturun
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# 2. Dependencies kurun
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Environment ayarlayın
cp .env.example .env
# .env dosyasını düzenleyin

# 4. PostgreSQL ve Redis'in çalıştığından emin olun

# 5. Database migration
alembic upgrade head

# 6. Uygulamayı başlatın
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### ⚡ Hızlı Test

```bash
# Health check
curl http://localhost:8000/health

# Kullanıcı kaydı
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Test123!@#","full_name":"Test User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=Test123!@#"
```

---

## 📁 Proje Yapısı

```
fast-api/
├── 📁 app/
│   ├── 📁 api/              # API endpoints
│   │   ├── 📁 v1/          
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── users.py     # User management endpoints
│   │   │   └── router.py    # API router aggregator
│   │   └── deps.py          # Reusable dependencies
│   ├── 📁 core/             # Core functionality
│   │   ├── config.py        # Configuration management
│   │   ├── database.py      # Database connection
│   │   ├── security.py      # JWT & password utilities
│   │   ├── cache.py         # Redis cache & blacklist
│   │   └── exceptions.py    # Custom exceptions
│   ├── 📁 crud/             # Database operations
│   │   ├── base.py          # Generic CRUD base class
│   │   └── user.py          # User CRUD operations
│   ├── 📁 models/           # SQLAlchemy models
│   │   ├── base.py          # Base model
│   │   └── user.py          # User model
│   ├── 📁 schemas/          # Pydantic schemas
│   │   ├── base.py          # Response schemas
│   │   └── user.py          # User schemas
│   ├── 📁 middleware/       # Custom middleware
│   │   └── error_handler.py
│   └── main.py              # FastAPI application
├── 📁 alembic/              # Database migrations
│   ├── versions/            # Migration files
│   └── env.py               # Alembic config
├── 📁 tests/                # Test files
│   ├── conftest.py          # Pytest fixtures
│   └── test_auth.py         # Auth endpoint tests
├── 📁 scripts/              # Utility scripts
│   ├── init_db.py           # Database initialization
│   └── create_superuser.py  # Admin user creation
├── 📁 .github/workflows/    # CI/CD pipeline
│   └── ci.yml               # GitHub Actions
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── .pre-commit-config.yaml  # Pre-commit hooks
├── alembic.ini              # Alembic configuration
├── docker-compose.yml       # Docker services
├── Dockerfile               # Docker image
├── Makefile                 # Development commands
├── pyproject.toml           # Project config (Ruff, mypy)
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
└── COMMIT_RULES.md          # Git commit guidelines
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `POST` | `/api/v1/auth/register` | Yeni kullanıcı kaydı | ❌ |
| `POST` | `/api/v1/auth/login` | Kullanıcı girişi (JWT token) | ❌ |
| `POST` | `/api/v1/auth/logout` | Çıkış (token blacklist) | ✅ |

### Users

| Method | Endpoint | Açıklama | Auth | Role |
|--------|----------|----------|------|------|
| `GET` | `/api/v1/users/me` | Profil bilgileri | ✅ | User |
| `PUT` | `/api/v1/users/me` | Profil güncelleme | ✅ | User |
| `GET` | `/api/v1/users` | Tüm kullanıcılar | ✅ | Superuser |
| `GET` | `/api/v1/users/{id}` | Kullanıcı detayı | ✅ | Superuser |
| `DELETE` | `/api/v1/users/{id}` | Kullanıcı silme | ✅ | Superuser |

### Health

| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/health` | Service health check | ❌ |
| `GET` | `/` | API bilgileri | ❌ |

### Detailed API Documentation

**Swagger UI:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

---

## 🗄️ Veritabanı

### Models

**User Model** (`app/models/user.py`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `email` | String(255) | Unique email |
| `username` | String(50) | Unique username |
| `full_name` | String(100) | Full name (optional) |
| `hashed_password` | String(255) | bcrypt hashed password |
| `is_active` | Boolean | Account status |
| `is_superuser` | Boolean | Admin flag |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

### Migrations

```bash
# Yeni migration oluştur
alembic revision --autogenerate -m "description"

# Migration uygula
alembic upgrade head

# Geri al
alembic downgrade -1

# Migration geçmişi
alembic history
```

### pgAdmin Access

- URL: http://localhost:5050
- Email: `admin@admin.com`
- Password: `admin`

**Server Connection:**
- Host: `postgres`
- Port: `5432`
- Database: `myapp_db`
- Username: `postgres`
- Password: `postgres`

---

## 🧪 Testing

### Run Tests

```bash
# Tüm testler
pytest

# Coverage ile
pytest --cov=app --cov-report=html

# Verbose mode
pytest -v

# Specific file
pytest tests/test_auth.py

# Specific test
pytest tests/test_auth.py::test_register_user
```

### Test Coverage

Coverage raporu: `htmlcov/index.html`

```bash
# Coverage raporu oluştur
pytest --cov=app --cov-report=html

# Tarayıcıda aç
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows
```

---

## 🔧 Development

### Makefile Commands

```bash
make help          # Tüm komutları göster
make dev           # Development setup
make run           # Run development server
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linter (Ruff)
make format        # Format code (Ruff)
make type-check    # Run type checker (mypy)
make migrate       # Run database migrations
make migration     # Create new migration (msg="description")
make docker-up     # Start Docker containers
make docker-down   # Stop Docker containers
make superuser     # Create admin user
make clean         # Clean Python cache files
```

### Code Quality

```bash
# Linting
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Formatting
ruff format .

# Type checking
mypy app --ignore-missing-imports

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Environment Variables

Tüm environment variables için `.env.example` dosyasına bakın.

**Kritik Değişkenler:**
- `SECRET_KEY` - JWT secret (production'da değiştirin!)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `ALLOWED_ORIGINS` - CORS allowed origins
- `DEBUG` - Debug mode (production'da False)

---

## 🚀 Deployment

### Production Checklist

- [ ] `SECRET_KEY` - Güçlü, random değer
- [ ] `DEBUG=False` - Debug mode kapalı
- [ ] `ALLOWED_ORIGINS` - Production domain'ler
- [ ] `ALLOWED_HOSTS` - Production host'lar
- [ ] HTTPS yapılandırması
- [ ] Database backups
- [ ] Redis persistence
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Error tracking (Sentry)
- [ ] Rate limiting aktif
- [ ] Log aggregation
- [ ] Security headers

### Docker Production Build

```bash
# Production image build
docker build -t fastapi-app:latest .

# Run production container
docker run -d \
  -p 8000:8000 \
  --env-file .env.production \
  --name fastapi-app \
  fastapi-app:latest
```

### GitHub Actions CI/CD

Pipeline otomatik çalışır:
1. Lint & format check (Ruff)
2. Type checking (mypy)
3. Tests (pytest)
4. Coverage report (Codecov)
5. Docker build & push (main branch)

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen [COMMIT_RULES.md](COMMIT_RULES.md) dosyasını okuyun.

### Geliştirme Adımları

1. **Fork edin**
2. **Feature branch oluşturun**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Değişiklikleri commit edin**
   ```bash
   git commit -m "feat(scope): add amazing feature"
   ```
4. **Push edin**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Pull Request açın**

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

Detaylar için [COMMIT_RULES.md](COMMIT_RULES.md) okuyun.

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

Bu proje aşağıdaki harika araçları kullanmaktadır:

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Alembic](https://alembic.sqlalchemy.org/) - Database migrations
- [PostgreSQL](https://www.postgresql.org/) - Advanced database
- [Redis](https://redis.io/) - In-memory data store
- [Docker](https://www.docker.com/) - Containerization

---

## 📧 İletişim

Burak Cihan - [@burakcihan61](https://github.com/burakcihan61)

Proje Link: [https://github.com/burakcihan61/fast-api-auth](https://github.com/burakcihan61/fast-api-auth)

---

## 🌟 Star History

Projeyi beğendiyseniz ⭐ vermeyi unutmayın!

[![Star History Chart](https://api.star-history.com/svg?repos=burakcihan61/fast-api-auth&type=Date)](https://star-history.com/#burakcihan61/fast-api-auth&Date)

---

**Built with ❤️ using FastAPI**


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

## 📄 License

MIT License

## 👤 Author

Your Name

---

For more detailed information, see [rules.md](rules.md)
