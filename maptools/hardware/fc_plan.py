from typing import Dict, Tuple, List, Generator

__all__ = ['fc_plan']

def fc_plan(path: Dict[str, Dict],
            config: Dict[Tuple, List[Tuple]]) -> Generator:
    '''
    This function analyzes flow control schemes for cast and gather networks and
    generates flow control planning information for network configuration.
    :param path: can be either `cast_path` or `gather_path` generated from `NocConfig`.
    :param config: can be either `cast_config` or `gather_config` generated from `NocConfig`.
    :return a generator which generates (src, dst_list) of credit-flow-controlled chain.
    '''
    pass
    fc_streams: List[Tuple] = [] # streams needing fc
    # for lst in config.

#“credit应该从PE内的buffer分配，而不是从网络接口分配，这样一旦credit反压说明buffer满了”