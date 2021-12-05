import glob
import json

paths = glob.glob('C:\\Users\\tsuka\\Macro\\quest\\event\\union\\**\\*.qst.json', recursive=True)
for path in paths:
    with open(path,'rt') as f:
        args = json.load(f)
    args['type'] = 'raid'
    with open(path,'wt') as f:
        json.dump(args,f,indent=2)
