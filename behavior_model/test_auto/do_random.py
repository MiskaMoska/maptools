'''
运行 ./run.sh
循环产生随机的通信规划，消除死锁环，运行VCS仿真查看是否会死锁
'''

import sys
sys.path.append("..") 
from scripts.configurator import Configurator
from scripts.noc_mapper import NocMapper
from scripts.deadlock_analyzer import DeadlockAnalyzer
from scripts.deadlock_killer import DeadlockKiller

W = 5
H = 11

maper = NocMapper(W,H,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
maper.Run_Mapping()
maper.Plot_Map()
con = maper.Get_Contention_Level()
print("contention level:",con)
dla = DeadlockAnalyzer(W,H,maper.cast_paths,maper.merge_paths,log=None)
dla.Run_Analyzing()
# dla.Plot_Loops()
dlk = DeadlockKiller(W,H,maper.merge_nodes,maper.cast_targets,maper.cast_paths,dla.sloops,dla.cloops)
dlk.Run_Killing()
dlk.Plot_Remain_Loops()
cfg = Configurator(W,H,maper.cast_paths,maper.merge_paths,maper.merge_nodes,e2e_dict=dlk.e2e_dict,ubm_nodes=dlk.ubm_nodes)
cfg.Run_Configuring()

