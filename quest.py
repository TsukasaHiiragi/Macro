import queue

from k_project import *


def gacha_raid():
    exe = Executer()
    exe.run('gacha_raid\\head.dmy.stt.json', timeout=None)

def present():
    exe = Executer()
    exe.run('present\\head.dmy.stt.json', timeout=None)

def regular(qs):
    attrs = ['ray','dark','fire','aqua','wind','volt',]
    for i in range(6):
        for attr in attrs:
            qs[i].put(mythread.Function(quest, i+1, f'raid\\disa\\ex\\{attr}', 1, f'disa{i}', 1))
        for attr in attrs:
            qs[i].put(mythread.Function(quest, i+1, f'raid\\disa\\st\\{attr}', 1, f'disa{i}', 1))     
    
    for i in range(6):
        for attr in attrs:
            for j in range(6):
                if i == j:
                    qs[i].put(
                        mythread.Function(
                            quest,i+1,f'raid\\catas\\ult\\{attr}',3,'uuid',6))
                else:
                    qs[i].put(
                        mythread.Function(
                            rescue,i+1,f'raid\\catas\\ult\\{attr}',3,'uuid',6))

def hyperion(qs):
    for i in range(6):
        for j in range(6):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,'raid\\titanhunt\\hyperion',1,'uuid',6,party_name='ray\\deffense'))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,'raid\\titanhunt\\hyperion',1,'uuid',6,party_name='ray\\deffense'))

def highlevel(qs, name, party_name=None,party_names=None):
    if party_names is None: party_names = [party_name]*6
    for i in range(6):
        for j in range(6):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,name,1,'uuid',6,party_name=party_names[i]))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,name,1,'uuid',6,party_name=party_names[i]))

def raid_rag(qs):
    for i in range(3):
        qs[2*i  ].put(mythread.Function(quest,  2*i+1, 'event\\raid\\rag', 75, f'raid_rag{i}', 2, ability_name='aqua\\ability\\debuff1'))
        qs[2*i+1].put(mythread.Function(rescue, 2*i+2, 'event\\raid\\rag', 75, f'raid_rag{i}', 2, ability_name='aqua\\ability\\none'))
        qs[2*i  ].put(mythread.Function(rescue, 2*i+1, 'event\\raid\\rag', 75, f'raid_rag{i}', 2, ability_name='aqua\\ability\\none'))
        qs[2*i+1].put(mythread.Function(quest,  2*i+2, 'event\\raid\\rag', 75, f'raid_rag{i}', 2, ability_name='aqua\\ability\\debuff1'))

def raid_ex(qs):
    for i in range(6):
        qs[i].put(mythread.Function(quest,  i+1, 'event\\raid\\ex', 150, f'raid_ex{i}', 1, 
                                    ability_name='aqua\\ability\\1'))
        
def orympia(qs, attr, tries=3, party_name=None, ability_name=None):
    for i in range(6):
        for _ in range(1):
            for j in range(6):
                if i == j:
                    qs[i].put(
                        mythread.Function(
                            quest,i+1,f'raid\\orympia\\rag\\{attr}',tries,'uuid',6,party_name=party_name,ability_name=ability_name))
                else:
                    qs[i].put(
                        mythread.Function(
                            rescue,i+1,f'raid\\orympia\\rag\\{attr}',tries,'uuid',6,party_name=party_name,ability_name=ability_name))

def catas(qs, level, attr, party_name=None, ability_name=None):
    for i in range(6):
        for j in range(6):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,f'raid\\catas\\{level}\\{attr}',3,'uuid',6,party_name=party_name,ability_name=ability_name))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,f'raid\\catas\\{level}\\{attr}',3,'uuid',6,party_name=party_name,ability_name=ability_name))

def catas_rag(qs, attr):
    for i in range(3):
        for j in range(3):
            if i == j:
                qs[2*i].put(
                    mythread.Function(
                        quest,2*i+1,f'raid\\catas\\rag\\{attr}',3,'uuid1',3,ability_name=f'catas\\rag\\{attr}'))
                qs[2*i+1].put(
                    mythread.Function(
                        quest,2*i+2,f'raid\\catas\\rag\\{attr}',3,'uuid2',3,ability_name=f'catas\\rag\\{attr}'))
            else:
                qs[2*i].put(
                    mythread.Function(
                        rescue,2*i+1,f'raid\\catas\\rag\\{attr}',3,'uuid1',3,ability_name=f'catas\\rag\\{attr}'))
                qs[2*i+1].put(
                    mythread.Function(
                        rescue,2*i+2,f'raid\\catas\\rag\\{attr}',3,'uuid2',3,ability_name=f'catas\\rag\\{attr}'))


