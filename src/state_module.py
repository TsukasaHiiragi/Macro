from json import dump
import queue
from state import *
import mythread

def page():
    a = Assister('page')
    names = ['main', 'raid', 'rescue', 'receive', 'item', 'attr', 'epic', 'advent', 
             'acce', 'guild', 'battlefield', 'event', 'challenge']
    a.dmy('head').connect(a.slc('count'))
    a.slc('count').connect(a.slc('count').path(), finish=a.dmy('tail'), retry=a.slc('head'))
    a.slc('head').connect('page', manual=DummyState.open('quest\\head'), default=a.brn('head'))
    a.brn('head').connect(a.slc('potal'), a.slc('rescue'), a.man('restart'), exception=a.man('default'))
    a.man('restart').connect(a.brn('restart'))
    a.brn('restart').connect(DummyState.open('restore\\battle\\head'), a.man('restart'))
    a.slc('potal').connect('page', **{name:a.man(f'potal\\{name}') for name in names})
    a.slc('rescue').connect('page', rescue=a.dmy('rescue'), default=a.man('default'))
    for name in names:
        a.man(f'potal\\{name}').connect(a.brn(name))
        a.brn(name).connect(a.man('retire'), a.dmy(name), exception=a.man('default'))
        a.dmy(name).connect(DummyState.open(f'{name}\\head'))
    a.man('retire').connect(a.brn('retire'))
    a.brn('retire').connect(a.man('confirm'))
    a.man('confirm').connect(a.brn('confirm'))
    a.brn('confirm').connect(a.man('ok'))
    a.man('ok').connect(a.brn('head'))
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
    a.dmy('head').connect(a.slc('count'))
    a.slc('count').connect(a.slc('count').path(), retry=a.slc('head'), finish=a.dmy('tail'))
    a.slc('head').connect('member', same=a.brn('head'), other=a.brn('other\\head'))
    a.brn('head').connect(a.man('unidentified'), a.man('random'), a.dmy('id'))
    a.man('unidentified').connect(a.brn('unidentified'))
    a.brn('unidentified').connect(a.dmy('result'), a.man('unidentified'))
    a.dmy('result').connect(DummyState.open('quest\\result'))
    a.man('random').connect(a.brn('head'))
    a.dmy('id').connect(a.dmy('notified'))
    a.dmy('notified').connect(a.dmy('paste'))
    a.dmy('paste').connect(a.dmy('clip_aquire'))
    a.dmy('clip_aquire').connect(a.dmy('receive'))
    a.dmy('receive').connect(a.man('paste'))
    a.man('paste').connect(a.dmy('clip_release'))
    a.dmy('clip_release').connect(a.man('join'))
    a.man('join').connect(a.brn('paste'))
    a.brn('paste').connect(a.dmy('paste'), a.man('raid'))
    a.man('raid').connect(DummyState.open('quest\\head'))

    a.brn('other\\head').connect(a.man('other\\raid'), a.man('other\\random'), a.man('other\\id'))
    a.man('other\\random').connect(a.brn('other\\head'))
    a.man('other\\id').connect(a.brn('other\\head'))
    a.man('other\\raid').connect(DummyState.open('quest\\head'))

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
    a.slc('attr').connect('attr', none=a.slc('scroll\\sc1'), **{attr:a.man(f'attr\\{attr}') for attr in attrs})
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

