# Prometheus Metrics Kullanım Kılavuzu

## 📊 Prometheus Metrics - Nedir?

Prometheus, uygulamanızın performans metriklerini toplar ve izler:
- HTTP request sayıları
- Response süreleri
- Error oranları
- CPU/Memory kullanımı
- Custom metrics

---

## 🎯 Mevcut Durum

Projenizde **prometheus-fastapi-instrumentator** kurulu ve hazır.

### Kod Konumu

`app/main.py` - Satır 65:
```python
Instrumentator().instrument(app).expose(app)
```

**Değişiklik:** Artık tüm ortamlarda aktif (development dahil)

---

## 🔌 Metrics Endpoint'i

### Erişim

```bash
# Metrics endpoint
http://localhost:8000/metrics
```

### Test

```bash
# PowerShell
Invoke-WebRequest http://localhost:8000/metrics

# curl
curl http://localhost:8000/metrics
```

### Response Örneği

```
# HELP http_requests_total Total number of requests
# TYPE http_requests_total counter
http_requests_total{method="GET",path="/health"} 42.0
http_requests_total{method="POST",path="/api/v1/auth/login"} 15.0

# HELP http_request_duration_seconds HTTP request duration
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.005",method="GET",path="/health"} 40.0
http_request_duration_seconds_bucket{le="0.01",method="GET",path="/health"} 42.0
http_request_duration_seconds_sum{method="GET",path="/health"} 0.123
http_request_duration_seconds_count{method="GET",path="/health"} 42.0

# HELP python_info Python platform information
# TYPE python_info gauge
python_info{version="3.11.0"} 1.0
```

---

## 📈 Toplanan Metrikler

### 1. HTTP Metrics (Otomatik)

| Metric | Açıklama |
|--------|----------|
| `http_requests_total` | Toplam HTTP request sayısı |
| `http_request_duration_seconds` | Request işlem süresi (histogram) |
| `http_requests_in_progress` | Aktif request sayısı |
| `http_request_size_bytes` | Request boyutu |
| `http_response_size_bytes` | Response boyutu |

### 2. System Metrics

| Metric | Açıklama |
|--------|----------|
| `process_cpu_seconds_total` | CPU kullanım süresi |
| `process_resident_memory_bytes` | RAM kullanımı |
| `process_open_fds` | Açık file descriptors |
| `python_info` | Python version bilgisi |

### 3. FastAPI Metrics

| Metric | Açıklama |
|--------|----------|
| `fastapi_requests_total` | Endpoint bazlı request sayıları |
| `fastapi_requests_duration_seconds` | Endpoint response süreleri |
| `fastapi_exceptions_total` | Exception sayıları |

---

## 🛠️ Prometheus Server Kurulumu

### Docker ile Prometheus + Grafana

`docker-compose.yml`'e ekleyin:

```yaml
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    networks:
      - app-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - app-network

volumes:
  prometheus_data:
  grafana_data:
```

### Prometheus Config (`prometheus.yml`)

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
```

### Başlatma

```bash
docker-compose up -d prometheus grafana
```

**Erişim:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

---

## 📊 Grafana Dashboard

### 1. Prometheus Data Source Ekle

Grafana → Configuration → Data Sources → Add:
- Type: Prometheus
- URL: `http://prometheus:9090`
- Save & Test

### 2. Dashboard Import

Hazır FastAPI dashboard:
- Dashboard ID: **14191** (FastAPI Observability)
- Import → Enter ID → Load → Select Prometheus → Import

### 3. Custom Queries

```promql
# Request rate (son 5 dakika)
rate(http_requests_total[5m])

# Average response time
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

## 🎯 Hızlı Test

### 1. Docker'ı Başlatın

```bash
docker-compose up -d
```

### 2. Metrics Endpoint'i Kontrol Edin

```bash
# Browser
http://localhost:8000/metrics

# PowerShell
Invoke-WebRequest http://localhost:8000/metrics | Select-Object -ExpandProperty Content

# curl
curl http://localhost:8000/metrics
```

### 3. Load Oluşturun

```bash
# 10 request loop
for ($i=0; $i -lt 10; $i++) { 
    Invoke-RestMethod http://localhost:8000/health 
}
```

### 4. Metrics'leri Tekrar Kontrol Edin

`http_requests_total` sayısının arttığını görmelisiniz!

---

## 🔍 Custom Metrics Ekleme

### Counter Örneği

```python
from prometheus_client import Counter

# app/main.py veya ilgili dosya
user_registration_counter = Counter(
    'user_registrations_total',
    'Total number of user registrations'
)

# Endpoint içinde
@router.post("/register")
async def register(user: UserCreate):
    # ... user creation logic ...
    user_registration_counter.inc()  # Metric artır
    return user
```

### Gauge Örneği

```python
from prometheus_client import Gauge

active_users_gauge = Gauge(
    'active_users',
    'Number of currently active users'
)

# Update
active_users_gauge.set(len(active_users))
```

### Histogram Örneği

```python
from prometheus_client import Histogram

db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds'
)

# Kullanım
with db_query_duration.time():
    result = await db.execute(query)
```

---

## 📱 Monitoring Best Practices

### 1. Alerts Tanımlama

```yaml
# prometheus/alerts.yml
groups:
  - name: fastapi
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: SlowResponses
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        annotations:
          summary: "95th percentile latency > 1s"
```

### 2. Key Metrics to Monitor

- **Request Rate** - Trafik analizi
- **Error Rate** - Hata oranı (5xx)
- **Latency P95/P99** - Response süreleri
- **Database Query Time** - DB performansı
- **Cache Hit Rate** - Redis etkinliği
- **Active Connections** - Concurrent users

---

## 🚀 Production Checklist

- [ ] Prometheus server kurulu
- [ ] Grafana dashboard oluşturuldu
- [ ] Alerts tanımlandı
- [ ] Notification channels (Slack, email) yapılandırıldı
- [ ] Retention policy belirlendi (ne kadar süre veri saklanacak)
- [ ] Backup stratejisi oluşturuldu
- [ ] Custom business metrics eklendi

---

## 📚 Kaynaklar

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)

---

## 💡 Öneriler

1. **Başlangıç:** Metrics endpoint'ini test edin
2. **Geliştirme:** Prometheus + Grafana'yı Docker'da çalıştırın
3. **Production:** Dedicated Prometheus/Grafana sunucuları
4. **Monitoring:** Alertmanager ile otomatik uyarılar
5. **Retention:** 15-30 gün data retention yeterli

---

**Metrics aktif ve `/metrics` endpoint'inde mevcut!** 🎉
