import json
import os
import datetime
from time import sleep, time
import random
import string

import numpy as np
import pyperclip
import pyautogui
import win32gui

from state import Executer, openwindow, openbrowser
import mythread
import utility
import action
import image

def quest(id, name, trial, key, members, party_id=None, ability_name=None, surpport=None, pre=None, arrange=True, time=None, limit=None, peer=False):
    start(id)
    path = os.path.join(utility.path_to_repo(),'quest',f'{name}.qst.json')
    args = {}
    if os.path.exists(path):
        new = False
        with utility.openx(path, 'rt') as f:
            args = json.load(f)
    else:
        new = True
        args = {}
    mythread.mt.text(trial=(0, trial))
    exe = Executer()
    exe.sys_args['trial'] = trial
    exe.sys_args['limit'] = limit
    exe.sys_args['battle\\host1.slc.stt.json'] = 'host'
    exe.sys_args['battle\\host2.slc.stt.json'] = 'host'
    exe.sys_args['restore\\battle\\host1.slc.stt.json'] = 'host'
    exe.sys_args['restore\\battle\\host2.slc.stt.json'] = 'host'
    exe.sys_args['battle\\auto.slc.stt.json'] = 'changed'
    exe.sys_args['battle\\team.slc.stt.json'] = 'solo' if members==1 or ('result' in args and args['result']=='union') else 'multi'
    exe.sys_args['battle\\request.slc.stt.json'] = 'solo' if members==1 or ('result' in args and args['result']=='union') else 'multi'
    exe.sys_args['quest\\result\\count.slc.stt.json'] = 'finish'
    exe.sys_args['page\\count.slc.stt.json'] = 'retry'
    if pre is not None:
        if 'battle_min' in pre.sys_args:
            exe.sys_args['battle_min'] = pre.sys_args['battle_min']
        if 'battle_start' in pre.sys_args:
            exe.sys_args['battle_start'] = pre.sys_args['battle_start']
        if 'time_mean' in pre.sys_args:
            exe.sys_args['time_mean'] = pre.sys_args['time_mean']
        if 'time_coef' in pre.sys_args:
            exe.sys_args['time_coef'] = pre.sys_args['time_coef']
    exe.set_trigger('quest\\start\\unidentified.man.stt.json', unidentified)
    exe.set_trigger('quest\\partyselect.dmy.stt.json', ready, key=key, members=members, host=True, peer=peer)
    exe.set_trigger('quest\\partyselect1.dmy.stt.json', send, uuid=key, key='battle', message='stay', peer=peer)
    exe.set_trigger('quest\\consume.dmy.stt.json', consume, id=id, name=name)
    if 'result' in args and args['result']=='union':
        exe.set_trigger('quest\\lock.dmy.stt.json', reset)
        exe.set_trigger('quest\\union.dmy.stt.json', syncronize, key='unionresult', members=12, peer=peer)
    elif arrange:
        exe.set_trigger('quest\\result1.dmy.stt.json', send, uuid=key, key='battle', message='reload', peer=peer)
        if members == 1:
            exe.set_trigger('quest\\lock.dmy.stt.json', lock, members=members, time_mean=time)
        else:
            exe.set_trigger('battle\\lock.dmy.stt.json', lock, members=members, time_mean=time)
    else:
        exe.set_trigger('quest\\lock.dmy.stt.json', reset)

    exe.set_trigger('battle\\clip_aquire.dmy.stt.json', clipboard_aquire)
    exe.set_trigger('battle\\send.dmy.stt.json', copy, uuid=key, key='raid_id', peer=peer)
    exe.set_trigger('battle\\clip_release.dmy.stt.json', clipboard_release)
    exe.set_trigger('battle\\notify.dmy.stt.json', syncronize, key=f'{key}_copy_completed', members=members, peer=peer)
    exe.set_trigger('battle\\sync.dmy.stt.json', syncronize, key=f'{key}_paste_completed', members=members, peer=peer)
    exe.set_trigger('battle\\isburst.slc.stt.json', mode, changed=False)
    exe.set_trigger('battle\\receive.slc.stt.json', receive, name='battle\\receive.slc.stt.json', uuid=key, key='battle')
    exe.set_trigger('battle\\wait_battle.dmy.stt.json', wait_battle, battle_min=None if time is None else time-12 if members==1 else time-18)
    exe.set_trigger('ability\\auto\\single.man.stt.json', mode, changed=True)
    exe.set_trigger('ability\\auto\\double.man.stt.json', mode, changed=True)

    exe.set_trigger('restore\\battle\\copy.man.stt.json', clipboard_aquire)
    exe.set_trigger('restore\\battle\\copy.dmy.stt.json', syncronize, key=f'{key}_crip_aquire', members=members, peer=peer)
    exe.set_trigger('restore\\battle\\syncronize.dmy.stt.json', syncronize, key=f'{key}_crip_release', members=members, peer=peer)
    exe.set_trigger('restore\\battle\\release.man.stt.json', clipboard_release)
    
    exe.set_trigger('quest\\result.dmy.stt.json', counter)
    exe.set_trigger('restore\\result.dmy.stt.json', counter)
    if type(party_id) == int:
        party_id = 0, party_id
    exe.sys_args['quest\\groupselect.slc.stt.json'] = f'group{party_id[0]}' if party_id else 'none'
    exe.sys_args['quest\\partyselect.slc.stt.json'] = f'party{party_id[1]}' if party_id else 'none'
    exe.sys_args['quest\\start\\surpport.slc.stt.json'] = surpport if surpport else 'none'
    if ability_name:
        exe.set_trigger('battle\\ability.dmy.stt.json', ability, name=ability_name, id=id, key=key, members=members)

    # exe.set_trigger('quest\\tail.dmy.stt.json', delete_message, uuid=key)
    # sleep(id*3.5)
    syncronize(None, f'{key}_start', members, timeout=None, peer=peer)
    exe.run('page\\head.dmy.stt.json', **args, timeout=360 if time is None else time+90)
    if new:
        with utility.openx(path, 'wt') as f:
            json.dump(exe.usr_args, f, indent=2)
    return exe

