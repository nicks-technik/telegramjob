"""
This module contains the PlaywrightBrowser class which is used to interact with web pages.
"""
from playwright.async_api import async_playwright
from logger_config import logger


from config import Config

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

    async def youtube_login(self, email, password):
        """Logs into YouTube with the provided credentials."""
        if not self.page:
            await self.launch()
        await self.page.goto("https://accounts.google.com/login")

        await self.page.locator('input[type="email"]').type(email)
        await self.page.locator("#identifierNext").click()
        await self.page.wait_for_selector('input[type="password"]', state="visible")
        await self.page.locator('input[type="password"]').type(password)
        await self.page.locator("#passwordNext").click()
        await self.page.wait_for_selector("#avatar-btn", state="visible")
        logger.info("Login Successful")

    async def process_youtube_video(self, url, video_id):
        """Opens a browser, logs in, likes, and subscribes."""
        if not self.page:
            await self.launch()
        try:
            await self.page.goto(url)
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.wait_for_load_state("networkidle")
            await self.page.screenshot(path="./png/" + video_id + ".png")
            logger.info(f"Screenshot saved for video ID: {video_id}")
        # pylint: disable=broad-exception-caught
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            await self.close()
