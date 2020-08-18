import re
import sys
import pickle
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import argparse

# get show/movie from command line argument
# make http request to decider website
# save hyperlink to the streaming service
# open link in chrome/firefox
# put help command for the program
# make a config file that sees what browser to use
# after making the app executable, can make sure he adds it to path and then
#       can see all the options for usage with configuring the browser
# All functionality with command line:
#   1. adding/removing/listing all streaming services
#   2. changing default browser
#   3. can specify browser with command line arguments
#   4. help function with command line

TEST_SHOW = "Game of Thrones"
BASE_URL = "https://decider.com/"

SUBSCRIPTION_LIST = ["Netflix", "Hulu", "HBO NOW", "Prime Video"]
CABLE_LIST = ["HBO MAX"]
FREE_SERVICES = ["Funimation", "Tubi TV", "Crunchyroll", "VUDU"]
BUY = []

CHROME_DRIVER_PATH = "./chromedriver"
FIREFOX_DRIVER_PATH = "./geckodriver"


# def open_streaming_service(show_type, show_name):
def find_streaming_service(vid_type, name):

    name = name.lower().replace(" ", "-")
    url = BASE_URL + vid_type + "/" + name

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    streaming_services = soup.find(
        "ul", class_="reelgood-platforms").find_all("li")

    # ignores the "more options" element from the list
    paid_service = False
    for li in streaming_services[:-1]:
        data_go_event = li.a["data-ga-event"]
        for sub in SUBSCRIPTION_LIST:
            if not paid_service and data_go_event.find(sub) != -1:
                video_link = li.a["href"]
                paid_service = True

    if paid_service:
        # go to link in browser
        launch_browser(video_link)
        pass

    else:
        # check free services
        pass

    # if no free services, then return None

    # with open("test.txt", "w") as file:
    #     file.write(str(streaming_services))


def launch_browser(video_hyperlink):
    # driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)

    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-data-dir={}".format(".config/google-chrome/Default"))
    # brave_path = "/usr/bin/brave-browser"
    # options.binary_location = brave_path

    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, chrome_options=options)

    driver.get(video_hyperlink)
    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    # driver.delete_all_cookies()

    # cookies = pickle.load(open("cookies.pkl", "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    # driver.quit()

    # driver = webdriver.Firefox()
    # driver.get(video_hyperlink)


def setup_cmd_interface():
    description = "Description: This program automatically finds the user-specified show or " \
        "movie on their subscribed or free streaming services, and opens it in " \
        "a browser, ready to play."

    test = "Enter \"movie\" or \"show\" to specify whether you would like to " \
        " watch a show or movie, and enter its name in quotes. The program will " \
        "automatically find a streaming service it is available on, and open " \
        "it in a browser."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-n", "--name", required=True)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--type", choices=["show", "movie"])
    group.add_argument("-s", "--show",  action="store_true")
    group.add_argument("-m", "--movie",  action="store_true")

    # should add config for list of streaming services/cable owned, browser to use (chrome or firefox)

    # parser.add_argument('-b', "--base", type=int,
    #                     help="defines the base value")
    # parser.add_argument("-s", "--show", action="store_true")

    # parser.add_argument("name")
    # parser.add_argument("videoType", default="movie", help="specify video type as show or movie. "
    # "Defaults to movie if unspecified")

    # parser.add_argument("movie/show", help="specifies video type")
    # parser.add_argument("show", help="specify video type as show")
    # parser.add_argument("movie", help="specify video type as movie")
    # parser.add_argument("<name>",
    #                     help="Name of the movie/show. Replace <name> with the name in quotes")
    args = parser.parse_args()
    print(args)
    return args


if __name__ == "__main__":
    args = setup_cmd_interface()
    vid_type = 'movie'

    if args.show or args.type == 'show':
        vid_type = 'show'

    find_streaming_service(vid_type, args.name)

    # if type != None and type != 'movie' and type != 'show':
    #     throw error
    # if not movie and not show and type == None or type != 'show' or type != 'movie':

    # if movie, show are false, and type is None/incorrect string,
