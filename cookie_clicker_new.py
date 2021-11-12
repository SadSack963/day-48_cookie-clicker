from selenium import webdriver  # pip install selenium==4.0.0
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time

# Selenium 4.0.0. changes
# =======================
# driver.find_element_by_id(), etc are deprecated
# Use driver.find_element(By.ID, value) instead
from selenium.webdriver.common.by import By


def webdriver_init(browser: str = "chrome"):
    b = browser.lower()
    if b == "chrome":
        from selenium.webdriver.chrome.service import Service as ChromeService
        chrome_driver_path = "E:/Python/WebDriver/chromedriver.exe"
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option("useAutomationExtension", False)
        service = ChromeService(executable_path=chrome_driver_path)
        return webdriver.Chrome(service=service)  # , options=options)
    elif b == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        firefox_driver_path = "E:/Python/WebDriver/geckodriver.exe"
        # options = webdriver.FirefoxOptions()
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option("useAutomationExtension", False)
        service = FirefoxService(executable_path=firefox_driver_path)
        return webdriver.Firefox(service=service)  # , options=options)
    elif b == "opera":
        print("Selenium 4 does not support Opera.")
        exit()
    else:
        print(f"Invalid browser \"{browser}\".\nOnly Chrome, Firefox and Opera are configured.")
        exit()


driver = webdriver_init()
# driver = webdriver_init("firefox")
driver.get("https://orteil.dashnet.org/cookieclicker/")

# item_names = [   # ids altered
#     "Cursor",
#     "Grandma",
#     "Factory",
#     "Mine",
#     "Shipment",
#     "Alchemy lab",
#     "Portal",
#     "Time machine",
#     "Elder Pledge"
# ]
item_names = [
    "product0",
    "product1",
    "product2",
    "product3",
    "product4",
    "product5",
    "product6",
    "product7",
    "product8",
    "product9",
    "product10",
    "product11",
    "product12",
    "product13",
    "product14",
    "product15",
    "product16",
    "product17",
]

items = [None] * len(item_names)

# Find the Cookie
# cookie = driver.find_element_by_id("cookie")  # id altered
cookie = driver.find_element(by=By.ID, value="bigCookie")


def get_cookies_total():
    while True:
        try:
            # cookies = driver.find_element_by_id("cookiea")
            cookies = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[15]/div[4]')
            print(cookies.text)
            break
        except NoSuchElementException:
            pass


def click_cookie(seconds):
    stop_time = time.time_ns() + seconds * 10**9
    # count = 0
    while stop_time > time.time_ns():
        # count += 1
        cookie.click()  # achieves approximately 45-50 clicks per second
    # print(f'{count / seconds} clicks per second')


def buy_most_expensive_item(click_sec):
    # See https://www.selenium.dev/exceptions/#stale_element_reference
    # The JavaScript replaces items with a more expensive one when clicked
    # Recreate the list of items to prevent StaleElementReferenceException
    for i in range(len(items)):
        # items[i] = driver.find_element_by_id("buy" + item_names[i])
        items[i] = driver.find_element(by=By.ID, value=item_names[i])
        # print(items[i].text)
        # Output:
        #     Rolling pin
        #     15
        #     Oven
        #     100
        #     ???
        #     1,100
        #     ???
        #     12,000
        # print(items[i].get_attribute("class"))
        # Output:
        #     product unlocked enabled
        #     product unlocked enabled
        #     product locked disabled
        #     product locked disabled
        #     product locked disabled toggledOff
        #     product locked disabled toggledOff

    for i in range(len(items) - 1, -1, -1):
        # if items[i].get_attribute("class") == "":  # class altered
        if items[i].get_attribute("class") == "product unlocked enabled":
            items[i].click()
            click_sec *= 1.4
            break
    return click_sec


# Accept cookies
time.sleep(3)
accept = driver.find_element(by=By.CSS_SELECTOR, value='a.cc_btn_accept_all')  # new cookie banner
accept.click()


run_time = time.time_ns() + 3600 * 10**9  # 60 minute run
delay = 1.0  # Initial seconds
while run_time > time.time_ns():
    print(f'Waiting {delay:.3f} seconds before buying the most expensive item')
    click_cookie(seconds=delay)
    # get_cookies_total()  # Not possible. The script is constantly updating the element.
    delay = buy_most_expensive_item(delay)
driver.get_screenshot_as_file("screenshot.png")
