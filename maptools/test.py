import torch
import torch.nn.functional as F
import torch.nn as nn

# a = torch.Tensor([1,2,3,4,5])

# b = [torch.ones(3,3)*a[i] for i in range(a.shape[0])]
# b = torch.stack(b)
# b = b.expand(1,-1,-1,-1)
# print(b.shape)


a = torch.tensor([2,4,6,8])
b = torch.tensor([[[[1,1,1],
                  [1,1,1],
                  [1,1,1]],
                 [[1,1,1],
                  [1,1,1],
                  [1,1,1]],
                 [[1,1,1],
                  [1,1,1],
                  [1,1,1]],
                 [[1,1,1],
                  [1,1,1],
                  [1,1,1]]]])

a = a.view(1,-1,1,1)
c = a * b
print(a.shape)
print(b.shape)
print(c)