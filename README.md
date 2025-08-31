# Telegram Job

This project is a Python-based automation tool that monitors a Telegram channel for messages containing links, takes screenshots of those links, and forwards them to another Telegram channel.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.11
- `uv` package manager

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd telegramjob
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    uv venv
    uv pip install .
    ```

3.  **Install Playwright browsers:**

    ```bash
    uv run playwright install
    ```

4.  **Set up your environment variables:**

    Copy the `.env.example` to `.env` and fill in your details:

    ```bash
    cp .env.example .env
    ```

    You will need to provide:
    - Telegram API credentials (`API_ID`, `API_HASH`)
    - Source and destination chat IDs (`SOURCE_CHAT_ID`, `DESTINATION_CHAT_ID`). You can obtain these by visiting https://web.telegram.org/a/ and inspecting the URL when you are in the desired chat.

5.  **Set up Google API credentials:**

    If you intend to use the YouTube functionality, you need to set up Google API credentials. Follow the instructions to create a `credentials.json` file.

    Then, generate a `token.pickle` file by running:

    ```bash
    uv run python3 ./youtubestuff.py
    ```

### Running the Script

- **Run directly:**

  ```bash
  uv run python3 telegramjob.py
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

## Modules

- **`telegramjob.py`**: The main script that orchestrates the entire process. It reads messages, processes jobs, and coordinates the other modules.
- **`config.py`**: Handles the application's configuration by loading values from environment variables defined in the `.env` file.
- **`logger_config.py`**: Configures the logging for the application, setting up both file and console logging.
- **`message_parser.py`**: Contains the logic for parsing messages from Telegram and extracting relevant information, such as task numbers and URLs.
- **`playwrightstuff.py`**: Manages browser automation using Playwright. It's responsible for taking screenshots and interacting with web pages.
- **`telegramstuff.py`**: Contains functions for interacting with the Telegram API, such as sending messages and pictures.
- **`youtubestuff.py`**: Handles interactions with the YouTube Data API, including liking videos and subscribing to channels.