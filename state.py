import os
import re
import string
import json
import time

import image
import action
import utility
import mythread
import gui

class State:
    def __init__(self, path, next=None):
        # no extension
        self.__path = path
        self.__next = next
        self.__log_stop = False
        self.__log_beg = True

    # static
    def join(path):
        if path is None: return None
        return os.path.join(utility.path_to_state(), path)

    def strip(path):
        return re.sub(r'\..+\.stt\.json','',path)

    def load(path):
        with utility.openx(State.join(path), 'rt') as f:
            state:State = json.load(f, cls=StateDecoder)
        return state

    # not override
    def print(self, str, state='MESSAGE', end='\n'):
        if self.__log_stop: return
        if self.__log_beg:
            mythread.mt.print(f"{State.strip(self.path())} ", 'KEYWORD', '')
            self.__log_beg = False
        mythread.mt.print(str, state, end)
        if end == '\n': self.__log_beg = True
    
    def save(self):
        self.print(f'save {self.path()}', state='DEBUG')
        with mythread.mt.disc():
            with utility.openx(State.join(self.path()), 'wt') as f:
                json.dump(self, f, cls=StateEncoder, indent=2)

    def log_view(self, flag):
        self.__log_stop = flag

    # getter
    def path(self, new=None): 
        if new: self.__path = new
        return self.extend(self.__path)
    def next(self): return self.__next
    
    # override
    def forward(self, usr_args, sys_args, prev):
        mythread.mt.text(state=self.path())
        return self.next()

    def connect(self, next):
        if next: self.__next = next.path()
        else: self.__next = None

    def extend(self, str):
        return State.ext(str)

    def ext(str):
        return f'{str}.stt.json'

    def exists(path):
        return os.path.exists(State.join(State.ext(path)))

    def default(self):
        code = {'_type':'State', 'value':{}}
        code['value']['path'] = self.__path
        code['value']['next'] = self.__next
        return code

class DummyState(State):
    def __init__(self, path, next=None):
        super().__init__(path, next=next)

    def forward(self, usr_args, sys_args, prev):
        super().forward(usr_args, sys_args, prev)
        return self.next()

    def connect(self, next):
        super().connect(next)
    
    def extend(self, str):
        return DummyState.ext(str)

    def ext(str):
        return State.ext(f'{str}.dmy')

    def exists(path):
        return State.exists(DummyState.ext(path))

    def open(path):
        if DummyState.exists(path):
            return State.load(DummyState.ext(path))
        else:
            return DummyState(path)

    def default(self):
        code = super().default()
        code['_type'] = 'DummyState'
        return code

class MainState(State):
    def __init__(self, path, next=None):
        super().__init__(path, next=next)

    def forward(self, usr_args, sys_args, prev):
        super().forward(usr_args, sys_args, prev)
        act = action.Action.load(State.strip(self.path()))
        if act is None: 
            self.record()
        else:
            act.exe()
        return self.next()

    def connect(self, next):
        super().connect(next)

    def extend(self, str):
        return MainState.ext(str)

    def ext(str):
        return State.ext(f'{str}.man')

    def exists(path):
        return State.exists(MainState.ext(path))

    def open(path):
        if MainState.exists(path):
            return State.load(MainState.ext(path))
        else:
            return MainState(path)

    def default(self):
        code = super().default()
        code['_type'] = 'MainState'
        return code

    def record(self):
        while 1:
            self.print('Record action', state='INPUT')
            self.print('y', state='KEY', end='');self.print(': Start, ', end='')
            action.key_input(['y'])
            self.print('Esc', state='KEY', end='');self.print(': Finish')
            monitor = action.Monitor()
            self.print('Save the action ', state='INPUT')
            self.print('y', state='KEY', end='');self.print(': Save, ', end='')
            self.print('n', state='KEY', end='');self.print(': Again')
            if action.key_input(['y','n']) == 'y':
                monitor.action.save(State.strip(self.path()))
                return

