import torch
from typing import Tuple, Union, Literal

__all__ = [
    'dec2bin',
    'destruct_scale'
]

def dec2bin(dec_num, bit_wide: int = 16) -> str:    
    _, bin_num_abs = bin(dec_num).split('b')    
    if len(bin_num_abs) > bit_wide:        
        raise ValueError   
    else:        
        if dec_num >= 0:            
            bin_num = bin_num_abs.rjust(bit_wide, '0')        
        else:            
            _, bin_num = bin(2**bit_wide + dec_num).split('b')    
    return bin_num


def atox(hex: str, radix: Literal['hex', 'int']) -> int:
    sign = -1 if hex[0] == '-' else 1
    hex = hex.lstrip('-').lstrip('+')
    value = 0
    for i, char in enumerate(hex, 1):
        char_byte = bytes(char, encoding='ASCII')
        char_int = int.from_bytes(char_byte, 'little')
        assert (48 <= char_int <= 57) or ((
            97 <= char_int <= 102) if radix == 'hex' else False), (
            f"not a {radix} number: {char_int}")
        if char_int <= 57:
            char_int -= 48
        else:
            char_int -= 87
        base = 16 if radix == 'hex' else 10
        value += char_int * pow(base, len(hex)-i)
    return value * sign


def atoi(data: str) -> int:
    return atox(data, radix='int')


def atohex(data: str) -> int:
    return atox(data, radix='hex')


def destruct_float(data: float) -> Tuple[int, int]:
    '''
    destruct a float number and return (`tail`, `rank`)
    where `tail` is a uint8 number, and `rank` is the opposite of the real rank
    '''
    assert data > 0, f"the scale factor must be a positive number, but got {data}"
    hex = data.hex()
    hex = hex.lstrip('-').lstrip('0x')
    hex = hex.replace('.', '')
    hex = hex.split('p')
    tail, rank = hex[0], hex[1]
    tail = tail[:3] # truncate at 9bit
    rank = atoi(rank) - 7
    tail = atohex(tail)
    tail = round(tail/2) # round 1bit, get 8bit
    assert rank < 0, f"rank should be a negetive number, but got {rank}"
    return tail, rank


def destruct_scale(
    data: Union[torch.Tensor, float]
) -> Union[Tuple[torch.Tensor, torch.Tensor], Tuple[int, int]]:

    if isinstance(data, float):
        return destruct_float(data)
    
    elif isinstance(data, torch.Tensor):
        assert data.dim() == 1, f"input Tensor dim should be 1, but got {data.dim()}"
        zipped = list(zip(*[destruct_float(float(i)) for i in data]))
        tail, rank = map(torch.tensor, zipped)
        return tail, rank

    else:
        raise AssertionError(f"input should be either Tensor or float, but got {type(data)}")
