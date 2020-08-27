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
CHROME_DRIVER_PATH = "./chromedriver_linux"
CLASSNAMES = ["css-1oymjns-CardGridDesktopPortrait__cardWrapperDesktop", 
              "css-1qv6lea-CardGridDesktopLandscape__cardWrapperDesktop", 
              "css-1adx3p4-BrowseGrid-styles__card"]

def grab_free_game(game_div):
    driver = setup_driver()
    time.sleep(3)
    game_div.click()
    print("clicked")
    # burner = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, CLASSNAMES[0])))

    wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, 
            ElementNotSelectableException, NoSuchElementException])
    button_xpath = "/html/body/div/div/div[4]/main/div/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div/div/div[3]/div"
    button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    button.click()
    
    print("done1")
    driver.quit()
    print("done2")


def select_games():
    driver = setup_driver()
        # driver = setup_driver()
    # temp_classes = ["css-1oymjns-CardGridDesktopPortrait__cardWrapperDesktop"]

    game_divs = []
    for className in CLASSNAMES:
        game_divs += driver.find_elements_by_class_name(className)
        # game_divs[0].click()
        # time.sleep(4)
        # driver.quit()


    for game_div in game_divs:
        soup = BeautifulSoup(game_div.get_attribute('innerHTML'), "html.parser")
        link = BASE_URL + soup.find('a')['href']
        print(link)
        print()
        
    
    # print()

    # response = requests.get(BASE_URL)
    # soup = BeautifulSoup(response.content, "html.parser")
    

    # game_divs= []
    # for className in temp_classes:
    #     game_divs += soup.findAll("div", class_=className)
    
        
    # for game_div in game_divs:
    #     print(game_div)
    #     print()
        # game_div.click()
        # print("clicked")
        # time.sleep(3)
        # driver.get(BASE_URL)
        # time.sleep(3)
        # grab_free_game(game_div)




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


def find(driver, className):
    element = driver.find_element_by_xpath(className)
    if element:
        return element
    else:
        return False
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


def setup_driver():
    """
    Instantiates a driver for Chrome or Brave that opens the browser.

    Retuns:
    webdriver instance
    """
    url = BASE_URL + "/store/en-US/free-games"
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-data-dir={}".format(".config/google-chrome"))

    ##### UNCOMMENT NEXT TWO LINES TO USE BRAVE BROWSER #####
    # brave_path = "/usr/bin/brave-browser"
    # options.binary_location = brave_path

    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, chrome_options=options)
    driver.get(url)
    return driver

# driver = setup_driver()
# driver.get(BASE_URL)
select_games()
