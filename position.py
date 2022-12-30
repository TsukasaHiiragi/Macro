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
    if monitor.x is not None:
        print(monitor.x,monitor.y)
        pyautogui.moveTo(monitor.x,monitor.y) 
    else:
        break
