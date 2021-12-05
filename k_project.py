import json
import os
import datetime
from time import sleep, time

from state import Executer
import mythread
import utility
import action
import image

def quest(id, name, trial, key, members, party_name=None, ability_name=None):
    path = os.path.join('quest',f'{name}.qst.json')
    if os.path.exists(path):
        with utility.openx(path, 'rt') as f:
            args = json.load(f)
    else: args = {}
    mythread.mt.text(trial=(0,trial))
    exe = Executer()
    exe.sys_args['battle\\host1.slc.stt.json'] = 'host'
    exe.sys_args['battle\\host2.slc.stt.json'] = 'host'
    exe.sys_args['battle\\auto.slc.stt.json'] = 'changed'
    exe.set_trigger('battle\\copy.man.stt.json', cripboard_aquire)
    exe.set_trigger('battle\\copy.dmy.stt.json', syncronize, key=key, members=members)
    exe.set_trigger('battle\\syncronize.dmy.stt.json', syncronize, key=key, members=members)
    exe.set_trigger('battle\\release.man.stt.json', cripboard_release)
    exe.set_trigger('battle\\isburst.slc.stt.json', mode, changed=False)
    exe.set_trigger('ability\\auto\\single.man.stt.json', mode, changed=True)
    exe.set_trigger('ability\\auto\\double.man.stt.json', mode, changed=True)
    
    exe.set_trigger('quest\\result.dmy.stt.json', counter, trial=trial)
    if args['type'] == 'orympia':
        exe.set_trigger('quest\\retry\\start.dmy.stt.json', encount, is_encount=False, id=id, key=key, members=members)
        exe.set_trigger('quest\\finish\\finish.dmy.stt.json', encount, is_encount=False, id=id, key=key, members=members)
        exe.set_trigger('quest\\result\\encount.dmy.stt.json', encount, is_encount=True, id=id, key=key, members=members)
    exe.set_trigger('quest\\union.dmy.stt.json', syncronize, key='unionresult', members=6)
    if party_name:
        exe.set_trigger('quest\\partyselect.man.stt.json', party, name=party_name, id=id)
    if ability_name:
        exe.set_trigger('battle\\ability.dmy.stt.json', ability, name=ability_name, id=id, key=key, members=members)
    syncronize(None, None, key, members)
    exe.run('page\\head.dmy.stt.json', **args)
    with utility.openx(path, 'wt') as f:
        json.dump(exe.usr_args, f, indent=2)

def counter(usr_args, sys_args, trial):
    if 'n_try' not in sys_args:
        sys_args['n_try'] = 0
    sys_args['n_try'] += 1
    mythread.mt.text(trial=(sys_args['n_try'],trial))
    if sys_args['n_try'] >= trial:
        sys_args['quest\\result\\count.slc.stt.json'] = 'finish'
        sys_args['quest\\result\\comeback.slc.stt.json'] = 'finish'
    else:
        sys_args['quest\\result\\count.slc.stt.json'] = 'retry'
        sys_args['quest\\result\\comeback.slc.stt.json'] = 'retry'

def mode(usr_args, sys_args, changed):
    if changed:
        sys_args['battle\\auto.slc.stt.json'] = 'changed'
    else:
        sys_args['battle\\auto.slc.stt.json'] = 'stay'


def syncronize(usr_args, sys_args, key, members):
    mythread.mt.syncronize(key, members)

def cripboard_aquire(usr_args, sys_args):
    mythread.mt.cripboard_aquire()

def cripboard_release(usr_args, sys_args):
    mythread.mt.cripboard_release()

def encount(usr_args, sys_args, is_encount, id, key, members):
    mythread.mt.glob['encount'] = is_encount
    mythread.mt.syncronize(key, members)
    if is_encount:
        quest(id,'raid\\orympia\\rag\\phantom',1,'orympia_phantom',members,
            party_name='aqua\\attack',ability_name='aqua\\burst\\normal')

def orympia_phantom(id, key, members):
    mythread.mt.syncronize(key, members)
    if mythread.mt.glob['encount']:
        rescue(id,'raid\\orympia\\rag\\phantom',1,'orympia_phantom',members,
            party_name='aqua\\attack',ability_name='aqua\\burst\\normal')

def rescue(id, name, trial, key, members, party_name=None, ability_name=None):
    path = os.path.join('quest',f'{name}.qst.json')
    if os.path.exists(path):
        with utility.openx(path, 'rt') as f:
            args = json.load(f)
    else: args = {}
    args['page'] = 'rescue'
    mythread.mt.text(trial=(0,trial))
    exe = Executer()
    exe.sys_args['battle\\host1.slc.stt.json'] = 'guest'
    exe.sys_args['battle\\host2.slc.stt.json'] = 'guest'
    exe.sys_args['quest\\result\\count.slc.stt.json'] = 'back'
    exe.sys_args['battle\\auto.slc.stt.json'] = 'changed'
    exe.set_trigger('battle\\isburst.slc.stt.json', mode, changed=False)
    exe.set_trigger('ability\\auto\\single.man.stt.json', mode, changed=True)
    exe.set_trigger('ability\\auto\\double.man.stt.json', mode, changed=True)
    exe.set_trigger('rescue\\id.dmy.stt.json', syncronize, key=key, members=members)
    exe.set_trigger('rescue\\raid.man.stt.json', syncronize, key=key, members=members)
    if party_name:
        exe.set_trigger('quest\\partyselect.man.stt.json', party, name=party_name, id=id)
    if ability_name:
        exe.set_trigger('battle\\ability.dmy.stt.json', ability, name=ability_name, id=id, key=key, members=members)
    syncronize(None, None, key, members)
    for i in range(trial):
        exe.run('page\\head.dmy.stt.json', **args)
        if args['type'] == 'orympia':
            orympia_phantom(id, key, members)
        mythread.mt.text(trial=(i+1,trial))

