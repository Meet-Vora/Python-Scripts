from pprint import pprint

import time
import requests
from bs4 import BeautifulSoup
# from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


# go to epic games store website where they list all the free games
# Get a list of all the free games available
# Click on each one, and then grab them for free

BASE_URL = "https://www.epicgames.com"
FREEGAME_URL_EXTENSION = "/store/en-US/free-games"
CHROME_DRIVER_PATH = "./chromedriver_linux"
# CHROME_DRIVER_PATH = "./chromedriver_windows"
CLASSNAMES = ["css-1oymjns-CardGridDesktopPortrait__cardWrapperDesktop",
              "css-1qv6lea-CardGridDesktopLandscape__cardWrapperDesktop",
              "css-1adx3p4-BrowseGrid-styles__card"]
CONSENT_TEXT = "This game contains mature content recommended only for ages 18+"


def claim_games(game_link):
    driver = setup_driver(game_link)

    # Wait for elements in game link webpage to load
    time.sleep(5)

    # consent_button_xpath = "/html/body/div/div/div[4]/main/div[2]/div/div[1]/p"
    consent_paragraph_xpath = "//*[contains(text(), '{0}')]".format(
        CONSENT_TEXT)
    consent_button_xpath = "/html/body/div/div/div[4]/main/div[2]/div/div[2]/div/button"
    consent_paragraph = None

    # claim_button_xpath = "/html/body/div/div/div[4]/main/div/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div/div/div[3]/div"
    # claim_button_xpath = "/html/body/div[1]/div/div[4]/main/div/div/div[2]/div/div[2]/div[2]/div/div/div[3]" \
    #     "/div/div/div/div[3]/div/button"
    claim_button_xpath = "//button[contains(., 'Get')]"
    claim_button_text_xpath = claim_button_xpath + "/span/span"
    claim_button_text = None

    placeorder_button_expath = "/html/body/div[3]/div/div/div[4]/div/div[4]/div[1]/div[2]/div[5]/div/div/button"

    try:
        consent_paragraph = driver.find_element_by_xpath(
            consent_paragraph_xpath)
        if consent_paragraph is not None:
            click_element(driver, consent_button_xpath)

    except NoSuchElementException:
        print("No consent button")

    click_element(driver, claim_button_xpath)
    click_element(driver, placeorder_button_expath)

    # if driver.find_element_by_xpath("/html/body/div/div/div[4]/main/div[2]/div/div[1]/p/text()") != "":
    #     button_xpath = "/html/body/div/div/div[4]/main/div[2]/div/div[2]/div/button"

    # try:
    #     claim_button_text = driver.find_element_by_xpath(
    #         claim_button_text_xpath)
    #     # print("BUTTON TEXT:", claim_button_text.text)
    #     if claim_button_text.text.lower() == "get":
    #         click_element(driver, claim_button_xpath)
    #         click_element(driver, placeorder_button_expath)

    # except NoSuchElementException:
    #     print("Button is not get button, or place order button doesn't work")
    # claim_button = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, claim_button_xpath)))
    # claim_button.click()
    # # print("clicked")
    # time.sleep(15)
    driver.quit()

    print("Got game")
    print("=====================")

    # game_div.click()
    # burner = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, CLASSNAMES[0])))


def click_element(driver, xpath):
    # wait = WebDriverWait(driver, 30, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException,
    #    ElementNotSelectableException])
    print("XPATH:", xpath)
    element = None
    try:
        # element = wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, xpath)))
        element = driver.find_element_by_xpath(xpath)
        if element is not None:
            element.click()
            time.sleep(3)
    except NoSuchElementException:
        print("DIDN'T WORK")


def logged_in(driver, login_xpath):
    logged_in = False

    try:
        login_button = driver.find_element_by_xpath(login_xpath)
    except NoSuchElementException:
        logged_in = True

    return logged_in


def get_game_links():
    driver = setup_driver()
    time.sleep(2)
    login_xpath = "//a[@title = 'Sign in']"

    if logged_in(driver, login_xpath):
        game_divs, game_links = [], []
        for className in CLASSNAMES:
            game_divs += driver.find_elements_by_class_name(className)

        for game_div in game_divs:
            soup = BeautifulSoup(game_div.get_attribute(
                'innerHTML'), "html.parser")
            game_links += [BASE_URL + soup.find('a')['href']]

        driver.quit()

        for game_link in game_links:
            claim_games(game_link)
        print("Claimed all games!")
    else:
        click_element(click_element(driver, login_xpath))
    # for elem in games:
    #     # elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, className)))
    #     elem.click()
    #     # button_class = "css-zc5dwj-Button-styles__main"
    #     button_class = "css-zc5dwj-Button-styles__main"
    #     button_xpath = "/html/body/div/div/div[4]/main/div/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div/div/div[3]/div"

    #     button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    #     button.click()
    #     print("done")
    #     driver.quit()

    # button_class = "css-14i612r-PurchaseButton-styles__ctaButtons"
    # button_xpath = "/html/body/div/div/div[4]/main/div/div/div[2]/div/div[2]/div[4]/div/div/div/div[3]/div/button"
    # driver.implicitly_wait(45)
    # button = driver.find_elements_by_xpath(button_xpath)[0]
    # button = WebDriverWait(driver, 45).until(find(driver, button_xpath))
    # print("done waiting")
    # print(button_xpath)
    # # driver.implicitly_wait(15)
    # print("waiting...")
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()


# def find(driver, className):
#     element = driver.find_element_by_xpath(className)
#     if element:
#         return element
#     else:
#         return False
# element = WebDriverWait(driver, secs).until(find)

    # test_class = "css-1oymjns-CardGridDesktopPortrait__cardWrapperDesktop"
    # elem = driver.find_elements_by_class_name(test_class)
    # print(elem)
    # elem.click()
    # # js = "document.getElementById('page_size').options[1].text = '100';"
    # # driver.execute_script(js)
    # # driver.find_element_by_class_name(test_class)
    # # driver.implicitly_wait(15)

    # response = requests.get(url)
    # # print(url, response.status_code)
    # # tree = html.fromstring(response.content)
    # # testing = tree.xpath("/html/body/div/div/div[4]/main/div/div/div/div/div[2]/div[2]/div/div/section/div")
    # # pprint(testing[0].__dict__)
    # soup = BeautifulSoup(response.content, "html.parser")
    # # soup = BeautifulSoup(response.content, "lxml")
    # free_games = []
    # # for className in CLASSNAMES:
    # # classes = soup.find(class_=CLASSNAMES[0])
    # classes = soup.find('div', class_="css-1oymjns-CardGridDesktopPortrait__cardWrapperDesktop")
    # # [print(x,"\n") for x in classes]
    # # print(len(classes))

    # with open("page.html", "w+") as file:
    #     file.write(soup.prettify())


def setup_driver(url=BASE_URL + FREEGAME_URL_EXTENSION):
    """
    Instantiates a driver for Chrome or Brave that opens the browser.

    Retuns:
    webdriver instance
    """
    # url = BASE_URL + "/store/en-US/free-games"
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-data-dir={}".format(".config/google-chrome"))

    ##### UNCOMMENT NEXT TWO LINES TO USE BRAVE BROWSER #####
    # brave_path = "/usr/bin/brave-browser"
    # options.binary_location = brave_path

    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, chrome_options=options)
    driver.get(url)
    print(url)
    return driver


def test():
    xpath = "//button[contains(., 'Get')]"
    driver = setup_driver(
        "https://www.epicgames.com/store/en-US/product/paladins/home")
    click_element(driver, xpath)


# driver = setup_driver()
# driver.get(BASE_URL)
get_game_links()
# test()
