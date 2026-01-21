# Deployment Guide

## 🚀 Production Checklist

Ensure these steps are completed before deploying to production:

1. **Security**
   - [ ] Set `DEBUG=False` in `.env`
   - [ ] Generate a strong, random `SECRET_KEY`
   - [ ] Configure HTTPS/SSL (e.g., via Nginx or Traefik)
   - [ ] Review `ALLOWED_HOSTS` / CORS settings

2. **Database**
   - [ ] Run `alembic upgrade head`
   - [ ] Configure automated backups
   - [ ] Set secure database passwords

3. **Performance**
   - [ ] Enable Gunicorn with Uvicorn workers
   - [ ] Configure Redis for caching and rate limiting
   - [ ] Set up connection pooling

4. **Monitoring**
   - [ ] Enable structured logging (JSON)
   - [ ] Set up Prometheus/Grafana (see [monitoring.md](monitoring.md))
   - [ ] Configure error tracking (Sentry, etc.)

## 🐳 Docker Production Command

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

*(Note: Ensure you have a production-specific compose file if needed, or override settings via environment variables)*
