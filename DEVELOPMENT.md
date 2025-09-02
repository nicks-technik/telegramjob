# Development Guide

This document provides detailed information about developing and maintaining the Telegram Job project using `uv`.

## Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd telegramjob

# Install all dependencies
uv sync

# Install browser for Playwright
uv run playwright install chromium

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Authenticate with YouTube
uv run python youtube_auth.py

# Run the main script
uv run python telegramjob.py
```

## Understanding the uv Workflow

### Project Configuration

This project uses `pyproject.toml` as the single source of truth for:
- Project metadata (name, version, description)
- Python version requirements
- Dependencies and their versions

### Key Files

- **`pyproject.toml`**: Project configuration and dependencies
- **`uv.lock`**: Lock file with exact dependency versions (auto-generated)
- **`.python-version`**: Python version specification (if needed)

### Common Commands

#### Environment Management

```bash
# Create/sync virtual environment with all dependencies
uv sync

# Add a new dependency
uv add requests

# Add development dependency
uv add --dev pytest

# Remove a dependency
uv remove package-name

# Show project info
uv tree
```

#### Running Code

```bash
# Run any Python script in the project environment
uv run python script.py

# Run with additional packages (temporary)
uv run --with jupyter jupyter lab

# Get a Python shell with project dependencies
uv run python

# Run specific module
uv run -m pytest
```

#### Dependency Updates

```bash
# Update all dependencies to latest compatible versions
uv sync --upgrade

# Update specific package
uv sync --upgrade-package package-name
```

## Project-Specific Setup

### YouTube Authentication

The project includes a streamlined YouTube authentication system:

```bash
# First time setup - will open browser for login
uv run python youtube_auth.py
```

This creates `token.pickle` which stores your YouTube session. Subsequent runs will automatically use the saved session.

### Telegram Configuration

1. Copy environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Telegram API credentials:
   - `API_ID` and `API_HASH` from https://my.telegram.org/apps
   - `SOURCE_CHAT_ID` and `DESTINATION_CHAT_ID`

### Browser Setup

```bash
# Install only Chromium (sufficient for this project)
uv run playwright install chromium

# Or install all browsers if needed
uv run playwright install
```

## Production Deployment

### Automated Execution

The project includes a shell script for automated execution:

```bash
# Run once
./telegramjob.sh

# Install cron job (every 30 minutes, 9 AM - 9 PM)
./telegramjob.sh --install-cron
```

### Environment Isolation

Thanks to `uv`, the project runs in complete isolation:
- No conflicts with system Python packages
- Reproducible builds via `uv.lock`
- Automatic virtual environment management

## Troubleshooting

### Common Issues

1. **Missing browsers**: Run `uv run playwright install chromium`
2. **Permission errors**: Ensure `telegramjob.sh` is executable: `chmod +x telegramjob.sh`
3. **Outdated dependencies**: Run `uv sync --upgrade`

### Debugging

```bash
# Check installed packages
uv tree

# Validate lock file
uv lock --check

# Show environment info
uv run python -c "import sys; print(sys.executable)"
```

## Contributing

When contributing to this project:

1. Ensure `uv sync` works cleanly
2. Update `pyproject.toml` for any new dependencies
3. Test that `uv run python script.py` works for all scripts
4. Commit the updated `uv.lock` file

## Migration from pip/venv

If migrating from traditional pip/venv setup:

1. Remove old virtual environment: `rm -rf .venv`
2. Remove `requirements.txt` if it exists
3. Run `uv sync` to create new environment
4. Update any documentation/scripts to use `uv run`

The `pyproject.toml` already contains all necessary dependencies - no additional setup needed!
