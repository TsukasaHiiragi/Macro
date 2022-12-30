import queue

from k_project import *


def gacha_raid():
    exe = Executer()
    exe.run('gacha_raid\\head.dmy.stt.json', timeout=None)

def present():
    exe = Executer()
    exe.run('present\\head.dmy.stt.json', timeout=None)

def regular(qs):
    attrs = ['fire','aqua','wind','volt','ray','dark']
    for attr in attrs:
        disa(qs, attr)
    for attr in attrs:
        catas_ult(qs, attr)
    for attr in attrs:
        catas_rag(qs, attr)
    # attrs = ['wind','volt','ray','dark']
    # for attr in attrs:
    #     orympia(qs, attr)
    
    
    
def highlevel(qs, name, party_id=None):
    for i in range(12):
        for j in range(12):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,name,1,f'{name}{j}',12,party_id=party_id))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,name,1,f'{name}{j}',12,party_id=party_id))

def raid_rag(qs):
    for i in range(3):
        qs[2*i  ].put(mythread.Function(quest,  2*i+1, 'event\\raid\\rag', 75, f'raid_rag{i}', 2, ability_name='aqua\\ability\\debuff1'))
        qs[2*i+1].put(mythread.Function(rescue, 2*i+2, 'event\\raid\\rag', 75, f'raid_rag{i}', 2, ability_name='aqua\\ability\\none'))
        qs[2*i  ].put(mythread.Function(rescue, 2*i+1, 'event\\raid\\rag', 75, f'raid_rag{i}', 2, ability_name='aqua\\ability\\none'))
        qs[2*i+1].put(mythread.Function(quest,  2*i+2, 'event\\raid\\rag', 75, f'raid_rag{i}', 2, ability_name='aqua\\ability\\debuff1'))

def raid_ex(qs):
    for i in range(6):
        qs[i].put(mythread.Function(quest,  i+1, f'event\\raid\\ex{i}', 150, f'raid_ex{i}', 1, 
                                    ability_name='aqua\\ability\\1'))
        
def orympia(qs, attr):
    for i in range(6):
        for _ in range(1):
            for j in range(6):
                if i == j:
                    qs[i].put(
                        mythread.Function(
                            quest,i+1,f'raid\\orympia\\rag\\{attr}',3,f'orympia\\rag\\{attr}{j}',6,party_id=10,surpport='phantom'))
                else:
                    qs[i].put(
                        mythread.Function(
                            rescue,i+1,f'raid\\orympia\\rag\\{attr}',3,f'orympia\\rag\\{attr}{j}',6,party_id=10,surpport='phantom'))
    for i in range(6,12):
        for _ in range(1):
            for j in range(6,12):
                if i == j:
                    qs[i].put(
                        mythread.Function(
                            quest,i+1,f'raid\\orympia\\rag\\{attr}',3,f'orympia\\rag\\{attr}{j}',6,party_id=8,ability_name='media'))
                else:
                    qs[i].put(
                        mythread.Function(
                            rescue,i+1,f'raid\\orympia\\rag\\{attr}',3,f'orympia\\rag\\{attr}{j}',6,party_id=8,ability_name='media'))

def orympia_phantom(qs):
    for i in range(6):
        qs[i].put(
            mythread.Function(
                quest,i+1,f'raid\\orympia\\rag\\phantom',2,f'orympia\\rag\\phantom{i}',7,party_id=8,surpport='phantom'))

        for j in range(6,12):
            qs[j].put(
                mythread.Function(
                    rescue,j+1,f'raid\\orympia\\rag\\phantom',2,f'orympia\\rag\\phantom{i}',7,ability_name='bursttime'))

    for i in range(6,12):
        for j in range(6,12):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,f'raid\\orympia\\rag\\phantom',2,f'orympia\\rag\\phantom{j}',6,ability_name='bursttime'))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,f'raid\\orympia\\rag\\phantom',2,f'orympia\\rag\\phantom{j}',6,ability_name='bursttime'))

    

def catas(qs, level, attr, party_name=None, ability_name=None):
    for i in range(6):
        for j in range(6):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,f'raid\\catas\\{level}\\{attr}',3,f'catas\\{level}\\{attr}{j}',6,party_name=party_name,ability_name=ability_name))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,f'raid\\catas\\{level}\\{attr}',3,f'catas\\{level}\\{attr}{j}',6,party_name=party_name,ability_name=ability_name))

def disa(qs, attr):
    for i in range(12):
        qs[i].put(mythread.Function(quest, i+1, f'raid\\disa\\ex\\{attr}', 1, f'disa_ex{i}', 1, party_id=7))
        qs[i].put(mythread.Function(quest, i+1, f'raid\\disa\\st\\{attr}', 1, f'disa_st{i}', 1, party_id=7)) 