class SelectState(State):
    def __init__(self, path, next=None, key=None, choices=None):
        super().__init__(path, next=next)
        self.__key = key
        if choices is None: self.__choices = {}
        else: self.__choices = choices

    def forward(self, usr_args, sys_args, prev):
        super().forward(usr_args, sys_args, prev)
        if self.__key == self.path():
            assert self.__key in sys_args, self.path()
            selected = sys_args[self.__key]
        else:
            if self.__key not in usr_args: 
                usr_args[self.__key] = self.select()
            selected = usr_args[self.__key]
        if selected not in self.__choices:
            return self.next()
        return self.__choices[selected]

    def extend(self, str):
        return SelectState.ext(str)

    def ext(str):
        return State.ext(f'{str}.slc')

    def exists(path):
        return State.exists(SelectState.ext(path))

    def open(path):
        if SelectState.exists(path):
            return State.load(SelectState.ext(path))
        else:
            return SelectState(path)

    def default(self):
        code = super().default()
        code['_type'] = 'SelectState'
        code['value']['key'] = self.__key
        code['value']['choices'] = self.__choices
        return code

    def select(self):
        while 1:
            self.print('Select', state='INPUT')
            dict = {}
            for i,choice in enumerate(self.__choices.keys()):
                key = string.ascii_lowercase[i]
                dict[key] = choice
                self.print(key, state='KEY', end='');self.print(': ', end='') 
                self.print(choice, state='KEYWORD')
            dict['esc'] = None
            self.print('Esc', state='KEY', end='');self.print(': Other') 
            key = action.key_input(dict.keys())
            if key == 'esc': 
                app:gui.Entry = mythread.mt.request(gui.Entry, items=['choice'])
                choice = app.str['choice']
                if choice: return choice
            else:
                return dict[key]

    def connect(self, key, default=None, **states:State):
        self.__key = key
        self.__choices = {}
        for key, state in states.items():
            self.__choices[key] = state.path()
        super().connect(default)

class BranchState(State):
    def __init__(self, path, next=None, possible=None, **kwargs):
        super().__init__(path, next=next)
        if possible: self.__possible = possible
        else: self.__possible = []

    def forward(self, usr_args, sys_args, prev):
        super().forward(usr_args, sys_args, prev)
        self.print('Start searching ', end='')
        self.print('esc', state='KEY', end='');self.print(': exit')
        self.print('Undefined symbols are below: ')
        alphabets = string.ascii_lowercase
        nosymbol = {'esc':None}
        i = 0
        for path in self.__possible:
            symbol_path = State.join(f'{State.strip(path)}.sym.json')
            if not os.path.exists(symbol_path):
                self.print(alphabets[i], state='KEY', end='');self.print(': ', end='')
                self.print(path, state='KEYWORD')
                nosymbol[alphabets[i]] = path
                i += 1
        monitor = action.KeyInput(nosymbol.keys())
        monitor.start()
        self.print(f'searching...', state='DEBUG')
        # hwnd = mythread.mt.empty() 
        hit = None
        while 1:
            for path in self.__possible:
                symbol:image.Symbol = image.Symbol.load(State.strip(path))
                if symbol is None: continue
                hit = symbol.search(hwnd=None)
                if hit: break
            if not monitor.is_alive(): 
                if monitor.key == 'esc':
                    # mythread.mt.close(hwnd)
                    print(self.path(), 'terminated')
                    return None
                else: 
                    # mythread.mt.close(hwnd)
                    self.capture(nosymbol[monitor.key])
                    monitor = action.KeyInput(nosymbol.keys())
                    monitor.start()
                    # hwnd = mythread.mt.empty() 
            if hit: break
            if self.next(): return self.next()
            time.sleep(0.6)
            
        # mythread.mt.close(hwnd)
        self.print(f'recognize {State.strip(path)}', state='DEBUG')
        monitor.stop()
        hwnd = mythread.mt.rect(*hit)
        symbol.save(State.strip(path))
        time.sleep(0.6)
        mythread.mt.close(hwnd)
        return path

    def extend(self, str):
        return BranchState.ext(str)

    def ext(str):
        return State.ext(f'{str}.brn')

    def exists(path):
        return State.exists(BranchState.ext(path))

    def open(path):
        if BranchState.exists(path):
            return State.load(BranchState.ext(path))
        else:
            return BranchState(path)

    def default(self):
        code = super().default()
        code['_type'] = 'BranchState'
        code['value']['possible'] = self.__possible
        return code

    def capture(self, next):
        name = State.strip(next)
        self.print('Capture symbol of ', state='INPUT', end='')
        self.print(name,state='KEYWORD')
        self.print('y', state='KEY', end='');self.print(': Start, ', end='')
        self.print('n', state='KEY', end='');self.print(': NULL')
        if action.key_input(['y', 'n']) == 'y':
            app:image.Capture = mythread.mt.request(image.Capture)
            time.sleep(0.5)

            if app.img_crop is None: return

            img_name = utility.unique_name(State.join(name),'.png')
            img_path = f'{img_name}.png'
            app.img_crop.save(img_path)

            symbol = image.LeafSymbol(img_path, utility.rect2region(app.rect))
        else:
            symbol = image.LeafSymbol(None, None)
        symbol.save(name)
    
    def connect(self, *states:State, exception=None):
        self.__possible = []
        for state in states:
            if state.path() not in self.__possible:
                self.__possible.append(state.path())
        super().connect(exception)

