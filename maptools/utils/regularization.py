from typing import List, Tuple
from maptools.core import DeviceGraph

__all__ = ['regularize_pad_sizes']

def _regu_size(
    ifs: List[int], 
    ofs: List[int], 
    ks: List[int], 
    pads: List[int], 
    strs: List[int]
) -> None:
    '''
    pads : List[int]
        `pads` is referenced, after performing this method, 
        `pads` can be modified to accomodate the feature map size
    '''
    def regu_one_dim(dim: int) -> None:
        while True:
            remain = ifs[dim] + pads[0+dim] + pads[2+dim]
            remain -= max([ks[dim], strs[dim]])
            size_o = remain // strs[dim] + 1
            if size_o < ofs[dim]:
                pads[2-dim] += 1
            elif size_o == ofs[dim]:
                break
            else:
                print(f'''
                    calculated output size {size_o} larger than onnx output size {ofs[dim]}
                    input_size: {ifs[dim]}, kernel_size: {ks[dim]},
                    strides: {strs[dim]}, pads: {[pads[0+dim], pads[2+dim]]}
                    need to decrease pads
                ''')
        extra = remain % strs[dim]
        if extra != 0:
            print('starting correcting one size ....')
            assert extra <= pads[2-dim], \
                "extra pixels larger than onnx outside (right and down) pads, cannot perform correction"
            for i in range(extra):
                pads[2-dim] -= 1

    for i in range(2):
        regu_one_dim(i)


def regularize_pad_sizes(graph: DeviceGraph) -> None:
    '''
    Some onnx models have incorrect convolution or pooling pads information.
    This method checks these incorrections and regularizes them.

    However, some incorrections cannot be regularized, for example: 
    1. the `conv_output_size` does not match `pool_input_size` in the same operator.
    2. the calculated `output_size` does not match onnx recorded `output_size`.
    3. the `conv_input size` still does not match `conv_output_size` though pads are corrected.
    Encountering these incorrections will trigger assertion failure.

    Make sure to call this method after finishing opterator-graph-converting.
    '''
    for node in graph.nodes:
        config = graph.config(node)
        if 'Conv' in config['op_type']:
            cks = config['conv_kernel_size']
            cpads = config['conv_pads']
            cstrs = config['conv_strides']
            cifs = config['conv_input_size']
            cofs = config['conv_output_size']
            _regu_size(cifs, cofs, cks, cpads, cstrs)
            graph.dicts[node]['conv_pads'] = cpads
            
            if 'Pool' in config['op_type']:
                pks = config['pool_kernel_size']
                ppads = config['pool_pads']
                pstrs = config['pool_strides']
                pifs = config['pool_input_size']
                pofs = config['pool_output_size']
                assert cofs == pifs, \
                    f"conv_output_size {cofs} not match pool_input_size {pifs}"
                _regu_size(pifs, pofs, pks, ppads, pstrs)
                graph.dicts[node]['pool_pads'] = ppads
