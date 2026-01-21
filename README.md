# FastAPI Professional Starter

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![License](https://img.shields.io/badge/license-MIT-green)

A production-ready FastAPI boilerplate with PostgreSQL, Redis, JWT Authentication, and professional structured logging.

## 🚀 Features

- **FastAPI** with async/await support
- **PostgreSQL** (SQLAlchemy 2.0 + Alembic)
- **Redis** Caching & Rate Limiting
- **JWT Authentication** (Access/Refresh Tokens)
- **Localization (i18n)** (English/Turkish support)
- **Structured Logging** (JSON logs, Correlation IDs)
- **Docker & Docker Compose** ready
- **Background Tasks** (Celery + Redis)
- **Prometheus** Metrics

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

| Topic | Description |
|-------|-------------|
| [📥 Setup Guide](docs/setup.md) | Installation, Local & Docker setup |
| [🔗 API & Features](docs/api.md) | Endpoints, Versioning, Localization, Rate Limits |
| [📊 Monitoring](docs/monitoring.md) | Prometheus metrics and Grafana dashboards |
| [📝 Logging](docs/logging.md) | Structured logging configuration and usage |
| [🚀 Deployment](docs/deployment.md) | Production checklist and deployment |
| [🤝 Contributing](CONTRIBUTING.md) | Development guidelines, testing, and standards |

## ⚡ Quick Start

1. **Clone & Setup:**
```bash
git clone <repository-url>
cd fast-api
cp .env.example .env
```

2. **Run with Docker:**
```bash
docker-compose up -d
```

Visit:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🛠️ Tech Stack

- **Framework:** FastAPI, Uvicorn
- **Database:** PostgreSQL 16
- **ORM:** SQLAlchemy 2.0 (Async)
- **Cache:** Redis 7
- **Validation:** Pydantic v2
- **Testing:** pytest
- **Tools:** Ruff, Pre-commit, Structlog

## 📄 License

This project is licensed under the MIT License.