def rescue(id, name, trial, key, members, party_id=None, ability_name=None, surpport=None, pre=None, arrange=True, time=None, peer=False):
    start(id)
    path = os.path.join(utility.path_to_repo(),'quest',f'{name}.qst.json')
    if os.path.exists(path):
        with utility.openx(path, 'rt') as f:
            args = json.load(f)
    else: args = {}
    args['page'] = 'rescue'
    # if members == 1: args['member'] = 'other'
    # else: args['member'] = 'same'
    args['member'] = 'same'
    mythread.mt.text(trial=(0,trial))
    exe = Executer()
    exe.sys_args['trial'] = trial
    exe.sys_args['battle\\host1.slc.stt.json'] = 'guest'
    exe.sys_args['battle\\host2.slc.stt.json'] = 'guest'
    exe.sys_args['battle\\auto.slc.stt.json'] = 'changed'
    exe.sys_args['battle\\team.slc.stt.json'] = 'multi'
    exe.sys_args['battle\\request.slc.stt.json'] = 'multi'
    exe.sys_args['quest\\result\\count.slc.stt.json'] = 'back'
    exe.sys_args['restore\\battle\\host1.slc.stt.json'] = 'guest'
    exe.sys_args['restore\\battle\\host2.slc.stt.json'] = 'guest'
    exe.sys_args['restore\\result\\potal.slc.stt.json'] = 'back'
    exe.sys_args['page\\count.slc.stt.json'] = 'retry'
    exe.sys_args['rescue\\count.slc.stt.json'] = 'retry'
    if pre is not None:
        if 'battle_min' in pre.sys_args:
            exe.sys_args['battle_min'] = pre.sys_args['battle_min']
        if 'battle_start' in pre.sys_args:
            exe.sys_args['battle_start'] = pre.sys_args['battle_start']
        if 'time_mean' in pre.sys_args:
            exe.sys_args['time_mean'] = pre.sys_args['time_mean']
        if 'time_coef' in pre.sys_args:
            exe.sys_args['time_coef'] = pre.sys_args['time_coef']
    exe.set_trigger('quest\\start\\unidentified.man.stt.json', unidentified)
    exe.set_trigger('quest\\result1.dmy.stt.json', send, uuid=key, key='battle', message='reload', peer=peer)
    exe.set_trigger('quest\\lock.dmy.stt.json', reset)
    exe.set_trigger('quest\\result.dmy.stt.json', finish_battle)
    exe.set_trigger('battle\\isburst.slc.stt.json', mode, changed=False)
    exe.set_trigger('battle\\receive.slc.stt.json', receive, name='battle\\receive.slc.stt.json', uuid=key, key='battle')
    exe.set_trigger('battle\\wait_battle.dmy.stt.json', wait_battle, battle_min=None if time is None else time-30)
    exe.set_trigger('ability\\auto\\single.man.stt.json', mode, changed=True)
    exe.set_trigger('ability\\auto\\double.man.stt.json', mode, changed=True)
    exe.set_trigger('rescue\\unidentified.man.stt.json', unidentified)
    exe.set_trigger('rescue\\id.dmy.stt.json', ready, key=key, members=members, host=False, peer=peer)
    exe.set_trigger('rescue\\clip_aquire.dmy.stt.json', clipboard_aquire)
    exe.set_trigger('rescue\\notified.dmy.stt.json', syncronize, key=f'{key}_copy_completed', members=members, peer=peer)
    exe.set_trigger('rescue\\receive.dmy.stt.json', paste, uuid=key, key='raid_id')
    exe.set_trigger('rescue\\clip_release.dmy.stt.json', clipboard_release)
    exe.set_trigger('rescue\\raid.man.stt.json', syncronize, key=f'{key}_paste_completed', members=members, peer=peer)
    if type(party_id) == int:
        party_id = 0, party_id
    exe.sys_args['quest\\groupselect.slc.stt.json'] = f'group{party_id[0]}' if party_id else 'none'
    exe.sys_args['quest\\partyselect.slc.stt.json'] = f'party{party_id[1]}' if party_id else 'none'
    exe.sys_args['quest\\start\\surpport.slc.stt.json'] = surpport if surpport else 'none'
    if ability_name:
        exe.set_trigger('battle\\ability.dmy.stt.json', ability, name=ability_name, id=id, key=key, members=members)
    syncronize(None, f'{key}_start', members, timeout=None, peer=peer)
    exe.run('page\\head.dmy.stt.json', **args, timeout=360 if time is None else time+90)
    return exe

