# Telegram Job

This project is a Python-based automation tool that monitors a Telegram channel for messages containing links, takes screenshots of those links, and forwards them to another Telegram channel.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.11 or higher
- [`uv`](https://docs.astral.sh/uv/) package manager

#### Installing uv

If you don't have `uv` installed yet:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd telegramjob
    ```

2.  **Install dependencies using uv:**

    ```bash
    uv sync
    ```

    This command will:
    - Create a virtual environment automatically
    - Install all dependencies defined in `pyproject.toml`
    - Generate/update the `uv.lock` file

3.  **Install Playwright browsers:**

    ```bash
    uv run playwright install chromium
    ```

4.  **Set up your environment variables:**

    Copy the `.env.example` to `.env` and fill in your details:

    ```bash
    cp .env.example .env
    ```

    You will need to provide:
    - Telegram API credentials (`API_ID`, `API_HASH`)
    - Source and destination chat IDs (`SOURCE_CHAT_ID`, `DESTINATION_CHAT_ID`). You can obtain these by visiting https://web.telegram.org/a/ and inspecting the URL when you are in the desired chat.


### Running the Scripts

- **Main Telegram job:**

  ```bash
  uv run python telegramjob.py
  ```

- **Run via shell script:**

  ```bash
  ./telegramjob.sh
  ```

### Installing the Cron Job

To run the script automatically every 30 minutes between 9 AM and 9 PM, you can install the cron job:

```bash
./telegramjob.sh --install-cron
```

## Development with uv

### Adding Dependencies

To add new dependencies to the project:

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Add a specific version
uv add "package-name>=1.0.0"
```

### Managing the Environment

```bash
# Sync dependencies (install/update based on pyproject.toml)
uv sync

# Run any Python command in the project environment
uv run python script.py

# Get a shell in the virtual environment
uv run --with ipython ipython
# or
uv run python
```

### Project Structure

The project uses `pyproject.toml` for dependency management and configuration:
- **`pyproject.toml`**: Defines project metadata and dependencies
- **`uv.lock`**: Locks exact versions for reproducible installs
- **`.env`**: Environment variables (copy from `.env.example`)


## Modules

- **`telegramjob.py`**: The main script that orchestrates the entire process. It reads messages, processes jobs, and coordinates the other modules.
- **`config.py`**: Handles the application's configuration by loading values from environment variables defined in the `.env` file.
- **`logger_config.py`**: Configures the logging for the application, setting up both file and console logging.
- **`message_parser.py`**: Contains the logic for parsing messages from Telegram and extracting relevant information, such as task numbers and URLs.
- **`playwrightstuff.py`**: Manages browser automation using Playwright. It's responsible for taking screenshots and interacting with web pages.
- **`telegramstuff.py`**: Contains functions for interacting with the Telegram API, such as sending messages and pictures.
