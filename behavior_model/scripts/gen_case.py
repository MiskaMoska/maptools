'''
Generate cases with user defined parameters (network wdith, height, etc) and target metrics (contention level, etc)
'''
import pickle
import os
from noc_mapper import NocMapper

if __name__ == "__main__":
    W = 5
    H = 11
    CONTENT_LEVEL = 16
    os.chdir('.')
    try:
        os.mkdir('cases')
    except:
        pass
    save_file = f"/mnt/c/git/nvcim-comm/behavior_model/scripts/cases/w{W}_h{H}_cl{CONTENT_LEVEL}.pkl"
    maper = NocMapper(W,H,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
    case_dict = dict()
    while True:
        maper.Run_Mapping()
        con = maper.Get_Contention_Level()
        if con == CONTENT_LEVEL:
            case_dict['cast_paths'] = maper.cast_paths
            case_dict['merge_paths'] = maper.merge_paths
            case_dict['cast_targets'] = maper.cast_targets
            case_dict['merge_nodes'] = maper.merge_nodes
            with open(save_file,'wb') as f_save:
                pickle.dump(case_dict, f_save)
            break
