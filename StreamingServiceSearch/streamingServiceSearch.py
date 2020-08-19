import argparse
import pickle
import re
import sys
import traceback

import pyinputplus as pyip
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


##### ADD/REMOVE SUBSCRIPTION SERVICES ON LINES 20-23 TO CHANGE THE ONES #####
##### THE PROGRAM OPENS. IF YOU REMOVE AN ENTIRE LIST, REMOVE THE LIST #####
##### NAME ON LINE 43 AS WELL. #####

### Can also change the order of the streaming services in ###
### each list to change the order in which they are opened ###
SUBSCRIPTION_LIST = ["Netflix", "Hulu", "HBO NOW", "Prime Video"]
FREE_SERVICES = ["Funimation", "Tubi TV", "Crunchyroll", "VUDU"]
CABLE_LIST = ["HBO MAX"]
BUY = ["YouTube"]

CHROME_DRIVER_PATH = "./chromedriver"
FIREFOX_DRIVER_PATH = "./geckodriver"

BASE_URL = "https://decider.com/"


def open_streaming_service(vid_type, name):
    """
    Locates and opens the specified movie in an online streaming service in 
    Chrome or Firefox.

    Parameters:
    vid_type (String): specifies if the video is a movie or show. Defaults to movie
    name (String): title of show/movie to search for
    """

    ###### CHANGE SERVICES HERE IF YOU ADD/REMOVE LISTS ABOVE ######
    ### Can also change the order of the lists to change the search order ###
    all_services = SUBSCRIPTION_LIST + FREE_SERVICES + BUY + CABLE_LIST

    url_name = name.lower().replace(" ", "-")
    url = BASE_URL + vid_type + "/" + url_name

    response = requests.get(url)
    if response.status_code not in range(200, 299):
        raise ValueError("Cannot find " + vid_type +
                         " with title " + "\"" + name + "\".")

    soup = BeautifulSoup(response.content, 'html.parser')
    streaming_services = soup.find(
        "ul", class_="reelgood-platforms").find_all("li")

    service_list = all_services[:]
    msg = "Sorry, could not open " + "\"" + \
        name + "\"" + " in any of your available streaming services."
    while True:
        driver = setup_driver()
        service_used, video_link = choose_service(
            service_list, streaming_services)
        if service_used is None:
            print(msg)
            break

        launch_browser(driver, video_link, service_used, name)

        ans = pyip.inputYesNo("Do you want to open " + "\"" +
                              name + "\"" + " in another service, if available? [yes/no] ")
        if ans == "no":
            print("\nShutting down...")
            break

        driver.quit()
        service_list = service_list[service_list.index(
            service_used) + 1:]
        msg = "\nSorry, could not open " + "\"" + \
            name + "\"" + " in any other streaming services."


def launch_browser(driver, video_link, service_used, name):
    print("\nOpening " + "\"" +
          name + "\"" + " in " + service_used + "...")
    driver.get(video_link)


def choose_service(service_list, streaming_services):
    for sub in service_list:
        lower_sub = sub.lower()
        for li in streaming_services:
            if li.has_attr("class"):
                data_go_event = li.a["data-ga-event"].lower()
                if data_go_event.find(lower_sub) != -1:
                    video_link = li.a["href"]
                    return sub, video_link
    return None, None


def setup_driver():

    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-data-dir={}".format(".config/google-chrome/Default"))

    ##### ALTERNATE BETWEEN THE NEXT TWO CODE BLOCKS #####
    ##### TO SWAP BETWEEN CHROME AND FIREFOX #####
    # driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)

    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, chrome_options=options)
    # driver.get(video_link)
    return driver
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
    parser.add_argument("-d", "--debug", action="store_true")

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
    return args


def exception_handler(exception_type, exception, traceback):
    print("\nERROR: {}".format(exception))


if __name__ == "__main__":
    try:
        args = setup_cmd_interface()

        if not args.debug:
            sys.excepthook = exception_handler

        vid_type = 'movie'
        if args.show or args.type == 'show':
            vid_type = 'show'

        open_streaming_service(vid_type, args.name)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except WebDriverException:
        print("\nERROR: Cannot run multiple instances of Chrome at once. "
              "Please close all your browsers launched with this program before running the program again.")
