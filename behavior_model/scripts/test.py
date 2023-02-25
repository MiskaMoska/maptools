import random
import networkx as nx

def Route_DyXY(sx,sy,dx,dy,path:list,sid=0)->list:
    if sx == dx and sy == dy:
        return
    if sx != dx and sy != dy:
        randbit = True if random.random() > 0.5 else False
        if randbit:
            nxt_sx = sx
            nxt_sy = sy + (1 if sy < dy else -1)
        else:
            nxt_sy = sy
            nxt_sx = sx + (1 if sx < dx else -1)
    else:
        if sx == dx:
            nxt_sx = sx
            nxt_sy = sy + (1 if sy < dy else -1)
        elif sy == dy:
            nxt_sy = sy
            nxt_sx = sx + (1 if sx < dx else -1)
    path.append(((sx,sy),(nxt_sx,nxt_sy)))
    Route_DyXY(nxt_sx,nxt_sy,dx,dy,path,sid=sid)

G = nx.MultiDiGraph()
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(2,3)
G.add_edge(2,5)
G.add_edge(3,4)
G.add_edge(4,5)


d = {1:111,2:222,3:333,4:444,5:555}

def gen():
    a = [1,2,3,4,5]
    for i in a:
        yield i


def wrap():
    for i in gen():
        yield d[i]

for m in wrap():
    print(m)