def lock(exe, members, time_mean=None):
    if time_mean is not None:
        t = time_mean/((12+members-1)//members)
        t = min(t,50)
        s = time()
        mythread.mt.battle(t)
        s = time() - s
        sleep(max(0, 3 - s))
    elif 'time_mean' in exe.sys_args and exe.sys_args['time_mean'] is not None:
        t = exe.sys_args['time_mean'].total_seconds()*0.9/((12+members-1)//members)
        t = min(t,50)
        s = time()
        mythread.mt.battle(t)
        s = time() - s
        sleep(max(0, 3 - s))
    exe.reset()

def reset(exe):
    exe.reset()

def send(exe, uuid, key, message, peer):
    mythread.mt.send(uuid, key, message, peer)

def receive(exe, name, uuid, key):
    exe.sys_args[name] = mythread.mt.receive(uuid, key)

def delete_message(exe, uuid):
    mythread.mt.delete_message(uuid)

def copy(exe, uuid, key, peer):
    s = pyperclip.paste()
    if s != exe.sys_args['prev_id']:
        mythread.mt.send(uuid, key, s, peer)
        exe.sys_args['battle\\check_copy.slc.stt.json'] = 'success'
    else:
        exe.sys_args['battle\\check_copy.slc.stt.json'] = 'failed'

def paste(exe, uuid, key):
    s = mythread.mt.receive(uuid, key)
    pyperclip.copy(s)

def counter(exe:Executer):
    # if 'n_try' not in exe.sys_args:
    #     exe.sys_args['n_try'] = 0
    # exe.sys_args['n_try'] += 1
    # exe.sys_args['already'] = False
    # mythread.mt.text(trial=(exe.sys_args['n_try'],exe.sys_args['trial']))
    # if exe.sys_args['n_try'] >= exe.sys_args['trial']:
    #     exe.sys_args['quest\\result\\count.slc.stt.json'] = 'finish'
    #     exe.sys_args['quest\\result\\comeback.slc.stt.json'] = 'finish'
    #     exe.sys_args['restore\\result\\potal.slc.stt.json'] = 'finish'
    #     exe.sys_args['restore\\result\\comeback.slc.stt.json'] = 'finish'
    # else:
    #     exe.sys_args['quest\\result\\count.slc.stt.json'] = 'retry'
    #     exe.sys_args['quest\\result\\comeback.slc.stt.json'] = 'retry'
    #     exe.sys_args['restore\\result\\potal.slc.stt.json'] = 'retry'
    #     exe.sys_args['restore\\result\\comeback.slc.stt.json'] = 'retry'
    
    d = exe.timer.elapse()
    if 'battle_start' in exe.sys_args:
        d = d - exe.sys_args['battle_start']
    d = d.total_seconds()
    if 'battle_min' in exe.sys_args:
        exe.sys_args['battle_min'] = min(d,exe.sys_args['battle_min'])
    else:
        exe.sys_args['battle_min'] = d
    # exe.reset()

def finish_battle(exe:Executer):
    d = exe.timer.elapse()
    if 'battle_start' in exe.sys_args:
        d = d - exe.sys_args['battle_start']
    d = d.total_seconds()
    if 'battle_min' in exe.sys_args:
        exe.sys_args['battle_min'] = min(d,exe.sys_args['battle_min'])
    else:
        exe.sys_args['battle_min'] = d

def mode(exe, changed):
    if changed:
        exe.sys_args['battle\\auto.slc.stt.json'] = 'changed'
    else:
        exe.sys_args['battle\\auto.slc.stt.json'] = 'stay'

def syncronize(exe, key, members, timeout=180, peer=False):
    if members >= 2 or peer:
        mythread.mt.syncronize(key, members, timeout, peer)

def clipboard_aquire(exe):
    mythread.mt.clipboard_aquire()
    s = pyperclip.paste()
    exe.sys_args['prev_id'] = s

def clipboard_release(exe):
    mythread.mt.clipboard_release()

def consume(exe:Executer, id, name):
    path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id}.json'
    with open(path, 'rt') as f:
        dic = json.load(f)
    today = datetime.datetime.now()
    today = today - datetime.timedelta(hours=4, minutes=55)
    today = today.strftime("%Y/%m/%d")
    if dic['timestamp']!=today:
        path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id}.back.json'
        with open(path, 'rt') as f:
            dic = json.load(f)
        dic['timestamp'] = today
        path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id}.json'
        with open(path, 'wt') as f:
            json.dump(dic, f, indent=2)
    remain = dic['remain']
    if name in remain:
        remain[name] = remain[name] - 1
        dic['remain'] = remain
    with open(path, 'wt') as f:
        json.dump(dic, f, indent=2)

