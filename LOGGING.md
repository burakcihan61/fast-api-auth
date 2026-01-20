# Professional Logging System

## 📝 Genel Bakış

FastAPI projenize profesyonel bir logging sistemi entegre ettim:

### ✨ Özellikler

- **Structured JSON Logging** - Machine-readable log format
- **Request/Response Tracking** - Her HTTP request izlenir
- **Correlation IDs** - Request'leri takip için unique ID
- **Log Levels** - DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation** - Otomatik log dosyası döndürme (10MB limit)
- **Multiple Handlers** - Console, File, Error logs
- **Performance Tracking** - Response time logging
- **Authentication Auditing** - Login/logout attempts

---

## 📊 Log Yapısı

### 1. Log Dosyaları

```
logs/
├── app.log       # Genel uygulama logları (JSON format)
├── error.log     # Sadece ERROR ve üzeri (JSON format)
└── access.log    # HTTP request/response logları (JSON format)
```

**Özellikler:**
- **Rotation**: Her dosya 10MB'a ulaşınca yeni dosya oluşturulur
- **Backup**: Son 5-10 backup dosyası saklanır
- **Format**: Production'da JSON, development'ta human-readable

### 2. Log Formatı

**Production (JSON):**
```json
{
  "timestamp": "2026-01-21T00:42:08.123456",
  "level": "INFO",
  "logger_name": "fastapi_app",
  "message": "Request completed: GET /api/v1/users/me - 200 (0.042s)",
  "app_name": "MyFastAPIApp",
  "app_version": "1.0.0",
  "environment": "production",
  "event": "request_completed",
  "correlation_id": "abc123-def456",
  "method": "GET",
  "path": "/api/v1/users/me",
  "status_code": 200,
  "duration_ms": 42.15
}
```

**Development (Console):**
```
2026-01-21 00:42:08 - fastapi_app - INFO - Request completed: GET /api/v1/users/me - 200 (0.042s)
```

---

## 🎯 Kullanım

### 1. Basic Logging

```python
from app.core.logging import logger

# Info log
logger.info("User profile updated successfully")

# Warning
logger.warning("API rate limit approaching")

# Error
logger.error("Database connection failed", exc_info=True)

# With extra context
logger.info(
    "Cache hit for user data",
    extra={
        "event": "cache_hit",
        "user_id": 123,
        "cache_key": "user:123",
    }
)
```

### 2. Request Tracking (Otomatik)

Her HTTP request otomatik olarak loglanır:

```json
{
  "event": "request_started",
  "correlation_id": "uuid-here",
  "method": "POST",
  "url": "http://localhost:8000/api/v1/auth/login",
  "path": "/api/v1/auth/login",
  "client_host": "127.0.0.1",
  "user_agent": "Mozilla/5.0..."
}
```

Response:
```json
{
  "event": "request_completed",
  "correlation_id": "uuid-here",
  "status_code": 200,
  "duration_ms": 45.23
}
```

### 3. Authentication Logging

```python
from app.middleware.logging import log_authentication

# Successful login
log_authentication(
    username="john_doe",
    success=True,
)

# Failed login
log_authentication(
    username="attacker",
    success=False,
    reason="invalid_credentials",
    ip_address="192.168.1.100",
)
```

### 4. Database Query Logging

```python
from app.middleware.logging import log_database_query

# Log slow queries
log_database_query(
    query="SELECT * FROM users WHERE id = $1",
    duration=1.234,  # seconds
    params={"id": 123}
)
```

### 5. Cache Operations

```python
from app.middleware.logging import log_cache_operation

# Cache hit
log_cache_operation(
    operation="get",
    key="user:123",
    hit=True,
    duration=0.002
)

# Cache miss
log_cache_operation(
    operation="get",
    key="user:456",
    hit=False,
    duration=0.001
)
```

### 6. Exception Logging

```python
from app.middleware.logging import log_exception

try:
    # Some operation
    result = risky_operation()
except Exception as exc:
    log_exception(
        exc,
        context={
            "user_id": user.id,
            "operation": "data_export",
        }
    )
    raise
```

---

## 🔍 Log Seviyeleri

