a = [((1,2),42),((3,4),5)]
b = list(zip(*a))
print((1,2) in b[0])
print(b[0].index((1,2)))