def ready(exe:Executer, key, members, host=True, peer=False):
    if members >= 2 or peer:
        mythread.mt.syncronize(f'{key}_ready', members, timeout=None, peer=peer)
    d = exe.timer.elapse()
    exe.reset()
    if 'time_coef' in exe.sys_args:
        c = exe.sys_args['time_coef']
    else:
        c = 0.0
    exe.sys_args['time_coef'] = 0.9*c + 0.1*0.9
    if 'time_mean' in exe.sys_args:
        if exe.sys_args['time_mean'] is None or exe.sys_args['time_coef'] is None:
            mean = d
        else:
            mean = c*exe.sys_args['time_mean'] + (1-c)*d
        exe.sys_args['time_mean'] = mean
        if 'n_try' not in exe.sys_args:
            exe.sys_args['n_try'] = 0
        if 'start_time' not in exe.sys_args and exe.sys_args['n_try'] >= 2:
            exe.sys_args['start_time'] = datetime.datetime.now()
        if exe.sys_args['trial'] is None:
            finish = exe.sys_args['limit']
        else:
            if exe.sys_args['n_try'] > 2:
                start = exe.sys_args['start_time']
                trial = exe.sys_args['trial'] - exe.sys_args['n_try']
                mean = (datetime.datetime.now() - start) / (exe.sys_args['n_try'] - 2)
                v = int(3600 / mean.total_seconds())
                finish = datetime.datetime.now() + (mean*trial)
                mythread.mt.text(time=(mean, v, start, finish))
    else:
        exe.sys_args['time_mean'] = None
    
    if 'n_try' not in exe.sys_args:
        exe.sys_args['n_try'] = 0
    exe.sys_args['n_try'] += 1

    mythread.mt.text(trial=(exe.sys_args['n_try'],  exe.sys_args['trial']))
    if exe.sys_args['trial'] is None:
        limit = exe.sys_args['limit']
        now = datetime.datetime.now()
        if now > limit:
            exe.sys_args['quest\\result\\count.slc.stt.json'] = 'finish'
            exe.sys_args['page\\count.slc.stt.json'] = 'finish'
        else:
            exe.sys_args['quest\\result\\count.slc.stt.json'] = 'retry'
            exe.sys_args['page\\count.slc.stt.json'] = 'retry'
    elif exe.sys_args['n_try'] >= exe.sys_args['trial']:
        if host:
            exe.sys_args['quest\\result\\count.slc.stt.json'] = 'finish'
        else:
            exe.sys_args['rescue\\count.slc.stt.json'] = 'finish'
        exe.sys_args['page\\count.slc.stt.json'] = 'finish'
    else:
        if host:
            exe.sys_args['quest\\result\\count.slc.stt.json'] = 'retry'
        else:
            exe.sys_args['rescue\\count.slc.stt.json'] = 'retry'
        exe.sys_args['page\\count.slc.stt.json'] = 'retry'

def unidentified(exe:Executer):
    exe.sys_args['quest\\result\\count.slc.stt.json'] = 'finish'
    
def wait_battle(exe:Executer, battle_min=None):
    exe.sys_args['battle_start'] = exe.timer.elapse()
    if battle_min is not None:
        t = battle_min*0.95
        if t > 0: sleep(t)
    elif 'battle_min' in exe.sys_args:
        t = exe.sys_args['battle_min']*0.99
        if t > 0: sleep(t)

def init_ability():
    exe = Executer()
    exe.run('ability\\head.dmy.stt.json', chara='chara1')

def ability(exe, name, id, key, members):
    dir = os.path.join('C:\\Users\\tsuka\\gitrepo\\Macro\\ability',name,f'{id}')
    if os.path.exists(os.path.join(dir,'ability.abi.json')):
        changed = use_ability(name, id, key, members)
        if changed: mode(exe, True)
    else:
        set_abi(name, id)

def use_ability(name, id, key, members):
    dir = os.path.join('C:\\Users\\tsuka\\gitrepo\\Macro\\ability',name,f'{id}')
    symbol:image.LeafSymbol = image.Symbol.load(f'ability\\id{id}\\list')
    symbol.image_path = os.path.join(dir,'img','list.png')
    symbol.save(f'ability\\id{id}\\list')
    charas = ['chara1','chara2','chara3','chara4','chara5']
    for chara in charas:
        symbol:image.LeafSymbol = image.Symbol.load(f'ability\\id{id}\\scroll\\{chara}')
        symbol.image_path = os.path.join(dir,'img',f'{chara}.png')
        symbol.save(f'ability\\id{id}\\scroll\\{chara}')
    with utility.openx(os.path.join(dir,'ability.abi.json'), 'rt') as f:
        abilities = json.load(f)

    exe = Executer()
    if exe.run('ability\\pre.dmy.stt.json', root=False): return
    path = f'ability\\id{id}\\list.slc.stt.json' 
    changed = False
    for abi in abilities:
        if 'special' in abi:
            if abi['special'] == 'mode':
                if exe.run('ability\\mode.dmy.stt.json', root=False, **abi): return
                changed = True
            elif abi['special'] == 'attack':
                if exe.run(f'ability\\attack.dmy.stt.json', root=False, **abi): return
                path = f'ability\\id{id}\\head.dmy.stt.json' 
            elif abi['special'] == 'syncronize':
                mythread.mt.syncronize(f'{key}_ability', members)
            elif abi['special'] == 'enemy':
                if exe.run('ability\\enemy.dmy.stt.json', root=False, **abi): return
            elif abi['special'] == 'next':
                if exe.run('ability\\forward.dmy.stt.json', root=False, **abi): return
                path = f'ability\\id{id}\\head.dmy.stt.json' 
            elif abi['special'] == 'wait':
                sleep(abi['interval'])
        else:
            if exe.run(path, root=False, **abi): return
            path = f'ability\\id{id}\\scroll\\{abi["chara"]}.slc.stt.json'
    return changed

