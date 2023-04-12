import torch

a=torch.randint(low=0,high=10,size=(10,1))
print(a)
b=torch.clamp(a,3,9)
print(b)
print(b.dtype)