import json
import threading
from time import sleep

import pyautogui
from pynput import mouse, keyboard

import log

class Action:
    def __init__(self, actions=[]):
        self.actions = actions

    def exe(self):
        for action in self.actions:
            action.exe()

    def append(self, action):
        self.actions.append(action)

class Wait:
    def __init__(self, t):
        self.t = t

    def exe(self):
        sleep(self.t)

class Click:
    def __init__(self, x, y, interval=None):
        self.x,self.y = x,y
        self.interval = interval

    def exe(self):
        pyautogui.click(self.x,self.y)
        if self.interval:
            sleep(self.interval)
        else:
            sleep(1.2)

class Press:
    def __init__(self, key, interval=None):
        self.key = key
        self.interval = interval

    def exe(self):
        pyautogui.press(self.key)
        if self.interval:
            sleep(self.interval)
        else:
            sleep(1.2)

class HotKey:
    def __init__(self, keys, interval=None):
        self.keys = keys
        self.interval = interval

    def exe(self):
        pyautogui.hotkey(*self.keys)
        if self.interval:
            sleep(self.interval)
        else:
            sleep(1.2)

class ActionEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Action):
            return {'_type': 'Action', 
                    'value': {'actions':o.actions}}
        if isinstance(o, Wait):
            return {'_type': 'Wait', 
                    'value': {'t':o.t}}
        if isinstance(o, Click):
            return {'_type': 'Click', 
                    'value': {'x':o.x,
                              'y':o.y,
                              'interval':o.interval}}
        if isinstance(o, Press):
            return {'_type': 'Press', 
                    'value': {'key':o.key,
                              'interval':o.interval}}
        if isinstance(o, HotKey):
            return {'_type': 'HotKey', 
                    'value': {'keys':o.keys,
                              'interval':o.interval}}
        return json.JSONEncoder.default(self, o)

class ActionDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook,
                                  *args, **kwargs)

    def object_hook(self, o):
        if '_type' not in o:
            return o
        type = o['_type']
        if type == 'Action':
            return Action(**o['value'])
        if type == 'Wait':
            return Wait(**o['value'])
        if type == 'Click':
            return Click(**o['value'])
        if type == 'Press':
            return Press(**o['value'])
        if type == 'HotKey':
            return HotKey(**o['value'])

class Monitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.action = Action([])

        self.shift = False
        self.hot = None

        with mouse.Listener(on_click=self.click) as mouse_listener, keyboard.Listener(
            on_press=self.press,on_release=self.release) as keyboard_listener:
            keyboard_listener.join()
            mouse_listener.stop()
            mouse_listener.join()

    def click(self, x, y, button, pressed):
        if pressed and button.name == 'left':
            self.lock.acquire()
            self.action.append(Click(x,y))
            log.logger.print(f'click {x} {y}', state='DEBUG')
            self.lock.release()

    def press(self, key):
        try:
            _ = key.char
        except AttributeError:
            if key.name == 'ctrl_l':
                self.hot = 'ctrl'
            elif key.name == 'alt_l':
                self.hot = 'alt'
            elif key.name == 'shift':
                self.shift = True

    def release(self, key):
        if key == keyboard.Key.esc:
            return False
        
        try:
            name = key.char
        except AttributeError:
            return
        
        keys = []
        if self.shift:
            keys.append('shift')
            self.shift = False
        if self.hot:
            keys.append(self.hot)
            self.hot = None
        keys.append(name)
        self.lock.acquire()
        if len(keys) == 1:
            self.action.append(Press(keys[0]))
        else:
            self.action.append(HotKey(keys))
        self.lock.release()

class KeyInput:
    def __init__(self, keys):
        self.keys= keys
        self.key = None
        self.keyboard_listener = keyboard.Listener(on_release=self.release)

    def release(self, key):
        try:
            name = key.char
        except AttributeError:
            name = key.name
        
        if name in self.keys:
            self.key = name
            return False

    def start(self):
        self.keyboard_listener.start()
    
    def stop(self):
        self.keyboard_listener.stop()
    
    def join(self):
        self.keyboard_listener.join()

    def is_alive(self):
        return self.keyboard_listener.is_alive()

def key_input(keys):
    monitor = KeyInput(keys)
    monitor.start()
    monitor.join()
    return monitor.key

def main():
    monitor = Monitor()
    monitor.start()
    monitor.join()
    with open('action.act.json','wt') as f:
        json.dump(monitor.action, f, cls=ActionEncoder, indent=2)

if __name__ == "__main__":
    main()