"""
def catas(qs):
    attrs = [['dark','aqua'],['volt'],['ray','wind','fire']]
    enemies = ['default','enemy2_2','enemy3_2']
    for j,enemy in enumerate(enemies):
        for attr in attrs[j]:
            for i in range(3):
                qs[2*i  ].put(mythread.Function(quest,  2*i+1, f'raid\\catas\\rag\\{attr}', 3, f'catas{i}', 2, 
                    party_name='aqua\\attack', ability_name=f'aqua\\burst\\bursttime\\{enemy}'))
                qs[2*i+1].put(mythread.Function(rescue, 2*i+2, f'raid\\catas\\rag\\{attr}', 3, f'catas{i}', 2, 
                    party_name='aqua\\attack', ability_name=f'aqua\\burst\\bursttime\\{enemy}'))
                qs[2*i  ].put(mythread.Function(rescue, 2*i+1, f'raid\\catas\\rag\\{attr}', 3, f'catas{i}', 2, 
                    party_name='aqua\\attack', ability_name=f'aqua\\burst\\bursttime\\{enemy}'))
                qs[2*i+1].put(mythread.Function(quest,  2*i+2, f'raid\\catas\\rag\\{attr}', 3, f'catas{i}', 2, 
                    party_name='aqua\\attack', ability_name=f'aqua\\burst\\bursttime\\{enemy}'))
"""
def dateline(qs):
    for i in range(6):
        qs[i].put(mythread.Function(wait, 5))

def pop(qs):
    for i in range(6):
        qs[i].get_nowait()

def init():
    qs = [None]*6
    for i in range(6):
        qs[i] = queue.Queue()
    return qs
        
def solo(qs, name, trial):
    for i in range(6):
        qs[i].put(mythread.Function(quest,i+1,name,trial,f'{name}_{i}',1))
    

if __name__=="__main__":
    qs = init()
    regular(qs)
    # solo(qs, 'attr\\all', 100)
    # orympia(qs, 'fire', 3)
    # orympia(qs, 'phantom', 1)
    # dateline(qs)
    # catas(qs, 'rag', 'fire')
    # regular(qs)
    
    # epic = init()
    # solo(epic,'epic',20)
    
    exp = init()
    solo(exp,'item\\exp',10)
    
    # advent = init()
    # solo(advent,'advent\\rag',10)
    
    # new = queue.Queue()
    # new.put(mythread.Function(restore,6))
    
    # harem = init()
    # for i in range(6):
    #     harem[i].put(mythread.Function(episode))
    
    # tmp = queue.Queue()
    # tmp.put(mythread.Function(quest,2,'tmp',1,'uuid',1))
    
    # event = init()
    # raid_rag(event)
    
    qs = init()
    for i in range(3):
        qs[i*2  ].put(mythread.Function(quest,i*2+1,f'event\\union\\main{i+1}',200,'uuid',1))
        qs[i*2+1].put(mythread.Function(quest,i*2+2,f'event\\union\\main{i+1}',200,'uuid',1))
    
    event = init()
    for i in range(6):
        event[i].put(mythread.Function(quest,i+1,f'event\\advent\\rag',85,'uuid',1))
    
    qs = init()
    catas_rag(qs,'fire')
    catas_rag(qs,'aqua')
    catas_rag(qs,'wind')
    catas_rag(qs,'volt')
    catas_rag(qs,'ray')
    catas_rag(qs,'dark')
    orympia(qs,'volt',ability_name='media')
    orympia(qs,'ray',ability_name='media')
    orympia(qs,'dark',ability_name='media')
    orympia(qs,'wind',ability_name='media')
    orympia(qs,'aqua',ability_name='media')
    orympia(qs,'fire',ability_name='media')

    
    epic = init()
    for i in range(6):
        epic[i].put(mythread.Function(quest,i+1,'epic',30,'uuid',1))
    
    
    q = queue.Queue()
    q.put(mythread.Function(quest,1,'epic',36,'uuid',1))
    
    s = init()
    for i in range(6):
        s[i].put(mythread.Function(start,i+1,'tfall'))

    mythread.mt = mythread.MyThread(qs=epic)
    mythread.mt.start()
    