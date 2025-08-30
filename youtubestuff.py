import os
import pickle
from typing import Optional

from google.auth.transport.requests import Request


from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from logger_config import logger

class YouTubeClient:
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self):
        self.creds = self._check_login()
        self.youtube = build(self.API_SERVICE_NAME, self.API_VERSION, credentials=self.creds)

    def _check_login(self):
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return creds

    def get_channel_id_from_video_id(self, video_id):
        """
        Gets the channel ID from the video ID.

        Args:
            video_id (str): The ID of the video.

        Returns:
            str: The ID of the channel, or None if an error occurs.
        """
        try:
            request = self.youtube.videos().list(part="snippet", id=video_id)
            response = request.execute()
            if "items" in response and len(response["items"]) > 0:
                return response["items"][0]["snippet"]["channelId"]
            else:
                logger.warning(f"Could not find channel ID for video {video_id}")
                return None
        except Exception as e:
            logger.error(f"An error occurred while getting channel id: {e}")
            return None

    def subscribe_to_channel(self, channel_id):
        """
        Subscribes to a YouTube channel using the YouTube Data API.

        Args:
            channel_id (str): The ID of the channel to subscribe to.

        Returns:
            bool: True if subscription was successful, False otherwise.
        """
        try:
            request = self.youtube.subscriptions().insert(
                part="snippet",
                body={
                    "snippet": {
                        "resourceId": {"kind": "youtube#channel", "channelId": channel_id}
                    }
                },
            )
            request.execute()
            logger.info(f"Subscribed to channel {channel_id}")
            return True
        except Exception as e:
            logger.error(f"An error occurred while subscribing to channel: {e}")
            return False

    def like_video(self, video_id):
        """
        Likes a specified video using the YouTube Data API.

        Args:
            video_id (str): The ID of the video to like.

        Returns:
            bool: True if the like operation was successful, False otherwise.
        """
        for i in range(2):
            try:
                request = self.youtube.videos().rate(id=video_id, rating="like")
                request.execute()
                logger.info(f"Video {video_id} liked.")
                return True
            except Exception as e:
                logger.error(f"An error occurred while liking video: {e}")
        return False

def extract_video_id(url) -> Optional[str]:
    """Extracts the YouTube video ID from a URL.

    Args:
        url (str): The YouTube URL.

    Returns:
        str: The extracted video ID, or None if not found.
    """
    if "youtu.be/" in url:
        try:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            return video_id
        except IndexError:
            logger.debug(f"Could not extract video id from {url}")
            return None
    elif "youtube.com/watch?v=" in url:
        try:
            video_id = url.split("youtube.com/watch?v=")[1].split("&")[0].split("?")[0]
            return video_id
        except IndexError:
            logger.debug(f"Could not extract video id from {url}")
            return None
    else:
        logger.debug(f"Could not extract video id from {url}")
        return None