'''
Test the function of tile mapper
'''

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
MODEL_VGG16[6] = {'ci':256, 'co':512, 'ks':3}
MODEL_VGG16[7] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[8] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[9] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[10] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[11] = {'ci':512, 'co':512, 'ks':3}
MODEL_VGG16[12] = {'ci':512, 'co':512, 'ks':3}

# test
MODEL_TEST = []
for i in range(5):
    MODEL_TEST.append(dict())
MODEL_TEST[0] = {'ci':3, 'co':600, 'ks':3}
MODEL_TEST[1] = {'ci':600, 'co':60, 'ks':3}
MODEL_TEST[2] = {'ci':60, 'co':512, 'ks':3}
MODEL_TEST[3] = {'ci':512, 'co':580, 'ks':3}
MODEL_TEST[4] = {'ci':580, 'co':256, 'ks':3}

if __name__ == "__main__":
    from tile_mapper import TileMapper
    from noc_mapper import NocMapper
    tm = TileMapper(MODEL_VGG16,w=256,h=256*5)
    tm.Run_Mapping()
    tm.Print_Config()
    nm = NocMapper(tm.tile_config,6,12)
    nm.Run_Mapping()

    # for i in range(len(nm.model_regions)-1):
    #     print('\nregions:',nm.model_regions[i+1])
    #     print('targets:',nm.cast_targets[i])

    print('\ntile_map')
    for k,v in nm.tile_map.items():
        print('pos:',k,'config:',v['icfg'])
    
    print('\ncast_comms')
    for i in nm.cast_comms:
        print(i)

    print('\nmerge_comms')
    for i in nm.merge_comms:
        print(i)

    nm.Plot_Map()
