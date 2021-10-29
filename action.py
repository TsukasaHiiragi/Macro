import os
import json
import threading
from time import sleep

import numpy as np
import pyautogui
from pynput import mouse, keyboard

import utility
import mythread
import image

class Action:
    def init(self):
        pass

    def exe():
        pass

    def default(self):
        code = {'_type':'Action', 'value':{}}
        return code
    
    def load(path):
        act_path = os.path.join(utility.path_to_state(),f'{path}.act.json')
        if os.path.exists(act_path):
            with open(act_path, 'rt') as f:
                action = json.load(f, cls=ActionDecoder)
        else: action = None
        return action

    def save(self, path):
        act_path = os.path.join(utility.path_to_state(),f'{path}.act.json')
        with mythread.mt.disc():
            with utility.openx(act_path, 'wt') as f:
                json.dump(self, f, cls=ActionEncoder, indent=2)

class Actions(Action):
    def __init__(self, actions=None):
        super().__init__()
        if actions: self.actions = actions
        else: self.actions = []

    def exe(self):
        for action in self.actions:
            action.exe()

    def append(self, action):
        self.actions.append(action)

    def default(self):
        code = super().default()
        code['_type'] = 'Action'
        code['value']['actions'] = self.actions
        return code

class Wait(Action):
    def __init__(self, t):
        super().__init__()
        self.t = t

    def exe(self):
        sleep(self.t)

    def default(self):
        code = super().default()
        code['_type'] = 'Wait'
        code['value']['t'] = self.t
        return code

class Click(Action):
    def __init__(self, x, y, interval=None, keys=None):
        super().__init__()
        self.coord = np.array([x,y])
        self.interval = interval
        self.keys = keys

    def exe(self):
        if self.interval: sleep(self.interval[0])
        scale = mythread.mt.local.scale
        position = mythread.mt.local.position[0]
        coord = mythread.centor+(self.coord-mythread.centor)*scale/50+position
        x,y = int(coord[0]),int(coord[1])
        with mythread.mt.mouse():
            pyautogui.click(x,y)
            if self.keys: pyautogui.hotkey(*self.keys)
        if self.interval: sleep(self.interval[1])
        else: sleep(1.2)

    def default(self):
        code = super().default()
        code['_type'] = 'Click'
        code['value']['x'] = int(self.coord[0])
        code['value']['y'] = int(self.coord[1])
        code['value']['interval'] = self.interval
        code['value']['keys'] = self.keys
        return code

class Scroll(Action):
    def __init__(self, x, y, amount, interval=None):
        super().__init__()
        self.coord = np.array([x,y])
        self.amount = amount
        self.interval = interval

    def exe(self):
        if self.interval: sleep(self.interval[0])
        scale = mythread.mt.local.scale
        position = mythread.mt.local.position[0]
        coord = mythread.centor+(self.coord-mythread.centor)*scale/50+position
        x,y = int(coord[0]),int(coord[1])
        with mythread.mt.mouse():
            pyautogui.moveTo(x,y)
            pyautogui.scroll(self.amount)
        if self.interval: sleep(self.interval[1])
        else: sleep(1.2)

    def default(self):
        code = super().default()
        code['_type'] = 'Scroll'
        code['value']['x'] = int(self.coord[0])
        code['value']['y'] = int(self.coord[1])
        code['value']['interval'] = self.interval
        code['value']['amount'] = self.amount
        return code

class Press(Action):
    def __init__(self, key, interval=None):
        super().__init__()
        self.key = key
        self.interval = interval

    def exe(self):
        pyautogui.press(self.key)
        if self.interval:
            sleep(self.interval)
        else:
            sleep(1.2)

    def default(self):
        code = super().default()
        code['_type'] = 'Press'
        code['value']['key'] = self.key
        code['value']['interval'] = self.interval
        return code

class HotKey(Action):
    def __init__(self, keys, interval=None):
        super().__init__()
        self.keys = keys
        self.interval = interval

    def exe(self):
        pyautogui.hotkey(*self.keys)
        if self.interval:
            sleep(self.interval)
        else:
            sleep(1.2)

    def default(self):
        code = super().default()
        code['_type'] = 'HotKey'
        code['value']['keys'] = self.keys
        code['value']['interval'] = self.interval
        return code

class Capture(Action):
    def __init__(self, symbol_path):
        super().__init__()
        self.symbol_path = symbol_path

    def exe(self):
        symbol:image.LeafSymbol = image.Symbol.load(self.symbol_path)
        symbol.capture()

    def default(self):
        code = super().default()
        code['_type'] = 'Capture'
        code['value']['symbol_path'] = self.symbol_path
        return code

class ActionEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Action): return o.default()
        return json.JSONEncoder.default(self, o)

class ActionDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook,
                                  *args, **kwargs)

    def object_hook(self, o):
        if '_type' not in o: return o
        type = o['_type']
        if type == 'Action': return Actions(**o['value'])
        if type == 'Wait': return Wait(**o['value'])
        if type == 'Click': return Click(**o['value'])
        if type == 'Scroll': return Scroll(**o['value'])
        if type == 'Press': return Press(**o['value'])
        if type == 'HotKey': return HotKey(**o['value'])
        if type == 'Capture': return Capture(**o['value'])

class Monitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.action = Actions()

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
            mythread.mt.print(f'click {x} {y}', state='DEBUG')
            self.lock.release()

        if pressed and button.name == 'right':
            self.lock.acquire()
            self.action.append(Scroll(x,y,-1000))
            mythread.mt.print(f'scroll {x} {y}', state='DEBUG')
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
            mythread.mt.print(f'press {keys[0]}', state='DEBUG')
            self.action.append(Press(keys[0]))
        else:
            mythread.mt.print(f'hotkey {keys.__str__()}', state='DEBUG')
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