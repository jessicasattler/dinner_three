# Dinner Three - Security-Focused Django Recipe Application

A small, secure Django application demonstrating security best practices including authentication, authorization, CSRF protection, and integrated security scanning.

## Features

- User authentication with login throttling
- Recipe management with server-rendered templates
- Favorites system with explicit ownership checks
- Small JSON API for testing
- Comprehensive security scanning pipeline

## Setup

See [SETUP.md](docs/SETUP.md) for detailed setup instructions.

## Security

This project implements:
- Django built-in security features
- Login throttling
- CSRF protection
- XSS prevention via template escaping
- OWASP Top 10:2025 mitigations
- Automated security scanning

See [SECURITY.md](SECURITY.md) for details.
