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
    weaks = ['aqua','volt','fire','wind','dark','ray']
    for attr in attrs:
        multi(qs,f'raid\\catas\\ult_multi\\{attr}',1,[0,1,2,3,4,5,6,7,8,9,10,11],[0])
    for i,(attr,weak) in enumerate(zip(attrs,weaks)):
        multi(qs,f'raid\\disa\\st\\{attr}',1,[0],[0,1,2,3,4,5,6,7,8,9,10,11])
        multi(qs,f'raid\\disa\\ex\\{attr}',1,[0],[0,1,2,3,4,5,6,7,8,9,10,11])
        multi(qs,f'raid\\catas\\rag\\{attr}',3,[0,4,8],[0,1,2,3],party_id=[11]*4+[i+1]*8,surpport=['phantom']*4+[weak]*8)

def orympia(qs):
    attrs = ['fire','aqua','wind','volt','ray','dark']
    weaks = ['aqua','volt','fire','wind','dark','ray']
    for i,(attr,weak) in enumerate(zip(attrs,weaks)):
        multi(qs,f'raid\\orympia\\rag\\{attr}',3,[0,4,8],[0,1,2,3],party_id=[11]*4+[i+1]*8,surpport=['phantom']*4+[weak]*8)
    
def orympia_wind(qs, assist=[], assist_party=None):
    for i in range(12):
        target = 'upper' if i%2==0 else 'lower'
        name = f'raid\\orympia\\plus\\wind_{target}'
        party_id = assist_party if i in assist else None
        for j in range(12):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,name,1,f'orympia_wind{j}',12,party_id=party_id))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,name,1,f'orympia_wind{j}',12,party_id=party_id))  

def beast_ray(qs, party_id=None):
    recover = [7,9,10]
    for i in range(12):
        ability_name = 'recover\\dark' if i+1 in recover else None
        for j in range(12):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,'raid\\beast\\ray',1,f'raid\\beast\\ray{j}',12,party_id=party_id,ability_name=ability_name))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,'raid\\beast\\ray',1,f'raid\\beast\\ray{j}',12,party_id=party_id,ability_name=ability_name))  
    
def highlevel(qs, name, assist=[], assist_party=None, party_id=None, **kwargs):
    for i in range(12):
        pid = assist_party if i+1 in assist else party_id
        for j in range(12):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,name,1,f'{name}{j}',12,party_id=pid,**kwargs))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,name,1,f'{name}{j}',12,party_id=pid,**kwargs))

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
        

def orympia_phantom(qs):
    multi(qs, 'raid\\orympia\\rag\\phantom',2,[0,1,2,6,7,8],[0,3],party_id=10,surpport='fire')

def orympia_phantom_plus(qs):
    recover = [7,9,10]
    for i in range(12):
        party_id = 6 if i+1 in recover else 5
        surpport = 'ray' if i+1 in recover else 'dark'
        ability_name = 'orympia_phantom'
        for j in range(12):
            if i == j:
                qs[i].put(
                    mythread.Function(
                        quest,i+1,'raid\\orympia\\plus\\phantom',1,f'raid\\orympia\\plus\\phantom{j}',12,party_id=party_id,surpport=surpport,ability_name=ability_name))
            else:
                qs[i].put(
                    mythread.Function(
                        rescue,i+1,'raid\\orympia\\plus\\phantom',1,f'raid\\orympia\\plus\\phantom{j}',12,party_id=party_id,surpport=surpport,ability_name=ability_name))  

def hyperion(qs):
    for _ in range(14):
        solo(qs,'battlefield\\titanhunt\\hyperion',1)

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
        
def solo(qs, name, trial,**kwargs):
    for i in range(12):
        qs[i].put(mythread.Function(quest,i+1,name,trial,f'{name}_{i}',1,**kwargs))

def multi(qs, name, trial, intra, inter, hosts=None, party_id=None, surpport=None, **kwargs):
    if type(party_id) is not list:
        party_id = [party_id]*12
    if type(surpport) is not list:
        surpport = [surpport]*12
    if hosts is None: hosts = intra
    for first in inter:
        for host in hosts:
            host_id = first + host
            for member in intra:
                member_id = first + member
                if member_id==host_id:
                    qs[member_id].put(mythread.Function(quest,member_id+1,name,trial,f'{name}_{host_id}',len(intra),party_id=party_id[member_id],surpport=surpport[member_id],**kwargs))
                else:
                    qs[member_id].put(mythread.Function(rescue,member_id+1,name,trial,f'{name}_{host_id}',len(intra),party_id=party_id[member_id],surpport=surpport[member_id],**kwargs))
                
