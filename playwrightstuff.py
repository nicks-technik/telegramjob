"""
This module contains the PlaywrightBrowser class which is used to interact with web pages.
"""

import os

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from config import Config
from logger_config import logger

headless: bool = Config.HEADLESS
logger.info(f"headless: {headless}")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/119.0.0.0 Safari/537.36"
)


class PlaywrightBrowser:
    """A class to manage a Playwright browser instance."""

    def __init__(self):
        """Initializes the PlaywrightBrowser instance."""
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    async def launch(self):
        """Launches the browser and creates a new page."""
        self.playwright = await async_playwright().start()
        storage_path = "youtube_state.json"

        storage_state = storage_path if os.path.exists(storage_path) else None
        if storage_state:
            logger.info(f"Loaded storage state from {storage_path}")

        self.browser = await self.playwright.chromium.launch(
            headless=Config.HEADLESS,
            args=[
                "--disable-blink-features=AutomationControlled",
                f"--user-agent={USER_AGENT}",
            ],
        )
        self.context = await self.browser.new_context(storage_state=storage_state)
        self.page = await self.context.new_page()

    async def close(self):
        """Closes the browser and the Playwright instance."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def take_screenshot(self, url: str, filename: str) -> None:
        """Takes a screenshot of a URL and saves it to the png directory.

        Args:
            url (str): The URL to take a screenshot of.
            filename (str): The desired filename for the screenshot (e.g., "YYMMDD_id.png").
        """
        if not self.page:
            await self.launch()  # Ensure browser and page are launched if not already
        await self.page.goto(url, timeout=60000)
        await self.page.screenshot(path=f"./png/{filename}")
        logger.info(f"Screenshot saved to ./png/{filename}")


# uv run python3 playwrightstuff.py
# creates a youtube_state.json if it is not existing
if __name__ == "__main__":
    storage_path = "youtube_state.json"
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                f"--user-agent={USER_AGENT}",
            ],
        )
        if os.path.exists(storage_path):
            context = browser.new_context(storage_state=storage_path)
            print(f"Loaded storage state from {storage_path}")
        else:
            context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.youtube.com")
        if not os.path.exists(storage_path):
            input("Please log in to YouTube and then press Enter to continue...")
            context.storage_state(path=storage_path)
            print(f"Storage state saved to {storage_path}")
        browser.close()