def battlefield():
    a = Assister('battlefield')
    a.dmy('head').connect(a.slc('head'))
    a.slc('head').connect('field', weaponbreak=a.man('weaponbreak'),  titanhunt=a.man('titanhunt'))
    a.man('titanhunt').connect(a.brn('titanhunt'))
    a.brn('titanhunt').connect(a.slc('level'))
    a.slc('level').connect('titanhunt', hyperion=a.man('hyperion'), atlas=a.man('atlas'))
    a.man('hyperion').connect(DummyState.open('quest\\head'))
    a.man('atlas').connect(DummyState.open('quest\\head'))
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
    a.brn('raid\\top').connect(a.man('restart'), a.slc('raid\\position'), a.man('raid\\top'))
    a.man('restart').connect(a.brn('restart'))
    a.brn('restart').connect(DummyState.open('restore\\battle\\head'), a.man('restart'))
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
        a.dmy('start\\surpport'), a.dmy('start\\elixer'), a.dmy('start\\seed'), a.man('start\\red'), a.man('start\\blue'),
        a.man('start\\ok'), a.man('start\\unidentified'), a.man('start\\restart'), DummyState.open('restore\\battle\\head'))
    a.dmy('start\\elixer').connect(a.man('start\\recover'))
    a.dmy('start\\seed').connect(a.man('start\\recover'))
    a.man('start\\recover').connect(a.brn('start\\recover'))
    a.brn('start\\recover').connect(a.man('start\\ok'))
    a.man('start\\ok').connect(a.brn('start'))
    a.man('start\\red').connect(a.brn('start'))
    a.man('start\\blue').connect(a.brn('start'))    
    a.man('start\\unidentified').connect(a.dmy('result'))
    a.man('start\\restart').connect(a.brn('start\\restart'))
    a.brn('start\\restart').connect(DummyState.open('restore\\battle\\head'), a.man('start\\restart'))
    a.dmy('start\\surpport').connect(a.slc('start\\surpport'))
    attrs = ['fire','aqua','wind','volt','ray','dark','phantom']
    a.slc('start\\surpport').connect(
        a.slc('start\\surpport').path(),
        none=a.man('start\\surpport'),
        **{attr:a.man(f'start\\surpport\\{attr}') for attr in attrs})
    for attr in attrs:
        a.man(f'start\\surpport\\{attr}').connect(a.man('start\\surpport'))
    a.man('start\\surpport').connect(a.brn('start\\surpport'))
    a.brn('start\\surpport').connect(a.dmy('partyselect'), a.dmy('start\\surpport'))
    a.dmy('partyselect').connect(a.dmy('partyselect1'))
    a.dmy('partyselect1').connect(a.dmy('consume'))
    a.dmy('consume').connect(a.slc('groupselect'))
    a.slc('groupselect').connect(a.slc('groupselect').path(), none=a.man('partyselect'), **{f'group{group}':a.man(f'groupselect\\group{group}') for group in range(7)})
    for group in range(7):
        a.man(f'groupselect\\group{group}').connect(a.slc('partyselect'))
    a.slc('partyselect').connect(a.slc('partyselect').path(), none=a.man('partyselect'), **{f'party{party}':a.man(f'partyselect\\party{party}') for party in range(1,13)})
    for party in range(1,13):
        a.man(f'partyselect\\party{party}').connect(a.man('partyselect'))
    a.man('partyselect').connect(a.dmy('lock'))
    a.dmy('lock').connect(a.brn('partyselect'))
    a.brn('partyselect').connect(DummyState.open('battle\\head'), a.man('servererror'), a.man('finished'), a.man('partyselect'), a.man('warning'))
    a.man('servererror').connect(a.brn('partyselect'))
    a.man('finished').connect(a.brn('finish'))
    a.man('warning').connect(a.brn('partyselect'))

    a.dmy('result').connect(a.dmy('result1'))
    a.dmy('result1').connect(a.slc('type1'))
    a.slc('type1').connect('type', solo=a.slc('result\\count'), raid=a.man('result\\mvp'))
    a.brn('result').connect(
        a.man('result\\mvp'), a.man('result\\newitem'), a.man('result\\reward'), a.man('result\\aquire'), a.slc('result\\count'),
        a.dmy('start\\surpport'), a.dmy('start\\elixer'), a.dmy('start\\seed'), a.dmy('start\\red'), a.dmy('start\\blue'))
    a.man('result\\mvp').connect(a.slc('result\\count'))
    a.man('result\\rankup').connect(a.brn('result'))
    a.man('result\\newitem').connect(a.brn('result'))
    a.man('result\\reward').connect(a.brn('result'))
    a.man('result\\aquire').connect(a.brn('result'))
    a.slc('result\\count').connect(
        a.slc('result\\count').path(), retry=a.slc('retry'), finish=a.slc('finish'), back=a.man('back'))
    
    a.slc('retry').connect('result', none=a.man('retry'), once=a.man('back'), union=a.dmy('union'))
    a.man('retry').connect(a.brn('retry1'))
    a.brn('retry1').connect(
        a.dmy('start\\surpport'), a.man('start\\red'), a.man('start\\blue'), a.dmy('start\\elixer'), a.dmy('start\\seed'),
        a.man('result\\mvp'), a.man('result\\newitem'), a.man('result\\reward'), a.man('result\\aquire'), a.slc('result\\count'))
    
    a.slc('finish').connect('result', none=a.man('potal'), once=a.man('potal'), union=a.man('back'))
    a.man('finish').connect(a.brn('finish'))
    a.man('back').connect(a.brn('finish'))
    names = ['rescue', 'union', 'guild', 'battlefield', 'raid_event']
    a.brn('finish').connect(
        a.man('finish\\friend'), a.man('finish\\reward'), a.dmy('finish\\mvp'), a.dmy('finish\\rankup'), 
        a.dmy('finish\\aquire'), a.dmy('finish\\count'), *[a.dmy(f'finish\\{name}') for name in names])
    for name in names: a.dmy(f'finish\\{name}').connect(a.dmy('finish\\finish'))
    a.dmy('finish\\finish').connect(DummyState.open('page\\head'))
    a.man('finish\\friend').connect(a.brn('result'))
    a.man('finish\\reward').connect(a.brn('result'))
    a.dmy('finish\\mvp').connect(a.brn('result'))
    a.dmy('finish\\rankup').connect(a.brn('result'))
    a.dmy('finish\\aquire').connect(a.brn('result'))
    a.dmy('finish\\count').connect(a.brn('result'))

    a.man('potal').connect(a.brn('potal'))
    a.brn('potal').connect(
        a.man('finish\\friend'), a.man('finish\\reward'), a.dmy('finish\\mvp'), a.dmy('finish\\rankup'), 
        a.dmy('finish\\aquire'), a.dmy('finish\\count'), a.dmy('potal'))
    a.dmy('potal').connect(DummyState.open('page\\head'))

    a.dmy('union').connect(a.man('union\\back'))
    a.man('union\\back').connect(a.brn('union\\back'))
    a.brn('union\\back').connect(a.slc('union\\scroll\\sc1'),a.man('union\\mvp'),a.man('union\\rankup'),a.man('union\\back'))
    a.man('union\\mvp').connect(a.brn('union\\back'))
    a.man('union\\rankup').connect(a.brn('union\\back'))
    a.slc('union\\scroll\\sc1').connect('scroll', sc1=a.slc('union\\position'), sc2=a.man('union\\scroll\\sc2'))
    a.man('union\\scroll\\sc2').connect(a.slc('union\\scroll\\sc2'))
    a.slc('union\\scroll\\sc2').connect('scroll', sc2=a.slc('union\\position'))
    positions = ['pos1','pos2','pos3']
    a.slc('union\\position').connect('position', 
        **{position:a.man(f'union\\position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'union\\position\\{position}').connect(a.brn(f'union\\start'))
    a.brn(f'union\\start').connect(
        a.dmy('start\\surpport'), a.dmy('start\\elixer'), a.dmy('start\\seed'), a.man('start\\red'), a.man('start\\blue'),
        a.man('start\\unidentified'), a.man('start\\restart'), DummyState.open('restore\\battle\\head'), a.slc('union\\scroll\\sc1'))

    a.save()

def battle():
    a = Assister('battle')
    a.dmy('head').connect(a.slc('team'))
    a.slc('team').connect(a.slc('team').path(), solo=a.dmy('ability'), multi=a.slc('host1'), random=a.man('multi'), union=a.slc('host1'))
    a.slc('host1').connect(a.slc('host1').path(), host=a.man('multi'), guest=a.dmy('ability'))
    a.man('multi').connect(a.brn('multi'))
    a.brn('multi').connect(a.slc('host2'), exception=a.man('multi'))
    a.slc('host2').connect(a.slc('host2').path(), host=a.man('create_id'), guest=a.man('request'))
    a.man('create_id').connect(a.dmy('clip_aquire'))
    a.dmy('clip_aquire').connect(a.man('copy'))
    a.man('copy').connect(a.dmy('send'))
    a.dmy('send').connect(a.slc('check_copy'))
    a.slc('check_copy').connect(a.slc('check_copy').path(), success=a.dmy('clip_release'), failed=a.man('copy'))
    a.dmy('clip_release').connect(a.dmy('notify'))
    a.dmy('notify').connect(a.dmy('lock'))
    a.dmy('lock').connect(a.dmy('sync'))
    a.dmy('sync').connect(a.slc('request'))
    a.slc('request').connect(a.slc('request').path(), multi=a.man('cancel'), random=a.man('request'), union=a.man('check'))
    a.man('cancel').connect(a.dmy('ability'))
    a.man('check').connect(a.man('request'))
    a.man('request').connect(a.brn('request'))
    a.brn('request').connect(a.man('request'), exception=a.dmy('ability'))
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
    a.brn('attack').connect(a.slc('target'), a.man('next'), DummyState.open('quest\\result'))
    targets = ['target2_1','target2_2','target3_1','target3_2','target3_3']
    a.slc('target').connect('target', default=a.man('attack'), none=a.man('attack'),**{target:a.man(f'target\\{target}') for target in targets})
    for target in targets:
        a.man(f'target\\{target}').connect(a.man('attack'))
    a.man('attack').connect(a.brn('except0'))
    a.brn('except0').connect(DummyState.open('quest\\result'), a.man('error'), a.slc('target'), a.dmy('wait_battle'))
    a.dmy('wait_battle').connect(a.brn('except'))
    a.brn('except').connect(DummyState.open('quest\\result'), a.man('error'), a.slc('target'), a.slc('receive'))
    # a.brn('except').connect(a.man('error'), a.slc('target'), a.man('next'), DummyState.open('quest\\result'), a.slc('receive'))
    a.man('error').connect(a.brn('except'))
    # a.slc('max').connect('burst', default=a.brn('except'), change=a.man('max'))
    # a.man('max').connect(a.brn('max'))
    # a.brn('max').connect(a.dmy('on'), a.dmy('off'), DummyState.open('quest\\result'))
    # a.dmy('off').connect(a.man('max'))python 
    # a.dmy('on').connect(a.brn('on'))
    # a.brn('on').connect(a.man('reload'), DummyState.open('quest\\result'))
    # a.man('reload').connect(a.slc('auto'))
    a.man('next').connect(a.brn('next'))
    a.brn('next').connect(a.man('reload'), DummyState.open('quest\\result'))
    a.man('reload').connect(a.brn('except'))
    a.slc('receive').connect(a.slc('receive').path(),stay=a.man('stay'),reload=a.man('advance1'))
    a.man('stay').connect(a.brn('except'))
    a.man('advance1').connect(a.brn('except1'))
    a.brn('except1').connect(DummyState.open('quest\\result'), a.man('error'), a.slc('target'), a.man('next'), a.man('advance2'))
    a.man('advance2').connect(a.brn('except2'))
    a.brn('except2').connect(DummyState.open('quest\\result'), a.man('error'), a.slc('target'), a.man('next'), a.man('advance3'))
    a.man('advance3').connect(a.brn('except3'))
    a.brn('except3').connect(DummyState.open('quest\\result'), a.man('error'), a.slc('target'), a.man('next'), a.dmy('receive'))
    a.dmy('receive').connect(a.man('reload'))
    a.save()

def ability():
    a = Assister('ability')
    a.dmy('pre').connect(a.brn('pre'))
    a.brn('pre').connect(a.dmy('available'), a.dmy('result'))
    a.dmy('available').connect(a.dmy('tail'))
    
    charas = ['chara1','chara2','chara3','chara4','chara5']
    for i in range(13):
        a.dmy(f'id{i}\\head').connect(a.brn(f'id{i}\\head'))
        a.brn(f'id{i}\\head').connect(a.slc(f'id{i}\\list'), *[a.slc(f'id{i}\\scroll\\{chara}') for chara in charas], a.dmy('result'))   
        a.slc(f'id{i}\\list').connect('chara', **{chara:a.man(f'id{i}\\list\\{chara}') for chara in charas})
        for chara in charas: 
            a.man(f'id{i}\\list\\{chara}').connect(a.brn(f'id{i}\\list\\{chara}'))
            a.brn(f'id{i}\\list\\{chara}').connect(a.slc(f'id{i}\\list'), a.slc(f'id{i}\\scroll\\{chara}'), a.dmy('result'), a.dmy('next'), exception=a.brn(f'id{i}\\head'))

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
            a.brn(f'id{i}\\scroll\\{chara}').connect(a.man(f'id{i}\\target\\cancel'), a.slc(f'id{i}\\scroll\\{chara}'), exception=a.brn(f'id{i}\\scroll'))
        a.man(f'id{i}\\target\\cancel').connect(a.brn(f'id{i}\\scroll'))
        a.brn(f'id{i}\\scroll').connect(*[a.slc(f'id{i}\\scroll\\{chara}') for chara in charas], a.dmy('result'), a.dmy('next'))
    
    abis = ['ability1','ability2','ability3','ability4']
    for chara in charas:
        a.slc(chara).connect('ability', **{abi:a.man(f'ability\\{abi}') for abi in abis})
    for abi in abis:
        a.man(f'ability\\{abi}').connect(a.slc('target'))
    a.slc('istarget').connect('target', default=a.brn('istarget'), none=a.dmy('tail'))
    a.brn('istarget').connect(a.slc('target'), a.dmy('result'), a.dmy('next'))
    a.slc('target').connect('target', none=a.dmy('tail'), **{chara:a.man(f'target\\{chara}') for chara in charas})
    for chara in charas:
        a.man(f'target\\{chara}').connect(a.dmy('tail'))

    a.dmy('mode').connect(a.brn('auto'))
    a.brn('auto').connect(
        a.slc('auto\\ability'), a.slc('auto\\auto'), a.slc('auto\\manual'), a.dmy('result'), a.dmy('next'))
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
    a.brn('burst').connect(*[a.slc(f'burst\\{burst}') for burst in bursts], a.dmy('result'), a.dmy('next'))
    for burst in bursts:
        a.slc(f'burst\\{burst}').connect('burst', default=a.man('burst\\default'), **{burst:a.dmy('tail')})
    a.man('burst\\default').connect(a.brn('burst'))

    a.dmy('attack').connect(a.man('attack'))
    a.man('attack').connect(a.brn('attack'))
    a.brn('attack').connect(a.dmy('canccel'), a.dmy('result'), a.dmy('next'), exception=a.man('reload'))
    a.dmy('canccel').connect(a.brn('attack'))
    a.man('reload').connect(a.brn('reload'))
    a.brn('reload').connect(a.dmy('available'), a.dmy('next') ,a.dmy('result'))

    a.dmy('enemy').connect(a.slc('enemy'))
    enemies = ['enemy2_1','enemy2_2','enemy3_1','enemy3_2','enemy3_3']
    a.slc('enemy').connect('enemy', default=a.dmy('tail'),**{enemy:a.man(f'enemy\\{enemy}') for enemy in enemies})
    for enemy in enemies:
        a.man(f'enemy\\{enemy}').connect(a.dmy('tail'))    

    a.dmy('forward').connect(a.brn('forward'))
    a.brn('forward').connect(a.man('forward'))
    a.man('forward').connect(a.brn('nextstage'))
    a.brn('nextstage').connect(a.dmy('nextstage'))
    
    a.save()

def set_abi():
    a = Assister('set_abi')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('capture'))
    a.man('capture').connect(a.slc('command'))
    a.slc('command').connect(a.slc('command').path(), 
        finish=a.dmy('tail'), scroll=a.brn('scroll'), ability=a.slc('ability'), target=a.slc('target'),
        mode=a.dmy('mode'), attack=a.dmy('attack'), next=a.dmy('next'))
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
    a.brn('auto').connect(
        a.dmy('auto\\ability'), a.dmy('auto\\auto'), a.dmy('auto\\manual'), DummyState.open('quest\\result'), a.dmy('result'))
    a.dmy('auto\\ability').connect(a.slc('auto\\ability'))
    a.slc('auto\\ability').connect(a.slc('auto\\ability').path(), manual=a.man('auto\\single'), auto=a.man('auto\\double'), ability=a.brn('burst'))
    a.dmy('auto\\auto').connect(a.slc('auto\\auto'))
    a.slc('auto\\auto').connect(a.slc('auto\\auto').path(), ability=a.man('auto\\single'), manual=a.man('auto\\double'), auto=a.brn('burst'))
    a.dmy('auto\\manual').connect(a.slc('auto\\manual'))
    a.slc('auto\\manual').connect(a.slc('auto\\manual').path(), auto=a.man('auto\\single'), ability=a.man('auto\\double'), manual=a.brn('burst'))
    a.man('auto\\single').connect(a.brn('auto'))
    a.man('auto\\double').connect(a.brn('auto'))
    
    a.brn('burst').connect(a.dmy(f'burst\\on'),a.dmy(f'burst\\off'))
    a.dmy('burst\\on').connect(a.slc('burst\\on'))
    a.slc('burst\\on').connect(a.slc('burst\\on').path(), on=a.slc('command'), off=a.man('burst\\default'))
    a.dmy('burst\\off').connect(a.slc('burst\\off'))
    a.slc('burst\\off').connect(a.slc('burst\\off').path(), off=a.slc('command'), on=a.man('burst\\default'))
    a.man('burst\\default').connect(a.brn('burst'))

    a.dmy('attack').connect(a.man('attack'))
    a.man('attack').connect(a.brn('attack'))
    a.brn('attack').connect(a.dmy('canccel'), exception=a.man('reload'))
    a.dmy('canccel').connect(a.brn('attack'))
    a.man('reload').connect(a.brn('reload'))
    a.brn('reload').connect(a.man('ready'))

    a.dmy('next').connect(a.man('next'))
    a.man('next').connect(a.brn('next'))
    a.brn('next').connect(a.man('ready'))

    a.man('ready').connect(a.slc('command'))

    a.save()

def party():
    a = Assister('party')
    a.dmy('head').connect(a.man('sleep1'))
    a.man('sleep1').connect(a.slc('check1'))
    a.slc('check1').connect(a.slc('check1').path(), **{f'id{i}':a.brn(f'check1\\id{i}') for i in range(1,13)})
    for i in range(1,13):
        a.brn(f'check1\\id{i}').connect(a.dmy(f'id{i}\\party'), exception=a.slc('slot'))
    a.slc('slot').connect('slot', **{f'slot{i}':a.man(f'slot\\slot{i}') for i in range(1,13)})
    for i in range(1,13):
        a.man(f'slot\\slot{i}').connect(a.man('sleep2'))
    a.man('sleep2').connect(a.slc('check2'))
    a.slc('check2').connect(a.slc('check2').path(), **{f'id{i}':a.brn(f'check2\\id{i}') for i in range(1,13)})
    for i in range(1,13):
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
    for i in range(1,13):
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

def gacha_normal():
    a = Assister('gacha_normal')
    a.dmy('head').connect(a.man('gacha'))
    a.man('gacha').connect(a.brn('gacha'))
    a.brn('gacha').connect(a.man('other'),exception=a.man('gacha'))
    a.man('other').connect(a.brn('other'))
    a.brn('other').connect(a.man('normal'),a.man('other'))
    a.man('normal').connect(a.brn('normal'))
    a.brn('normal').connect(a.dmy('top'),a.brn('normal'))
    a.dmy('top').connect(a.brn('top'))
    a.brn('top').connect(a.man('ok'),a.man('portal'),exception=a.man('draw'))
    a.man('ok').connect(a.brn('top'))
    a.man('draw').connect(a.brn('top'))
    a.man('portal').connect(a.brn('portal'))
    a.brn('portal').connect(a.dmy('tail'),a.man('portal'))
    a.save()

def gache_special():
    a = Assister('gacha_special')
    a.dmy('head').connect(a.man('gacha'))
    a.man('gacha').connect(a.brn('gacha'))
    a.brn('gacha').connect(a.man('pickup'),exception=a.man('gacha'))
    a.man('pickup').connect(a.brn('pickup'))
    a.brn('pickup').connect(a.man('special'),a.man('pickup'))
    a.man('special').connect(a.brn('special'))
    a.brn('special').connect(a.dmy('top'),a.brn('special'))
    a.dmy('top').connect(a.brn('top'))
    a.brn('top').connect(a.dmy('ok'),a.man('close'),a.man('portal'),a.man('draw'),exception=a.man('skip'))
    a.dmy('ok').connect(a.man('ok'))
    a.man('ok').connect(a.brn('top'))
    a.man('close').connect(a.brn('top'))
    a.man('skip').connect(a.brn('top'))
    a.man('draw').connect(a.brn('top'))
    a.man('portal').connect(a.brn('portal'))
    a.brn('portal').connect(a.dmy('tail'),a.man('close'),a.man('portal'))
    a.save()
    
def receive():
    a = Assister('receive')
    a.dmy('head').connect(a.man('return'))
    a.man('return').connect(a.brn('return'))
    a.brn('return').connect(a.dmy(f'equipment{0}'))
    for i,e in enumerate(['weapon','genju']):
        a.dmy(f'equipment{i}').connect(a.man(e))
        a.man(e).connect(a.man(f'{e}\\recommend'))
        a.man(f'{e}\\recommend').connect(a.brn(f'{e}\\recommend'))
        a.brn(f'{e}\\recommend').connect(a.man(f'{e}\\return'), a.man(f'{e}\\finish'), a.man(f'{e}\\ok'), exception=a.man(f'{e}\\recommend'))
        a.man(f'{e}\\return').connect(a.brn(f'{e}\\return'))
        a.brn(f'{e}\\return').connect(a.man(f'{e}\\ok'), a.man(f'{e}\\return'), exception=a.man(f'{e}\\recommend'))
        a.man(f'{e}\\ok').connect(a.brn(f'{e}\\ok'))
        a.brn(f'{e}\\ok').connect(a.man(f'{e}\\recommend'), a.man(f'{e}\\ok'))
        a.man(f'{e}\\finish').connect(a.brn(f'{e}\\finish'))
        a.brn(f'{e}\\finish').connect(a.dmy(f'equipment{i+1}'))
    a.dmy(f'equipment{2}').connect(a.man('mypage'))
    a.man('mypage').connect(a.brn('mypage'))
    a.brn('mypage').connect(a.man('jem'), a.man('mission'), exception=a.man('mypage'))
    a.man('jem').connect(a.brn('mypage'))
    a.man('mission').connect(a.brn('mission'))
    a.brn('mission').connect(a.man(f'mission\\receive'),a.man('jem'),a.man('mission'))
    # a.brn('mission').connect(a.dmy(f'mission{0}'),a.man('jem'),a.man('mission'))
    # for i,m in enumerate(['daily','weekly','event']):
    #     m = f'mission\\{m}'
    #     a.dmy(f'mission{i}').connect(a.man(m))
    #     a.man(m).connect(a.man(f'{m}\\receive'))
    #     a.man(f'{m}\\receive').connect(a.dmy(f'{m}\\ok'))
    #     a.dmy(f'{m}\\ok').connect(a.brn(f'{m}\\ok'))
    #     a.brn(f'{m}\\ok').connect(a.dmy(f'mission{i+1}'))
    # a.dmy(f'mission{3}').connect(a.dmy(f'pass{0}'))
    # for i,m in enumerate(['daily','weekly']):
    #     m = f'pass\\{m}'
    #     a.dmy(f'pass{i}').connect(a.man(m))
    #     a.man(m).connect(a.man(f'{m}\\receive'))
    #     a.man(f'{m}\\receive').connect(a.dmy(f'{m}\\ok'))
    #     a.dmy(f'{m}\\ok').connect(a.brn(f'{m}\\ok'))
    #     a.brn(f'{m}\\ok').connect(a.man(f'{m}\\cancel'), a.dmy(f'pass{i+1}'))
    #     a.man(f'{m}\\cancel').connect(a.brn(f'{m}\\ok'))
    a.man(f'mission\\receive').connect(a.dmy(f'mission\\ok'))
    a.dmy(f'mission\\ok').connect(a.brn(f'mission\\ok'))
    a.brn(f'mission\\ok').connect(a.man(f'mission\\cancel'), exception=a.man(f'present'))
    a.man(f'mission\\cancel').connect(a.brn(f'mission\\ok'))
    a.man('present').connect(a.brn('present'))
    a.brn('present').connect(a.man('tab'), exception=a.man('present'))
    a.man('tab').connect(a.brn('tab'))
    a.brn('tab').connect(a.man('receive'), a.brn('finish'), exception=a.man('ok2'))
    a.man('receive').connect(a.man('ok1'))
    a.man('ok1').connect(a.man('ok2'))
    a.man('ok2').connect(a.brn('tab'))
    a.brn('finish').connect(a.dmy('yet'), exception=a.man('portal'))
    a.dmy('yet').connect(a.man('tab'))
    a.man('portal').connect(a.brn('portal'))
    a.brn('portal').connect(a.dmy('tail'), a.man('portal'))  
    a.save()  

def present():
    a = Assister('present')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('receive'))
    a.man('receive').connect(a.brn('receive'))
    a.brn('receive').connect(a.man('ok1'), a.man('ok2'), a.man('receive'))
    a.man('ok1').connect(a.brn('ok1'))
    a.brn('ok1').connect(a.man('ok2'), a.man('ok1'))
    a.man('ok2').connect(a.brn('ok2'))
    a.brn('ok2').connect(a.man('ok2'), a.man('receive'))
    a.save()

def story():
    a = Assister('story')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('newquest'), a.man('pos1'))
    a.man('pos1').connect(a.brn('pos1'))
    a.brn('pos1').connect(a.man('surpport'), a.man('skip'), a.man('scenario'), a.man('recover'), a.man('nobattle'), a.man('tail'), a.man('pos1'))
    a.man('scenario').connect(a.brn('pos1'))
    a.man('recover').connect(a.brn('recover'))
    a.brn('recover').connect(a.man('ok'))
    a.man('ok').connect(a.brn('pos1'))
    a.man('nobattle').connect(a.brn('pos1'))
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
    a.brn('result').connect(a.man('surpport'), a.man('recover'), a.man('reward'), a.man('newitem'), a.man('rankup'), a.man('result'), a.man('skip'))
    a.man('newitem').connect(a.brn('result'))
    a.man('rankup').connect(a.brn('result'))
    a.man('reward').connect(a.brn('reward'))
    a.brn('reward').connect(a.man('newquest'), a.man('result'))
    a.man('newquest').connect(a.brn('head'))
    a.save()

