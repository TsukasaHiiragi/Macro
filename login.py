from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import re
import local
import time

class MyActions:
    def __init__(self, driver):
        self.actions = ActionChains(driver)
        self.actions.move_by_offset(0,0)
        self.cx, self.cy = 0, 0

    def click(self, c, offset):
        x, y = c
        x = int((x - offset)/900*884)
        y = int(y/900*884-20)
        self.actions.move_by_offset(x - self.cx, y - self.cy).click().pause(3)
        self.cx, self.cy = x, y

    def perform(self):
        self.actions.perform()

chromedriver_path = local.driver_path
chromium_path = local.chrome_path

coord = [
    (2255, 370),
    (2447, 418),
    (2315, 368),
    (2836, 276),
]

for id in range(61, 73):
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    options.add_argument("--app=https://pc-play.games.dmm.co.jp/play/kamipror/")
    options.add_argument(f"--user-data-dir=C:/chrominum{id:0=2d}")
    options.add_argument("--window-size=900,1050")
    options.add_argument("--window-position=2000,0")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-default-browser-check")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver1 = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    actions = MyActions(driver1)

    time.sleep(3)

    for c in coord:
        actions.click(c, 2000)
    # actions.actions.pause(3).key_down(Keys.CONTROL)
    # for _ in range(5):
    #     actions.actions.send_keys(Keys.SUBTRACT).pause(1)
    # actions.actions.key_up(Keys.CONTROL)
    actions.perform()
    
    time.sleep(5)

    driver1.quit()
