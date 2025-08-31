"""
This module contains the PlaywrightBrowser class which is used to interact with web pages.
"""

import os
import argparse
import asyncio
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


if __name__ == "__main__":

    async def generate_auth_file():
        browser_instance = PlaywrightBrowser()
        try:
            # Load environment variables and initialize config
            parser = argparse.ArgumentParser(
                description="Generate Playwright auth file."
            )
            parser.add_argument(
                "--env-file",
                type=str,
                default=".env",
                help="Path to the .env file to load (default: .env)",
            )
            args = parser.parse_args()
            env_file_path = os.path.abspath(args.env_file)
            Config.load_env_file(env_file_path)
            Config.init_config()

            # Launch browser in headful mode for manual login
            browser_instance.playwright = await async_playwright().start()
            browser_instance.browser = (
                await browser_instance.playwright.chromium.launch_persistent_context(
                    "./tmp",
                    headless=False,  # Force headful for manual login
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        f"--user-agent={USER_AGENT}",
                    ],
                )
            )
            browser_instance.page = await browser_instance.browser.new_page()

            logger.info(
                f"Please log in to YouTube/Google in the opened browser window. Auth file will be saved to: {Config.AUTH_FILE}"
            )
            logger.info("Press Enter in this console after you have logged in.")

            # Navigate to YouTube to prompt login
            await browser_instance.page.goto("https://www.youtube.com")

            input("Press Enter to continue...")  # Wait for user input
            await browser_instance.browser.storage_state(path=Config.AUTH_FILE)
            logger.info(f"Browser storage state saved to {Config.AUTH_FILE}")

        except Exception as e:
            logger.error(f"An error occurred during auth file generation: {e}")
        finally:
            if browser_instance.browser:
                await browser_instance.browser.close()
            if browser_instance.playwright:
                await browser_instance.playwright.stop()

    asyncio.run(generate_auth_file())
