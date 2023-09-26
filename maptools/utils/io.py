import os
import torch
import pickle
import logging
from PIL import Image
from typing import Tuple, Dict, Any
from torchvision import transforms as transforms
from maptools.core import ROOT_DIR, ModelParams

__all__ = [
    'get_input',
    'read_params',
    'read_quantparams',
    'read_mapinfo',
    'read_generalcfg',
    'read_castcfg',
    'read_mergecfg',
    'read_results',
    'get_logger'
]

def get_input(img_path: str, resize: Tuple = (224, 224)) -> torch.Tensor:
    assert len(resize) == 2, f"resize must be a 2-element tuple, but got {len(resize)}"
    trans = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
    ])
    image_file = img_path
    img = Image.open(image_file)
    img = img.resize(resize)
    img = trans(img)
    return torch.unsqueeze(img, dim=0)

def _read_pkl(file_path: str) -> Any:
    with open(file_path, 'rb') as f:
        res = pickle.load(f)
    return res

def read_params(mapname: str) -> ModelParams:
    file_path = os.path.join(ROOT_DIR, 'mapsave', mapname, 'params.pkl')
    return _read_pkl(file_path)

def read_quantparams(mapname: str) -> ModelParams:
    file_path = os.path.join(ROOT_DIR, 'mapsave', mapname, 'quantparams.pkl')
    return _read_pkl(file_path)

def read_mapinfo(mapname: str) -> Dict:
    file_path = os.path.join(ROOT_DIR, 'mapsave', mapname, 'mapinfo.pkl')
    return _read_pkl(file_path)

def read_generalcfg(mapname: str) -> Dict:
    file_path = os.path.join(ROOT_DIR, 'mapsave', mapname, 'hwconfig', 'general_config.pkl')
    return _read_pkl(file_path)

def read_castcfg(mapname: str) -> Dict:
    file_path = os.path.join(ROOT_DIR, 'mapsave', mapname, 'hwconfig', 'cast_config.pkl')
    return _read_pkl(file_path)

def read_mergecfg(mapname: str) -> Dict:
    file_path = os.path.join(ROOT_DIR, 'mapsave', mapname, 'hwconfig', 'merge_config.pkl')
    return _read_pkl(file_path)

def read_results(mapname: str, file_name: str) -> Dict:
    file_name = file_name.rstrip('.pkl') + '.pkl'
    file_path = os.path.join(ROOT_DIR, 'mapsave', mapname, 'calcusim', file_name)
    return _read_pkl(file_path)

def get_logger(name: str, dir: str) -> logging.Logger:
    filename = os.path.join(dir, f'{name}.log')
    logger = logging.getLogger(name)
    fh = logging.FileHandler(filename, mode='w', encoding='utf-8')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger