import pathlib
import json
import numpy as np

import action
import image

def update_coord_act(act: action.Action):
    if isinstance(act, action.Actions):
        actions = []
        for a in act.actions:
            actions.append(update_coord_act(a))
        return action.Actions(actions)
    elif isinstance(act, action.Click):
        coord = act.coord - np.array([711, 84])
        return action.Click(coord[0], coord[1], act.interval, act.keys, act.rand)
    elif isinstance(act, action.Scroll):
        coord = act.coord - np.array([711, 84])
        return action.Scroll(coord[0], coord[1], act.amount, act.interval)
    else:
        return act
    
def update_coord_sym(sym: image.Symbol):
    if isinstance(sym, image.AndSymbol):
        left = update_coord_sym(sym.left)
        right = update_coord_sym(sym.right)
        return image.AndSymbol(left, right)
    elif isinstance(sym, image.OrSymbol):
        left = update_coord_sym(sym.left)
        right = update_coord_sym(sym.right)
        return image.OrSymbol(left, right)
    elif isinstance(sym, image.LeafSymbol):
        region = [sym.region[0]-711, sym.region[1]-84, sym.region[2], sym.region[3]]
        return image.LeafSymbol(sym.image_path, region, sym.accuracy)
    else:
        return sym

p = pathlib.Path("C:\\Users\\tsuka\\gitrepo\\Macro\\state")
 
# ディレクトリ配下のテキストファイル一覧を表示（拡張子指定）
# for f in p.glob("**/*.act.json"):
#     print(f)
#     with open(f, 'rt') as fp:
#         act = json.load(fp, cls=action.ActionDecoder)

#     act_updated = update_coord_act(act)

#     with open(f, 'wt') as fp:
#         json.dump(act_updated, fp, cls=action.ActionEncoder, indent=2)

for f in p.glob("**/*.sym.json"):
    print(f)
    with open(f, 'rt') as fp:
        sym = json.load(fp, cls=image.SymbolDecoder)

    sym_updated = update_coord_sym(sym)

    with open(f, 'wt') as fp:
        json.dump(sym_updated, fp, cls=image.SymbolEncoder, indent=2)
