# Project Setup Guide

## 📋 Requirements

- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional but recommended)

## 🛠️ Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fast-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings (DB, Redis)
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🐳 Docker Development

1. **Environment Setup**
   ```bash
   cp .env.example .env
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **View Logs**
   ```bash
   docker-compose logs -f api
   ```

4. **Access Services**
   - API: http://localhost:8000
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379
   - pgAdmin: http://localhost:5050
