import sys
sys.path.append("..") 
from scripts.configurator import Configurator
from scripts.mapper import Mapper
from scripts.deadlock_analyzer import DeadlockAnalyzer

W = 5
H = 11

accum_con = 1000
while(True):
    maper = Mapper(W,H,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
    maper.Run_Mapping()
    con = maper.Get_Contention_Level()

    if con < accum_con:
        print("\ncontention level:",con)
        accum_con = con
        da = DeadlockAnalyzer(W,H,maper.cast_paths,maper.merge_paths)
        da.Run_Analyzing()
    
    if con == 0:
        cfg = Configurator(W,H,maper.cast_paths,maper.merge_paths,maper.merge_nodes)
        cfg.Run_Configuring()
        break

