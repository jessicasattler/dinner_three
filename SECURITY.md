# Dinner Three Security Documentation

## Overview

Dinner Three implements Django security best practices with additional hardening for OWASP Top 10:2025 mitigations.

## Security Features

### 1. Authentication & Authorization

- **Django Built-in Authentication**: Uses Django's secure password hashing (PBKDF2)
- **Login Throttling**: Implemented via django-axes (5 attempts, 1-hour lockout)
- **Explicit Authorization Checks**: All resource modifications check `created_by == request.user`
- **Password Validation**: Minimum 8 characters, no common passwords, no user attribute similarity

### 2. CSRF Protection

- Django CSRF middleware enabled
- CSRF tokens required for all state-changing requests
- Template auto-escaping enabled

### 3. XSS Prevention

- Template auto-escaping enabled by default
- No `|safe` filter used on user input
- All user data displayed through Django templates

### 4. SQL Injection Prevention

- Django ORM used exclusively, no raw SQL
- All queries parameterized

### 5. Session Security

- `SESSION_COOKIE_SECURE` (set to True in production)
- `CSRF_COOKIE_SECURE` (set to True in production)
- `SECURE_SSL_REDIRECT` (set to True in production)

### 6. Configuration Security

- `DEBUG=False` in production
- `ALLOWED_HOSTS` explicitly configured
- `SECRET_KEY` environment variable
- Secure cookie settings configured

## Security Testing

### Unit Tests

Run security tests with:
```bash
pytest tests/test_security.py -v
```

Tests cover:
- Authorization checks for recipe CRUD operations
- Favorite ownership verification
- CSRF token protection

### Automated Scanning

See `docs/SCANNING.md` for:
- CodeQL (SAST)
- pip-audit (SCA)
- TruffleHog (secret scanning)
- KICS (configuration scanning)
- ZAP (DAST)

## OWASP Top 10:2025 Mapping

| OWASP | Implementation |
|-------|-----------------|
| A01:2025 - Broken Access Control | Explicit ownership checks in views |
| A02:2025 - Cryptographic Failures | PBKDF2 password hashing, secure cookies |
| A03:2025 - Injection | Django ORM parameterized queries |
| A04:2025 - Insecure Design | CSRF protection, login throttling |
| A05:2025 - Security Misconfiguration | DEBUG=False, ALLOWED_HOSTS, env vars |
| A06:2025 - Vulnerable Components | pip-audit, dependency pinning |
| A07:2025 - Authentication Failures | Login throttling, session security |
| A08:2025 - Software/Data Integrity | No untrusted dependencies |
| A09:2025 - Logging/Monitoring | Admin audit trail |
| A10:2025 - SSRF | No external service calls |

## Environment Variables

Required for production:

```bash
SECRET_KEY=<generate-with-django-insecure-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Running Locally

For local testing, `DEBUG=True` is acceptable, but set secure cookies to False.

## Production Deployment

1. Set all `SECURE_*` variables to True
2. Use HTTPS only
3. Set `DEBUG=False`
4. Change `SECRET_KEY` to a random value
5. Review `ALLOWED_HOSTS`
6. Run migrations
7. Collect static files