| Level | Kullanım | Örnek |
|-------|----------|-------|
| **DEBUG** | Detaylı debugging bilgisi | SQL queries, cache operations |
| **INFO** | Genel bilgilendirme | User actions, API calls |
| **WARNING** | Potential problems | Rate limit approaching, deprecated API |
| **ERROR** | Hatalar | Database errors, failed operations |
| **CRITICAL** | Ciddi sistem hataları | Service down, data corruption |

### Seviye Ayarlama

`.env` dosyasında:
```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## 📈 Correlation ID Tracking

Her request için unique bir ID üretilir ve response header'ına eklenir:

**Response Header:**
```
X-Correlation-ID: 123e4567-e89b-12d3-a456-426614174000
```

Bu ID ile tüm logları filtreleyebilirsiniz:

```bash
# Logs dosyasında arama
grep "123e4567-e89b-12d3-a456-426614174000" logs/app.log
```

---

## 🛠️ Log Görüntüleme

### 1. Canlı Log İzleme (Tail)

```bash
# Son logları izle
tail -f logs/app.log

# JSON pretty-print ile
tail -f logs/app.log | jq

# Sadece ERROR logları
tail -f logs/error.log | jq
```

### 2. Log Filtreleme

```bash
# Belirli event'leri filtrele
cat logs/app.log | jq 'select(.event == "request_completed")'

# Başarısız authentication
cat logs/app.log | jq 'select(.event == "authentication" and .success == false)'

# Yavaş requestler (> 1 saniye)
cat logs/app.log | jq 'select(.duration_ms > 1000)'

# Belirli endpoint
cat logs/access.log | jq 'select(.path == "/api/v1/users/me")'
```

### 3. Log Analizi

**En çok çağrılan endpoint'ler:**
```bash

cat logs/access.log | jq -r '.path' | sort | uniq -c | sort -rn | head -10
```

**Ortalama response time:**
```bash
cat logs/access.log | jq '.duration_ms' | awk '{sum+=$1; count++} END {print sum/count}'
```

**Status code dağılımı:**
```bash
cat logs/access.log | jq -r '.status_code' | sort | uniq -c
```

---

## 📊 Production Best Practices

### 1. Log Aggregation

Production'da logları merkezi bir sisteme gönderin:

**Seçenekler:**
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Loki + Grafana**
- **Datadog**
- **CloudWatch** (AWS)
- **Google Cloud Logging**

**Python integration örneği:**
```python
# app/core/logging.py içinde
import logging
from logging.handlers import SysLogHandler

# Syslog handler (for log aggregation)
syslog = SysLogHandler(address=('logserver.example.com', 514))
syslog.setFormatter(json_formatter)
logger.addHandler(syslog)
```

### 2. Log Retention

```python
# Retention policy
RotatingFileHandler(
    filename="logs/app.log",
    maxBytes=10 * 1024 * 1024,  # 10MB per file
    backupCount=30,  # Keep 30 files = ~300MB total
)
```

### 3. Sensitive Data

**❌ Asla loglamayın:**
- Passwords
- API keys
- Credit card numbers
- Personal identification numbers (SSN, etc.)
- Session tokens

**✅ Log edilebilir:**
- Usernames (hash'lenebilir)
- Email addresses (production'da mask edilebilir)
- Request paths
- Response status codes
- Timing information

**Masking örneği:**
```python
def mask_email(email: str) -> str:
    """Mask email for logging"""
    username, domain = email.split('@')
    return f"{username[0]}***@{domain}"

logger.info(f"User registered: {mask_email(user.email)}")
```

### 4. Performance Impact

- Log kes **asenkron** olmalı (production için)
- File I/O minimize edilmeli
- Buffering kullanılmalı
- Kritik path'lerde sadece ERROR/WARNING

```python
# Async logging handler örneği
from logging.handlers import QueueHandler, QueueListener
import queue

log_queue = queue.Queue()
queue_handler = QueueHandler(log_queue)
logger.addHandler(queue_handler)

