import os
import sys
import argparse
root_dir = os.environ.get('NVCIM_HOME')
sys.path.append(os.path.join(root_dir, 'network', 'scripts'))
from gen_routing_tables import *
from gen_cast_network import *
from gen_cast_network_config import *
from gen_merge_network import *
from gen_merge_network_config import *
from gen_gather_network import *
from gen_gather_network_config import *
from gen_top_network import *
from gen_top_network_config import *
from gen_params_header import *
from maptools import read_mapinfo, read_cfginfo

parser = argparse.ArgumentParser(description='Network Builder')
parser.add_argument('--mapname', type=str, default='newmap' , help='name of the mapping case to be loaded')
parser.add_argument("--datawidth", type=int, default=34, help='network data width')
parser.add_argument("--packetlen", type=int, default=18, help='packet length for cast and gather network')
parser.add_argument("--cbufdepth", type=int, default=64, help='buffer depth in cast router')
parser.add_argument("--test", action='store_true', help='generate files for local testing, not needed in system simulation')
parser.add_argument("--flitnum", type=int, default=10000, help='number of flits to be generated, must be divided by `packetlen-2`')
parser.add_argument("--clean", action='store_true', help='clean all generated files to reset the folder')
args = parser.parse_args()

if args.clean:
    config_folder = os.path.join(root_dir, 'network', 'config')
    generated_folder = os.path.join(root_dir, 'network', 'rtl', 'generated')
    test_files = [os.path.join(root_dir, 'network', 'test', 'system.sv'),
                    os.path.join(root_dir, 'network', 'test', 'top_tb.sv'),
                    os.path.join(root_dir, 'network', 'test', 'send_pool.txt')
                    ]
    send_pool = os.path.join(root_dir, 'network', 'test', 'send_pool')
    for f in [config_folder, generated_folder] + test_files:
        print(f'removing {f}')
        os.system(f'rm -rf {f}')
    sys.exit()

# read configuration information
mapinfo = read_mapinfo(args.mapname)
cfginfo = read_cfginfo(args.mapname)
w = cfginfo['network_width']
h = cfginfo['network_height']
cast_config = cfginfo['cast_config']
merge_config = cfginfo['merge_config']
gather_config = cfginfo['gather_config']
dw = args.datawidth
tail_xbars = mapinfo['tail_xbars']

# get flees ports
flees = []
for xbar in tail_xbars:
    paths = cast_config[xbar]
    print('tail_xbar:', xbar, 'path_config:', paths)
    flag = False
    for i in range(1, 5): # west, east, vert0, vert1
        if i not in [tup[1] for tup in paths]:
            flees.append((xbar, i))
            flag = True
            break
    if not flag:
        print(f'cannot find proper flee port for xbar: {xbar}, paths: {paths}')
        sys.exit()

flees = list(zip(*flees))

# complete cast config dictionary by adding stab and flee paths
cast_config[(0, 0)].append((1, 0, 1023))
for i, node in enumerate(flees[0]):
    cast_config[node].append((0, flees[1][i], 1022))

# generate cast and gather routing tables
gen_routing_tables(root_dir, w, h, cast_config, 'cast')
gen_routing_tables(root_dir, w, h, gather_config, 'gather')

# generate cast, merge, and gather networks
gen_cast_network(root_dir, dw, w, h, flees)
gen_merge_network(root_dir, dw, w, h)
gen_gather_network(root_dir, dw, w, h)

# generate cast, merge, and gather network configuration files
gen_cast_network_config(root_dir, w, h)
gen_merge_network_config(root_dir, merge_config)
gen_gather_network_config(root_dir, w, h)

# generate top network
gen_top_network(root_dir, w, h, flees)

# generate top network configuration file
top_config = dict()
xbar_config = mapinfo['xbar_config']
for xbar in xbar_config:
    top_config[xbar] = {'cast_out': xbar_config[xbar]['cast_out'], 
                        'merge_out': xbar_config[xbar]['merge_out'],
                        'gather_out': xbar_config[xbar]['gather_out'],
                        'merge_in': xbar_config[xbar]['merge_in'],
                        'gather_in': xbar_config[xbar]['gather_in']}

cast_paths = mapinfo['cast_paths']
for item in cast_paths.values():
    src = item['src'][0]
    sid = item['sid']
    top_config[src]['cast_sid'] = sid

gather_paths = mapinfo['gather_paths']
for item in gather_paths.values():
    src = item['src'][0]
    sid = item['sid']
    top_config[src]['gather_sid'] = sid

gen_top_network_config(root_dir, w, h, top_config, flees)

# generate params header
gen_params_header(root_dir, w, h, args.datawidth, args.packetlen, args.cbufdepth)

if args.test:
    assert args.flitnum % (args.packetlen-2) == 0, f"`flitnum`({args.flitnum}) must be divided by `packetlen-2`({args.packetlen-2}))"
    print("-"*50)
    print("generating files for local testing ....")
    from gen_system import *
    from gen_top_tb import *
    from gen_packets import *
    gen_system(root_dir, w, h, flees)
    gen_top_tb(root_dir, flees, args.flitnum)
    gen_packets(root_dir, args.datawidth, args.flitnum)

# 只剩下 virtual pe， top_tb了, 把生成数据包拿到外面来放到bulder里执行
