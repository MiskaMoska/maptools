'''
TODO support for STMX
'''

import math
from onnx_converter import OperatorGraph
from typing import List, Dict, Tuple

__all__ = ['XbarMapper']

class CTG(object):

    def __init__(self) -> None:
        pass


class XbarMapper(object):

    def __init__(self, model: OperatorGraph, 
                    w: int = 256, h: int = 256, arch: str = 'resnet') -> None:
        '''
        Parameters
        ----------
        model : OperatorGraph
            pass

        w : int
            Xbar width
        
        h : int
            Xbar height
        '''
        assert w <= h, "Xbar height must be no smaller than width"
        self.model = model
        self.w = w
        self.h = h

    def _xbar_map_resnet(self) -> None:
        '''
        In ResNet, there is no concat operation
        '''
        self.xbar_config = []
        for layer in self.model.nodes:
            assert layer['op_type'] in ['Conv','Conv-Pool','Conv-Add','Conv-Pool-Add','Pool','Pool-Add'], \
                f"unexpected operation in resnet operation graph: {layer['op_type']}"
            if not "Conv" in layer['op_type']: # this layer contains no Conv
                n_inchan = layer['input_dims'][1]
                n_outchan = n_inchan
                k_size = (1,1)
            else: # this layer contains Conv
                n_inchan = layer['conv_num_inchan']
                n_outchan = layer['conv_num_outchan']
                k_size = layer['conv_kernel_size']

            layer_xbar_config = []
            pes_o = math.ceil(n_outchan / self.w) 
            for i in range(pes_o):
                layer_xbar_config.append([]) # add a new region

                # output vector mapping
                start_co = i * self.w
                if (i + 1) * self.w > n_outchan:
                    end_co = n_outchan
                else:
                    end_co = (i + 1) * self.w
                
                # input vector mapping
                slcs = math.ceil(n_inchan / self.w) # how many slcs a channel vector is divided to
                # get slice length, each slice is shorter than Xbar width
                for j in range(slcs):
                    layer_xbar_config[i].append([]) # add a new block
                    if (j + 1) * self.w > n_inchan:
                        slc_len = n_inchan % self.w
                    else:
                        slc_len = self.w
                    start_ci = j * self.w
                    end_ci = j * self.w + slc_len
                    slc_pt = (self.h // slc_len) # max slices per tile
                    pes_i = math.ceil((k_size[0]*k_size[1]) / slc_pt) 
                    for t in range(pes_i):
                        icfg = []
                        if (t + 1) * slc_pt > k_size[0]*k_size[1]:
                            it = k_size[0]*k_size[1] % slc_pt
                        else:
                            it = slc_pt
                        for k in range(it):
                            icfg.append((t*slc_pt+k,start_ci,end_ci))
                        xbar_dict = {'icfg': icfg, 'ocfg': (start_co,end_co)}
                        xbar_dict.update(layer)
                        layer_xbar_config[i][j].append(xbar_dict)

            self.xbar_config.append(layer_xbar_config)

    def xbar_map(self) -> None: 
        '''
        Map the operator graph to xbars
        Note that any xbar supports all ops
        '''
        pass

    def Print_Config(self):
        for i,layer in enumerate(self.xbar_config):
            for j,region in enumerate(layer):
                print('\n')
                print('-'*50)
                print(f'layer{i+1}_region{j+1}')
                print('-'*50)
                for k,block in enumerate(region):
                    print('`'*50)
                    print(f'block{k+1}')
                    for h,tile in enumerate(block):
                        print(f'\ntile{h}')
                        print('icfg:',tile['icfg'])
                        print('ocfg:',tile['ocfg'])

