import queue

from k_project import *

def attrs():
    return ['fire','aqua','wind','volt','ray','dark']

def surpport(attr):
    surpport_list = ['aqua','volt','fire','wind','dark','ray']
    support_dict = {attrs()[i]:surpport_list[i] for i in range(6)}
    return support_dict[attr]

def pid(attr):
    party_dict = {attrs()[i]:i+1 for i in range(6)}
    return party_dict[attr]

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

def dateline(qs, h=5):
    for q in qs:
        q.put(mythread.Function(wait, h))

def pop(qs,n=1):
    for _ in range(n):
        for q in qs:
            q.get_nowait()

def init():
    qs = [None]*24
    for i in range(24):
        qs[i] = queue.Queue()
    return qs

def put_open(qs, ids=None):
    for i,q in enumerate(qs):
        if ids is None or i in ids:
            q.put(mythread.Function(start,i+1))

def put_close(qs, ids=None):
    for i,q in enumerate(qs):
        if ids is None or i in ids:
            q.put(mythread.Function(close))

def close_state(qs, cl=None, preset=None):
    if preset is not None:
        if preset==1: cl = list(range(24))
        if preset==2: cl = list(range(12))
        if preset==3: cl = list(range(12,24))
    
    if cl is not None:
        for i in cl:
            qs[i].put(mythread.Function(close))

def group(qs, code=2):
    ids = [
        list(range(1,25)),
        list(range(1,13)),
        list(range(13,25)),
        list(range(1,7))+list(range(13,19)),
        list(range(7,13))+list(range(19,25)),
        list(range(1,7)),
        list(range(7,13)),
        list(range(13,19)),
        list(range(19,25)),
    ][code-1]
    qs = [qs[id-1] for id in ids]
    return qs, ids

def check(id, name, trial):
    path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id+1}.json'
    with open(path, 'rt') as f:
        dic = json.load(f)
    today = datetime.datetime.now()
    today = today - datetime.timedelta(hours=5)
    today = today.strftime("%Y/%m/%d")
    if dic['timestamp']!=today:
        path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id+1}.back.json'
        with open(path, 'rt') as f:
            dic = json.load(f)
        dic['timestamp'] = today
        path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id+1}.json'
        with open(path, 'wt') as f:
            json.dump(dic, f, indent=2)
    remain = dic['remain']
    if name in remain:
        return min(trial, remain[name])
    else:
        return trial
    
def update_remain():
        for id in range(1,25):
            path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id}.json'
            with open(path, 'rt') as f:
                dic = json.load(f)
            today = datetime.datetime.now().strftime("%Y/%m/%d")
            if dic['timestamp']!=today:
                path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id}.back.json'
                with open(path, 'rt') as f:
                    dic = json.load(f)
                dic['timestamp'] = today
                path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id}.json'
                with open(path, 'wt') as f:
                    dic = json.dump(dic, f)
        
def solo(qs, name, trial, pre=False, **kwargs):
    for i in range(24):
        if type(name) == list:
            for s in name:
                n = check(i, s, trial)
                if n is None or n > 0:
                    qs[i].put(mythread.Function(quest,i+1,s,n,f'{s}_{i}',1,pre=pre,**kwargs)) 
        else:
            n = check(i, name, trial)
            if n is None or n > 0:
                qs[i].put(mythread.Function(quest,i+1,name,n,f'{name}_{i}',1,pre=pre,**kwargs))

