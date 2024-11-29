import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

import local

def is_chromium_running(id):
    try:
        response = requests.get(f"http://127.0.0.1:92{id:0=2d}/json/version", timeout=2)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
    except requests.Timeout:
        pass
    return False

def activate_driver(id):
    chromedriver_path = local.driver_path
    options = webdriver.ChromeOptions()
    options.debugger_address = f"127.0.0.1:92{id:0=2d}"
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
    actions = ActionChains(driver)
    actions.move_by_offset(0, 0)
    return driver, actions

def apply_css(driver):
    css = """
    body {
        overflow: hidden;
    }
    div.dmm-ntgnavi {
        display: none;
    }
    div#leftnavi {
        display: none;
    }
    div#main-ntg {
        text-align: left;
        margin-top: -28px;
        margin-left: -160px !important;
    }
    """
    
    driver.execute_script(f"""
        const style = document.createElement('style');
        style.type = 'text/css';
        style.appendChild(document.createTextNode(`{css}`));
        document.head.appendChild(style);
    """)