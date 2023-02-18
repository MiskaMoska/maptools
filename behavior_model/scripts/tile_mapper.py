'''
TODO support for STMX
'''

import math

class TileMapper(object):

    def __init__(self,model:list,w=256,h=256,num_xbar=1):
        '''
            Parameters
            ----------
            model : list[dict] = [layer_dict1, layer_dict2, layer_dict3, ....]
                AI model that contains information about each layer
                The information is stored in a dictionary, which is defined as:
                    
                layer_dict = {"ci","co","ks","st","pad","pool"}
                    "ci" : int
                        number of input channels
                    
                    "co" : int
                        number of output channels

                    "ks" : int
                        kernel size

                    "st" : int
                        stride

                    "pad" : list[int] = [p_left, p_right, p_up, p_down]
                        padding mode, layer_dict["pad"] being None means no padding.
                    
                    "pool" : int
                        size of pooling window, layer_dict["pool"] being None means no pooling.

            w : int
                Xbar width
            
            h : int
                Xbar height

            num_xbar : int
                number of Xbars in a Tile (PE)
        '''
        assert w <= h, "Xbar height must be no smaller than width"
        self.model = model
        self.w = w
        self.h = h
        self.num_xbar = num_xbar

    def __map_one_slice(self,slc_len,ks,start_ci,end_ci,start_co,end_co,
                            layer_tile_config_i:list):
        slc_pt = (self.h // slc_len) # max slices per tile
        pes_i = math.ceil((ks**2) / slc_pt) 
        for j in range(pes_i):
            icfg = []
            if (j + 1) * slc_pt > ks ** 2:
                it = ks ** 2 % slc_pt
            else:
                it = slc_pt
            for k in range(it):
                icfg.append((j*slc_pt+k,start_ci,end_ci))
            layer_tile_config_i.append({'icfg':icfg,'ocfg':(start_co,end_co)})

    def Model_Segmentation(self):
        '''
        Get model segments by distributing each model layer to several tiles
        '''
        self.pes_i = []
        self.pes_o = []
        self.tile_config = []
        for layer in self.model:
            layer_tile_config = []
            if self.num_xbar > 1: # STMX
                pass
            else: # STSX
                pes_o = math.ceil(layer['co'] / self.w) 
                self.pes_o.append(pes_o) # occupied PEs (Tiles) by output vector of this layer
                for i in range(pes_o):
                    layer_tile_config.append([])

                    # output vector mapping
                    start_co = i * self.w
                    if (i + 1) * self.w > layer['co']:
                        end_co = layer['co']
                    else:
                        end_co = (i + 1) * self.w
                    
                    # input vector mapping
                    if layer['ci'] <= self.w:
                        self.__map_one_slice(layer['ci'],layer['ks'],0,layer['ci'],
                                                start_co,end_co,layer_tile_config[i])

                    else:
                        slcs = math.ceil(layer['ci'] / self.w) # how many slcs a channel vector is divided to
                        # get slice length, each slice is shorter than Xbar width
                        for j in range(slcs):
                            if (j + 1) * self.w > layer['ci']:
                                slc_len = layer['ci'] % self.w
                            else:
                                slc_len = self.w
                            start_ci = j * self.w
                            end_ci = j * self.w + slc_len
                            self.__map_one_slice(slc_len,layer['ks'],start_ci,end_ci,
                                                    start_co,end_co,layer_tile_config[i])

                self.pes_i.append(len(layer_tile_config[i])) # occupied PEs (Tiles) by input vector of this layer
            self.tile_config.append(layer_tile_config)
        
    def Print_Config(self):
        for i,layer in enumerate(self.tile_config):
            for j,region in enumerate(layer):
                print('\n')
                print('-'*50)
                print(f'layer{i+1}_region{j+1}')
                print('-'*50)
                for k,tile in enumerate(region):
                    print(f'\ntile{k+1}')
                    print('icfg:',tile['icfg'])
                    print('ocfg:',tile['ocfg'])

if __name__ == "__main__":
    dict1 = dict()
    dict1['ci'] = 96
    dict1['co'] = 128
    dict1['ks'] = 3

    dict2 = dict()
    dict2['ci'] = 64
    dict2['co'] = 256
    dict2['ks'] = 3

    model = [dict1,dict2]
    tm = TileMapper(model,w=64,h=64)
    tm.Model_Segmentation()
    tm.Print_Config()


