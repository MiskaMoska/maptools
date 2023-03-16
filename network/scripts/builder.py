from gen_cast_network import *
from gen_merge_network import *

w = 5
h = 10
data_width = 34
root_dir = 'c:/git/nvcim-comm'

gen_cast_network(root_dir, data_width, w, h, flees)
gen_merge_network(root_dir, data_width, w, h, flees)
