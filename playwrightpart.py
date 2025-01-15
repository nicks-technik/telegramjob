from multiprocessing import process
import os
from time import sleep
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import asyncio

load_dotenv()

YOUTUBE_EMAIL = os.getenv(key="ENV_YOUTUBE_EMAIL")
YOUTUBE_PASSWORD = os.getenv(key="ENV_YOUTUBE_PASSWORD")


def like_and_subscribe(page):
    """Clicks like and subscribe buttons on a YouTube video page."""

    # Click the like button
    like_button = page.locator(
        'yt-button-shape[aria-label="like this video along with 1 other person"]'
    )
    like_button.click()

    # Click the subscribe button
    subscribe_button = page.locator('yt-button-shape[aria-label="Subscribe to"]')
    subscribe_button.click()

    print("Liked and subscribed to the video")


def youtube_login(page, email, password):
    """Logs into YouTube with the provided credentials."""
    page.goto("https://accounts.google.com/login")

    # Type Email
    page.locator('input[type="email"]').type(email)
    page.locator("#identifierNext").click()
    sleep(4)
    # Type Password
    page.wait_for_selector('input[type="password"]', state="visible")
    page.locator('input[type="password"]').type(password)
    page.locator("#passwordNext").click()
    # Wait until the login is completed
    page.wait_for_selector("#avatar-btn", state="visible")
    print("Login Successful")


def process_youtube_video(video_id):
    """Opens a browser, logs in, likes, and subscribes."""
    with sync_playwright() as p:
        url = "https://www.youtube.com/watch?v=" + video_id
        user_data_dir = "./tmp"  # choose a name for the directory
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
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
            sleep(10)
            # like_and_subscribe(page)
            page.screenshot(path="./png/" + video_id + ".png")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # sleep(10)
            browser.close()


def main():
    process_youtube_video("3JZ_D3ELwOQ")
    # process_youtube_video("https://www.youtube.com/watch?v=3JZ_D3ELwOQ")


if __name__ == "__main__":
    # asyncio.run(main())
    main()
