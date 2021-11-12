from selenium import webdriver  # pip install selenium==4.0.0
# from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
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
driver.get("https://orteil.dashnet.org/experiments/cookie/")

item_names = [
    "Cursor",
    "Grandma",
    "Factory",
    "Mine",
    "Shipment",
    "Alchemy lab",
    "Portal",
    "Time machine",
    "Elder Pledge"
]
items = [None] * len(item_names)
# cookie = driver.find_element_by_id("cookie")  # Deprecated in selenium 4.0
# NOTE: find_element will return a dictionary if you use an old webdriver.
#   https://github.com/SeleniumHQ/selenium/issues/9978
# Also, Opera is no longer supported
#   https://www.lambdatest.com/blog/what-is-deprecated-in-selenium4/
#   The native support for Opera (and PhantomJS) is removed in Selenium 4,
#   as their WebDriver implementations are no longer under development.
#   The Opera browser is based on Chromium, and users looking to test their implementation
#   on Opera can opt for testing on the Chrome browser.
cookie = driver.find_element(by=By.ID, value="cookie")
print(cookie)


def click_cookie(seconds):
    stop_time = time.time_ns() + seconds * 10**9
    count = 0
    while stop_time > time.time_ns():
        count += 1
        cookie.click()  # 216, 238, 248 clicks per second
    print(f'{count / seconds} clicks per second')


def buy_most_expensive_item():
    # See https://www.selenium.dev/exceptions/#stale_element_reference
    # The JavaScript replaces items with a more expensive one when clicked
    # Recreate the list of items to prevent StaleElementReferenceException
    for i in range(len(items)):
        items[i] = driver.find_element(by=By.ID, value="buy" + item_names[i])
    for i in range(len(items) - 1, -1, -1):
        if items[i].get_attribute("class") == "":
            items[i].click()
            break


run_time = time.time_ns() + 300 * 10**9  # 5 minute run
delay = 5.0  # Initial seconds
while run_time > time.time_ns():
    click_cookie(seconds=delay)
    buy_most_expensive_item()
driver.get_screenshot_as_file("screenshot.png")
