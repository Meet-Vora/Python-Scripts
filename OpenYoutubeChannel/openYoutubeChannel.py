from selenium import webdriver
import requests
import time
import json
from api_key import API_KEY

BASE_VIDEO_URL = "https://www.youtube.com/watch?v="
BASE_API_URL = "https://www.googleapis.com/youtube/v3/search?"

# LEMMiNO channel
CHANNEL_ID = "UCRcgy6GzDeccI7dkbbBna3Q"


def look_for_new_video():
    """
    Opens YouTube when youtuber posts a new video. Currently set to LEMMiNO's channel. 
    Checks Youtube approximately every 7 minutes, which meets the 100 searches per day
    YouTube API quota in around 12 hours.
    """
    url = BASE_API_URL + \
        "key={}&channelId={}&part=snippet,id&order=date&maxResults=1".format(
            API_KEY, CHANNEL_ID)
    response = requests.get(url)
    vidID = response.json()["items"][0]["id"]["videoId"]

    new_video = False
    with open("videoid.json", "r") as json_file:
        data = json.load(json_file)
        if data["videoId"] != vidID:

            driver_path = "/home/meetv/Downloads/chromedriver"
            brave_path = "/usr/bin/brave-browser"

            options = webdriver.ChromeOptions()
            options.binary_location = brave_path
            # options.add_argument("--incognito") --- Incognito window

            driver = webdriver.Chrome(
                executable_path=driver_path, chrome_options=options)
            # driver = webdriver.Chrome(
            #     executable_path=driver_path)
            driver.get(BASE_VIDEO_URL + vidID)
            new_video = True

    if new_video:
        with open("videoid.json", "w") as json_file:
            data = {"videoId": vidID}
            json.dump(data, json_file)


# One lookup every 7.2 minutes to have max lookups in 12 hours per day
try:
    while True:
        look_for_new_video()
        time.sleep(432)
except KeyboardInterrupt:
    print("\nShutting down...")
