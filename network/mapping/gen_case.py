'''
Generate cases with user defined parameters (network wdith, height, etc) and target metrics (contention level, etc)
'''
import pickle
import os
from tile_mapper import TileMapper
from noc_mapper import NocMapper

# VGG16
MODEL_VGG16 = []
for i in range(13):
    MODEL_VGG16.append(dict())

MODEL_VGG16[0] = {'ci':3, 'co':64, 'ks':3}
MODEL_VGG16[1] = {'ci':64, 'co':64, 'ks':3}
MODEL_VGG16[2] = {'ci':64, 'co':128, 'ks':3}
MODEL_VGG16[3] = {'ci':128, 'co':128, 'ks':3}
MODEL_VGG16[4] = {'ci':128, 'co':256, 'ks':3}
MODEL_VGG16[5] = {'ci':256, 'co':256, 'ks':3}
MODEL_VGG16[6] = {'ci':256, 'co':256, 'ks':3}
MODEL_VGG16[7] = {'ci':256, 'co':512, 'ks':3}
MODEL_VGG16[8] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[9] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[10] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[11] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[12] = {'ci':512, 'co':512, 'ks':3}

if __name__ == "__main__":
    W = 7
    H = 8
    CONTENT_LEVEL = 13
    os.chdir('.')
    try:
        os.mkdir('cases')
    except:
        pass
    save_file = f"/mnt/c/git/nvcim-comm/network/cases/w{W}_h{H}_cl{CONTENT_LEVEL}.pkl"
    tm = TileMapper(MODEL_VGG16,w=256,h=256*5)
    tm.Run_Mapping()
    tm.Print_Config()
    nm = NocMapper(tm.tile_config,W,H)
    case_dict = dict()
    while True:
        nm.Run_Mapping()
        con = nm.Get_Contention_Level()
        if con == CONTENT_LEVEL:
            case_dict['cast_paths'] = nm.cast_paths
            case_dict['merge_paths'] = nm.merge_paths
            case_dict['cast_targets'] = nm.cast_targets
            case_dict['merge_nodes'] = nm.merge_nodes
            with open(save_file,'wb') as f_save:
                pickle.dump(case_dict, f_save)
            break
