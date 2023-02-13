'''
Reconstruct cast_paths from cast_routing table
'''

import os
import sys

W = 5
H = 11

merge_paths = [
    ((1,1),(2,1)),
    ((3,1),(4,1)),
    ((2,2),(1,2)),
    ((4,3),(3,3)),
    ((2,3),(1,3)),
    ((1,3),(0,3)),
    ((4,4),(3,4)),
    ((3,4),(2,4)),
    ((2,4),(1,4)),
    ((4,5),(3,5)),
    ((3,5),(2,5)),
    ((2,5),(1,5)),
    ((0,6),(1,6)),
    ((1,6),(2,6)),
    ((4,7),(3,7)),
    ((2,7),(1,7)),
    ((1,7),(0,7)),
    ((1,8),(2,8)),
    ((3,8),(2,8)),
    ((4,8),(3,8)),
    ((4,9),(3,9)),
    ((2,9),(3,9)),
    ((1,9),(2,9)),
    ((1,10),(0,10)),
    ((2,10),(1,10)),
    ((0,1),(0,2)),
    ((0,3),(0,4)),
    ((0,5),(0,6)),
    ((0,7),(0,8)),
    ((0,9),(0,10)),
    ((3,2),(3,3)),
    ((3,6),(3,7)),
    ((4,2),(4,3)),
    ((4,6),(4,7)),
]

def reconstruct_paths():
    dir = '/mnt/c/git/nvcim-comm/behavior_model/test_auto/config/'
    cast_paths = dict()

    def str_2_int(string)->int:
        data = 0
        for i in range(len(string)):
            if string[i] == '1':
                data += 2**(len(string)-1-i)
        return data

    for x in range(W):
        for y in range(H):
            for c in range(5):
                file = dir + f"cast_rt_{x}_{y}_{c}"
                with open(file,"r") as f:
                    for i,line in enumerate(f):
                        dst = line[0:5]
                        sid = line[5:15]
                        for b in range(len(dst)):
                            if dst[b] == "1":
                                if (x,y) not in cast_paths.keys():
                                    cast_paths[(x,y)] = []
                                cast_paths[(x,y)].append((c,4-b,str_2_int(sid)))

    return cast_paths

if __name__ == "__main__":
    from deadlock_analyzer import DeadlockAnalyzer
    dla = DeadlockAnalyzer(W,H,reconstruct_paths(),merge_paths,log=None)
    dla.Run_Analyzing()
    dla.Plot_Loops()

