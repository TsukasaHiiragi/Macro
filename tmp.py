import glob
import json

paths = glob.glob('C:\\Users\\miyas\\Macro\\quest\\raid\\disa\\ex\\*.qst.json', recursive=True)
for path in paths:
    with open(path,'rt') as f:
        args = json.load(f)
    args['position'] = 'pos1'
    with open(path,'wt') as f:
        json.dump(args,f,indent=2)
