import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle


def get_channel_id_from_video_id(video_id):
    """
    Gets the channel ID from the video ID.

    Args:
        video_id (str): The ID of the video.

    Returns:
        str: The ID of the channel, or None if an error occurs.
    """
    SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    try:
        youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]["snippet"]["channelId"]
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def subscribe_to_channel(channel_id):
    """
    Subscribes to a YouTube channel using the YouTube Data API.

    Args:
       channel_id (str): The ID of the channel to subscribe to.

    Returns:
       bool: True if subscription was successful, False otherwise.
    """
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    try:
        youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        request = youtube.subscriptions().insert(
            part="snippet",
            body={
                "snippet": {
                    "resourceId": {"kind": "youtube#channel", "channelId": channel_id}
                }
            },
        )
        request.execute()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def like_video(video_id):
    """
    Likes a specified video using the YouTube Data API.

    Args:
        video_id (str): The ID of the video to like.

    Returns:
        bool: True if the like operation was successful, False otherwise.
    """
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]  # Correct Scope!
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    try:
        youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        request = youtube.videos().rate(id=video_id, rating="like")
        request.execute()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
    video_to_like = "kCDUbJU99F8"  # Replace with the actual video ID
    channel_id = get_channel_id_from_video_id(video_to_like)
    if channel_id:
        if like_video(video_to_like):
            if subscribe_to_channel(channel_id):
                print(f"Successfully liked and subscribed to video: {video_to_like}")
            else:
                print(
                    f"Successfully liked video, but failed to subscribe to channel: {video_to_like}"
                )
        else:
            print(f"Failed to like video: {video_to_like}")
    else:
        print(f"Could not get the channel ID for video id: {video_to_like}")
