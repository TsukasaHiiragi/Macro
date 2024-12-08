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
        self.actions.move_by_offset(x - self.cx, y - self.cy).click().pause(1.5)
        self.cx, self.cy = x, y

    def perform(self):
        self.actions.perform()

chromedriver_path = local.driver_path
chromium_path = local.chrome_path

options = webdriver.ChromeOptions()
options.binary_location = chromium_path
options.add_argument("--app=https://m.kuku.lu/recv.php")
options.add_argument("--user-data-dir=C:/master")
options.add_argument("--window-size=900,1050")
options.add_argument("--window-position=2900,0")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--no-default-browser-check")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
actions = MyActions(driver)
time.sleep(3)

password = 'ahg34icb29ih4h'

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(password + '\n')

for id in range(13,25):
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    options.add_argument("--app=https://accounts.dmm.co.jp/welcome/signup/email/=/channel=games/back_url=DRVESRUMTh1IAENLXFgHW08CV1tVSkpdDw8ZBV1LXUBKEUJWAF8NVxcXVF9aRRIYEg5fRg9bBVoJPUIUXlhzYjMkY2szezVaCQNzfktSN3UGJmFRSHUybwkHYh5jMg__?auth_method_type=email")
    options.add_argument(f"--user-data-dir=C:/chrominum{id:0=2d}")
    options.add_argument("--window-size=900,1050")
    options.add_argument("--window-position=2000,0")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-default-browser-check")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver1 = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    coord = [
        (1063, 285),
        (1305, 479),
        (1320, 598),
        (1305, 303),
        (1634, 847),
    ]

    for c in coord:
        actions.click(c, 900)
    actions.perform()
    s = pyperclip.paste()
    print(s)
    with open("output.txt", "w+", encoding="utf-8") as file:
        file.write(s + '\n')

    coord = [
        (438, 271),
        (434, 382),
        (437, 435),
    ]

    actions1 = MyActions(driver1)
    actions1.click(coord[0], 0)
    actions1.actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).pause(0.3)
    actions1.perform()

    pyperclip.copy(password)
    actions1.click(coord[1], 0)
    actions1.actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).pause(0.3)
    actions1.perform()

    actions1.click(coord[2], 0)
    actions1.perform()

    time.sleep(3)

    coord = [
        (1153, 283),
        (1290, 420),
        (1700, 286),
        (1330, 468),
        (1309, 697),
    ]

    while True:
        for c in coord:
            actions.click(c, 900)
        actions.actions.key_down(Keys.CONTROL).send_keys('a').send_keys('c').key_up(Keys.CONTROL)
        actions.perform()

        s = pyperclip.paste()
        match = re.search(r"認証コード:\s*(\d+)", s)
        if match:
            code = match.group(1)
            print(f"認証コード: {code}")
            break
        else:
            print("認証コードが見つかりません。")

    coord = [
        (438, 271),
        (434, 382),
        (437, 435),
        (740, 328),
        (284, 261),
    ]

    actions1.click((284, 261), 0)
    for chara in code:
        actions1.actions.send_keys(chara).pause(0.1)
    actions1.perform()

    time.sleep(5)

    driver1.quit()


driver.quit()
