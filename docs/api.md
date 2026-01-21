# API Documentation

## 🔐 Authentication & Endpoints

### Authentication
- `POST /api/v1/auth/register` - Create new account
- `POST /api/v1/auth/login` - Get access/refresh tokens

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update profile
- `GET /api/v1/users` - Admin list users

## 🔄 Versioning

The API uses URL path versioning:
- **/api/v1**: Stable production endpoints
- **/api/v2**: Experimental features

## 🌍 Localization (i18n)

The API supports multiple languages for error messages and responses.

**Supported Languages:**
- English (`en`) - Default
- Turkish (`tr`)

**Usage:**
Send the `Accept-Language` header with your request:

```http
GET /api/v2/example/
Accept-Language: tr
```

**Response:**
```json
{
  "message": "API'ye hoşgeldiniz"
}
```

## 🛡️ Rate Limiting

Dynamic rate limiting is implemented via `slowapi` and Redis.

**Limits:**
- **Anonymous**: 5 req/min
- **Authenticated**: 10 req/min
- **Premium**: 20 req/min

Headers included in response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