class CallState(State):
    def __init__(self, path, next=None, table=None):
        super().__init__(path, next=next)
        if table: self.__table = table
        else: self.__table = {'__main__':None}

    # override
    def forward(self, usr_args, sys_args, prev):
        super().forward(usr_args, sys_args, prev)
        if self.path() in sys_args:
            caller_path = sys_args.pop(self.path())
            return self.__table[caller_path]
        else:
            sys_args[self.path()] = prev
            return self.next()

    def extend(self, str):
        return CallState.ext(str)

    def ext(str):
        return State.ext(f'{str}.cll')

    def exists(path):
        return State.exists(CallState.ext(path))

    def open(path):
        if CallState.exists(path):
            return State.load(CallState.ext(path))
        else:
            return CallState(path)

    def default(self):
        code = super().default()
        code['_type'] = 'CallState'
        code['value']['table'] = self.__table
        return code

    # original
    def define(self, head:State, tail:State):
        super()._connect(next=head.path(), prev=tail.path())
        head._connect(prev=self.path())
        tail._connect(next=self.path())

    def call(self, caller:State, returner:State):
        caller._connect(next=self.path())
        returner._connect(prev=self.path())
        self.__table[caller.path()] = returner.path()

class StateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, State): return o.default()
        if isinstance(o, image.Symbol):
            return image.SymbolEncoder.default(self, o)
        if isinstance(o, action.Action):
            return action.ActionEncoder.default(self, o)
        return json.JSONEncoder.default(self, o)

class StateDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook,
                                  *args, **kwargs)

    def object_hook(self, o):
        if '_type' not in o:
            return o
        type = o['_type']
        if type == 'DummyState': return DummyState(**o['value'])
        if type == 'MainState': return MainState(**o['value'])
        if type == 'SelectState': return SelectState(**o['value'])
        if type == 'BranchState': return BranchState(**o['value'])
        if type == 'CallState': return CallState(**o['value'])
        symbol = image.SymbolDecoder().object_hook(o)
        if symbol: return symbol
        act = action.ActionDecoder().object_hook(o)
        if act: return act

class Executer:
    def __init__(self):
        self.path = None
        self.usr_args = {}
        self.sys_args = {}
        self.trigger = {}

    def forward(self):
        self.path = self.state.forward(self.usr_args, self.sys_args, self.path)
        if self.path is None: return
        if self.path in self.trigger:
            func, args, kwargs = self.trigger[self.path]
            func(self.usr_args, self.sys_args, *args, **kwargs)
        self.state = State.load(self.path)

    def run(self, initial, **usr_args):
        self.path = '__main__'
        self.usr_args = usr_args
        self.state = State.load(initial)
        while self.path:
            self.forward()

    def set_trigger(self, path, func, *args, **kwargs):
        self.trigger[path] = func, args, kwargs

class Assister:
    def __init__(self, dir):
        self.__dir = dir
        self.__dmy:dict[str, DummyState] = {}
        self.__man:dict[str, MainState] = {}
        self.__slc:dict[str, SelectState] = {}
        self.__brn:dict[str, BranchState] = {}

    def dmy(self, name):
        if name not in self.__dmy:
            self.__dmy[name] = DummyState.open(f'{self.__dir}\\{name}')
        return self.__dmy[name]

    def man(self, name):
        if name not in self.__man:
            self.__man[name] = MainState.open(f'{self.__dir}\\{name}')
        return self.__man[name]
    
    def slc(self, name):
        if name not in self.__slc:
            self.__slc[name] = SelectState.open(f'{self.__dir}\\{name}')
        return self.__slc[name]

    def brn(self, name):
        if name not in self.__brn:
            self.__brn[name] = BranchState.open(f'{self.__dir}\\{name}')
        return self.__brn[name]

    def save(self):
        for state in self.__dmy.values(): state.save()
        for state in self.__man.values(): state.save()
        for state in self.__slc.values(): state.save()
        for state in self.__brn.values(): state.save()
        