def init_ability():
    exe = Executer()
    exe.run('ability\\head.dmy.stt.json', chara='chara1')

def ability(usr_args, sys_args, name, id, key, members):
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\ability',name,f'{id}')
    if os.path.exists(os.path.join(dir,'ability.abi.json')):
        use_ability(name, id, key, members)
    else:
        set_abi(name, id)

def use_ability(name, id, key, members):
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\ability',name,f'{id}')
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
    exe.run('ability\\pre.dmy.stt.json')
    path = f'ability\\id{id}\\list.slc.stt.json' 
    for abi in abilities:
        if 'special' in abi:
            if abi['special'] == 'mode':
                exe.run('ability\\mode.dmy.stt.json', **abi)
            elif abi['special'] == 'attack':
                exe.run(f'ability\\attack.dmy.stt.json', **abi)
                path = f'ability\\id{id}\\head.dmy.stt.json' 
            elif abi['special'] == 'syncronize':
                mythread.mt.syncronize(key, members)
            elif abi['special'] == 'enemy':
                exe.run('ability\\enemy.dmy.stt.json', **abi)
        else:
            exe.run(path, **abi)
            path = f'ability\\id{id}\\scroll\\{abi["chara"]}.slc.stt.json'

def set_abi(name, id):
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\ability',name,f'{id}')
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
       
def ability_command(usr_args, sys_args):
    charas = ['chara1','chara2','chara3','chara4','chara5']
    abilities = {'q':'ability1','w':'ability2','a':'ability3','s':'ability4',}
    cur = charas.index(usr_args['chara'])
    mythread.mt.print('ability_command ', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('esc, up, down, q, w, a, s, 1, 2, 3, 4, 5, space, enter', state='KEY')
    key = action.key_input(['esc','up','down','q','w','a','s','1','2','3','4','5','space','enter','p'])
    if usr_args['target'] != 'none':
        sys_args['config'].append(usr_args.copy())
        usr_args['ability'] = 'none'
        usr_args['target'] = 'none'
    if key in ('esc','up','down','q','w','a','s','space','enter','p'):
        if usr_args['ability'] != 'none':
            sys_args['config'].append(usr_args.copy())
            usr_args['ability'] = 'none'
            usr_args['target'] = 'none'
    if key == 'esc':
        sys_args['set_abi\\command.slc.stt.json'] = 'finish'
    elif key == 'up':
        sys_args['set_abi\\command.slc.stt.json'] = 'scroll'
        usr_args['chara'] = charas[(cur-1)%5]
    elif key == 'down':
        sys_args['set_abi\\command.slc.stt.json'] = 'scroll'
        usr_args['chara'] = charas[(cur+1)%5]
    elif key in ('q','w','a','s'):
        sys_args['set_abi\\command.slc.stt.json'] = 'ability'
        usr_args['ability'] = abilities[key]
    elif key in ('1','2','3','4','5'):
        sys_args['set_abi\\command.slc.stt.json'] = 'target'
        usr_args['target'] = 'chara'+key
    elif key == 'space':
        sys_args['set_abi\\command.slc.stt.json'] = 'mode'
        args = {'special':'mode','auto':'auto','burst':'on'}
        sys_args['config'].append(args)
    elif key == 'enter':
        sys_args['set_abi\\command.slc.stt.json'] = 'attack'
        args = {'special':'attack'}
        sys_args['config'].append(args)
    elif key == 'p':
        args = {'special':'syncronize'}
        sys_args['config'].append(args)

def init_party():
    exe = Executer()
    exe.run('party\\head.dmy.stt.json')

def party(usr_args, sys_args, name, id):
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\party',f'{id}',name)
    if os.path.exists(os.path.join(dir,'party.pty.json')):
        use_party(name, id)
    else:
        set_party(name, id)

def use_party(name, id):
    mythread.mt.print(name, state='KEYWORD')
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\party',f'{id}',name)
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
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\party',f'{id}',name)
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

def slot(usr_args, sys_args):
    mythread.mt.print('slot ', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('1 2 3 4 5 6 7 8 9 a b c', state='KEY')
    key = action.key_input(['1','2','3','4','5','6','7','8','9','a','b','c'])
    table = {'a':'10','b':'11','c':'12'}
    if key in table.keys():
        key = table[key]
    usr_args['slot'] = f'slot{key}'

def tab(usr_args, sys_args):
    mythread.mt.print('tab ', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('a b c d e f', state='KEY')
    key = action.key_input(['a','b','c','d','e','f'])
    usr_args['tab'] = key

def preset(usr_args, sys_args):
    mythread.mt.print('preset ', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('1 2 3 4 5 6 7 8 9 a b c', state='KEY')
    key = action.key_input(['1','2','3','4','5','6','7','8','9','a','b','c'])
    table = {'a':'10','b':'11','c':'12'}
    if key in table.keys():
        key = table[key]
    usr_args['preset'] = f'preset{key}'

def story():
    exe = Executer()
    exe.run('story\\head.dmy.stt.json')

def wait(t):
    while datetime.datetime.now().hour < t:
        sleep(10)