def open():
    a = Assister('open')
    a.dmy('head').connect(a.brn('open'))
    a.brn('open').connect(a.dmy('tail'), exception=a.dmy('open'))
    a.dmy('open').connect(BranchState.open('restore'),a.brn('open'))
    a.save()

def restore():
    a = Assister('restore')
    # a.dmy('head').connect(a.dmy('open'))
    # a.dmy('open').connect(a.brn('open'))
    # a.brn('open').connect(a.man('demado'))
    # a.man('demado').connect(a.brn('demado'))
    # a.brn('demado').connect(a.man('kpro'), a.man('demado'))
    # a.man('kpro').connect(a.slc('id'))
    # a.slc('id').connect('id', id10=a.man('activate'), default=a.man('closemain'))
    # a.man('activate').connect(a.man('closemain'))
    # a.man('closemain').connect(a.dmy('tail'))

    a.dmy('head').connect(a.brn('isopen'))
    a.brn('isopen').connect(a.dmy('top'), exception=a.dmy('open'))
    a.dmy('top').connect(a.slc('top'))
    a.slc('top').connect('mode', validate=a.dmy('tail'), default=a.dmy('shut'))
    a.dmy('shut').connect(a.brn('isopen'))
    a.dmy('open').connect(a.brn('open'))
    a.brn('open').connect(a.brn('top'))
    a.brn('top').connect(a.man('login'), a.man('popup'), a.man('start'))
        
    # a.dmy('closemain').connect(a.brn('closemain'))
    # a.brn('closemain').connect(a.man('popup'), a.man('start'))
    a.man('login').connect(a.brn('open'))
    a.man('popup').connect(a.brn('open'))
    a.man('start').connect(a.brn('start'))
    a.brn('start').connect(a.man('ok'), a.man('expire'), a.dmy('tail'), a.man('start'), a.man('close'), exception=a.man('quest'))
    a.man('ok').connect(a.brn('start'))
    a.man('close').connect(a.brn('start'))
    a.man('expire').connect(a.brn('start'))
    a.man('quest').connect(a.man('quest1'))
    a.man('quest1').connect(a.brn('start'))

    a.dmy('result\\head').connect(a.brn('result\\head'))
    a.brn('result\\head').connect(
        a.man('result\\mvp'), a.man('result\\rankup'), a.man('result\\aquire'), a.dmy('result\\potal'),
        exception=a.man('result\\potal'))
    a.man('result\\mvp').connect(a.man('result\\potal'))
    a.man('result\\rankup').connect(a.brn('result\\head'))
    a.man('result\\aquire').connect(a.brn('result\\head'))
    a.man('result\\potal').connect(a.brn('result\\head'))
    a.dmy('result\\potal').connect(DummyState.open('page\\head'))
    
    a.dmy('battle\\head').connect(a.slc('battle\\team'))
    a.slc('battle\\team').connect('team', solo=SelectState.open('battle\\auto'), multi=a.slc('battle\\host1'), random=a.man('battle\\multi'))
    a.slc('battle\\host1').connect(a.slc('battle\\host1').path(), host=a.man('battle\\multi'), guest=SelectState.open('battle\\auto'))
    a.man('battle\\multi').connect(a.brn('battle\\multi'))
    a.brn('battle\\multi').connect(a.slc('battle\\host2'), exception=a.man('battle\\multi'))
    a.slc('battle\\host2').connect(a.slc('battle\\host2').path(), host=a.man('battle\\copy'), guest=a.man('battle\\request'))
    a.man('battle\\copy').connect(a.dmy('battle\\copy'))
    a.dmy('battle\\copy').connect(a.dmy('battle\\syncronize'))
    a.dmy('battle\\syncronize').connect(a.man('battle\\release'))
    a.man('battle\\release').connect(SelectState.open('battle\\auto'))
    a.man('battle\\request').connect(SelectState.open('battle\\auto'))
    a.save()

