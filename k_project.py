import json
import os
import queue

from state import Executer
import mythread
import utility
import action
import image

def quest(name, trial, key, n):
    path = os.path.join('quest',f'{name}.qst.json')
    if os.path.exists(path):
        with utility.openx(path, 'rt') as f:
            args = json.load(f)
    else: args = {}
    mythread.mt.text(trial=(0,trial))
    exe = Executer()
    exe.sys_args['battle\\host.slc.stt.json'] = 'host'
    exe.set_trigger('quest\\result.dmy.stt.json', counter, trial=trial)
    exe.set_trigger('battle\\request.dmy.stt.json', syncronize, key=key, n=n)
    exe.run('page\\head.dmy.stt.json', **args)
    with utility.openx(path, 'wt') as f:
        json.dump(exe.usr_args, f, indent=2)

def counter(usr_args, sys_args, trial):
    if 'n_try' not in sys_args:
        sys_args['n_try'] = 0
    sys_args['n_try'] += 1
    mythread.mt.text(trial=(sys_args['n_try'],trial))
    if sys_args['n_try'] >= trial:
        sys_args['quest\\count.slc.stt.json'] = 'finish'
    else:
        sys_args['quest\\count.slc.stt.json'] = 'retry'

def syncronize(usr_args, sys_args, key, n):
    mythread.mt.syncronize(key, n)

def rescue(name, trial, key, n):
    path = os.path.join('quest',f'{name}.qst.json')
    if os.path.exists(path):
        with utility.openx(path, 'rt') as f:
            args = json.load(f)
    else: args = {}
    args['page'] = 'rescue'
    mythread.mt.text(trial=(0,trial))
    exe = Executer()
    exe.sys_args['battle\\host.slc.stt.json'] = 'guest'
    exe.sys_args['quest\\count.slc.stt.json'] = 'back'
    exe.set_trigger('rescue\\id.dmy.stt.json', syncronize, key=key, n=n)
    for i in range(trial):
        exe.run('page\\head.dmy.stt.json', **args)
        mythread.mt.text(trial=(i+1,trial))

def ability(name, id):
    dir = os.path.join('C:\\Users\\miyas\\Macro\\ability',f'{id}',name)
    symbol:image.LeafSymbol = image.Symbol.load('ability\\list')
    symbol.image_path = os.path.join(dir,'img','list.png')
    symbol.save('ability\\list')
    charas = ['chara1','chara2','chara3','chara4','chara5']
    for chara in charas:
        symbol:image.LeafSymbol = image.Symbol.load(f'ability\\scroll\\{chara}')
        symbol.image_path = os.path.join(dir,'img',f'{chara}.png')
        symbol.save(f'ability\\scroll\\{chara}')
    with utility.openx(os.path.join(dir,'ability.abi.json'), 'rt') as f:
        abilities = json.load(f)

    exe = Executer()
    path = 'ability\\head.dmy.stt.json' 
    for abi in abilities:
        exe.run(path, **abi)
        path = f'ability\\scroll\\{abi["chara"]}.slc.stt.json'

def set_abi(name, id):
    dir = os.path.join('C:\\Users\\miyas\\Macro\\ability',f'{id}',name)
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
    mythread.mt.print('ability_command', state='KEYWORD', end='')
    mythread.mt.print('input command', state='INPUT')
    mythread.mt.print('esc, up, down, q, w, a, s, 1, 2, 3, 4, 5', state='KEY')
    key = action.key_input(['esc','up','down','q','w','a','s','1','2','3','4','5'])
    if usr_args['target'] != 'none':
        sys_args['config'].append(usr_args.copy())
        usr_args['ability'] = 'none'
        usr_args['target'] = 'none'
    if key in ('esc','up','down','q','w','a','s'):
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

def party(name, id):
    mythread.mt.print(name, state='KEYWORD')
    dir = os.path.join('C:\\Users\\miyas\\Macro\\party',f'{id}',name)
    symbol:image.LeafSymbol = image.Symbol.load(f'party\\party')
    symbol.image_path = os.path.join(dir,'party.png')
    symbol.save(f'party\\party')
    with utility.openx(os.path.join(dir,'party.pty.json'), 'rt') as f:
        party = json.load(f)
    exe = Executer()
    exe.run('party\\head.dmy.stt.json', **party)

def set_party(name, id):
    mythread.mt.print(name, state='KEYWORD')
    dir = os.path.join('C:\\Users\\miyas\\Macro\\party',f'{id}',name)
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

if __name__=="__main__":
    q = queue.Queue()
    q1 = queue.Queue()
    q2 = queue.Queue()
    q3 = queue.Queue()
    q4 = queue.Queue()
    q5 = queue.Queue()
    q6 = queue.Queue()
    q1.put(mythread.Function(quest, 'event\\advent\\rag', 25, 'uuid', 1))
    q2.put(mythread.Function(quest, 'event\\advent\\rag', 25, 'uuid', 1))
    q3.put(mythread.Function(quest, 'event\\advent\\rag', 25, 'uuid', 1))
    q4.put(mythread.Function(quest, 'event\\advent\\rag', 25, 'uuid', 1))
    q5.put(mythread.Function(quest, 'event\\advent\\rag', 25, 'uuid', 1))
    q6.put(mythread.Function(quest, 'event\\advent\\rag', 25, 'uuid', 1))

    q.put(mythread.Function(set_party, 'aqua\\attack', 2))
    q.put(mythread.Function(set_party, 'volt\\attack', 2))
    q.put(mythread.Function(set_party, 'fire\\attack', 2))
    q.put(mythread.Function(set_party, 'wind\\attack', 2))
    q.put(mythread.Function(set_party, 'dark\\attack', 2))
    q.put(mythread.Function(set_party, 'ray\\attack', 2))
    q.put(mythread.Function(set_party, 'aqua\\deffense', 2))
    q.put(mythread.Function(set_party, 'volt\\deffense', 2))
    q.put(mythread.Function(set_party, 'fire\\deffense', 2))
    q.put(mythread.Function(set_party, 'wind\\deffense', 2))
    q.put(mythread.Function(set_party, 'dark\\deffense', 2))
    q.put(mythread.Function(set_party, 'ray\\deffense', 2))

    r = queue.Queue()
    r.put(mythread.Function(quest, 'item\\exp', 30, 'uuid', 1))

    # mythread.mt = mythread.MyThread(qs=[q1,q2,q3,q4,q5,q6])
    mythread.mt = mythread.MyThread(q=q)
    mythread.mt.start()