# Gemini Best Practices for the Telegram Job Project

This document outlines the best practices and conventions to be followed in this project.

## General Best Practices

*   **Configuration:** All configuration should be stored in `config.py`. No hardcoded values in the code.
*   **Secrets:** Sensitive information like API keys and tokens must be stored in a `.env` file and not committed to version control. Use `.env.example` as a template.
*   **Logging:** Use the `logger_config.py` for consistent logging throughout the application.
*   **Dependencies:** All Python dependencies are managed with `uv` and defined in `pyproject.toml`. The `requirements.txt` file is not strictly necessary for dependency management but can be used for specific environment freezes.

## Python Best Practices

*   **Style Guide:** Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
*   **Linting:** Use `pylint` with the provided `.pylintrc` configuration to enforce code quality.
*   **Typing:** Use type hints for all function signatures.
*   **Docstrings:** Write clear and concise docstrings for all modules, functions, and classes.

## Telegram API Best Practices

*   **Error Handling:** Implement robust error handling for all Telegram API calls.
*   **Rate Limiting:** Be mindful of Telegram's rate limits to avoid being banned.
*   **Asynchronous Operations:** Use asynchronous operations when interacting with the Telegram API for better performance.

## Playwright Best Practices

*   **Selectors:** Prefer user-visible selectors (like text or ARIA roles) over CSS or XPath selectors.
*   **Waits:** Use Playwright's auto-waiting mechanism and explicit waits instead of fixed delays (`time.sleep()`).
*   **Browser Contexts:** Use browser contexts to isolate tests and sessions.
*   **Headless Mode:** Run Playwright in headless mode in production and CI environments.

## Security Best Practices

*   **Secrets Management:** Never commit secrets to the repository. Use environment variables loaded from a `.env` file.
*   **Input Validation:** Validate and sanitize all input from external sources to prevent injection attacks.
*   **Permissions:** Run the application with the least privileges necessary.

## Testing Best Practices

*   **Unit Tests:** Write unit tests for individual components, especially for `message_parser.py`.
*   **Integration Tests:** Write integration tests for the interaction between different parts of the system.
*   **End-to-End Tests:** Use Playwright to write end-to-end tests that simulate user interactions.

## Commit Message Conventions

*   **Format:** Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.
*   **Subject:** The subject line should be a concise summary of the change (max 50 chars).
*   **Body:** The body should explain the "what" and "why" of the change.
*   **Type:** Use a type prefix like `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

## Changes

*   Make only small changes in the agent