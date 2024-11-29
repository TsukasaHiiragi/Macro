import os
import datetime
from time import sleep

import numpy as np
import pyperclip
import pyautogui

from state import Executer
import action
import image


def send(exe: Executer, uuid, key, message):
    exe.mt.send(uuid, key, message)

def receive(exe: Executer, name, uuid, key):
    exe.sys_args[name] = exe.mt.receive(uuid, key)

def delete_message(exe: Executer, uuid):
    exe.mt.delete_message(uuid)

def copy(exe: Executer, uuid, key):
    s = pyperclip.paste()
    exe.mt.send(uuid, key, s)

def paste(exe: Executer, uuid, key):
    s = exe.mt.receive(uuid, key)
    pyperclip.copy(s)

def counter(exe:Executer):
    if 'n_try' not in exe.sys_args:
        exe.sys_args['n_try'] = 0
    exe.sys_args['n_try'] += 1
    exe.mt.text(trial=(exe.sys_args['n_try'],exe.sys_args['trial']))
    if exe.sys_args['n_try'] >= exe.sys_args['trial']:
        exe.sys_args['quest\\result\\count.slc.stt.json'] = 'finish'
        exe.sys_args['quest\\result\\comeback.slc.stt.json'] = 'finish'
        exe.sys_args['restore\\result\\potal.slc.stt.json'] = 'finish'
        exe.sys_args['restore\\result\\comeback.slc.stt.json'] = 'finish'
    else:
        exe.sys_args['quest\\result\\count.slc.stt.json'] = 'retry'
        exe.sys_args['quest\\result\\comeback.slc.stt.json'] = 'retry'
        exe.sys_args['restore\\result\\potal.slc.stt.json'] = 'retry'
        exe.sys_args['restore\\result\\comeback.slc.stt.json'] = 'retry'
    
    d = exe.timer.elapse().total_seconds()
    if 'battle_mean' in exe.sys_args:
        exe.sys_args['battle_mean'] = 0.9*exe.sys_args['battle_mean'] + 0.1*d
    else:
        exe.sys_args['battle_mean'] = 0.1*d

def mode(exe: Executer, changed):
    if changed:
        exe.sys_args['battle\\auto.slc.stt.json'] = 'changed'
    else:
        exe.sys_args['battle\\auto.slc.stt.json'] = 'stay'

def syncronize(exe: Executer, key, members, timeout=180):
    if members >= 2:
        exe.mt.syncronize(key, members, timeout)

def clipboard_aquire(exe: Executer):
    exe.mt.clipboard_aquire()

def clipboard_release(exe: Executer):
    exe.mt.clipboard_release()

def ready(exe:Executer, key, members):
    if members >= 2:
        exe.mt.syncronize(f'{key}_ready', members, timeout=None)
    d = exe.timer.elapse()
    if 'time_mean' in exe.sys_args:
        if exe.sys_args['time_mean'] is None:
            mean = d
        else:
            mean = 0.9*exe.sys_args['time_mean'] + 0.1*d
        exe.sys_args['time_mean'] = mean
        if 'n_try' not in exe.sys_args:
            exe.sys_args['n_try'] = 0
        trial = exe.sys_args['trial'] - exe.sys_args['n_try']
        finish = datetime.datetime.now() + (mean * trial)
        exe.mt.text(time=(mean,finish))
    else:
        exe.sys_args['time_mean'] = None
    
    exe.reset()

def wait_battle(exe:Executer, offset):
    if 'battle_mean' in exe.sys_args:
        t = exe.sys_args['battle_mean']-offset
        if t > 0: sleep(t)

def ability(exe: Executer, name, id, key, members):
    dir = os.path.join('C:\\Users\\tsuka\\gitrepo\\Macro\\ability',name,f'{id}')
    if os.path.exists(os.path.join(dir,'ability.abi.json')):
        changed = use_ability(exe.mt, name, id, key, members)
        if changed: mode(exe, True)
    else:
        set_abi(exe.mt, name, id)

