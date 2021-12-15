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
    
    for i in range(3):
        for attr in attrs:
            qs[2*i  ].put(mythread.Function(quest,  2*i+1, f'raid\\catas\\ult\\{attr}', 3, f'catas{i}', 2, ability_name='media2_2'))
            qs[2*i+1].put(mythread.Function(rescue, 2*i+2, f'raid\\catas\\ult\\{attr}', 3, f'catas{i}', 2, ability_name='media2_2'))
    for i in range(3):   
        for attr in attrs:
            qs[2*i  ].put(mythread.Function(rescue, 2*i+1, f'raid\\catas\\ult\\{attr}', 3, f'catas{i}', 2, ability_name='media2_2'))
            qs[2*i+1].put(mythread.Function(quest,  2*i+2, f'raid\\catas\\ult\\{attr}', 3, f'catas{i}', 2, ability_name='media2_2'))
    
    for i in range(6):
        for attr in attrs:
            qs[i].put(mythread.Function(quest, i+1, f'raid\\disa\\st\\{attr}', 1, f'disa{i}', 1))
        for attr in attrs:
            qs[i].put(mythread.Function(quest, i+1, f'raid\\disa\\ex\\{attr}', 1, f'disa{i}', 1))     
    
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
        # qs[2*i  ].put(mythread.Function(quest,  2*i+1, 'event\\raid\\rag', 300, f'raid_rag{i}', 2, ability_name='raid_rag_host'))
        # qs[2*i+1].put(mythread.Function(rescue, 2*i+2, 'event\\raid\\rag', 300, f'raid_rag{i}', 2, ability_name='raid_rag_guest'))
        qs[2*i  ].put(mythread.Function(rescue, 2*i+1, 'event\\raid\\rag', 200, f'raid_rag{i}', 2, ability_name='raid_rag_guest'))
        qs[2*i+1].put(mythread.Function(quest,  2*i+2, 'event\\raid\\rag', 200, f'raid_rag{i}', 2, ability_name='raid_rag_host'))

def raid_ex(qs):
    for i in range(6):
        qs[i].put(mythread.Function(quest,  i+1, 'event\\raid\\ex', 45, f'raid_ex{i}', 1, ability_name='raid_ex'))
        
def orympia(qs, attr, party_name=None, ability_name=None):
    for i in range(6):
        for _ in range(1):
            for j in range(6):
                if i == j:
                    qs[i].put(
                        mythread.Function(
                            quest,i+1,f'raid\\orympia\\rag\\{attr}',3,'uuid',6,party_name=party_name,ability_name=ability_name))
                else:
                    qs[i].put(
                        mythread.Function(
                            rescue,i+1,f'raid\\orympia\\rag\\{attr}',3,'uuid',6,party_name=party_name,ability_name=ability_name))

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

def dateline(qs):
    for i in range(6):
        qs[i].put(mythread.Function(wait, 5))

def pop(qs):
    for i in range(6):
        qs[i].get_nowait()

if __name__=="__main__":
    qs = [None]*6
    for i in range(6):
        qs[i] = queue.Queue()
    """
    dateline(qs)
    highlevel(qs,'raid\\machinebeast\\dark',party_name='ray\\deffense')
    highlevel(qs,'raid\\machinebeast\\volt',party_name='wind\\deffense')
    highlevel(qs,'raid\\machinebeast\\fire',party_name='aqua\\deffense')
    highlevel(qs,'raid\\orympia\\rag+\\volt',party_name='wind\\deffense')
    highlevel(qs,'raid\\orympia\\rag+\\aqua',
        party_names=['volt\\deffense',
                     'volt\\deffense',
                     'volt\\attack',
                     'volt\\attack',
                     'volt\\deffense',
                     'volt\\deffense'])
    highlevel(qs,'raid\\orympia\\rag+\\dark',party_name='ray\\deffense')
    regular(qs)
    """
    hyperion(qs)
    # orympia(qs, 'aqua', party_name='volt\\attack')
    # pop(qs)
    # pop(qs)

    raid = [None]*6
    for i in range(6):
        raid[i] = queue.Queue()

    regular(raid)
    orympia(raid, 'ray', party_name='dark\\attack')
    # raid_rag(raid)    
    
    advent = [None]*6
    for i in range(6):
        advent[i] = queue.Queue()
        advent[i].put(mythread.Function(quest,i+1,'advent\\rag',20,f'uuid{i}',1))

    stories = [None]*6
    for i in range(6):
        stories[i] = queue.Queue()
        stories[i].put(mythread.Function(story))
    
    exp = [None]*6
    for i in range(6):
        exp[i] = queue.Queue()
        exp[i].put(mythread.Function(quest,i+1,'item\\exp',15,f'uuid{i}',1))
    
    epic = [None]*6
    for i in range(6):
        epic[i] = queue.Queue()
        epic[i].put(mythread.Function(quest,i+1,'epic',35,f'uuid{i}',1))
    
    cross = [None]*6
    for i in range(6):
        cross[i] = queue.Queue()
        cross[i].put(mythread.Function(quest,i+1,'event\\union\\cross',10,f'uuid{i}',1))
    
    union = [None]*6
    for i in range(2):
        union[3*i  ] = queue.Queue()
        union[3*i  ].put(mythread.Function(quest,3*i+1,f'event\\union\\main\\pos{i+1}',120,f'union{i}',3, 
            ability_name='aqua\\burst\\phase4'))
        union[3*i+1] = queue.Queue()
        union[3*i+1].put(mythread.Function(quest,3*i+2,f'event\\union\\main\\pos{i+1}',120,f'union{i}',3, 
            ability_name='aqua\\burst\\phase4'))
        union[3*i+2] = queue.Queue()
        union[3*i+2].put(mythread.Function(quest,3*i+3,f'event\\union\\main\\pos{i+1}',120,f'union{i}',3, 
            ability_name='aqua\\burst\\phase4'))
        
    gacha = [None]*6
    for i in range(6):
        gacha[i] = queue.Queue()
        gacha[i].put(mythread.Function(gacha_raid))

    other = [None]*6
    for i in range(6):
        other[i] = queue.Queue()
        other[i].put(mythread.Function(rescue,1,'rescue',24,'uuid',1))

    receive = [None]*6
    for i in range(6):
        receive[i] = queue.Queue()
        receive[i].put(mythread.Function(present))

    id = 6
    q = queue.Queue()
    attrs = ['aqua']
    for attr in attrs:
        q.put(mythread.Function(set_party, f'{attr}\\deffense', id))

    new = queue.Queue()
    new.put(mythread.Function(restore, 6))
    
    tmp = queue.Queue()
    tmp.put(mythread.Function(rescue,1,'tmp',1,'uuid',1))
    

    abi = queue.Queue()
    abi.put(mythread.Function(set_abi, 'union\\phase4', id))

    abi1 = queue.Queue()
    abi1.put(mythread.Function(use_ability, 'union\\phase4', 5, 'uuid', 2))
    abi2 = queue.Queue()
    abi2.put(mythread.Function(use_ability, 'union\\phase4', 6, 'uuid', 2))
    
    abis = [None]*6
    for i in range(6):
        abis[i] = queue.Queue()

    for i in range(3):
        abis[2*i  ].put(mythread.Function(use_ability, 'union\\phase4', 2*i+1, f'uuid{i}', 2))
        abis[2*i+1].put(mythread.Function(use_ability, 'union\\phase4', 2*i+2, f'uuid{i}', 2))

    mythread.mt = mythread.MyThread(qs=other)
    mythread.mt.start()
    