"""
This module contains the PlaywrightBrowser class which is used to interact with web pages.
"""

from playwright.async_api import async_playwright

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
        self.page = None
        self.playwright = None

    async def launch(self):
        """Launches the browser and creates a new page."""
        self.playwright = await async_playwright().start()
        user_data_dir = "./tmp"
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir,
            headless=Config.HEADLESS,
            args=[
                "--disable-blink-features=AutomationControlled",
                f"--user-agent={USER_AGENT}",
            ],
        )
        self.page = await self.browser.new_page()

    async def close(self):
        """Closes the browser and the Playwright instance."""
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
        await self.page.goto(url)
        await self.page.screenshot(path=f"./png/{filename}")
        logger.info(f"Screenshot saved to ./png/{filename}")