def catas_ult(qs, attr):
    for i in range(12):
        qs[i].put(mythread.Function(quest,i+1,f'raid\\catas\\ult\\{attr}',1,f'catas\\ult\\{attr}{i}',1,party_id=9,ability_name='burst',surpport='phantom'))

def catas_rag(qs, attr):
    for i in range(2):
        for j in range(2):
            if i == j:
                qs[3*i].put(
                    mythread.Function(
                        quest,3*i+1,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
                qs[3*i+1].put(
                    mythread.Function(
                        quest,3*i+2,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j+1}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
                qs[3*i+2].put(
                    mythread.Function(
                        quest,3*i+3,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j+2}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
            else:
                qs[3*i].put(
                    mythread.Function(
                        rescue,3*i+1,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
                qs[3*i+1].put(
                    mythread.Function(
                        rescue,3*i+2,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j+1}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
                qs[3*i+2].put(
                    mythread.Function(
                        rescue,3*i+3,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j+2}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
    for i in range(2,4):
        for j in range(2,4):
            if i == j:
                qs[3*i].put(
                    mythread.Function(
                        quest,3*i+1,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
                qs[3*i+1].put(
                    mythread.Function(
                        quest,3*i+2,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j+1}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
                qs[3*i+2].put(
                    mythread.Function(
                        quest,3*i+3,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j+2}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
            else:
                qs[3*i].put(
                    mythread.Function(
                        rescue,3*i+1,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
                qs[3*i+1].put(
                    mythread.Function(
                        rescue,3*i+2,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j+1}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))
                qs[3*i+2].put(
                    mythread.Function(
                        rescue,3*i+3,f'raid\\catas\\rag\\{attr}',3,f'catas\\rag\\{attr}{3*j+2}',2,party_id=9,ability_name=f'catas\\rag\\{attr}',surpport='phantom'))


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
    for i in range(12):
        qs[i].put(mythread.Function(wait, 5))

def pop(qs,start,stop):
    for i in range(start,stop):
        qs[i].get_nowait()

def init():
    qs = [None]*12
    for i in range(12):
        qs[i] = queue.Queue()
    return qs
        
def solo(qs, name, trial):
    for i in range(12):
        qs[i].put(mythread.Function(quest,i+1,name,trial,f'{name}_{i}',1))

def daily(qs):
    for i in range(6):
        qs[i].put(mythread.Function(quest,i+1,'acce\\pos1',3,f'acce_{i}',1))
    for i in range(6,12):
        qs[i].put(mythread.Function(quest,i+1,'acce\\pos2',3,f'acce_{i}',1))
    

if __name__=="__main__":
    qs = init()
    regular(qs)
    
    exp = init()
    solo(exp,'item\\exp',10)
    
    advent = init()
    solo(advent,'event\\advent\\ult',2)
    
    
    event = init()
    # for i in range(6,12):
    #     event[i].put(mythread.Function(quest,i+1,f'event\\raid\\ex',2000,'event',1))
    # for i in range(6):
    #     event[i].put(mythread.Function(quest,i+1,f'event\\raid\\rag',2000,'event',1,ability_name='event\\raid\\rag'))
    # for i in range(6):
    #     event[i].put(mythread.Function(present))

    
    union = init()
    for i in range(12):
        union[i].put(mythread.Function(quest,i+1,f'event\\union\\main{i%6+1}',127,'uuid',1))
    for i in range(12):
        union[i].put(mythread.Function(quest,i+1,f'event\\union\\main{i%3+1}',400,'uuid',1))
    
    hl = init()

    highlevel(hl,'raid\\orympia\\plus\\ray')
    highlevel(hl,'raid\\orympia\\plus\\volt')
    highlevel(hl,'raid\\orympia\\plus\\dark')
    dateline(hl)
    orympia_phantom(hl)
    regular(hl)
    highlevel(hl,'raid\\beast\\aqua')
    highlevel(hl,'raid\\beast\\fire')
    highlevel(hl,'raid\\beast\\dark')
    highlevel(hl,'raid\\beast\\volt')
    highlevel(hl,'raid\\orympia\\plus\\fire')
    highlevel(hl,'raid\\orympia\\plus\\aqua')
    highlevel(hl,'raid\\orympia\\plus\\ray')
    highlevel(hl,'raid\\orympia\\plus\\volt')
    highlevel(hl,'raid\\orympia\\plus\\dark')

    tmp =init()
    daily(tmp)
    
    
    epic = init()
    for i in range(6,12):
        epic[i].put(mythread.Function(quest,i+1,'epic',25,f'epic{i}',1))
    
    
    q = queue.Queue()
    q.put(mythread.Function(mythread.Function(quest,4,'acce\\pos2',1,'uuid',1)))

    w = queue.Queue()
    w.put(mythread.Function(mythread.Function(work)))


    s = init()
    for i in range(12):
        s[i].put(mythread.Function(restore,i+1))

    mythread.mt = mythread.MyThread(qs=tmp)
    mythread.mt.start()
    