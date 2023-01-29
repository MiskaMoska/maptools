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

# path = []
# Route_DyXY(5,0,0,10,path,0)
# for i in path:
#     print(i)

G = nx.MultiDiGraph()
# for i in range(10):
#     G.add_node(i)
# x = [(1,3,2),(1,2,'k')]
G.add_edge(1,2)
# G.add_edges_from(x)
print(G.nodes())