import json
import os
import queue

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
    exe.sys_args['battle\\host.slc.stt.json'] = 'host'
    exe.set_trigger('quest\\result.dmy.stt.json', counter, trial=trial)
    exe.set_trigger('battle\\request.man.stt.json', cripboard_aquire)
    exe.set_trigger('battle\\request.dmy.stt.json', syncronize, key=key, members=members)
    exe.set_trigger('battle\\syncronize.dmy.stt.json', syncronize, key=key, members=members)
    exe.set_trigger('battle\\release.dmy.stt.json', cripboard_release)
    if party_name:
        exe.set_trigger('quest\\partyselect.man.stt.json', party, name=party_name, id=id)
    if ability_name:
        exe.set_trigger('battle\\ability.dmy.stt.json', ability, name=ability_name, id=id, key=key, members=members)
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

def syncronize(usr_args, sys_args, key, members):
    mythread.mt.syncronize(key, members)

def cripboard_aquire(usr_args, sys_args):
    mythread.mt.cripboard_aquire()

def cripboard_release(usr_args, sys_args):
    mythread.mt.cripboard_release()

def rescue(id, name, trial, key, members, party_name=None, ability_name=None):
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
    exe.set_trigger('rescue\\id.dmy.stt.json', syncronize, key=key, members=members)
    exe.set_trigger('rescue\\raid.man.stt.json', syncronize, key=key, members=members)
    if party_name:
        exe.set_trigger('quest\\partyselect.man.stt.json', party, name=party_name, id=id)
    if ability_name:
        exe.set_trigger('battle\\ability.dmy.stt.json', ability, name=ability_name, id=id, key=key, members=members)
    for i in range(trial):
        exe.run('page\\head.dmy.stt.json', **args)
        mythread.mt.text(trial=(i+1,trial))

def init_ability():
    exe = Executer()
    exe.run('ability\\head.dmy.stt.json', chara='chara1')

def ability(usr_args, sys_args, name, id, key, members):
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\ability',f'{id}',name)
    if os.path.exists(os.path.join(dir,'ability.abi.json')):
        use_ability(name, id, key, members)
    else:
        set_abi(name, id)

def use_ability(name, id, key, members):
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\ability',f'{id}',name)
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
    exe.set_trigger('ability\\id.slc.stt.json', syncronize, key=key, members=members)
    exe.sys_args['ability\\id.slc.stt.json'] = f'id{id}'
    path = 'ability\\head.dmy.stt.json' 
    for abi in abilities:
        exe.run(path, **abi)
        path = f'ability\\id{id}\\scroll\\{abi["chara"]}.slc.stt.json'

def set_abi(name, id):
    dir = os.path.join('C:\\Users\\tsuka\\Macro\\ability',f'{id}',name)
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

if __name__=="__main__":
    q = queue.Queue()
    qs = [None]*6
    attrs = ['fire','aqua','wind','volt','ray','dark']

    for i in range(6):
        qs[i] = queue.Queue()
    for i in range(3):
        for attr in attrs:
            qs[2*i  ].put(mythread.Function(quest,  2*i+1, f'raid\\catas\\ult\\{attr}', 3, f'uuid{i}', 2, party_name='media2', ability_name='media2_2'))
            qs[2*i+1].put(mythread.Function(rescue, 2*i+2, f'raid\\catas\\ult\\{attr}', 3, f'uuid{i}', 2, party_name='media2', ability_name='media2_2'))
    for i in range(3):   
        for attr in attrs:
            qs[2*i  ].put(mythread.Function(rescue, 2*i+1, f'raid\\catas\\ult\\{attr}', 3, f'uuid{i}', 2, party_name='media2', ability_name='media2_2'))
            qs[2*i+1].put(mythread.Function(quest,  2*i+2, f'raid\\catas\\ult\\{attr}', 3, f'uuid{i}', 2, party_name='media2', ability_name='media2_2'))
    for i in range(6):
        for attr in attrs:
            qs[i].put(mythread.Function(quest, f'raid\\disa\\st\\{attr}', 1, f'uuid{i}', 1))
        for attr in attrs:
            qs[i].put(mythread.Function(quest, f'raid\\disa\\ex\\{attr}', 1, f'uuid{i}', 1))     

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
    r.put(mythread.Function(quest, 6, 'raid\\orympia\\rag\\volt', 1, 'uuid', 1))

    """
    for i in range(3):
        qs[2*i  ].put(mythread.Function(quest,  2*i+1, 'event\\raid\\rag', 100, f'uuid{i}', 2, party_name='media2', ability_name='media2_2'))
        qs[2*i+1].put(mythread.Function(rescue, 2*i+2, 'event\\raid\\rag', 100, f'uuid{i}', 2, party_name='media2', ability_name='media2_2'))
        qs[2*i  ].put(mythread.Function(rescue, 2*i+1, 'event\\raid\\rag', 100, f'uuid{i}', 2, party_name='media2', ability_name='media2_2'))
        qs[2*i+1].put(mythread.Function(quest,  2*i+2, 'event\\raid\\rag', 100, f'uuid{i}', 2, party_name='media2', ability_name='media2_2'))
    """
    mythread.mt = mythread.MyThread(qs=qs)
    # mythread.mt = mythread.MyThread(q=r)
    mythread.mt.start()