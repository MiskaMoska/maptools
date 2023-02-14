'''
Test the function of tile mapper
'''

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
    from tile_mapper import TileMapper
    from noc_mapper import NocMapper
    tm = TileMapper(MODEL_VGG16,w=256,h=256*5)
    tm.Model_Segmentation()
    tm.Print_Config()
    print(tm.pes_i)
    print(tm.pes_o)
    nm = NocMapper(5,11,tm.pes_i,tm.pes_o)
    nm.Run_Mapping()
    # maper.Plot_Map()
    print(nm.model_regions)