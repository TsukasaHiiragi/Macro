import argparse
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
    
parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store_const', const=True)
args = parser.parse_args()

dx = 481
dy = 354
while 1:
    monitor = Monitor()
    monitor.start()
    if monitor.x is not None:
        if not args.a:
            if 0<=monitor.x and monitor.x<481 and -1080<=monitor.y and monitor.y<355-1080:
                sleep(0.10)
                for i in range(1,6):
                    # sleep(0.01)
                    pyautogui.click((monitor.x+dx*(i//3))*3//2,(monitor.y+dy*(i%3))*3//2)
                # sleep(0.01)
                pyautogui.moveTo(monitor.x*3//2,monitor.y*3//2)
            if 962<=monitor.x and monitor.x<1443 and -1080<=monitor.y and monitor.y<355-1080:
                sleep(0.10)
                for i in range(1,6):
                    # sleep(0.01)
                    pyautogui.click((monitor.x+dx*(i//3))*3//2,(monitor.y+dy*(i%3))*3//2)
                # sleep(0.01)
                pyautogui.moveTo(monitor.x*3//2,monitor.y*3//2) 
        else:
            if 0<=monitor.x and monitor.x<481 and -1080<=monitor.y and monitor.y<355-1080:
                sleep(0.10)
                for i in range(1,12):
                    # sleep(0.01)
                    pyautogui.click((monitor.x+dx*(i//3))*3//2,(monitor.y+dy*(i%3))*3//2)
                # sleep(0.01)
                pyautogui.moveTo(monitor.x*3//2,monitor.y*3//2)    
    else:
        break
