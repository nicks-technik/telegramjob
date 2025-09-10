import os
import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


class YouTubeAPI:
    def __init__(self, client_secrets_file, scopes):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.youtube = self.get_authenticated_service()

    def get_authenticated_service(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes
        )
        credentials = flow.run_local_server()
        return googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
        )

    def get_video_id(self, url):
        """Parse video ID from a YouTube URL."""
        video_id_match = re.search(r"(?<=v=)[^&#]+", url)
        if not video_id_match:
            video_id_match = re.search(r"(?<=be/)[^&#]+", url)
        return video_id_match.group(0) if video_id_match else None

    def like_video(self, video_id):
        """Like a YouTube video."""
        if not video_id:
            print("Invalid video ID")
            return
        try:
            self.youtube.videos().rate(id=video_id, rating="like").execute()
            print(f"Liked video: {video_id}")
        except googleapiclient.errors.HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")

    def get_channel_id_from_video(self, video_id):
        """Get the channel ID from a video ID."""
        if not video_id:
            print("Invalid video ID")
            return None
        try:
            response = self.youtube.videos().list(part="snippet", id=video_id).execute()
            if response["items"]:
                return response["items"][0]["snippet"]["channelId"]
        except googleapiclient.errors.HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None

    def subscribe_to_channel(self, channel_id):
        """Subscribe to a YouTube channel."""
        if not channel_id:
            print("Invalid channel ID")
            return
        try:
            self.youtube.subscriptions().insert(
                part="snippet",
                body={
                    "snippet": {
                        "resourceId": {
                            "kind": "youtube#channel",
                            "channelId": channel_id,
                        }
                    }
                },
            ).execute()
            print(f"Subscribed to channel: {channel_id}")
        except googleapiclient.errors.HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")


# Example usage:
if __name__ == "__main__":
    # This should be stored securely and not hardcoded
    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    youtube_api = YouTubeAPI(CLIENT_SECRETS_FILE, SCOPES)

    # Example URL
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = youtube_api.get_video_id(video_url)

    if video_id:
        youtube_api.like_video(video_id)
        channel_id = youtube_api.get_channel_id_from_video(video_id)
        if channel_id:
            youtube_api.subscribe_to_channel(channel_id)
