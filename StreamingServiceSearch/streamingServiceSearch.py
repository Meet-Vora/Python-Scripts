import argparse
# import pickle
import re
import sys
import traceback
import time
import os
import json

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
SUBSCRIPTION_LIST = ["Netflix", "Hulu", "HBO NOW", "Prime Video", "STARZ",
                     "AMC", "AMC Premiere", "fuboTV"]
FREE_SERVICES = ["Funimation", "Tubi TV", "Crunchyroll", "VUDU"]
CABLE_LIST = ["HBO MAX"]
BUY = ["YouTube", "iTunes", "Google Play", "Microsoft Store"]

CHROME_DRIVER_PATH = "../chromedriver_linux"
# CHROME_DRIVER_PATH = "../chromedriver_mac"
# CHROME_DRIVER_PATH = "../chromedriver_windows"

BASE_URL = "https://decider.com/"


def open_streaming_service(vid_type, name, chromedriver_path, browser="chrome"):
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
        driver = setup_driver(
            browser=browser, chromedriver_path=chromedriver_path)
        service_used, video_link = choose_service(
            service_list, streaming_services)
        if service_used is None:
            print(msg)
            break

        launch_browser(driver, video_link, service_used, name)

        ans = pyip.inputYesNo("Do you want to open " + "\"" +
                              name + "\"" + " in another service, if available? [yes/no] ")
        if ans == "no":
            print("\nEnjoy the " + vid_type + "!")
            break

        driver.quit()
        service_list = service_list[service_list.index(
            service_used) + 1:]
        msg = "\nSorry, could not open " + "\"" + \
            name + "\"" + " in any other streaming service."


def choose_service(service_list, streaming_services):
    """
    Finds a streaming service to use based on the ones available from the user
    and online.

    Parameters:
    service_list: list of streaming services available to the user
    streaming_services: list of services the title is available to stream on

    Returns:
    1. the name of the service used to stream the title, or None if unavailable
    2. the link to the title, or None if unavailable
    """
    for sub in service_list:
        lower_sub = sub.lower()
        for li in streaming_services:
            if li.has_attr("class"):
                data_go_event = li.a["data-ga-event"].lower()
                if data_go_event.find(lower_sub) != -1:
                    video_link = li.a["href"]
                    return sub, video_link
    return None, None


def launch_browser(driver, video_link, service_used, name):
    print("\nOpening " + "\"" +
          name + "\"" + " in " + service_used + "...")
    driver.get(video_link)


def setup_driver(browser, chromedriver_path):
    """
    Instantiates a driver for Chrome or Brave that opens the browser.

    Retuns:
    webdriver instance
    """

    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-data-dir={}".format(".config/google-chrome"))

    if browser == "brave":
        brave_path = "/usr/bin/brave-browser"
        options.binary_location = brave_path

    driver = webdriver.Chrome(
        executable_path=chromedriver_path, chrome_options=options)

    return driver


def setup_cmd_interface():
    """
    Sets up the command line interface.

    Returns:
    an object containing the arguments specified by the user
    """
    description = "Description: This program automatically finds the user-specified show or " \
        "movie on their subscribed or free streaming services, and opens it in " \
        "a browser, ready to play."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-n", "--name", required=True, help="title of the "
                        "show/movie, specified after this argument")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="prints the stack trace")

    # browser_group = parser.add_mutually_exclusive_group()
    parser.add_argument("-b", "--brave", action="store_true",
                        help="launches show in brave browser instead of defaulting to Chrome")

    parser.add_argument("-c", "--config-os", action="store_true", help="Opens a config menu that"
                        "lets you select your Operating System.")

    title_group = parser.add_mutually_exclusive_group()
    title_group.add_argument("-t", "--type", choices=["show", "movie"], help="idenitifies the type of "
                             "video, either a show or movie, specified after this argument")
    title_group.add_argument("-s", "--show",  action="store_true",
                             help="specifies video type as a show")
    title_group.add_argument("-m", "--movie",  action="store_true",
                             help="specifies video type as a movie. if [-s | -m | -t] "
                             "are unspecified, video type defaults to movie")

    # os_group = parser.add_mutually_exclusive_group()
    # os_group.add_argument("-w", "--windows")
    # os_group.add_argument()
    # os_group.add_argument()

    args = parser.parse_args()
    return args


def exception_handler(exception_type, exception, traceback):
    """
    Handles exceptions in a user-friendly format. Can be overriden to print the entire
    stack trace using the -d and --debug tags.

    Parameters:
    exception_type: type of exception
    exception: exception instance
    traceback: instance of the stack trace
    """
    print("\nERROR: {}".format(exception))


def save_os(filename, prompt):
    op_sys = pyip.inputMenu(prompt=prompt, choices=[
        "windows", "mac", "linux"], numbered=True)

    with open(filename, "w+") as outfile:
        json.dump({"operating system": op_sys}, outfile)


def get_os(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)
        return data["operating system"]


if __name__ == "__main__":
    try:
        args = setup_cmd_interface()
        dirname = os.path.dirname(__file__)
        chromedriver_path = os.path.join(dirname, "../chromedriver_")

        defaults_filename = "defaults.json"
        file_exists = os.path.isfile(defaults_filename)
        os_prompt = "\nPlease choose the Operating System you would like to switch " \
            "to:\n" if file_exists else "\nBefore you run this program, " \
            "please select your Operating System:\n"

        if args.config_os or not file_exists:
            save_os(filename=defaults_filename, prompt=os_prompt)

        chromedriver_path += get_os(filename=defaults_filename)
        browser = "chrome"
        if args.brave:
            browser = "brave"

        if not args.debug:
            sys.excepthook = exception_handler

        vid_type = 'movie'
        if args.show or args.type == 'show':
            vid_type = 'show'

        open_streaming_service(vid_type, args.name.strip(
        ), browser=browser, chromedriver_path=chromedriver_path)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except WebDriverException as e:
        msg = e.msg
        if "chromedriver" in e.msg:
            msg = "Incorrect Operating System chosen. Please reconfigure " \
                "it using the \"-c\" or \"--config-os\" token."

        if "--user-data-dir" in e.msg:
            msg = "Cannot run multiple instances of Chrome at once. " \
                "Please close all your browser tabs launched with this program " \
                "before running the program again."

        raise WebDriverException(msg=msg)
