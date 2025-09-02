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

5.  **Set up YouTube authentication:**

    For YouTube functionality, you can authenticate using the simplified login script:

    ```bash
    uv run python youtube_auth.py
    ```

    This will:
    - Open a browser window
    - Allow you to log in to YouTube manually
    - Save your session to `token.pickle` for future use
    - Automatically load saved sessions on subsequent runs

### Running the Scripts

- **Main Telegram job:**

  ```bash
  uv run python telegramjob.py
  ```

- **YouTube authentication:**

  ```bash
  uv run python youtube_auth.py
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
- **`token.pickle`**: Stores YouTube authentication session (auto-generated)
- **`.env`**: Environment variables (copy from `.env.example`)

## YouTube Integration

The project includes two approaches for YouTube integration:

### 1. Simple Browser Authentication (`youtube_auth.py`)
For basic login and session management:
```bash
uv run python youtube_auth.py
```

### 2. Full YouTube Client (`youtube_client.py`)
Integrated client with both browser automation and YouTube Data API:
```python
from youtube_client import YouTubeClient

async def example():
    async with YouTubeClient() as youtube:
        # Extract video ID
        video_id = youtube.extract_video_id(url)
        
        # Get channel info
        channel_id = youtube.get_channel_id_from_video_id(video_id)
        
        # Check subscription
        is_subscribed = youtube.is_subscribed(channel_id)
        
        # Subscribe to channel
        youtube.subscribe_to_channel(channel_id)
        
        # Like video
        youtube.like_video(video_id)
```

### Authentication Files
- **`token.pickle`**: Browser session cookies (created by `youtube_auth.py` or `YouTubeClient`)
- **`youtube_api_token.pickle`**: YouTube Data API credentials (requires `credentials.json`)
- **`credentials.json`**: Google API credentials file (download from Google Cloud Console)

## Modules

- **`telegramjob.py`**: The main script that orchestrates the entire process. It reads messages, processes jobs, and coordinates the other modules.
- **`youtube_client.py`**: **NEW** - Integrated YouTube client with Playwright authentication and Data API functionality.
- **`youtube_auth.py`**: Simple standalone YouTube authentication script.
- **`config.py`**: Handles the application's configuration by loading values from environment variables defined in the `.env` file.
- **`logger_config.py`**: Configures the logging for the application, setting up both file and console logging.
- **`message_parser.py`**: Contains the logic for parsing messages from Telegram and extracting relevant information, such as task numbers and URLs.
- **`playwrightstuff.py`**: Manages browser automation using Playwright. It's responsible for taking screenshots and interacting with web pages.
- **`telegramstuff.py`**: Contains functions for interacting with the Telegram API, such as sending messages and pictures.
- **`youtubestuff.py`**: Legacy YouTube Data API handler (consider migrating to `youtube_client.py`).
