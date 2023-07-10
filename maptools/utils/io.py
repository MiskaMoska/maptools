import os
import torch
import pickle
import logging
from PIL import Image
from typing import Tuple, Dict
from torchvision import transforms as transforms
from maptools.core import ROOT_DIR, ModelParams

__all__ = [
    'get_input',
    'read_params',
    'read_quantparams',
    'read_mapinfo',
    'read_cfginfo',
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

def read_params(mapname: str) -> ModelParams:
    file_dir = os.path.join(ROOT_DIR, 'mapsave', mapname, 'params.pkl')
    with open(file_dir, 'rb') as f:
        params = pickle.load(f)
    return params

def read_quantparams(mapname: str) -> ModelParams:
    file_dir = os.path.join(ROOT_DIR, 'mapsave', mapname, 'quantparams.pkl')
    with open(file_dir, 'rb') as f:
        params = pickle.load(f)
    return params

def read_mapinfo(mapname: str) -> Dict:
    file_dir = os.path.join(ROOT_DIR, 'mapsave', mapname, 'mapinfo.pkl')
    with open(file_dir, 'rb') as f:
        mapinfo = pickle.load(f)
    return mapinfo

def read_cfginfo(mapname: str) -> Dict:
    file_dir = os.path.join(ROOT_DIR, 'mapsave', mapname, 'cfginfo.pkl')
    with open(file_dir, 'rb') as f:
        cfginfo = pickle.load(f)
    return cfginfo

def read_results(mapname: str, file_name: str) -> Dict:
    file_name = file_name.rstrip('.pkl') + '.pkl'
    file_dir = os.path.join(ROOT_DIR, 'mapsave', mapname, 'calcusim', file_name)
    with open(file_dir, 'rb') as f:
        results = pickle.load(f)
    return results

def get_logger(name: str, dir: str) -> logging.Logger:
    filename = os.path.join(dir, f'{name}.log')
    logger = logging.getLogger(name)
    fh = logging.FileHandler(filename, mode='w', encoding='utf-8')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger