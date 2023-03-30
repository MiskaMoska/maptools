from typing import Dict, Tuple, List, Generator

__all__ = ['fc_plan']

def fc_plan(paths: Dict[str, Dict], config: Dict[Tuple, List[Tuple]]) -> Dict[Tuple, List[Tuple]]:
    '''
    This function analyzes flow control schemes for cast and gather networks and
    generates flow control planning information for network configuration.

    :param paths: can be either `cast_path` or `gather_path` generated from `NocConfig`.
    :param config: can be either `cast_config` or `gather_config` generated from `NocConfig`.

    :return: a dictionary with flow control source node as keys and corresponding destination node list as values.
    '''
    fc_streams: List[int] = [] # streams needing flow control
    for lst in config.values():
        local_dict = dict()
        for p in lst:
            if p[1] not in local_dict.keys():
                local_dict[p[1]] = []
            local_dict[p[1]].append(p[2]) # record stream id
        for v in local_dict.values():
            if len(v) > 1: # multiple streams contend at the same putput port
                for sid in v:
                    fc_streams.append(sid)
    
    fc_dict: Dict[Tuple, List[Tuple]] = dict()
    for comm in paths.values():
        if comm['sid'] in fc_streams: # is a flow-controlled connection
            fc_dict[comm['src'][0]] = comm['dst']
    
    return fc_dict