def daily(qs):
    # multi(qs,'event\\raid\\rag_multi',3,[0,6],[0,1,2,3,4,5])
    for i in range(12):
        qs[i].put(mythread.Function(quest,i+1,'acce\\pos1',3,f'acce_{i}',1))
    for i in range(12):
        qs[i].put(mythread.Function(quest,i+1,'item\\weapon',3,f'genju_{i}',1))
    for i in range(12):
        qs[i].put(mythread.Function(gacha_normal))
    for i in range(12):
        qs[i].put(mythread.Function(receive_present))
    

if __name__=="__main__":
    qs = init()
    regular(qs)
    
    exp = init()
    solo(exp,'item\\exp',10)
    
    advent = init()
    solo(advent,'event\\advent\\ult',2)
    
    
    event = init()
    # for i in range(6,12):
    #     event[i].put(mythread.Function(quest,i+1,f'event\\raid\\ex',6000,f'event_{i}',1))
    # for i in range(6):
    #     event[i].put(mythread.Function(quest,i+1,f'event\\raid\\rag',3000,f'event_{i}',1,ability_name='event\\raid\\rag'))
    multi(event,f'event\\raid\\rag',3000,[0],[0,1,2,3,4,5],ability_name='event\\raid\\rag')
    multi(event,f'epic',1000,[6],[0,1,2,3,4,5])
    gacha = init()
    for i in range(6):
        gacha[i].put(mythread.Function(reduction))
    multi(gacha,'epic',1000,[6],[0,1,2,3,4,5])
    
    union = init()
    for i in range(12):
        union[i].put(mythread.Function(quest,i+1,f'event\\union\\main{i%6+1}',200,'uuid',1))
    # for i in range(12):
    #     union[i].put(mythread.Function(quest,i+1,f'event\\union\\main{i%3+1}',400,'uuid',1))
    # for i in range(6,12):
    #     union[i].put(mythread.Function(quest,i+1,'epic',100,f'epic{i}',1))
    
    hl = init()
    # regular(hl)
    # orympia(hl)
    # solo(hl,'event\\raid\\ex',300)
    # dateline(hl)
    # orympia_phantom(hl)
    # beast_ray(hl)
    # highlevel(hl,'raid\\beast\\wind')
    # highlevel(hl,'raid\\beast\\aqua')
    # highlevel(hl,'raid\\beast\\fire')
    # highlevel(hl,'raid\\beast\\dark')
    # highlevel(hl,'raid\\beast\\volt')
    # orympia_wind(hl)
    # highlevel(hl,'raid\\orympia\\plus\\fire')
    # highlevel(hl,'raid\\orympia\\plus\\aqua')
    # highlevel(hl,'raid\\orympia\\plus\\ray')
    # highlevel(hl,'raid\\orympia\\plus\\volt')
    # highlevel(hl,'raid\\orympia\\plus\\dark')
    orympia_phantom_plus(hl)
    pop(hl,0,12)
    pop(hl,0,12)
    pop(hl,0,12)
    pop(hl,0,12)
    pop(hl,0,12)
    pop(hl,0,12)
    pop(hl,0,12)

    tmp =init()
    daily(tmp)

    test = init()
    orympia_phantom_plus(test)
    pop(test,0,12)
    pop(test,0,12)

    epic = init()
    for i in range(12):
        epic[i].put(mythread.Function(quest,i+1,'epic',50,f'epic{i}',1))
    
    auto = init()
    for i in range(12):
        auto[i].put(mythread.Function(quest,i+1,'auto',50,f'auto{i}',1))
    
    
    q = queue.Queue()
    q.put(mythread.Function(reduction))

    w = queue.Queue()
    w.put(mythread.Function(work))

    abi = queue.Queue()
    id = 8
    ability_name = 'orympia_phantom'
    abi.put(mythread.Function(quest,id,'epic',1,f'epic{i}',1,ability_name=ability_name))

    ad = init()
    multi(ad,f'event\\advent\\ult',130,[0],[0,1,3,4])

    s = init()
    for i in range(12):
        s[i].put(mythread.Function(start,i+1))

    mythread.mt = mythread.MyThread(qs=s)
    mythread.mt.start()
    