def ability_command(exe: Executer):
    charas = ['chara1','chara2','chara3','chara4','chara5']
    abilities = {'q':'ability1','w':'ability2','a':'ability3','s':'ability4',}
    cur = charas.index(exe.usr_args['chara'])
    exe.mt.print('ability_command ', state='KEYWORD', end='')
    exe.mt.print('input command', state='INPUT')
    exe.mt.print('esc, up, down, q, w, a, s, 1, 2, 3, 4, 5, space, enter', state='KEY')
    key = action.key_input(['esc','up','down','q','w','a','s','1','2','3','4','5','space','enter','p'])
    if exe.usr_args['target'] != 'none':
        exe.sys_args['config'].append(exe.usr_args.copy())
        exe.usr_args['ability'] = 'none'
        exe.usr_args['target'] = 'none'
    if key in ('esc','up','down','q','w','a','s','space','enter','p'):
        if exe.usr_args['ability'] != 'none':
            exe.sys_args['config'].append(exe.usr_args.copy())
            exe.usr_args['ability'] = 'none'
            exe.usr_args['target'] = 'none'
    if key == 'esc':
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'finish'
    elif key == 'up':
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'scroll'
        exe.usr_args['chara'] = charas[(cur-1)%5]
    elif key == 'down':
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'scroll'
        exe.usr_args['chara'] = charas[(cur+1)%5]
    elif key in ('q','w','a','s'):
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'ability'
        exe.usr_args['ability'] = abilities[key]
    elif key in ('1','2','3','4','5'):
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'target'
        exe.usr_args['target'] = 'chara'+key
    elif key == 'space':
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'mode'
        args = {'special':'mode','auto':'auto','burst':'on'}
        exe.sys_args['config'].append(args)
    elif key == 'enter':
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'attack'
        args = {'special':'attack'}
        exe.sys_args['config'].append(args)
    elif key == 'p':
        args = {'special':'syncronize'}
        exe.sys_args['config'].append(args)

def party(exe: Executer, name, id):
    dir = os.path.join('C:\\Users\\tsuka\\gitrepo\\Macro\\party',f'{id}',name)
    if os.path.exists(os.path.join(dir,'party.pty.json')):
        use_party(exe.mt, name, id)
    else:
        set_party(exe.mt, name, id)

def slot(exe: Executer):
    exe.mt.print('slot ', state='KEYWORD', end='')
    exe.mt.print('input command', state='INPUT')
    exe.mt.print('1 2 3 4 5 6 7 8 9 a b c', state='KEY')
    key = action.key_input(['1','2','3','4','5','6','7','8','9','a','b','c'])
    table = {'a':'10','b':'11','c':'12'}
    if key in table.keys():
        key = table[key]
    exe.usr_args['slot'] = f'slot{key}'

def tab(exe: Executer):
    exe.mt.print('tab ', state='KEYWORD', end='')
    exe.mt.print('input command', state='INPUT')
    exe.mt.print('a b c d e f', state='KEY')
    key = action.key_input(['a','b','c','d','e','f'])
    exe.usr_args['tab'] = key

def preset(exe: Executer):
    exe.mt.print('preset ', state='KEYWORD', end='')
    exe.mt.print('input command', state='INPUT')
    exe.mt.print('1 2 3 4 5 6 7 8 9 a b c', state='KEY')
    key = action.key_input(['1','2','3','4','5','6','7','8','9','a','b','c'])
    table = {'a':'10','b':'11','c':'12'}
    if key in table.keys():
        key = table[key]
    exe.usr_args['preset'] = f'preset{key}'

def click_button(exe: Executer, sym_path):
    exe.mt.print(f"{exe.path} ", 'DEBUG')
    symbol:image.Symbol = image.Symbol.load(sym_path)
    hit = symbol.search(hwnd=None)
    sleep(1.2)
    if hit:
        pos = np.array(hit[:2], dtype=np.float)
        size = np.array(hit[2:], dtype=np.float)
        centor = pos+size/2
        x,y = int(centor[0]),int(centor[1])
        with exe.mt.mouse():
            pyautogui.click(x,y)
        sleep(1.2)

