from json import dump
import queue
from state import *
import mythread

def page():
    a = Assister('page')
    names = ['main', 'raid', 'rescue', 'item', 'attr', 'epic', 'advent', 
             'acce', 'guild', 'battlefield', 'event', 'challenge']
    a.dmy('head').connect(a.slc('head'))
    a.slc('head').connect('page',manual=DummyState.open('quest\\head'),
        **{name:a.brn('head') for name in names})
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

def main():
    a = Assister('main')
    a.dmy('head').connect(a.slc('scroll\\sc1'))
    a.slc('scroll\\sc1').connect('scroll', sc1=a.slc('position'), sc2=a.man('scroll\\sc2'))
    a.man('scroll\\sc2').connect(a.slc('scroll\\sc2'))
    a.slc('scroll\\sc2').connect('scroll', sc2=a.slc('position'))
    positions = ['pos1','pos2','pos3','pos4']
    a.slc('position').connect('position', 
        **{position:a.man(f'position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'position\\{position}').connect(a.slc('episode'))
    episodes = ['episode1','episode2','episode3','episode4']
    a.slc('episode').connect('episode', 
        **{episode:a.man(f'episode\\{episode}') for episode in episodes})
    for episode in episodes: 
        a.man(f'episode\\{episode}').connect(a.man('ok'))
    a.man('ok').connect(DummyState.open('quest\\head'))
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
    a.brn('top').connect(a.dmy('quest'), a.dmy('event'))
    a.dmy('quest').connect(a.slc('scroll\\sc1'))
    a.dmy('event').connect(a.slc('scroll\\sc1'))
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
    a.slc('type').connect('event_type', 
        advent=DummyState.open('advent\\head'), raid=a.dmy('raid\\head'), union=a.dmy('union\\head'))

    a.dmy('raid\\head').connect(a.brn('raid\\head'))
    a.brn('raid\\head').connect(a.man('raid\\top'))
    a.man('raid\\top').connect(a.brn('raid\\top'))
    a.brn('raid\\top').connect(a.man('raid\\tab'), a.man('raid\\top'))
    a.man('raid\\tab').connect(a.slc('raid\\position'))
    a.slc('raid\\position').connect('event_raid_pos', 
        **{position:a.man(f'raid\\position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'raid\\position\\{position}').connect(DummyState.open('quest\\head'))

    a.dmy('union\\head').connect(a.brn('union\\head'))
    a.brn('union\\head').connect(a.slc('union\\top'))
    a.slc('union\\top').connect('union_type', main=a.man('union\\main'), cross=a.man('union\\cross'))

    a.man('union\\main').connect(a.brn('union\\main'))
    a.brn('union\\main').connect(a.slc('union\\main\\scroll\\sc1'), a.slc('union\\top'))
    a.slc('union\\main\\scroll\\sc1').connect('scroll', sc1=a.slc('union\\main\\position'), sc2=a.man('union\\main\\scroll\\sc2'))
    a.man('union\\main\\scroll\\sc2').connect(a.slc('union\\main\\scroll\\sc2'))
    a.slc('union\\main\\scroll\\sc2').connect('scroll', sc2=a.slc('union\\main\\position'))
    positions = ['pos1','pos2','pos3']
    a.slc('union\\main\\position').connect('position', 
        **{position:a.man(f'union\\main\\position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'union\\main\\position\\{position}').connect(DummyState.open('quest\\head'))

    a.man('union\\cross').connect(a.brn('union\\cross'))
    a.brn('union\\cross').connect(a.slc('union\\cross\\position'), a.slc('union\\top'))
    positions = ['pos1','pos2']
    a.slc('union\\cross\\position').connect('position', 
        **{position:a.man(f'union\\cross\\position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'union\\cross\\position\\{position}').connect(DummyState.open('quest\\head'))

    a.save()
      
def quest():
    a = Assister('quest')
    a.dmy('head').connect(a.brn('start'))

    a.brn('start').connect(
        a.man('start\\surpport'), a.man('start\\red'), a.man('start\\blue'), a.man('start\\recover'))
    a.man('start\\recover').connect(a.brn('start\\recover'))
    a.brn('start\\recover').connect(a.man('start\\ok'))
    a.man('start\\ok').connect(a.brn('start'))
    a.man('start\\red').connect(a.brn('start'))
    a.man('start\\blue').connect(a.brn('start'))    
    a.man('start\\surpport').connect(a.brn('start\\surpport'))
    a.brn('start\\surpport').connect(a.man('partyselect'), a.man('start\\surpport'))
    a.man('partyselect').connect(a.brn('partyselect'))
    a.brn('partyselect').connect(DummyState.open('battle\\head'), a.man('partyselect'))

    a.dmy('result').connect(a.slc('type1'))
    a.slc('type1').connect('type', solo=a.slc('result\\count'), raid=a.man('result\\mvp'), orympia=a.brn('result'))
    a.brn('result').connect(
        a.man('result\\mvp'), a.man('result\\rankup'), a.man('result\\encount'), a.man('result\\aquire'), a.slc('result\\count'),
        a.dmy('retry\\surpport'), a.dmy('retry\\red'), a.dmy('retry\\blue'), a.dmy('retry\\recover'))
    a.man('result\\mvp').connect(a.slc('result\\count'))
    a.man('result\\rankup').connect(a.brn('result'))
    a.man('result\\aquire').connect(a.brn('result'))
    a.slc('result\\count').connect(
        a.slc('result\\count').path(), retry=a.slc('retry'), finish=a.slc('finish'), back=a.man('back'))
    a.man('result\\encount').connect(a.dmy('result\\encount'))
    a.dmy('result\\encount').connect(a.slc('result\\comeback'))
    a.slc('result\\comeback').connect(
        a.slc('result\\comeback').path(), retry=DummyState.open('page\\head'), finish=a.dmy('tail'))
    
    a.slc('retry').connect('result', none=a.man('retry'), once=a.man('back'), union=a.dmy('union'))
    a.man('retry').connect(a.slc('type2'))
    a.slc('type2').connect('type', default=a.brn('retry1'), orympia=a.brn('retry2'))
    a.brn('retry1').connect(
        a.man('start\\surpport'), a.man('start\\red'), a.man('start\\blue'), a.man('start\\recover'),
        a.man('result\\mvp'), a.man('result\\rankup'), a.man('result\\encount'), a.man('result\\aquire'), a.slc('result\\count'))
    a.brn('retry2').connect(
        a.dmy('retry\\surpport'), a.dmy('retry\\red'), a.dmy('retry\\blue'), a.dmy('retry\\recover'), 
        a.man('result\\mvp'), a.man('result\\rankup'), a.man('result\\encount'), a.man('result\\aquire'), a.slc('result\\count'))
    a.dmy('retry\\recover').connect(a.dmy('retry\\start'))
    a.dmy('retry\\red').connect(a.dmy('retry\\start'))
    a.dmy('retry\\blue').connect(a.dmy('retry\\start'))
    a.dmy('retry\\surpport').connect(a.dmy('retry\\start'))
    a.dmy('retry\\start').connect(a.brn('start'))
    
    a.slc('finish').connect('result', none=a.man('finish'), once=a.man('back'), union=a.man('back'))
    a.man('finish').connect(a.brn('finish'))
    a.man('back').connect(a.brn('finish'))
    names = ['main', 'raid', 'rescue', 'item', 'attr', 'epic', 'advent', 
             'acce', 'guild', 'battlefield', 'event', 'challenge', 'cross']
    a.brn('finish').connect(
        *[a.dmy(f'finish\\{name}') for name in names], a.man('finish\\friend'), a.man('finish\\reward'), 
        a.dmy('finish\\mvp'), a.dmy('finish\\rankup'), a.dmy('finish\\encount'), a.dmy('finish\\aquire'), a.dmy('finish\\count'))
    a.man('finish\\friend').connect(a.brn('finish'))
    a.man('finish\\reward').connect(a.brn('finish'))
    for name in names: a.dmy(f'finish\\{name}').connect(a.dmy('finish\\finish'))
    a.dmy('finish\\finish').connect(a.dmy('tail'))
    a.dmy('finish\\mvp').connect(a.brn('result'))
    a.dmy('finish\\rankup').connect(a.brn('result'))
    a.dmy('finish\\encount').connect(a.brn('result'))
    a.dmy('finish\\aquire').connect(a.brn('result'))
    a.dmy('finish\\count').connect(a.brn('result'))

    a.dmy('union').connect(a.man('union\\back'))
    a.man('union\\back').connect(a.brn('union\\back'))
    a.brn('union\\back').connect(a.slc('union\\scroll\\sc1'))
    a.slc('union\\scroll\\sc1').connect('scroll', sc1=a.slc('union\\position'), sc2=a.man('union\\scroll\\sc2'))
    a.man('union\\scroll\\sc2').connect(a.slc('union\\scroll\\sc2'))
    a.slc('union\\scroll\\sc2').connect('scroll', sc2=a.slc('union\\position'))
    positions = ['pos1','pos2','pos3']
    a.slc('union\\position').connect('position', 
        **{position:a.man(f'union\\position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'union\\position\\{position}').connect(DummyState.open('quest\\head'))

    a.save()

def battle():
    a = Assister('battle')
    a.dmy('head').connect(a.slc('team'))
    a.slc('team').connect('team', solo=a.dmy('ability'), multi=a.slc('host1'), random=a.man('multi'))
    a.slc('host1').connect(a.slc('host1').path(), host=a.man('multi'), guest=a.dmy('ability'))
    a.man('multi').connect(a.brn('multi'))
    a.brn('multi').connect(a.slc('host2'), exception=a.man('multi'))
    a.slc('host2').connect(a.slc('host2').path(), host=a.man('copy'), guest=a.man('request'))
    a.man('copy').connect(a.dmy('copy'))
    a.dmy('copy').connect(a.dmy('syncronize'))
    a.dmy('syncronize').connect(a.man('release'))
    a.man('release').connect(a.dmy('ability'))
    a.man('request').connect(a.dmy('ability'))
    a.dmy('ability').connect(a.slc('auto'))

    a.slc('auto').connect(a.slc('auto').path(), default=a.slc('isburst'), changed=a.brn('auto'))
    a.brn('auto').connect(
        a.slc('auto\\ability'), a.slc('auto\\auto'), a.slc('auto\\manual'), DummyState.open('quest\\result'))
    a.slc('auto\\ability').connect('auto', 
        ability=a.slc('isburst'), manual=a.man('auto\\single'), auto=a.man('auto\\double'))
    a.slc('auto\\auto').connect('auto', 
        auto=a.slc('isburst'), ability=a.man('auto\\single'), manual=a.man('auto\\double'))
    a.slc('auto\\manual').connect('auto', 
        manual=a.slc('isburst'), auto=a.man('auto\\single'), ability=a.man('auto\\double'))
    a.man('auto\\single').connect(a.brn('auto'))
    a.man('auto\\double').connect(a.brn('auto'))
    
    a.slc('isburst').connect('burst', default=a.brn('burst'), none=a.brn('attack'))
    a.brn('burst').connect(a.slc('burst\\off'), a.slc('burst\\on'), DummyState.open('quest\\result'))
    a.slc(f'burst\\off').connect('burst', default=a.man('burst\\default'), off=a.brn('attack'), change=a.brn('attack'))
    a.slc(f'burst\\on').connect('burst', default=a.man('burst\\default'), on=a.brn('attack'))
    a.man('burst\\default').connect(a.brn('burst'))
    a.brn('attack').connect(a.slc('target'), DummyState.open('quest\\result'))
    targets = ['target2_1','target2_2','target3_1','target3_2','target3_3']
    a.slc('target').connect('target', default=a.man('attack'),**{target:a.man(f'target\\{target}') for target in targets})
    for target in targets:
        a.man(f'target\\{target}').connect(a.man('attack'))
    a.man('attack').connect(a.brn('except'))
    a.brn('except').connect(a.man('error'), a.slc('target'), a.slc('max'), DummyState.open('quest\\result'))
    a.man('error').connect(a.brn('except'))
    a.slc('max').connect('burst', default=a.brn('except'), change=a.man('max'))
    a.man('max').connect(a.brn('max'))
    a.brn('max').connect(a.man('reload'), DummyState.open('quest\\result'))
    a.man('reload').connect(a.slc('auto'))
    a.dmy('battle').connect(a.brn('except'))
    a.save()

def ability():
    a = Assister('ability')
    a.dmy('pre').connect(a.brn('pre'))
    a.brn('pre').connect(a.dmy('available'), a.dmy('result'))
    a.dmy('available').connect(a.dmy('tail'))
    
    charas = ['chara1','chara2','chara3','chara4','chara5']
    for i in range(1,7):
        a.dmy(f'id{i}\\head').connect(a.brn(f'id{i}\\head'))
        a.brn(f'id{i}\\head').connect(a.slc(f'id{i}\\list'), *[a.slc(f'id{i}\\scroll\\{chara}') for chara in charas], a.dmy('result'))   
        a.slc(f'id{i}\\list').connect('chara', **{chara:a.man(f'id{i}\\list\\{chara}') for chara in charas})
        for chara in charas: 
            a.man(f'id{i}\\list\\{chara}').connect(a.brn(f'id{i}\\list\\{chara}'))
            a.brn(f'id{i}\\list\\{chara}').connect(a.slc(f'id{i}\\scroll\\{chara}'), a.dmy('result'), exception=a.brn(f'id{i}\\head'))

        for j in range(5):
            a.slc(f'id{i}\\scroll\\chara{j+1}').connect('chara',
                **{f'chara{(j-2)%5+1}':a.man(f'id{i}\\scroll\\upper2'),
                   f'chara{(j-1)%5+1}':a.man(f'id{i}\\scroll\\upper1'),
                   f'chara{j+1}':      a.slc(f'chara{j+1}'),
                   f'chara{(j+1)%5+1}':a.man(f'id{i}\\scroll\\lower1'),
                   f'chara{(j+2)%5+1}':a.man(f'id{i}\\scroll\\lower2')})
        a.man(f'id{i}\\scroll\\upper2').connect(a.slc(f'id{i}\\scroll'))
        a.man(f'id{i}\\scroll\\upper1').connect(a.slc(f'id{i}\\scroll'))
        a.man(f'id{i}\\scroll\\lower1').connect(a.slc(f'id{i}\\scroll'))
        a.man(f'id{i}\\scroll\\lower2').connect(a.slc(f'id{i}\\scroll'))
        a.slc(f'id{i}\\scroll').connect('chara', **{chara:a.brn(f'id{i}\\scroll\\{chara}') for chara in charas})
        for chara in charas:
            a.brn(f'id{i}\\scroll\\{chara}').connect(a.slc(f'id{i}\\scroll\\{chara}'), exception=a.brn(f'id{i}\\scroll'))
        a.brn(f'id{i}\\scroll').connect(*[a.slc(f'id{i}\\scroll\\{chara}') for chara in charas], a.dmy('result'))

    
    abis = ['ability1','ability2','ability3','ability4']
    for chara in charas:
        a.slc(chara).connect('ability', **{abi:a.man(f'ability\\{abi}') for abi in abis})
    for abi in abis:
        a.man(f'ability\\{abi}').connect(a.slc('target'))
    a.slc('istarget').connect('target', default=a.brn('istarget'), none=a.dmy('tail'))
    a.brn('istarget').connect(a.slc('target'), a.dmy('result'))
    a.slc('target').connect('target', none=a.dmy('tail'), **{chara:a.man(f'target\\{chara}') for chara in charas})
    for chara in charas:
        a.man(f'target\\{chara}').connect(a.dmy('tail'))

    a.dmy('mode').connect(a.brn('auto'))
    a.brn('auto').connect(
        a.slc('auto\\ability'), a.slc('auto\\auto'), a.slc('auto\\manual'), DummyState.open('quest\\result'), a.dmy('result'))
    a.slc('auto\\ability').connect('auto', 
        ability=a.slc('isburst'), manual=a.man('auto\\single'), auto=a.man('auto\\double'))
    a.slc('auto\\auto').connect('auto', 
        auto=a.slc('isburst'), ability=a.man('auto\\single'), manual=a.man('auto\\double'))
    a.slc('auto\\manual').connect('auto', 
        manual=a.slc('isburst'), auto=a.man('auto\\single'), ability=a.man('auto\\double'))
    a.man('auto\\single').connect(a.brn('auto'))
    a.man('auto\\double').connect(a.brn('auto'))
    
    bursts = ['off', 'on']
    a.slc('isburst').connect('burst', default=a.brn('burst'), none=a.dmy('tail'))
    a.brn('burst').connect(*[a.slc(f'burst\\{burst}') for burst in bursts], a.dmy('result'))
    for burst in bursts:
        a.slc(f'burst\\{burst}').connect('burst', default=a.man('burst\\default'), **{burst:a.dmy('tail')})
    a.man('burst\\default').connect(a.brn('burst'))

    a.dmy('attack').connect(a.man('attack'))
    a.man('attack').connect(a.brn('attack'))
    a.brn('attack').connect(a.dmy('canccel'), a.dmy('result'), exception=a.man('reload'))
    a.dmy('canccel').connect(a.brn('attack'))
    a.man('reload').connect(a.brn('reload'))
    a.brn('reload').connect(a.dmy('available'), a.dmy('result'))

    a.dmy('enemy').connect(a.slc('enemy'))
    enemies = ['enemy2_1','enemy2_2','enemy3_1','enemy3_2','enemy3_3']
    a.slc('enemy').connect('enemy', default=a.dmy('tail'),**{enemy:a.man(f'enemy\\{enemy}') for enemy in enemies})
    for enemy in enemies:
        a.man(f'enemy\\{enemy}').connect(a.dmy('tail'))    
    
    a.save()

def set_abi():
    a = Assister('set_abi')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('capture'))
    a.man('capture').connect(a.slc('command'))
    a.slc('command').connect(a.slc('command').path(), 
        finish=a.dmy('tail'), scroll=a.brn('scroll'), ability=a.slc('ability'), target=a.slc('target'),
        mode=a.dmy('mode'), attack=a.dmy('attack'))
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

    autos = ['manual', 'auto', 'ability']
    a.dmy('mode').connect(a.brn('auto'))
    a.brn('auto').connect(*[a.dmy(f'auto\\{auto}') for auto in autos])
    for auto in autos:
        if auto == 'auto':
            a.dmy(f'auto\\{auto}').connect(a.brn('burst'))
        else:
            a.dmy(f'auto\\{auto}').connect(a.man('auto\\default'))
    a.man('auto\\default').connect(a.brn('auto'))
    a.brn('burst').connect(a.dmy(f'burst\\on'),a.dmy(f'burst\\off'))
    a.dmy('burst\\on').connect(a.slc('command'))
    a.dmy('burst\\off').connect(a.man('burst\\default'))
    a.man('burst\\default').connect(a.brn('burst'))

    a.dmy('attack').connect(a.man('attack'))
    a.man('attack').connect(a.brn('attack'))
    a.brn('attack').connect(a.dmy('canccel'), exception=a.man('reload'))
    a.dmy('canccel').connect(a.brn('attack'))
    a.man('reload').connect(a.slc('command'))

    a.save()

def party():
    a = Assister('party')
    a.dmy('head').connect(a.man('sleep1'))
    a.man('sleep1').connect(a.slc('check1'))
    a.slc('check1').connect(a.slc('check1').path(), **{f'id{i}':a.brn(f'check1\\id{i}') for i in range(1,7)})
    for i in range(1,7):
        a.brn(f'check1\\id{i}').connect(a.dmy(f'id{i}\\party'), exception=a.slc('slot'))
    a.slc('slot').connect('slot', **{f'slot{i}':a.man(f'slot\\slot{i}') for i in range(1,13)})
    for i in range(1,13):
        a.man(f'slot\\slot{i}').connect(a.man('sleep2'))
    a.man('sleep2').connect(a.slc('check2'))
    a.slc('check2').connect(a.slc('check2').path(), **{f'id{i}':a.brn(f'check2\\id{i}') for i in range(1,7)})
    for i in range(1,7):
        a.brn(f'check2\\id{i}').connect(a.dmy(f'id{i}\\party'), exception=a.man('select'))
    a.man('select').connect(a.brn('select'))
    a.brn('select').connect(a.slc('tab'),a.man('sleep2'))
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
    a.brn('ok').connect(a.man('sleep2'))
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

def gacha_raid():
    a = Assister('gacha_raid')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('try1'))
    a.man('try1').connect(a.brn('try1'))
    a.brn('try1').connect(a.man('try2'))
    a.man('try2').connect(a.brn('try2'))
    a.brn('try2').connect(a.man('try2'))
    a.save()

def story():
    a = Assister('story')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('newquest'), a.man('pos1'))
    a.man('pos1').connect(a.brn('pos1'))
    a.brn('pos1').connect(a.man('surpport'), a.man('skip'), a.man('recover'), a.man('tail'), a.man('pos1'))
    a.man('recover').connect(a.brn('recover'))
    a.brn('recover').connect(a.man('ok'))
    a.man('ok').connect(a.brn('pos1'))
    a.man('skip').connect(a.brn('skip'))
    a.brn('skip').connect(a.man('summary'), a.man('skip'))
    a.man('summary').connect(a.brn('summary'))
    a.brn('summary').connect(a.man('result'), a.man('attack'), a.man('harem'), a.man('summary'), a.man('skip'))
    a.man('harem').connect(a.brn('harem'))
    a.brn('harem').connect(a.man('skipharem'), a.man('harem'))
    a.man('skipharem').connect(a.brn('skipharem'))
    a.brn('skipharem').connect(a.man('result'), a.man('skipharem'))
    a.man('surpport').connect(a.brn('surpport'))
    a.brn('surpport').connect(a.man('partyselect'), a.man('surpport'))
    a.man('partyselect').connect(a.brn('partyselect'))
    a.brn('partyselect').connect(a.man('attack'), a.man('partyselect'), a.man('skip'))
    a.man('attack').connect(a.brn('attack'))
    a.brn('attack').connect(a.man('result'), a.man('skip'), a.man('attack'))
    a.man('result').connect(a.brn('result'))
    a.brn('result').connect(a.man('surpport'), a.man('newitem'), a.man('reward'), a.man('rankup'), a.man('result'), a.man('skip'))
    a.man('newitem').connect(a.brn('result'))
    a.man('rankup').connect(a.brn('result'))
    a.man('reward').connect(a.brn('reward'))
    a.brn('reward').connect(a.man('newquest'), a.man('result'))
    a.man('newquest').connect(a.brn('head'))
    a.save()

def tmp():
    page()
    main()
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
    gacha_raid()
    story()

if __name__=="__main__":
    q = queue.Queue()
    q.put(tmp)
    mythread.mt = mythread.MyThread(q=q)
    mythread.mt.start()