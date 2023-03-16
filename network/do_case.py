'''
Get cases from ./behavior_model/scripts/cases and run configuration
'''

import sys
import pickle
from configurator import Configurator
from noc_mapper import NocMapper
from deadlock_analyzer import DeadlockAnalyzer
from deadlock_killer import DeadlockKiller

W = 7
H = 8
CONTENT_LEVEL = 13

save_file = f"/mnt/c/git/nvcim-comm/network/cases/w{W}_h{H}_cl{CONTENT_LEVEL}.pkl"

with open(save_file, 'rb') as f_read:
    case_dict = pickle.load(f_read)
cast_paths = case_dict['cast_paths']
merge_paths = case_dict['merge_paths']
merge_nodes = case_dict['merge_nodes']
cast_targets = case_dict['cast_targets']
dla = DeadlockAnalyzer(W,H,cast_paths,merge_paths,log=None)
dla.Run_Analyzing()
dlk = DeadlockKiller(W,H,merge_nodes,cast_targets,cast_paths,dla.sloops,dla.cloops)
dlk.Run_Killing()
dlk.Plot_Remain_Loops()
cfg = Configurator(W,H,cast_paths,merge_paths,merge_nodes,
                    e2e_dict=dlk.e2e_dict,ubm_nodes=dlk.ubm_nodes)
cfg.Run_Configuring()
for k,v in cfg.cast_paths.items():
    print(k,v)