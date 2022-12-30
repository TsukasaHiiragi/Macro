import glob
import shutil
import json

src = 'C:\\Users\\tsuka\\gitrepo\\Macro\\ability\\burst'
attrs = ['fire','aqua','wind','volt','ray','dark']
enemies = ['3_2',None,'3_2','2_2','3_2',None]

for i in range(6):
    dst = f'C:\\Users\\tsuka\\gitrepo\\Macro\\ability\\catas\\rag\\{attrs[i]}'
    shutil.copytree(src,dst)

    paths = glob.glob(dst+'\\**\\*.abi.json', recursive=True)
    for path in paths:
        with open(path,'rt') as f:
            abis = json.load(f)
        if enemies[i] is not None:
            abis = [{"special":"enemy","enemy":"enemy"+enemies[i]}]+abis
        with open(path,'wt') as f:
            json.dump(abis,f,indent=2)

