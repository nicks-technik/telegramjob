import sys
import os
from time import sleep
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from logger_config import logger

# from multiprocessing import process

load_dotenv()

headless: bool = os.getenv(key="ENV_HEADLESS") == "True"
logger.info(f"headless: {headless}")


# def like_and_subscribe(page):
#     """Clicks like and subscribe buttons on a YouTube video page."""

#     # Click the like button
#     like_button = page.locator(
#         'yt-button-shape[aria-label="like this video along with 1 other person"]'
#     )
#     like_button.click()

#     # Click the subscribe button
#     subscribe_button = page.locator('yt-button-shape[aria-label="Subscribe to"]')
#     subscribe_button.click()

#     logger.info(f"Liked and subscribed to the video {page}")


def youtube_login(page, email, password):
    """Logs into YouTube with the provided credentials."""
    page.goto("https://accounts.google.com/login")

    # Type Email
    page.locator('input[type="email"]').type(email)
    page.locator("#identifierNext").click()
    sleep(5)
    # Type Password
    page.wait_for_selector('input[type="password"]', state="visible")
    page.locator('input[type="password"]').type(password)
    page.locator("#passwordNext").click()
    # Wait until the login is completed
    page.wait_for_selector("#avatar-btn", state="visible")
    logger.info("Login Successful")


def process_youtube_video(url, video_id):
    """Opens a browser, logs in, likes, and subscribes."""
    with sync_playwright() as p:
        # url = "https://www.youtube.com/watch?v=" + video_id
        user_data_dir = "./tmp"  # choose a name for the directory
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            ],
        )
        # browser = p.firefox.launch_persistent_context(user_data_dir, headless=False)
        page = browser.new_page()

        try:
            # youtube_login(page, YOUTUBE_EMAIL, YOUTUBE_PASSWORD)
            page.goto(url)
            sleep(1)
            # like_and_subscribe(page)
            page.screenshot(path="./png/" + video_id + ".png")
            logger.warning(f"Screenshot saved for video ID: {video_id}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            # sleep(10)
            browser.close()


def main() -> None:
    """
    Main function to process a YouTube video.

    This function expects two command-line arguments: a video URL and a video ID.
    If the number of arguments is incorrect, it prints a usage message and exits.

    Usage:
        python playwrightpart.py <video_url> <video_id>

    Args:
        None

    Returns:
        None
    """
    if len(sys.argv) != 3:
        logger.error("Usage: python playwrightpart.py <video_url> <video_id>")
        sys.exit(1)

    video_url = sys.argv[1]
    video_id = sys.argv[2]
    process_youtube_video(video_url, video_id)


if __name__ == "__main__":

    YOUTUBE_EMAIL = os.getenv(key="ENV_YOUTUBE_EMAIL")
    YOUTUBE_PASSWORD = os.getenv(key="ENV_YOUTUBE_PASSWORD")

    # logging.basicConfig(
    #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #     level=logging.INFO,
    # )

    main()
