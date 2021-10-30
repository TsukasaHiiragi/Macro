import queue
from state import *
import mythread

def page():
    a = Assister('page')
    names = ['main', 'raid', 'rescue', 'item', 'attr', 'epic', 'advent', 
             'acce', 'guild', 'battlefield', 'event', 'challenge']
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.slc('potal'), *[a.slc(name) for name in names], exception=a.man('default'))
    a.slc('potal').connect('page', **{name:a.man(f'potal\\{name}') for name in names})
    for name in names:
        a.man(f'potal\\{name}').connect(a.brn('head'))
        a.slc(name).connect(
            'page',
            default=a.man('default'),
            **{name:DummyState.open(f'{name}\\head')})
    a.man('default').connect(a.brn('head'))
    a.save()

def raid():
    a = Assister('raid')
    a.dmy('head').connect(a.slc('attr'))
    attrs = ['fire','aqua','wind','volt','ray','dark','phantom']
    a.slc('attr').connect('attr', **{attr:a.man(f'attr\\{attr}') for attr in attrs})
    for attr in attrs: a.man(f'attr\\{attr}').connect(a.slc('scroll\\sc1'))
    a.slc('scroll\\sc1').connect('scroll', sc1=a.slc('position'), sc2=a.man('scroll\\sc2'))
    a.man('scroll\\sc2').connect(a.slc('scroll\\sc2'))
    a.slc('scroll\\sc2').connect('scroll', sc2=a.slc('position'))
    positions = ['pos1','pos2','pos3','pos4']
    a.slc('position').connect('position', 
        **{position:a.man(f'position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'position\\{position}').connect(DummyState.open('quest\\head'))
    a.save()

def rescue():
    a = Assister('rescue')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('random'), a.dmy('id'))
    a.man('random').connect(a.brn('head'))
    a.dmy('id').connect(a.man('id'))
    a.man('id').connect(a.brn('id'))
    a.brn('id').connect(a.man('id'), a.man('raid'))
    a.man('raid').connect(DummyState.open('quest\\head'))
    a.save()

def attr():
    a = Assister('attr')
    a.dmy('head').connect(a.slc('attr'))
    attrs = ['fire','aqua','wind','volt','ray','dark','all']
    a.slc('attr').connect('attr', **{attr:a.man(f'attr\\{attr}') for attr in attrs})
    for attr in attrs: a.man(f'attr\\{attr}').connect(a.slc('scroll\\sc1'))
    a.slc('scroll\\sc1').connect('scroll', sc1=a.slc('position'), sc2=a.man('scroll\\sc2'))
    a.man('scroll\\sc2').connect(a.slc('scroll\\sc2'))
    a.slc('scroll\\sc2').connect('scroll', sc2=a.slc('position'))
    positions = ['pos1','pos2','pos3','pos4']
    a.slc('position').connect('position', 
        **{position:a.man(f'position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'position\\{position}').connect(DummyState.open('quest\\head'))
    a.save()

def item():
    a = Assister('item')
    a.dmy('head').connect(a.slc('item'))
    items = ['exp','weapon','genju','gem']
    a.slc('item').connect('item', **{item:a.man(f'item\\{item}') for item in items})
    for item in items: a.man(f'item\\{item}').connect(a.slc('position'))
    positions = ['pos1','pos2','pos3','pos4']
    a.slc('position').connect('position', 
        **{position:a.man(f'position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'position\\{position}').connect(DummyState.open('quest\\head'))
    a.save()

def acce():
    a = Assister('acce')
    a.dmy('head').connect(a.slc('attr'))
    attrs = ['fire','aqua','wind','volt','ray','dark','all']
    a.slc('attr').connect('attr', **{attr:a.man(f'attr\\{attr}') for attr in attrs})
    for attr in attrs: a.man(f'attr\\{attr}').connect(a.slc('scroll\\sc1'))
    a.slc('scroll\\sc1').connect('scroll', sc1=a.slc('position'), sc2=a.man('scroll\\sc2'))
    a.man('scroll\\sc2').connect(a.slc('scroll\\sc2'))
    a.slc('scroll\\sc2').connect('scroll', sc2=a.slc('position'))
    positions = ['pos1','pos2','pos3','pos4']
    a.slc('position').connect('position', 
        **{position:a.man(f'position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'position\\{position}').connect(DummyState.open('quest\\head'))
    a.save()

def advent():
    a = Assister('advent')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('top1'), a.man('top2'))
    a.man('top1').connect(a.brn('top'))
    a.man('top2').connect(a.brn('top'))
    a.brn('top').connect(a.dmy('quest'))
    a.dmy('quest').connect(a.slc('scroll\\sc1'))
    a.slc('scroll\\sc1').connect('scroll', sc1=a.slc('position'), sc2=a.man('scroll\\sc2'))
    a.man('scroll\\sc2').connect(a.slc('scroll\\sc2'))
    a.slc('scroll\\sc2').connect('scroll', sc2=a.slc('position'))
    positions = ['pos1','pos2','pos3','pos4']
    a.slc('position').connect('position', 
        **{position:a.man(f'position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'position\\{position}').connect(DummyState.open('quest\\head'))
    a.save()

def event():
    a = Assister('event')
    a.dmy('head').connect(a.slc('position'))
    positions = ['pos1','pos2','pos3']
    a.slc('position').connect('event_pos', 
        **{position:a.man(f'position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'position\\{position}').connect(a.slc('type'))
    a.slc('type').connect('event_type', advent=DummyState.open('advent\\head'), raid=a.dmy('raid\\head'))
    a.dmy('raid\\head').connect(a.brn('raid\\head'))
    a.brn('raid\\head').connect(a.man('raid\\top'))
    a.man('raid\\top').connect(a.brn('raid\\top'))
    a.brn('raid\\top').connect(a.man('raid\\tab'))
    a.man('raid\\tab').connect(a.slc('raid\\position'))
    a.slc('raid\\position').connect('event_raid_pos', 
        **{position:a.man(f'raid\\position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'raid\\position\\{position}').connect(DummyState.open('quest\\head'))
    a.save()
      
def quest():
    a = Assister('quest')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('recover'), a.man('red'), a.man('blue'), a.man('surpport'),
        a.man('friend'), a.man('reward'), a.man('mvp'), a.man('rankup'), a.man('aquire'), a.man('encount'), a.slc('count'))
    a.man('recover').connect(a.brn('recover'))
    a.brn('recover').connect(a.man('ok'))
    a.man('ok').connect(a.brn('head'))
    a.man('red').connect(a.brn('head'))
    a.man('blue').connect(a.brn('head'))    
    a.man('surpport').connect(a.brn('surpport'))
    a.brn('surpport').connect(a.man('partyselect'), a.man('surpport'))
    a.man('partyselect').connect(a.brn('partyselect'))
    a.brn('partyselect').connect(DummyState.open('battle\\head'), a.man('partyselect'))

    a.dmy('result').connect(a.brn('result'))
    a.brn('result').connect(
        a.man('mvp'), a.man('rankup'), a.man('encount'), a.man('aquire'), a.slc('count'))
    a.man('mvp').connect(a.brn('result'))
    a.man('rankup').connect(a.brn('result'))
    a.man('aquire').connect(a.brn('result'))
    a.man('encount').connect(a.brn('result'))
    a.slc('count').connect(
        a.slc('count').path(), retry=a.man('retry'), finish=a.man('finish'), back=a.man('back'))
    a.man('retry').connect(a.brn('head'))
    a.man('finish').connect(a.brn('finish'))
    a.man('back').connect(a.brn('finish'))
    names = ['main', 'raid', 'rescue', 'item', 'attr', 'epic', 'advent', 
             'acce', 'guild', 'battlefield', 'event', 'challenge']
    a.brn('finish').connect(a.man('friend'), a.man('reward'), a.man('mvp'), a.man('rankup'), 
        a.man('aquire'), a.man('encount'), a.slc('count'), *[a.dmy(name) for name in names])
    a.man('friend').connect(a.brn('finish'))
    a.man('reward').connect(a.brn('finish'))
    for name in names: a.dmy(name).connect(a.dmy('finish'))
    a.save()

def battle():
    a = Assister('battle')
    a.dmy('head').connect(a.slc('host'))
    a.slc('host').connect(a.slc('host').path(), host=a.slc('team'), guest=a.dmy('ability'))
    a.slc('team').connect('team', solo=a.dmy('ability'), multi=a.man('multi'))
    a.man('multi').connect(a.brn('multi'))
    a.brn('multi').connect(a.man('request'), exception=a.man('multi'))
    a.man('request').connect(a.dmy('request'))
    a.dmy('request').connect(a.dmy('syncronize'))
    a.dmy('syncronize').connect(a.dmy('release'))
    a.dmy('release').connect(a.dmy('ability'))
    a.dmy('ability').connect(a.brn('auto'))
    autos = ['manual', 'auto', 'ability']
    a.brn('auto').connect(*[a.slc(f'auto\\{auto}') for auto in autos])
    for auto in autos:
        a.slc(f'auto\\{auto}').connect('auto', default=a.man('auto\\default'), **{auto:a.brn('burst')})
    a.man('auto\\default').connect(a.brn('auto'))
    bursts = ['on', 'off']
    a.brn('burst').connect(*[a.slc(f'burst\\{burst}') for burst in bursts])
    for burst in bursts:
        a.slc(f'burst\\{burst}').connect('burst', default=a.man('burst\\default'), **{burst:a.brn('except')})
    a.man('burst\\default').connect(a.brn('burst'))
    a.brn('except').connect(
        a.man('attack'), a.dmy('battle'), DummyState.open('quest\\result'))
    a.man('attack').connect(a.brn('except'))
    a.dmy('battle').connect(a.brn('except'))
    a.save()

def ability():
    a = Assister('ability')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.slc('id'))
    a.slc('id').connect(a.slc('id').path(), **{f'id{i}':a.brn(f'id{i}\\head') for i in range(1,7)})
    charas = ['chara1','chara2','chara3','chara4','chara5']
    for i in range(1,7):
        a.brn(f'id{i}\\head').connect(a.slc(f'id{i}\\list'), a.brn(f'id{i}\\scroll'))   
        a.slc(f'id{i}\\list').connect('chara', **{chara:a.man(f'id{i}\\list\\{chara}') for chara in charas})
        for chara in charas: a.man(f'id{i}\\list\\{chara}').connect(a.brn(f'id{i}\\head'))
        a.brn(f'id{i}\\scroll').connect(*[a.slc(f'id{i}\\scroll\\{chara}') for chara in charas])
        for j in range(5):
            a.slc(f'id{i}\\scroll\\chara{j+1}').connect('chara',
                **{f'chara{(j-2)%5+1}':a.man(f'id{i}\\scroll\\upper2'),
                   f'chara{(j-1)%5+1}':a.man(f'id{i}\\scroll\\upper1'),
                   f'chara{j+1}':      a.slc(f'chara{j+1}'),
                   f'chara{(j+1)%5+1}':a.man(f'id{i}\\scroll\\lower1'),
                   f'chara{(j+2)%5+1}':a.man(f'id{i}\\scroll\\lower2')},)
        a.man(f'id{i}\\scroll\\upper2').connect(a.brn(f'id{i}\\scroll'))
        a.man(f'id{i}\\scroll\\upper1').connect(a.brn(f'id{i}\\scroll'))
        a.man(f'id{i}\\scroll\\lower1').connect(a.brn(f'id{i}\\scroll'))
        a.man(f'id{i}\\scroll\\lower2').connect(a.brn(f'id{i}\\scroll'))
    abis = ['ability1','ability2','ability3','ability4']
    for chara in charas:
        a.slc(chara).connect('ability', **{abi:a.man(f'ability\\{abi}') for abi in abis})
    for abi in abis:
        a.man(f'ability\\{abi}').connect(a.slc('target'))
    a.slc('istarget').connect('target', default=a.brn('istarget'), none=a.dmy('tail'))
    a.brn('istarget').connect(a.slc('target'))
    a.slc('target').connect('target', none=a.dmy('tail'), **{chara:a.man(f'target\\{chara}') for chara in charas})
    for chara in charas:
        a.man(f'target\\{chara}').connect(a.dmy('tail'))
    a.save()

def set_abi():
    a = Assister('set_abi')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('capture'))
    a.man('capture').connect(a.slc('command'))
    a.slc('command').connect(a.slc('command').path(), 
        finish=a.dmy('tail'), scroll=a.brn('scroll'), ability=a.slc('ability'), target=a.slc('target'))
    charas = ['chara1','chara2','chara3','chara4','chara5']
    a.brn('scroll').connect(*[a.slc(f'scroll\\{chara}') for chara in charas])
    for i in range(5):
        a.slc(f'scroll\\chara{i+1}').connect('chara',
            **{f'chara{(i-2)%5+1}':a.man('scroll\\upper2'),
               f'chara{(i-1)%5+1}':a.man('scroll\\upper1'),
               f'chara{i+1}'      :a.slc('command'),
               f'chara{(i+1)%5+1}':a.man('scroll\\lower1'),
               f'chara{(i+2)%5+1}':a.man('scroll\\lower2')},)
    a.man('scroll\\upper2').connect(a.slc('command'))
    a.man('scroll\\upper1').connect(a.slc('command'))
    a.man('scroll\\lower1').connect(a.slc('command'))
    a.man('scroll\\lower2').connect(a.slc('command'))
    abis = ['ability1','ability2','ability3','ability4']
    a.slc('ability').connect('ability', none=a.slc('command'), **{abi:a.man(f'ability\\{abi}') for abi in abis})
    for abi in abis:
        a.man(f'ability\\{abi}').connect(a.slc('command'))
    a.slc('target').connect('target', **{chara:a.man(f'target\\{chara}') for chara in charas})
    for chara in charas:
        a.man(f'target\\{chara}').connect(a.slc('command'))
    a.save()

def party():
    a = Assister('party')
    a.dmy('head').connect(a.slc('check1'))
    a.slc('check1').connect(a.slc('check1').path(), **{f'id{i}':a.brn(f'check1\\id{i}') for i in range(1,7)})
    for i in range(1,7):
        a.brn(f'check1\\id{i}').connect(a.dmy(f'id{i}\\party'), exception=a.slc('slot'))
    a.slc('slot').connect('slot', **{f'slot{i}':a.man(f'slot\\slot{i}') for i in range(1,13)})
    for i in range(1,13):
        a.man(f'slot\\slot{i}').connect(a.slc('check2'))
    a.slc('check2').connect(a.slc('check2').path(), **{f'id{i}':a.brn(f'check2\\id{i}') for i in range(1,7)})
    for i in range(1,7):
        a.brn(f'check2\\id{i}').connect(a.dmy(f'id{i}\\party'), exception=a.man('select'))
    a.man('select').connect(a.brn('select'))
    a.brn('select').connect(a.slc('tab'))
    tabs = ['a','b','c','d','e','f']
    a.slc('tab').connect('tab', **{tab:a.man(f'tab\\{tab}') for tab in tabs})
    for tab in tabs:
        a.man(f'tab\\{tab}').connect(a.slc('preset'))
    a.slc('preset').connect('preset', **{f'preset{i}':a.man(f'preset\\preset{i}') for i in range(1,13)})
    for i in range(1,13):
        a.man(f'preset\\preset{i}').connect(a.man('call'))
    a.man('call').connect(a.brn('call'))
    a.brn('call').connect(a.man('ok'))
    a.man('ok').connect(a.brn('ok'))
    a.brn('ok').connect(a.slc('check2'))
    for i in range(1,7):
        a.dmy(f'id{i}\\party').connect(a.dmy('tail'))
    a.save()

def set_party():
    a = Assister('set_party')
    a.dmy('head').connect(a.slc('slot'))
    a.slc('slot').connect('slot', **{f'slot{i}':a.man(f'slot\\slot{i}') for i in range(1,13)})
    for i in range(1,13):
        a.man(f'slot\\slot{i}').connect(a.man('select'))
    a.man('select').connect(a.brn('select'))
    a.brn('select').connect(a.slc('tab'))
    tabs = ['a','b','c','d','e','f']
    a.slc('tab').connect('tab', **{tab:a.man(f'tab\\{tab}') for tab in tabs})
    for tab in tabs:
        a.man(f'tab\\{tab}').connect(a.slc('preset'))
    a.slc('preset').connect('preset', **{f'preset{i}':a.man(f'preset\\preset{i}') for i in range(1,13)})
    for i in range(1,13):
        a.man(f'preset\\preset{i}').connect(a.man('call'))
    a.man('call').connect(a.brn('call'))
    a.brn('call').connect(a.man('ok'))
    a.man('ok').connect(a.brn('ok'))
    a.brn('ok').connect(a.man('capture'))
    a.man('capture').connect(a.dmy('tail'))
    a.save()

def tmp():
    page()
    raid()
    rescue()
    attr()
    item()
    acce()
    advent()
    event()
    quest()
    battle()
    ability()
    set_abi()
    party()
    set_party()

if __name__=="__main__":
    q = queue.Queue()
    q.put(tmp)
    mythread.mt = mythread.MyThread(q=q)
    mythread.mt.start()