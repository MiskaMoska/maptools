from typing import List

def is_subseq(a: List, b: List) -> bool:
    '''
    Judges if is the susequence of b, where a must be a 2-element list.
    '''
    for i in range(len(b)-1):
        if a[0] == b[i]:
            if b[i+1] == a[1]:
                return True
    return False

