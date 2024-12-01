import os
import psutil
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

import local

def terminate_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)  # 子プロセスをすべて取得
        for child in children:
            print(f"終了中: 子プロセス (PID: {child.pid})")
            child.terminate()  # 子プロセスを終了
        parent.terminate()  # 親プロセスを終了
        _, alive = psutil.wait_procs([parent] + children, timeout=5)
        for proc in alive:
            print(f"強制終了中: (PID: {proc.pid})")
            proc.kill()  # 強制終了
        print("プロセスツリーを終了しました。")
    except psutil.NoSuchProcess:
        print(f"プロセス (PID: {pid}) は存在しません。")
    except Exception as e:
        print(f"エラー: {e}")

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

def close_chromium_via_debugger(id):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'chromium' in proc.info['name'] or 'chrome' in proc.info['name']:
            # デバッグポートが含まれるプロセスを特定
            if f"--remote-debugging-port=92{id:0=2d}" in ' '.join(proc.info['cmdline']):
                try:
                    print(f"終了中: {proc.info['name']} (PID: {proc.info['pid']})")
                    # terminate_process_tree(proc.info['pid'])
                    os.kill(proc.info['pid'], 9)  # 強制終了
                    print("Chromiumを強制終了しました")
                except Exception as e:
                    print(f"プロセス終了に失敗: {e}")
    print("該当するChromiumプロセスが見つかりませんでした")

def activate_driver(id):
    chromedriver_path = local.driver_path
    options = webdriver.ChromeOptions()
    options.debugger_address = f"127.0.0.1:92{id:0=2d}"
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
    driver.implicitly_wait(0)
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