def abandon():
    a = Assister('abandon')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.dmy('potal\\head1'), exception=a.man('potal'))
    a.man('potal').connect(a.brn('head'))

    # move to rescue
    a.dmy('potal\\head1').connect(a.man('potal\\rescue'))
    a.man('potal\\rescue').connect(a.brn('potal\\rescue'))
    a.brn('potal\\rescue').connect(a.dmy('rescue\\head'), a.dmy('potal\\head1'))

    # confirm that there is no active raid
    a.dmy('rescue\\head').connect(a.man('rescue\\random'))
    a.man('rescue\\random').connect(a.brn('rescue\\random'))
    a.brn('rescue\\random').connect(a.man('rescue\\active'), exception=a.man('rescue\\event'))
    a.man('rescue\\event').connect(a.brn('rescue\\event'))
    a.brn('rescue\\event').connect(a.man('rescue\\active'), exception=a.dmy('rescue\\unidentified'))

    a.man('rescue\\active').connect(a.brn('rescue\\active'))
    a.brn('rescue\\active').connect(a.dmy('battle\\head'), a.man('recover'), a.man('surpport'), a.man('rescue\\active'))
    a.man('recover').connect(a.brn('recover'))
    a.brn('recover').connect(a.man('recover'), exception=a.dmy('rescue\\unidentified'))
    a.man('surpport').connect(a.brn('surpport'))
    a.brn('surpport').connect(a.man('surpport'), exception=a.dmy('rescue\\unidentified'))

    # confirm that there is no unidentified raid
    a.dmy('rescue\\unidentified').connect(a.brn('rescue\\unidentified'))
    a.brn('rescue\\unidentified').connect(a.man('rescue\\check'), exception=a.man('rescue\\potal'))

    a.man('rescue\\check').connect(a.brn('rescue\\check'))
    a.brn('rescue\\check').connect(a.man('rescue\\check_pos1'), a.man('rescue\\check'))
    a.man('rescue\\check_pos1').connect(a.brn('rescue\\check_pos1'))
    a.brn('rescue\\check_pos1').connect(a.dmy('result\\head'), a.man('rescue\\check_pos1'))

    a.man('rescue\\potal').connect(a.brn('rescue\\potal'))
    a.brn('rescue\\potal').connect(a.dmy('potal\\head2'), a.man('rescue\\potal'))

    # move to item
    a.dmy('potal\\head2').connect(a.man('potal\\item'))
    a.man('potal\\item').connect(a.brn('potal\\item'))
    a.brn('potal\\item').connect(a.dmy('item\\head'), a.dmy('potal\\head2'))

    # confirm that there is no active quest
    a.dmy('item\\head').connect(a.brn('item\\head'))
    a.brn('item\\head').connect(a.man('item\\restart'), a.man('item\\potal'))
    a.man('item\\restart').connect(a.brn('item\\restart'))
    a.brn('item\\restart').connect(a.dmy('battle\\head'), a.dmy('result\\head'), a.man('item\\restart'))
    # a.man('item\\retire').connect(a.brn('item\\retire'))
    # a.brn('item\\retire').connect(a.man('item\\retire1'), a.man('item\\retire'))
    # a.man('item\\retire1').connect(a.brn('item\\retire1'))
    # a.brn('item\\retire1').connect(a.man('item\\ok'), a.man('item\\retire1'))
    # a.man('item\\ok').connect(a.brn('item\\ok'))
    # a.brn('item\\ok').connect(a.man('item\\potal'), a.man('item\\ok'))
    # a.man('item\\potal').connect(a.brn('item\\potal'))
    # a.brn('item\\potal').connect(a.dmy('potal\\head3'), a.man('item\\potal'))

    a.dmy('battle\\head').connect(a.brn('battle\\head'))
    a.brn('battle\\head').connect(a.dmy('battle\\attack'), a.dmy('battle\\revive'), a.dmy('result\\head'))
    a.dmy('battle\\attack').connect(a.man('battle\\menu'))
    a.dmy('battle\\revive').connect(a.man('battle\\menu'))
    a.man('battle\\menu').connect(a.brn('battle\\menu'))
    a.brn('battle\\menu').connect(a.man('battle\\retire')),a.dmy('battle\\attack'), a.dmy('battle\\revive')
    a.man('battle\\retire').connect(a.brn('battle\\retire'))
    a.brn('battle\\retire').connect(a.man('battle\\retire1'), a.man('battle\\retire2'), a.man('battle\\retire'))
    a.man('battle\\retire1').connect(a.brn('battle\\retire1'))
    a.brn('battle\\retire1').connect(a.man('battle\\ok'), a.man('battle\\retire1'))
    a.man('battle\\retire2').connect(a.brn('battle\\ok'))
    a.man('battle\\ok').connect(a.brn('battle\\ok'))
    a.brn('battle\\ok').connect(a.man('battle\\ok'), a.man('battle\\retire2'), a.dmy('tail'), exception=a.man('potal1'))
    a.man('potal1').connect(a.brn('battle\\ok'))
    
    a.dmy('result\\head').connect(a.brn('result\\head'))
    a.brn('result\\head').connect(
        a.man('result\\mvp'), a.man('result\\aquire'), a.dmy('tail'), exception=a.man('result\\potal'))
    a.man('result\\mvp').connect(a.man('result\\potal'))
    a.man('result\\aquire').connect(a.brn('result\\\potal'))
    a.man('result\\potal').connect(a.brn('result\\head'))

    a.save()

def episode():
    a = Assister('episode')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.man('list'))
    a.man('list').connect(a.brn('list'))
    a.brn('list').connect(a.dmy('2episodes'),a.dmy('3episodes'),a.man('list'))

    a.man('lock').connect(a.brn('head'))
    
# 2episodes\\pos1
    a.dmy('2episodes').connect(a.man('2episodes\\pos1'))
    a.man('2episodes\\pos1').connect(a.brn('2episodes\\pos1'))
    a.brn('2episodes\\pos1').connect(
        a.man('2episodes\\pos1\\seen'),a.man('2episodes\\pos1\\skip'),a.man('2episodes\\pos1'))
    a.man('2episodes\\pos1\\seen').connect(a.brn('2episodes\\pos2'))
    a.man('2episodes\\pos1\\skip').connect(a.brn('2episodes\\pos1\\skip'))
    a.brn('2episodes\\pos1\\skip').connect(a.man('2episodes\\pos1\\summary'))
    a.man('2episodes\\pos1\\summary').connect(a.brn('2episodes\\pos1\\summary'))
    a.brn('2episodes\\pos1\\summary').connect(a.man('2episodes\\pos1\\back'))
    a.man('2episodes\\pos1\\back').connect(a.brn('2episodes\\pos1\\back'))
    a.brn('2episodes\\pos1\\back').connect(
        a.man('2episodes\\pos1\\reward'),a.man('2episodes\\pos2'),a.man('2episodes\\pos1\\back'))
    a.man('2episodes\\pos1\\reward').connect(a.brn('2episodes\\pos1\\back'))
