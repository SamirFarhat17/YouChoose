import httplib2
import requests
import sys
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

def get_videos(channel_name, CLIENT_SECRETS_FILE):
    """Get videos uploaded to the specified channel"""

    video_list = []

    MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

    YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE,
                                   scope=YOUTUBE_READONLY_SCOPE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    http=credentials.authorize(httplib2.Http()))

    # Retrieve the contentDetails part of the channel resource for the
    # authenticated user's channel.
    channels_response = youtube.channels().list(
        forUsername=channel_name,
        part="contentDetails"
    ).execute()

    for channel in channels_response["items"]:
        # From the API response, extract the playlist ID that identifies the list
        # of videos uploaded to the authenticated user's channel.
        uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

        # Retrieve the list of videos uploaded to the authenticated user's channel.
        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=uploads_list_id,
            part="snippet",
            maxResults=50
        )

        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            # Print information about each video.
            for playlist_item in playlistitems_list_response["items"]:
                title = playlist_item["snippet"]["title"]
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                video_list.append((title, video_id, 'https://img.youtube.com/vi/' + video_id + '/0.jpg'))

            playlistitems_list_request = youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)

    return(video_list)


def get_comments(video_id, CLIENT_SECRETS_FILE):
    """Retrieve comments from a video specified by given ID"""

