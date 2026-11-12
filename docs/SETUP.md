# Setup Instructions for Windows PowerShell + VS Code

## Prerequisites

- Python 3.10+ installed
- VS Code installed
- Git installed

## Step 1: Clone Repository

```powershell
git clone git@github.com:jessicasattler/dinner_three.git
cd dinner_three
git checkout feature/initial_setup
```

## Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

## Step 4: Configure Environment

```powershell
Copy-Item .env.example .env
# Edit .env with your settings
```

For local development:
```
DEBUG=True
SECRET_KEY=dev-secret-key-12345
ALLOWED_HOSTS=localhost,127.0.0.1
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
ENVIRONMENT=development
```

## Step 5: Initialize Database

```powershell
python manage.py migrate
python manage.py createsuperuser
```

## Step 6: Run Development Server

```powershell
python manage.py runserver
```

Visit: `http://localhost:8000`
Admin: `http://localhost:8000/admin`

## Step 7: Run Tests

```powershell
pytest tests/ -v
pytest tests/test_security.py -v --cov=recipes
```

## Step 8: Security Scanning

### pip-audit (Dependency Scanning)
```powershell
pip-audit --desc
```

### Linting
```powershell
black .
flake8 recipes/ --max-line-length=100
isort recipes/
```

## VS Code Setup

### Recommended Extensions

1. **Python** (Microsoft)
2. **Django** (Baptiste Darthenay)
3. **Pylance** (Microsoft)
4. **Black Formatter** (Microsoft)

### Launch Configuration

Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver"],
            "django": true,
            "justMyCode": true
        }
    ]
}
```

### Settings

Create `.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.linting.flake8Args": ["--max-line-length=100"],
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

## Troubleshooting

### Virtual Environment Issues
```powershell
# Remove and recreate
Remove-Item venv -Recurse -Force
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Database Issues
```powershell
Remove-Item db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Port 8000 In Use
```powershell
python manage.py runserver 8001
```

## Next Steps

1. Review [SECURITY.md](SECURITY.md) for security details
2. Review [docs/SCANNING.md](docs/SCANNING.md) for CI/CD pipeline setup
3. Create a pull request from `feature/initial_setup` to `main`
4. Set up GitHub Actions workflows
