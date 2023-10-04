from maptools import *
from maptools.utils.io import _read_pkl

file_path = os.path.join(ROOT_DIR, 'mapsave', 'resnet18', 'toksim', 'tokens.pkl')
d: Dict = _read_pkl(file_path)
l: List = d[(19, 0, 0, 0)]
print(d.keys())
print(l.index(1)/len(l))