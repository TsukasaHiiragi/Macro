from time import sleep
import pyautogui
from pynput import mouse

class Monitor:
    def __init__(self):
        self.x,self.y = None,None

    def start(self):
        with mouse.Listener(on_click=self.click) as mouse_listener:
            mouse_listener.join()

    def click(self, x, y, button, pressed):
        if button.name == 'left':
            self.x,self.y = x,y
        return False

dx = [0,635,635,1270,1270]
dy = [520,0,520,0,520]
while 1:
    monitor = Monitor()
    monitor.start()
    if monitor.x and monitor.y:
        if monitor.x <= 635 and monitor.y <= 470:
            sleep(0.15)
            for i in range(5):
                sleep(0.05)
                pyautogui.click(monitor.x+dx[i],monitor.y+dy[i])
            sleep(0.05)
            pyautogui.moveTo(monitor.x,monitor.y)
    else:
        break
