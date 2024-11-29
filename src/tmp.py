import glob
import shutil
import json
import datetime

quests = ['beast\\plus', 'beast', 'orympia\\plus', 'orympia\\rag', 'catas\\rag', 'catas\\ult', 'disa\\ex', 'disa\\st']
attrs = ['fire','aqua','wind','volt','ray','dark']
today = datetime.datetime.now().strftime("%Y/%m/%d")

for id in range(1,25):
    path = f'C:\\Users\\tsuka\\gitrepo\\Macro\\remain\\id{id}.back.json'
    remain = {f'raid\\{quest}\\{attr}':1 for quest in quests for attr in attrs}
    remain['acce\\pos1'] = 3
    remain['acce\\pos2'] = 3
    remain['acce\\pos3'] = 3
    remain['item\\weapon'] = 3
    remain['attr\\all'] = 3
    remain['raid\\orympia\\rag\\phantom'] = 2
    remain['raid\\orympia\\plus\\phantom'] = 1
    remain['gacha_normal'] = 1
    remain['gacha_special'] = 1
    remain['receive_present'] = 1
    dic = {'timestamp':None, 'remain':remain}
    with open(path, 'wt') as f:
        json.dump(dic,f,indent=2)

