import os
import pickle
from matplotlib import pyplot as plt
from maptools.core import ROOT_DIR

__all__ = ['plot_tokens']

def plot_tokens(mapname: str, start: int = 0, end: int = 1e6) -> None:
    '''
    plot the tokens generated from `TokSim`.

    Parameters
    ----------
    mapname : str
        Map name

    start : int = 0
        starting iteration index.

    end : int = 0
        ending iteration index.
    '''
    file_dir = os.path.join(ROOT_DIR, 'mapsave', mapname, 'toksim', 'token.pkl')
    assert os.path.exists(file_dir), f"No such file: {file_dir}"
    with open(file_dir, 'rb') as f:
        info_dict = pickle.load(f)

    total = []
    for i, exe_list in enumerate(info_dict.values()):
        total.append([])
        for j, d in enumerate(exe_list):
            if d != 0:
                if j > start and j < end:
                    total[i].append((j, i))

    for list in total:
        if len(list) == 0:
            continue
        x, y = zip(*list)
        plt.scatter(x, y, marker='|') 
    plt.show()