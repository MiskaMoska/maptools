import torch
from torchvision import transforms
from PIL import Image
from typing import Tuple

__all__ = ['get_input']

def get_input(img_path: str, resize: Tuple = (224, 224)) -> torch.Tensor:
    assert len(resize) == 2, f"resize must be a 2-element tuple, but got {len(resize)}"
    trans = transforms.Compose([
        transforms.ToTensor()
    ])
    image_file = img_path
    img = Image.open(image_file)
    img = img.resize(resize)
    img = trans(img)
    return torch.unsqueeze(img, dim=0)