# 2episodes\\pos2  
    a.man('2episodes\\pos2').connect(a.brn('2episodes\\pos2'))
    a.brn('2episodes\\pos2').connect(
        a.man('lock'),a.man('2episodes\\pos2\\seen'),a.man('2episodes\\pos2\\skip'),a.man('2episodes\\pos2'))
    a.man('2episodes\\pos2\\seen').connect(a.brn('head'))
    a.man('2episodes\\pos2\\skip').connect(a.brn('2episodes\\pos2\\skip'))
    a.brn('2episodes\\pos2\\skip').connect(a.man('2episodes\\pos2\\summary'))
    a.man('2episodes\\pos2\\summary').connect(a.brn('2episodes\\pos2\\summary'))
    a.brn('2episodes\\pos2\\summary').connect(a.man('2episodes\\pos2\\harem'))
    a.man('2episodes\\pos2\\harem').connect(a.brn('2episodes\\pos2\\harem'))
    a.brn('2episodes\\pos2\\harem').connect(a.man('2episodes\\pos2\\ok'),a.man('2episodes\\pos2\\harem'))
    a.man('2episodes\\pos2\\ok').connect(a.brn('2episodes\\pos2\\ok'))
    a.brn('2episodes\\pos2\\ok').connect(a.man('2episodes\\pos2\\back'))
    a.man('2episodes\\pos2\\back').connect(a.brn('2episodes\\pos2\\back'))
    a.brn('2episodes\\pos2\\back').connect(
        a.man('2episodes\\pos2\\reward'),a.man('2episodes\\pos2\\aquire'),a.man('list'),
        a.man('2episodes\\pos2\\back'))
    a.man('2episodes\\pos2\\reward').connect(a.brn('2episodes\\pos2\\back'))
    a.man('2episodes\\pos2\\aquire').connect(a.brn('2episodes\\pos2\\back'))
# 3episodes\\pos1   
    a.dmy('3episodes').connect(a.man('3episodes\\pos1'))
    a.man('3episodes\\pos1').connect(a.brn('3episodes\\pos1'))
    a.brn('3episodes\\pos1').connect(
        a.man('3episodes\\pos1\\seen'),a.man('3episodes\\pos1\\skip'),a.dmy('3episodes'))
    a.man('3episodes\\pos1\\seen').connect(a.brn('3episodes\\pos2'))
    a.man('3episodes\\pos1\\skip').connect(a.brn('3episodes\\pos1\\skip'))
    a.brn('3episodes\\pos1\\skip').connect(a.man('3episodes\\pos1\\summary'))
    a.man('3episodes\\pos1\\summary').connect(a.brn('3episodes\\pos1\\summary'))
    a.brn('3episodes\\pos1\\summary').connect(a.man('3episodes\\pos1\\back'))
    a.man('3episodes\\pos1\\back').connect(a.brn('3episodes\\pos1\\back'))
    a.brn('3episodes\\pos1\\back').connect(
        a.man('3episodes\\pos1\\reward'),a.man('3episodes\\pos2'),a.man('3episodes\\pos1\\back'))
    a.man('3episodes\\pos1\\reward').connect(a.brn('3episodes\\pos1\\back'))
# 3episodes\\pos2   
    a.man('3episodes\\pos2').connect(a.brn('3episodes\\pos2'))
    a.brn('3episodes\\pos2').connect(
        a.man('lock'),a.man('3episodes\\pos2\\seen'),a.man('3episodes\\pos2\\skip'),a.man('3episodes\\pos2'))
    a.man('3episodes\\pos2\\seen').connect(a.brn('3episodes\\pos3'))
    a.man('3episodes\\pos2\\skip').connect(a.brn('3episodes\\pos2\\skip'))
    a.brn('3episodes\\pos2\\skip').connect(a.man('3episodes\\pos2\\summary'))
    a.man('3episodes\\pos2\\summary').connect(a.brn('3episodes\\pos2\\summary'))
    a.brn('3episodes\\pos2\\summary').connect(a.man('3episodes\\pos2\\harem'))
    a.man('3episodes\\pos2\\harem').connect(a.brn('3episodes\\pos2\\harem'))
    a.brn('3episodes\\pos2\\harem').connect(a.man('3episodes\\pos2\\ok'),a.man('3episodes\\pos2\\harem'))
    a.man('3episodes\\pos2\\ok').connect(a.brn('3episodes\\pos2\\ok'))
    a.brn('3episodes\\pos2\\ok').connect(a.man('3episodes\\pos2\\back'))
    a.man('3episodes\\pos2\\back').connect(a.brn('3episodes\\pos2\\back'))
    a.brn('3episodes\\pos2\\back').connect(
        a.man('3episodes\\pos2\\reward'),a.man('3episodes\\pos2\\aquire'),a.man('3episodes\\pos3'),
        a.man('3episodes\\pos2\\back'))
    a.man('3episodes\\pos2\\reward').connect(a.brn('3episodes\\pos2\\back'))
    a.man('3episodes\\pos2\\aquire').connect(a.brn('3episodes\\pos2\\back'))
# 3episodes\\pos3
    a.man('3episodes\\pos3').connect(a.brn('3episodes\\pos3'))
    a.brn('3episodes\\pos3').connect(
        a.man('lock'),a.man('3episodes\\pos3\\seen'),a.man('3episodes\\pos3\\skip'),a.man('3episodes\\pos3'))
    a.man('3episodes\\pos3\\seen').connect(a.brn('head'))
    a.man('3episodes\\pos3\\skip').connect(a.brn('3episodes\\pos3\\skip'))
    a.brn('3episodes\\pos3\\skip').connect(a.man('3episodes\\pos3\\summary'))
    a.man('3episodes\\pos3\\summary').connect(a.brn('3episodes\\pos3\\summary'))
    a.brn('3episodes\\pos3\\summary').connect(a.man('3episodes\\pos3\\harem'))
    a.man('3episodes\\pos3\\harem').connect(a.brn('3episodes\\pos3\\harem'))
    a.brn('3episodes\\pos3\\harem').connect(a.man('3episodes\\pos3\\ok'),a.man('3episodes\\pos3\\harem'))
    a.man('3episodes\\pos3\\ok').connect(a.brn('3episodes\\pos3\\ok'))
    a.brn('3episodes\\pos3\\ok').connect(a.man('3episodes\\pos3\\back'))
    a.man('3episodes\\pos3\\back').connect(a.brn('3episodes\\pos3\\back'))
    a.brn('3episodes\\pos3\\back').connect(
        a.man('3episodes\\pos3\\reward'),a.man('3episodes\\pos3\\aquire'),a.man('list'),
        a.man('3episodes\\pos3\\back'))
    a.man('3episodes\\pos3\\reward').connect(a.brn('3episodes\\pos3\\back'))
    a.man('3episodes\\pos3\\aquire').connect(a.brn('3episodes\\pos3\\back'))
    a.save()

def theater():
    a = Assister('theater')
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.slc('favorite'), exception=a.man('read'))
    a.man('read').connect(a.brn('head'))
    a.slc('favorite').connect('episode', **{f'episode{i}':a.man(f'episode{i}') for i in range(12)})
    for i in range(12):
        a.man(f'episode{i}').connect(a.man('play'))
    a.man('play').connect(a.dmy('tail'))
    a.save()

def reduction():
    a = Assister('reduction')
    actions = ['present','overlimit','overlimit_genju','powerup_genju','move','weapon','genju','episode','save_acce','load_acce','acce','kamihime','party']
    a.dmy('head').connect(a.slc('actions'))
    a.slc('actions').connect('action', **{act:a.man(act) for act in actions})
    for act in actions:
        a.man(act).connect(a.dmy('count'))
    a.dmy('count').connect(a.slc('retry'))
    a.slc('retry').connect(a.slc('retry').path(),retry=a.dmy('head'),finish=a.dmy('tail'))
    a.save()

def epic():
    a = Assister('epic')
    
    a.dmy('head').connect(a.brn('head'))
    a.brn('head').connect(a.dmy('page\\head'))
    
    a.dmy('page\\head').connect(a.slc('page\\attr'))
    attrs = ['fire','aqua','wind','volt','ray','dark','phantom']
    a.slc('page\\attr').connect('attr', **{attr:a.man(f'page\\attr\\{attr}') for attr in attrs})
    for attr in attrs: a.man(f'page\\attr\\{attr}').connect(a.slc('page\\scroll'))
    scrolls = ['sc1','sc2','sc3','sc4','sc5','sc6','sc7']
    a.slc('page\\scroll').connect('scroll', **{sc:a.man(f'page\\scroll\\{sc}') for sc in scrolls})
    for sc in scrolls: a.man(f'page\\scroll\\{sc}').connect(a.slc('page\\position'))
    positions = ['pos1','pos2','pos3']
    a.slc('page\\position').connect('position', 
        **{position:a.man(f'page\\position\\{position}') for position in positions})
    for position in positions: 
        a.man(f'page\\position\\{position}').connect(a.dmy('release\\head'))
     
    a.dmy('release\\head').connect(a.brn('release\\head'))
    a.brn('release\\head').connect(a.man('release\\pay'),a.dmy('page1\\head'))
    a.man('release\\pay').connect(a.brn('release\\pay'))
    a.brn('release\\pay').connect(a.man('release\\skip'),a.man('release\\pay'))
    a.man('release\\skip').connect(a.brn('release\\skip'))
    a.brn('release\\skip').connect(a.man('release\\skip_summary'),a.man('release\\skip'))
    a.man('release\\skip_summary').connect(a.brn('release\\skip_summary'))
    a.brn('release\\skip_summary').connect(a.man('release\\get'),a.man('release\\back'),a.man('release\\skip_summary'))
    a.man('release\\get').connect(a.brn('release\\get'))
    a.brn('release\\get').connect(a.man('release\\back'),a.man('release\\get'))
    a.man('release\\back').connect(a.brn('release\\back'))
    a.brn('release\\back').connect(a.man('release\\ok'),a.dmy('page1\\head'),a.man('release\\back'))
    a.man('release\\ok').connect(a.brn('release\\ok'))
    a.brn('release\\ok').connect(a.dmy('page1\\head'),a.man('release\\ok'))
    
    a.dmy('page1\\head').connect(a.man('page1\\quest'))
    a.man('page1\\quest').connect(a.brn('page1\\quest'))
    a.brn('page1\\quest').connect(a.dmy('quest\\head'),a.man('page1\\quest'))
    
    a.dmy('quest\\head').connect(a.brn('quest\\head'))
    a.brn('quest\\head').connect(a.man('quest\\read'),exception=a.dmy('page2\\head'))
    a.man('quest\\read').connect(a.brn('quest\\read'))
    a.brn('quest\\read').connect(a.man('quest\\skip'),a.dmy('quest\\surpport'),a.dmy('quest\\elixer'),a.man('quest\\read'))
    a.man('quest\\skip').connect(a.brn('quest\\skip'))
    a.brn('quest\\skip').connect(a.man('quest\\skip_summary'),a.man('quest\\skip'))
    a.man('quest\\skip_summary').connect(a.brn('quest\\skip_summary'))
    a.brn('quest\\skip_summary').connect(a.man('quest\\back'),a.man('quest\\skip_summary'))
    a.man('quest\\back').connect(a.brn('quest\\back'))
    a.brn('quest\\back').connect(a.man('quest\\reward'),a.man('quest\\back'))
    a.man('quest\\reward').connect(a.brn('quest\\reward'))
    a.brn('quest\\reward').connect(a.dmy('quest\\head'),a.man('quest\\reward'))
    a.dmy('quest\\surpport').connect(a.dmy('quest\\quest'))
    a.dmy('quest\\elixer').connect(a.dmy('quest\\quest'))
    a.dmy('quest\\quest').connect(a.dmy('quest\\head'))
    
    a.dmy('page2\\head').connect(a.man('page2\\top'))
    a.man('page2\\top').connect(a.brn('page2\\top'))
    a.brn('page2\\top').connect(a.man('page2\\exchange'),a.man('page2\\top'))
    a.man('page2\\exchange').connect(a.brn('page2\\exchange'))
    a.brn('page2\\exchange').connect(a.dmy('exchange\\head'),a.man('page2\\exchange'))
    
    a.dmy('exchange\\head').connect(a.dmy('exchange\\phase1'))
    
    a.dmy('exchange\\phase1').connect(a.brn('exchange\\phase1'))
    a.brn('exchange\\phase1').connect(a.dmy('exchange\\phase2'),a.man('exchange\\phase1\\exchange1'))
    a.man('exchange\\phase1\\exchange1').connect(a.brn('exchange\\phase1\\exchange1'))
    a.brn('exchange\\phase1\\exchange1').connect(a.man('exchange\\phase1\\exchange2'))
    a.man('exchange\\phase1\\exchange2').connect(a.brn('exchange\\phase1\\exchange2'))
    a.brn('exchange\\phase1\\exchange2').connect(a.man('exchange\\phase1\\ok'))
    a.man('exchange\\phase1\\ok').connect(a.dmy('exchange\\phase1'))
    
    a.dmy('exchange\\phase2').connect(a.brn('exchange\\phase2'))
    a.brn('exchange\\phase2').connect(a.dmy('page3\\head'),a.man('exchange\\phase2\\exchange1'))
    a.man('exchange\\phase2\\exchange1').connect(a.brn('exchange\\phase2\\exchange1'))
    a.brn('exchange\\phase2\\exchange1').connect(a.man('exchange\\phase2\\exchange2'))
    a.man('exchange\\phase2\\exchange2').connect(a.brn('exchange\\phase2\\exchange2'))
    a.brn('exchange\\phase2\\exchange2').connect(a.man('exchange\\phase2\\ok'))
    a.man('exchange\\phase2\\ok').connect(a.dmy('exchange\\phase2'))
    
    a.dmy('page3\\head').connect(a.man('page3\\top'))
    a.man('page3\\top').connect(a.brn('page3\\top'))
    a.brn('page3\\top').connect(a.man('page3\\home'),a.man('page3\\top'))
    a.man('page3\\home').connect(a.brn('page3\\home'))
    a.brn('page3\\home').connect(a.dmy('tail'),a.man('page3\\home'))
    
    a.save()

def close():
    a = Assister('close')
    a.dmy('head').connect(a.man('close'))
    a.dmy('close').connect(a.brn('close'))
    a.brn('close').connect(a.dmy('close'), exception=a.dmy('tail'))
    a.save()

def reload():
    a = Assister('reload')
    a.dmy('head').connect(a.man('reload'))
    a.save()

def demado():
    a = Assister('demado')
    a.dmy('head').connect(a.dmy('open'))
    a.dmy('open').connect(a.slc('id'))
    a.slc('id').connect('id', id1=a.man('copy'), default=a.dmy('paste'))
    a.man('copy').connect(a.dmy('copy'))
    a.dmy('copy').connect(a.man('close'))
    a.dmy('paste').connect(a.man('paste'))
    a.man('paste').connect(a.dmy('name'))
    a.dmy('name').connect(a.man('name'))
    a.man('name').connect(a.man('close'))
    a.man('close').connect(a.dmy('tail'))
    a.save()

def login():
    a = Assister('login')
    a.dmy('head').connect(a.dmy('open'))
    a.dmy('open').connect(a.brn('open'))
    a.brn('open').connect(a.man('kamipro'))
    a.man('kamipro').connect(a.brn('kamipro'))
    a.brn('kamipro').connect(a.man('login'),a.man('close'))
    a.man('login').connect(a.brn('kamipro'))
    a.man('close').connect(a.dmy('tail'))
    a.save()

def cache_clear():
    a = Assister('cache_clear')
    a.dmy('head').connect(a.dmy('open'))
    a.dmy('open').connect(a.man('clear'))
    a.man('clear').connect(a.dmy('tail'))
    a.save()

def move():
    a = Assister('move')
    a.dmy('head').connect(a.dmy('open'))
    a.dmy('open').connect(a.man('start'))
    a.man('start').connect(a.dmy('move'))
    a.dmy('move').connect(a.dmy('tail'))
    a.save()

def work():
    a = Assister('work')
    a.dmy('head').connect(a.brn('head'))
    names = ['random']
    a.brn('head').connect(*[a.man(name) for name in names])
    for name in names:
        a.man(name).connect(a.brn('head'))
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
    battlefield()
    quest()
    battle()
    ability()
    set_abi()
    party()
    set_party()
    gacha_raid()
    present()
    story()
    restore()
    episode()
    work()
    epic()
    abandon()
    gacha_normal()
    gache_special()
    receive()
    reduction()
    close()
    reload()
    demado()
    move()
    login()
    cache_clear()
    theater()

if __name__=="__main__":
    q = queue.Queue()
    q.put(mythread.Function(tmp))
    mythread.mt = mythread.MyThread()
    mythread.mt.start(q=q)