# Listener separate thread'de çalışır
listener = QueueListener(log_queue, file_handler, console_handler)
listener.start()
```

---

## 🔒 Security Logging

### Important Events to Log

1. **Authentication:**
   - Login attempts (success/fail)
   - Logout events
   - Password changes
   - Account lockouts

2. **Authorization:**
   - Permission denied events
   - Role changes
   - Access to sensitive resources

3. **Data Changes:**
   - User profile updates
   - Critical data modifications
   - Deletions

4. **Security Events:**
   - Invalid tokens
   - Rate limit exceeded
   - Suspicious patterns
   - Failed validations

---

## 📱 Monitoring & Alerting

### 1. Error Rate Monitoring

```bash
# Count errors per minute
cat logs/error.log | \
  jq -r '.timestamp' | \
  cut -c1-16 | \
  uniq -c
```

### 2. Alert Rules

**Prometheus AlertManager örneği:**
```yaml
groups:
  - name: logging_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(log_messages_total{level="ERROR"}[5m]) > 10
        annotations:
          summary: "High error rate detected"
          
      - alert: FailedLogins
        expr: rate(authentication_attempts{success="false"}[5m]) > 5
        annotations:
          summary: "Multiple failed login attempts"
```

### 3. Dashboards

**Grafana queries:**
```
# Request rate
sum(rate(http_requests_total[5m]))

# Error rate
sum(rate(http_requests_total{status_code=~"5.."}[5m]))

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_milliseconds_bucket[5m]))
```

---

## 🧪 Testing Logs

```bash
# Test logging sistemi
curl http://localhost:8000/health

# app.log'da görmeli:
tail -1 logs/app.log | jq

# access.log'da görmeli:
tail -1 logs/access.log | jq

# Hatalı login test:
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=wrong&password=wrong"

# error.log'da görmeli:
tail -1 logs/error.log | jq
```

---

## 📚 Log Rotasyonu

### Otomatik Rotation

Python `RotatingFileHandler` otomatik olarak:
1. Dosya 10MB'a ulaşınca yeni dosya oluşturur
2. Eski dosya `app.log.1`, `app.log.2` gibi adlandırılır
3. En eski backup silinir (backupCount kadar tutar)

### Manuel Cleanup

```bash
# 30 günden eski logları sil
find logs/ -name "*.log.*" -mtime +30 -delete

# Toplam log boyutu
du -sh logs/
```

---

## 🎯 Hızlı Başlangıç

1. **Sistemi Aktifleştir:**
   - ✅ Zaten aktif! (main.py'de setup_logging() çağrılıyor)

2. **Logları Gör:**
   ```bash
   # Console'da (development mode)
   docker-compose logs -f api
   
   # Dosyalarda
   tail -f logs/app.log | jq
   ```

3. **Test Et:**
   ```bash
   # API çağrısı yap
   curl http://localhost:8000/health
   
   # Log'u kontrol et
   cat logs/access.log | jq | tail -5
   ```

---

## ❓ Sorun Giderme

### Problem: Logs klasörü oluşmadı
```bash
mkdir -p logs
chmod 755 logs
```

### Problem: Permission denied
```bash
# Docker içinde
docker-compose exec api mkdir -p /app/logs
docker-compose exec api chmod 777 /app/logs
```

### Problem: JSON parse hatası
```bash
# Log dosyası boş veya bozuk olabilir
tail -100 logs/app.log | jq  # Son 100 satır
```

---

## 📦 Dosya Yapısı

```
app/
├── core/
│   └── logging.py          # Logging configuration
├── middleware/
│   ├── logging.py          # Logging middleware + helpers
│   └── error_handler.py    # Error handling
└── main.py                 # Logging initialization

logs/                       # Log files (auto-created)
├── app.log                 # Application logs
├── app.log.1               # Rotated backups
├── error.log               # Error logs
└── access.log              # HTTP access logs
```

---

## 🚀 Production Checklist

- [x] Structured JSON logging
- [x] Log rotation configured
- [x] Correlation IDs implemented
- [x] Request/Response tracking
- [x] Authentication auditing
- [x] Error logging
- [ ] Log aggregation setup (ELK/Loki)
- [ ] Monitoring & alerting configured
- [ ] Log retention policy defined
- [ ] PII masking implemented
- [ ] Async logging for high load

---

**Logging sisteminiz hazır ve production-ready! 🎉**

Logları test etmek için Docker container'ları başlatın ve API'yi kullanın.
