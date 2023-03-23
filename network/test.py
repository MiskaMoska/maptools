import os

os.chdir('/mnt/c/git/nvcim-comm/network/rtl/generated')

for i in os.listdir():
    print(f'./rtl/generated/{i}')