def multi(qs, name, trial, intra, inter, hosts=None, party_id=None, surpport=None, ability_name=None, pre=False, peer=False, **kwargs):
    if type(party_id) is not list:
        party_id = [party_id]*24
    if type(surpport) is not list:
        surpport = [surpport]*24
    if type(ability_name) is not list:
        ability_name = [ability_name]*24
    if hosts is None: hosts = intra
    for first in inter:
        for host in hosts:
            host_id = first + host
            if type(name) == list:
                for s in name:
                    n = check(host_id, s, trial)
                    if n > 0:
                        for member in intra:
                            member_id = first + member
                            if member_id==host_id:
                                qs[member_id].put(
                                    mythread.Function(
                                        quest,
                                        member_id+1,
                                        s,n,
                                        f'{s}_{host_id}',
                                        len(intra),
                                        party_id=party_id[member_id],
                                        surpport=surpport[member_id],
                                        ability_name=ability_name[member_id],
                                        pre=pre,
                                        peer=peer,
                                        **kwargs
                                    )
                                )
                            else:
                                qs[member_id].put(
                                    mythread.Function(
                                        rescue,
                                        member_id+1,
                                        s,n,
                                        f'{s}_{host_id}',
                                        len(intra),
                                        party_id=party_id[member_id],
                                        surpport=surpport[member_id],
                                        ability_name=ability_name[member_id],
                                        pre=pre,
                                        peer=peer,
                                        **kwargs
                                    )
                                )
            else:
                n = check(host_id, name, trial)
                if n > 0:
                    for member in intra:
                        member_id = first + member
                        if member_id==host_id:
                            qs[member_id].put(
                                mythread.Function(
                                    quest,
                                    member_id+1,
                                    name,n,
                                    f'{name}_{host_id}',
                                    len(intra),
                                    party_id=party_id[member_id],
                                    surpport=surpport[member_id],
                                    ability_name=ability_name[member_id],
                                    pre=pre,
                                    peer=peer,
                                    **kwargs
                                )
                            )
                        else:
                            qs[member_id].put(
                                mythread.Function(
                                    rescue,
                                    member_id+1,
                                    name,n,
                                    f'{name}_{host_id}',
                                    len(intra),
                                    party_id=party_id[member_id],
                                    surpport=surpport[member_id],
                                    ability_name=ability_name[member_id],
                                    pre=pre,
                                    peer=peer,
                                    **kwargs
                                )
                            )

def multi2(qs, main, sub, func):
    n = main
    m = sub
    for i in range(m//n):
        intra = list(range(i*n, (i+1)*n)) + list(range(12,12+m))
        inter = list(range(0,12,m))
        hosts = list(range(i*n, (i+1)*n)) + list(range(i*n+12, (i+1)*n+12))
        new = [j+k for j in range(0,12,m) for k in range(i*n, (i+1)*n)]
        if i!=0:
            for j,id in enumerate(new):
                qs[id].put(mythread.Function(dependency, f'job{i-1}_{j}', 2))
        func(qs, intra, inter, hosts)
        put_close(qs, new)
        if i!=m//n-1:
            for j,id in enumerate(new):
                qs[id].put(mythread.Function(dependency, f'job{i}_{j}', 2))
    
def multi3(qs, main, sub, func):
    n = main
    m = sub
    for i in range(m//n):
        intra = list(range(i*n, (i+1)*n)) + list(range(12,12+m))
        inter = list(range(0,12,m))
        hosts = list(range(i*n, (i+1)*n))
        new = [j+k for j in range(0,12,m) for k in range(i*n, (i+1)*n)]
        if i!=0:
            for j,id in enumerate(new):
                qs[id].put(mythread.Function(dependency, f'job{i-1}_{j}', 2))
        func(qs, intra, inter, hosts)
        put_close(qs, new)
        if i!=m//n-1:
            for j,id in enumerate(new):
                qs[id].put(mythread.Function(dependency, f'job{i}_{j}', 2))

def sequencial(qs, ids, uuid, func):
    for i,id in enumerate(ids):
        if i!=0:
            qs[id].put(mythread.Function(dependency, f'{uuid}{i-1}', 2))
        func(qs, id)
        if i!=len(ids)-1:
            qs[id].put(mythread.Function(dependency, f'{uuid}{i}', 2))
    
                
def daily(qs, pos, special=False):
    # multi(qs,'event\\raid\\rag_multi',3,[0,3],[0,1,2,6,7,8,12,13,14,18,19,20],arrange=False)
    for id in range(24):
        multi(qs,f'acce\\pos{pos}', 3, [id], [0], arrange=False)
        if check(id, 'gacha_normal', 1) > 0:
            qs[id].put(mythread.Function(gacha_normal))
        if check(id, 'receive_present', 1) > 0:
            qs[id].put(mythread.Function(receive_present)) 
        if special and check(id, 'gacha_special', 1) > 0:
            qs[id].put(mythread.Function(gacha_special))
        # multi(qs,'item\\exp', 1, [id], [0], arrange=False)  

def daily2(qs, id, special=False):
    multi(qs,f'acce\\pos1', 3, [id], [0], arrange=False)
    if check(id, 'gacha_normal', 1) > 0:
        qs[id].put(mythread.Function(gacha_normal))
    if check(id, 'receive_present', 1) > 0:
        qs[id].put(mythread.Function(receive_present))
    if special and check(id, 'gacha_special', 1) > 0:
        qs[id].put(mythread.Function(gacha_special))
    # multi(qs,'item\\exp', 1, [id], [0], arrange=False)
    
def reset(qs):
    for q in qs:
        q.put(mythread.Function(lambda: None))