def set_abi(name, id):
    dir = os.path.join('C:\\Users\\tsuka\\gitrepo\\Macro\\ability',name,f'{id}')
    with utility.openx(os.path.join(dir,'img','list.png'), 'wt') as f:
        pass
    symbol:image.LeafSymbol = image.Symbol.load('set_abi\\list')
    symbol.image_path = os.path.join(dir,'img','list.png')
    symbol.save('set_abi\\list')
    charas = ['chara1','chara2','chara3','chara4','chara5']
    for chara in charas:
        symbol:image.LeafSymbol = image.Symbol.load(f'set_abi\\scroll\\{chara}')
        symbol.image_path = os.path.join(dir,'img',f'{chara}.png')
        symbol.save(f'set_abi\\scroll\\{chara}')

    exe = Executer()
    exe.sys_args['config'] = []
    exe.sys_args['set_abi\\command.slc.stt.json'] = 'keepon'
    exe.set_trigger('set_abi\\command.slc.stt.json', ability_command)
    exe.run('set_abi\\head.dmy.stt.json', chara='chara1', ability='none', target='none')
    with utility.openx(os.path.join(dir,'ability.abi.json'), 'wt') as f:
        json.dump(exe.sys_args['config'], f, indent=2)
       
def ability_command(exe):
    charas = ['chara1','chara2','chara3','chara4','chara5']
    abilities = {'q':'ability1','w':'ability2','a':'ability3','s':'ability4',}
    cur = charas.index(exe.usr_args['chara'])
    mythread.mt.print('ability_command ', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('esc, up, down, q, w, a, s, 1, 2, 3, 4, 5, space, enter, p, m, n', state='KEY')
    key = action.key_input(['esc','up','down','q','w','a','s','1','2','3','4','5','space','enter','p','m','n'])
    if exe.usr_args['target'] != 'none':
        exe.sys_args['config'].append(exe.usr_args.copy())
        exe.usr_args['ability'] = 'none'
        exe.usr_args['target'] = 'none'
    if key in ('esc','up','down','q','w','a','s','space','enter','p','m','n'):
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
        exe.sys_args['set_abi\\auto\\manual.slc.stt.json'] = 'auto'
        exe.sys_args['set_abi\\auto\\auto.slc.stt.json'] = 'auto'
        exe.sys_args['set_abi\\auto\\ability.slc.stt.json'] = 'auto'
        exe.sys_args['set_abi\\burst\\on.slc.stt.json'] = 'on'
        exe.sys_args['set_abi\\burst\\off.slc.stt.json'] = 'on'
        args = {'special':'mode','auto':'auto','burst':'on'}
        exe.sys_args['config'].append(args)
    elif key == 'enter':
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'attack'
        args = {'special':'attack'}
        exe.sys_args['config'].append(args)
    elif key == 'p':
        args = {'special':'syncronize'}
        exe.sys_args['config'].append(args)
    elif key == 'm':
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'mode'
        exe.sys_args['set_abi\\auto\\manual.slc.stt.json'] = 'manual'
        exe.sys_args['set_abi\\auto\\auto.slc.stt.json'] = 'manual'
        exe.sys_args['set_abi\\auto\\ability.slc.stt.json'] = 'manual'
        exe.sys_args['set_abi\\burst\\on.slc.stt.json'] = 'off'
        exe.sys_args['set_abi\\burst\\off.slc.stt.json'] = 'off'
        args = {'special':'mode','auto':'manual','burst':'off'}
        exe.sys_args['config'].append(args)
    elif key == 'n':
        exe.sys_args['set_abi\\command.slc.stt.json'] = 'next'
        args = {'special':'next'}
        exe.sys_args['config'].append(args)

def init_party():
    exe = Executer()
    exe.run('party\\head.dmy.stt.json')

def party(exe, name, id):
    dir = os.path.join('C:\\Users\\tsuka\\gitrepo\\Macro\\party',f'{id}',name)
    if os.path.exists(os.path.join(dir,'party.pty.json')):
        use_party(name, id)
    else:
        set_party(name, id)

def use_party(name, id):
    mythread.mt.print(name, state='KEYWORD')
    dir = os.path.join('C:\\Users\\tsuka\\gitrepo\\Macro\\party',f'{id}',name)
    symbol:image.LeafSymbol = image.Symbol.load(f'party\\id{id}\\party')
    symbol.image_path = os.path.join(dir,'party.png')
    symbol.save(f'party\\id{id}\\party')
    with utility.openx(os.path.join(dir,'party.pty.json'), 'rt') as f:
        party = json.load(f)
    exe = Executer()
    exe.sys_args['party\\check1.slc.stt.json'] = f'id{id}'
    exe.sys_args['party\\check2.slc.stt.json'] = f'id{id}'
    exe.run('party\\head.dmy.stt.json', **party)

def set_party(name, id):
    mythread.mt.print(name, state='KEYWORD')
    dir = os.path.join('C:\\Users\\tsuka\\gitrepo\\Macro\\party',f'{id}',name)
    with utility.openx(os.path.join(dir,'party.png'), 'wt') as f:
        pass
    symbol:image.LeafSymbol = image.Symbol.load(f'set_party\\party')
    symbol.image_path = os.path.join(dir,'party.png')
    symbol.save(f'set_party\\party')

    exe = Executer()
    exe.set_trigger('set_party\\slot.slc.stt.json', slot)
    exe.set_trigger('set_party\\tab.slc.stt.json', tab)
    exe.set_trigger('set_party\\preset.slc.stt.json', preset)
    exe.run('set_party\\head.dmy.stt.json')

    with utility.openx(os.path.join(dir,'party.pty.json'), 'wt') as f:
        json.dump(exe.usr_args, f, indent=2)

def slot(exe):
    mythread.mt.print('slot ', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('1 2 3 4 5 6 7 8 9 a b c', state='KEY')
    key = action.key_input(['1','2','3','4','5','6','7','8','9','a','b','c'])
    table = {'a':'10','b':'11','c':'12'}
    if key in table.keys():
        key = table[key]
    exe.usr_args['slot'] = f'slot{key}'

def tab(exe):
    mythread.mt.print('tab ', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('a b c d e f', state='KEY')
    key = action.key_input(['a','b','c','d','e','f'])
    exe.usr_args['tab'] = key

def preset(exe):
    mythread.mt.print('preset ', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('1 2 3 4 5 6 7 8 9 a b c', state='KEY')
    key = action.key_input(['1','2','3','4','5','6','7','8','9','a','b','c'])
    table = {'a':'10','b':'11','c':'12'}
    if key in table.keys():
        key = table[key]
    exe.usr_args['preset'] = f'preset{key}'

def story():
    exe = Executer()
    exe.run('story\\head.dmy.stt.json', timeout=None)

def gacha_normal():
    id = mythread.mt.local.thread_id
    start(id)
    exe = Executer()
    consume(exe, id, 'gacha_normal')
    exe.run('gacha_normal\\head.dmy.stt.json')

def gacha_special():
    exe = Executer()
    exe.set_trigger(f'gacha_special\\ok.dmy.stt.json', click_button, sym_path='gacha_special\\ok')
    exe.run('gacha_special\\head.dmy.stt.json')

def click_button(exe, sym_path):
    mythread.mt.print(f"{exe.path} ", 'DEBUG')
    symbol:image.Symbol = image.Symbol.load(sym_path)
    hit = symbol.search(hwnd=None)
    sleep(1.2)
    if hit:
        pos = np.array(hit[:2], dtype=np.float)
        size = np.array(hit[2:], dtype=np.float)
        centor = pos+size/2
        x,y = int(centor[0]),int(centor[1])
        with mythread.mt.mouse():
            pyautogui.click(x,y)
        sleep(1.2)

def receive_present():
    id = mythread.mt.local.thread_id
    start(id)
    exe = Executer()
    exe.sys_args['page\\count.slc.stt.json'] = 'retry'
    consume(exe, id, 'receive_present')
    # for m in ['daily','weekly','event']:
    #     m = f'mission\\{m}'
    #     exe.set_trigger(f'receive\\{m}\\ok.dmy.stt.json', click_button, sym_path='receive\\ok')
    # for m in ['daily','weekly']:
    #     m = f'pass\\{m}'
    #     exe.set_trigger(f'receive\\{m}\\ok.dmy.stt.json', click_button, sym_path='receive\\ok')
    exe.set_trigger(f'receive\\mission\\ok.dmy.stt.json', click_button, sym_path='receive\\ok')
    exe.set_trigger(f'receive\\ok1.man.stt.json', click_button, sym_path='receive\\ok')
    exe.set_trigger(f'receive\\ok2.man.stt.json', click_button, sym_path='receive\\ok')
    exe.run('page\\head.dmy.stt.json', page='receive', timeout=1800)


def restore(id):
    exe = Executer()
    exe.run('close\\head.dmy.stt.json')
    exe = Executer()
    exe.set_trigger(f'restore\\open.dmy.stt.json',openwindow,id)
    exe.run('restore\\head.dmy.stt.json')
    
def start(id):
    # id = mythread.mt.local.thread_id
    # scale = mythread.mt.local.scale
    # position = mythread.mt.local.position
    # with mythread.mt.screen(), mythread.mt.mouse(), mythread.mt.disc():
    #     mythread.mt.local.thread_id = 0
    #     mythread.mt.local.scale = 50
    #     mythread.mt.local.position = (np.array([0.,0.]),np.array([np.inf,np.inf]))
    #     exe = Executer()
    #     exe.set_trigger(f'restore\\open.dmy.stt.json',openwindow,id)
    #     error = exe.run(f'restore\\head.dmy.stt.json',timeout=180, root=False, id=f'id{id}')
    # mythread.mt.local.thread_id = id
    # mythread.mt.local.scale = scale
    # mythread.mt.local.position = position
    exe = Executer()
    exe.set_trigger(f'restore\\open.dmy.stt.json',openwindow,id)
    error = exe.run('restore\\head.dmy.stt.json', timeout=180, root=False, mode='validate')
    if error:
        close()
        start(id)

def close():
    exe = Executer()
    exe.run('close\\head.dmy.stt.json')

def reload():
    exe = Executer()
    exe.run('reload\\head.dmy.stt.json')

def abandon():
    exe = Executer()
    exe.run('abandon\\head.dmy.stt.json')

def wait(t):
    while datetime.datetime.now().hour < t:
        sleep(10)

def episode():
    exe = Executer()
    exe.run('episode\\head.dmy.stt.json', timeout=None)

def reduction(action,trial=None):
    def count(exe:Executer, trial):
        c = exe.sys_args['count']
        if trial is not None and c+1>=trial:
            exe.sys_args['reduction\\retry.slc.stt.json'] = 'finish'
        else:
            exe.sys_args['reduction\\retry.slc.stt.json'] = 'retry'
        exe.sys_args['count'] = c+1

    exe = Executer()
    exe.sys_args['count'] = 0
    exe.set_trigger('reduction\\count.dmy.stt.json',count,trial=trial)
    exe.run('reduction\\head.dmy.stt.json', timeout=None, action=action)

def work():
    exe = Executer()
    exe.run('work\\head.dmy.stt.json')

def epic(id,attr,scroll,position,trial):
    def _quest(exe:Executer,id,trial):
        quest(id,'epic',trial[exe.sys_args['level']],f'uuid_{id}',1)
        exe.sys_args['level'] += 1

    exe = Executer()
    exe.sys_args['level'] = 0
    exe.set_trigger('epic\\quest\\quest.dmy.stt.json',_quest,id=id,trial=trial)
    exe.run('epic\\head.dmy.stt.json',timeout=None,attr=attr,scroll=f'sc{scroll}',position=f'pos{position}')

def demado():
    def __copy(exe):
        s = pyperclip.paste()
        exe.sys_args['text'] = s

    def __paste(exe):
        s = exe.sys_args['text']
        pyperclip.copy(s)

    def __name(exe):
        pyperclip.copy('kpro')

    exe = Executer()
    id = 1
    exe.set_trigger('demado\\open.dmy.stt.json',openwindow,id)
    exe.set_trigger('demado\\copy.dmy.stt.json',__copy)
    exe.set_trigger('demado\\paste.dmy.stt.json',__paste)
    exe.set_trigger('demado\\name.dmy.stt.json',__name)
    exe.run('demado\\head.dmy.stt.json',timeout=None,id=f'id{id}')
    for id in range(2,25):
        exe.set_trigger('demado\\open.dmy.stt.json',openwindow,id)
        exe.set_trigger('demado\\copy.dmy.stt.json',__copy)
        exe.set_trigger('demado\\paste.dmy.stt.json',__paste)
        exe.set_trigger('demado\\name.dmy.stt.json',__name)
        exe.run('demado\\head.dmy.stt.json',timeout=None,id=f'id{id}')

def move(id):
    def __move(exe, id):
        id = id-1
        x = id//3
        y = id%3
        e = -6
        hwnd = win32gui.GetForegroundWindow()
        print(hwnd)
        win32gui.MoveWindow(hwnd, e+480*x, 350*y, 494, 357, True)
        sleep(1.2)

    exe = Executer()
    exe.set_trigger('move\\open.dmy.stt.json',openwindow,id)
    exe.set_trigger('move\\move.dmy.stt.json',__move,id)
    exe.run('move\\head.dmy.stt.json',timeout=None,id=f'id{id}')

def login(id):
    exe = Executer()
    exe.run('close\\head.dmy.stt.json')
    id = mythread.mt.local.thread_id
    scale = mythread.mt.local.scale
    position = mythread.mt.local.position
    with mythread.mt.screen(), mythread.mt.mouse(), mythread.mt.disc():
        mythread.mt.local.thread_id = 0
        mythread.mt.local.scale = 50
        mythread.mt.local.position = (np.array([0.,0.]),np.array([np.inf,np.inf]))
        exe = Executer()
        exe.set_trigger(f'login\\open.dmy.stt.json',openbrowser,id)
        error = exe.run(f'login\\head.dmy.stt.json',timeout=180, root=False)
    mythread.mt.local.thread_id = id
    mythread.mt.local.scale = scale
    mythread.mt.local.position = position

def cache_clear(id):
    exe = Executer()
    exe.set_trigger(f'cache_clear\\open.dmy.stt.json',openwindow,id)
    error = exe.run(f'cache_clear\\head.dmy.stt.json')

def theater():
    exe = Executer()
    sleep((mythread.mt.local.thread_id%12)*5)
    while 1:
        i = random.randint(0,11)
        exe.run('theater\\head.dmy.stt.json', episode=f'episode{i}', timeout=None)

def dependency(key, members):
    syncronize(None, key, members, timeout=None)

def capture():
    app:image.Capture = mythread.mt.request(image.Capture)
    sleep(0.5)

    if app.img_crop is None: return

    img_name = utility.unique_name(os.path.join(utility.path_to_state(), 'tmp'), '.png')
    img_path = f'{img_name}.png'
    app.img_crop.save(img_path)

    alphabets = list(string.ascii_lowercase)[:-2]
    dic = {c:i for i,c in enumerate(alphabets)}
    mythread.mt.print('Select id: ', state='INPUT')
    for i,c in enumerate(alphabets):
        mythread.mt.print(f'{c}', state='KEY', end='')
        mythread.mt.print(f': ', end='')
        mythread.mt.print(f'{i+1}', state='KEYWORD')
    id = dic[action.key_input(alphabets)]+1
    mythread.mt.print(f'id{id} is selected.')

    position = (
        (np.array([0.,0.]),np.array([np.inf,np.inf])),
        (np.array([-711., -84.]),np.array([0.01,0.01])),
        (np.array([-711., 266.]),np.array([0.01,0.01])),
        (np.array([-711., 616.]),np.array([0.01,0.01])),
        (np.array([-231., -84.]),np.array([0.01,0.01])),
        (np.array([-231., 266.]),np.array([0.01,0.01])),
        (np.array([-231., 616.]),np.array([0.01,0.01])),
        (np.array([ 249., -84.]),np.array([0.01,0.01])),
        (np.array([ 249., 266.]),np.array([0.01,0.01])),
        (np.array([ 249., 616.]),np.array([0.01,0.01])),
        (np.array([ 729., -84.]),np.array([0.01,0.01])),
        (np.array([ 729., 266.]),np.array([0.01,0.01])),
        (np.array([ 729., 616.]),np.array([0.01,0.01])),
        (np.array([1209., -84.]),np.array([0.01,0.01])),
        (np.array([1209., 266.]),np.array([0.01,0.01])),
        (np.array([1209., 616.]),np.array([0.01,0.01])),
        (np.array([1689., -84.]),np.array([0.01,0.01])),
        (np.array([1689., 266.]),np.array([0.01,0.01])),
        (np.array([1689., 616.]),np.array([0.01,0.01])),
        (np.array([2169., -84.]),np.array([0.01,0.01])),
        (np.array([2169., 266.]),np.array([0.01,0.01])),
        (np.array([2169., 616.]),np.array([0.01,0.01])),
        (np.array([2649., -84.]),np.array([0.01,0.01])),
        (np.array([2649., 266.]),np.array([0.01,0.01])),
        (np.array([2649., 616.]),np.array([0.01,0.01]))
    )[id][0]
    scale = 50

    r = image.Region(app.region)
    r.translation(-position)
    r.scaling(50/scale, mythread.centor)
    region = r.region()

    symbol = image.LeafSymbol(img_path, region)
    symbol.save('tmp')

    mythread.mt.print(f'The image and the symbol are successfully saved to')
    mythread.mt.print(img_name, state='OUTPUT')

def record():
    alphabets = list(string.ascii_lowercase)[:-2]
    dic = {c:i for i,c in enumerate(alphabets)}
    mythread.mt.print('Select id: ', state='INPUT')
    for i,c in enumerate(alphabets):
        mythread.mt.print(f'{c}', state='KEY', end='')
        mythread.mt.print(f': ', end='')
        mythread.mt.print(f'{i+1}', state='KEYWORD')
    id = dic[action.key_input(alphabets)]+1
    mythread.mt.print(f'id{id} is selected.')

    x = ((id - 1) // 3) % 4
    y = (id - 1) % 3
    position = np.array([479. * x, 350. * y])
    scale = 50

    while 1:
        mythread.mt.print('Record action', state='INPUT')
        mythread.mt.print('y', state='KEY', end='');mythread.mt.print(': Start, ', end='')
        action.key_input(['y'])
        mythread.mt.print('Esc', state='KEY', end='');mythread.mt.print(': Finish')
        monitor = action.Monitor(scale=scale, position=position)
        mythread.mt.print('Save the action ', state='INPUT')
        mythread.mt.print('y', state='KEY', end='');mythread.mt.print(': Save, ', end='')
        mythread.mt.print('n', state='KEY', end='');mythread.mt.print(': Again')
        if action.key_input(['y','n']) == 'y':
            monitor.action.save('tmp')
            break

    mythread.mt.print(f'The action is successfully saved to')
    mythread.mt.print(os.path.join(utility.path_to_state(), 'tmp'), state='OUTPUT')

