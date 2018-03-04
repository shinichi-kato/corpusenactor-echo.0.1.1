

formula = "Ba*x+Ca*(1-x)+Ti+O*3"
vars = [
    {'var':'x','l':0.1,'h':0.2},
    {'var':'y','l':0,'h':1},
    {'var':'z','l':0.6,'h':0.7},
]

""" 変数名のリスト """
vnames = [x['var'] for x in vars]

""" 元素のリスト """
elms = {'Ba','Ca','O','Ti'}

""" lとhのタプルのリスト """
vlhs = [(x['l'],x['h']) for x in vars]

import itertools
ranges = {}

for e in elms:
    vlocals = {x:0 for x in elms}
    vlocals[e] = 1
    ranges[e] = []

    for vs in itertools.product(*vlhs):
        for k,v in zip(vnames,vs):
            vlocals[k]=v

        ranges[e].append(eval(formula,{},vlocals))

    ranges[e] = {'val':e,'l':min(ranges[e]),'h':max(ranges[e]),'unit':'mol'}

print (ranges)
