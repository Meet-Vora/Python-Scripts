# Get a playlist by a user and get every video
# Convert the video to mp3
# Download the mp3 to a specified folder with the same name as the playlist

from youtube_dl import YoutubeDL
import os
import math
import json
import requests
from api_key import API_KEY

BASE_API_URL = "https://www.googleapis.com/youtube/v3/playlistItems?"

# Get this from user in command line? Perhaps just ask them for
# the entire link of the playlist, then just parse it for the ID
PLAYLIST_IDS = ["PLSdiGGfcvClzm47L3dgWDpu8wsFNNAmnN"]

# My channel ID. Can ask for user's channel link in the command prompt,
# then parse it
# CHANNEL_ID = "UC0YQO0tWlYxYXEmHFPIuiAQ"
CHANNEL_ID = "UCBJycsmduvYEL83R_U4JriQ"


def downloadYoutubePlaylist():
    """
    Downloads the videos in the specified playlist in .mp3 format onto the local machine.  
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    videos = ["TpigJNeY3RU", "mCxmPNGtuWQ"]
    # ydl_opts = {}
    ydl = YoutubeDL(ydl_opts)
    ydl.download(videos)
    # print(ydl_opts)
    # base_url = BASE_API_URL + \
    #     "key={}&playlistId={}&part=snippet,id".format(
    #         API_KEY, "PLSdiGGfcvClzm47L3dgWDpu8wsFNNAmnN")
    # # print(url)
    # # print(response.json())
    # response = requests.get(base_url)
    # # num_pages = math.ceil(response.json()[
    # #                       "pageInfo"]["totalResults"]/response.json()["pageInfo"]["resultsPerPage"])

    # next_page = True
    # while next_page:
    #     data = response.json()
    #     for video in data["items"]:
    #         videoId = data["snippet"]["resourceId"]["videoId"]
    #         # convert it to mp3 here, with the title of the video as the name of the file

    #     if "nextPageToken" not in data:
    #         next_page = False


downloadYoutubePlaylist()
