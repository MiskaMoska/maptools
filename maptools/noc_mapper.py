'''
TODO need to provide support for random region division
'''
import random
from random import shuffle
import networkx as nx
from matplotlib import pyplot as plt
from typing import List, Dict, Tuple, Any, Optional
from functools import cached_property
from xbar_mapper import *
from copy import deepcopy
from ctg import *
from utils import *

__all__ = ['NocMapper']

class NocMapper(object):

    def __init__(self, ctg: CTG, w: int, h: int, *args, **kwargs) -> None:
        '''
            Parameters
            ----------
            ctg : CTG
                communication trace graph

            w : int
                xbar array width

            h : int
                xbar array height

            kwargs : Dict
                dir_name : str = './'
                    root path to save the map figure.
            
                cast_method : bool = 'steiner'
                    'dyxy'      : DyXY-routing-based algorithm to run cast routing path plan, random.
                    'steiner'   : minimum steiner-tree-based algorithm to run cast routing path plan, deterministic.
        
            Key Members:
            ------------
            self.map_dict : Dict[Tuple[int, int, int, int], Tuple[int, int]]
                Map the logical xbar (4-element tuple) to the physical xbar (2-element tuple).

            self.xxx_paths : Dict[str, Dict[str, Any]]
                xxx can be any of [cast, merge, gather].
                Stores the mapped paths and corresponding attributes for each connection type.
                {'connection_name' : {'sid' : int, 'path' : List[Tuple], 'load_ratio' : float, ....}}
        '''
        self.ctg = ctg
        self.w = w
        self.h = h
        self.dir_name = './'
        self.cast_method = 'steiner'
        self.__dict__.update(kwargs)

        # mapping from logical xbars to physical xbars
        self.map_dict: Dict[Tuple[int, int, int, int], Tuple[int, int]] = dict()

        # intermediate representations
        self.projected_model = []
        self.model_regions = []
        self.merge_nodes = []
        self.cast_targets = []

        # network routing paths
        self.cast_paths: Dict[str, Dict[str, Any]] = dict()
        self.merge_paths: Dict[str, Dict[str, Any]] = dict()
        self.gather_paths: Dict[str, Dict[str, Any]] = dict()

    @staticmethod
    def _gen_reverse_s(w: int, h: int) -> List[Tuple[int, int]]:
        '''
        generate reverse-s path
        '''
        rs_path = []
        for i in range(h):
            for j in range(w):
                idx = (i+1)*w-j-1 if i % 2 else i*w+j
                rs_path.append((idx % w, idx // w))
        return rs_path
    
    def map_xbars(self) -> None:
        '''
        Map the xbars to the xbar array following reverse-s path
        '''
        rs_path = self._gen_reverse_s(self.w, self.h)
        for idx, region in self.ctg.regions:
            merge_xbar = region[0]
            while True:
                valid = True
                shuffle(region) # random mapping
                merge_idx = region.index(merge_xbar) # find the merge xbar
                y_pos_merge = rs_path[idx+merge_idx]
                for i in range(merge_idx, len(region)):
                    if rs_path[idx+i] > y_pos_merge: # larger y_pos than merge xbar
                        valid = False
                        break
                if not valid: # begin next loop
                    continue

                for i, xbar in enumerate(region):
                    self.map_dict[xbar] = rs_path[idx+i] # record map
                break

    @staticmethod
    def _route_dyxy(w: int, h: int, sx: int, sy: int, 
                        dx: int, dy: int, path: List[Tuple], 
                        region: Optional[List[Tuple]] = None) -> None:
        '''
        Route from (sx, sy) to (dx, dy) following DyXY routing algorithm.

        Parameters
        -------------------
        path : List[Tuple]
            Where the routing path results is located after performing this method.

        region : Optional[List[Tuple]]
            To constraint the routing path in a region.
            When asserted, the routing path is limited to the nodes in `region`.
        '''
        if sx == dx and sy == dy:
            return
        if sx != dx and sy != dy:
            # prechoose horizontal
            nxt_sy = sy
            nxt_sx = sx + (1 if sx < dx else -1)
            go_vertical = True if random.random() > 0.5 else False
            if go_vertical:
                nxt_sx = sx
                nxt_sy = sy + (1 if sy < dy else -1)
        else:
            if sx == dx:
                nxt_sx = sx
                nxt_sy = sy + (1 if sy < dy else -1)
            elif sy == dy:
                nxt_sy = sy
                nxt_sx = sx + (1 if sx < dx else -1)

        # if constrained routing region considered
        if not region is None:
            if (nxt_sx, nxt_sy) not in region:
                if sy == nxt_sy:
                    nxt_sx = sx
                    nxt_sy = sy + (1 if sy < dy else -1)
                elif sx == nxt_sx:
                    nxt_sy = sy
                    nxt_sx = sx + (1 if sx < dx else -1)
            assert (nxt_sx, nxt_sy) in region, "critical error ecountered at merge path"
        path.append(((sx, sy), (nxt_sx ,nxt_sy)))
        NocMapper._route_dyxy(w,h,nxt_sx,nxt_sy,dx,dy,path,region=region)

    @staticmethod
    def _get_channel(bias_pos: Tuple, now_pos: Tuple, root_pos: Tuple) -> int:
        if bias_pos[0] < now_pos[0]: # west
            return 1
        if bias_pos[0] > now_pos[0]: # east
            return 2
        if now_pos[0] < root_pos[0]: # vert0
            return 3
        return 4 # vert1

    def _cast_plan(self) -> None:
        '''
        Planning cast routing paths
        Make sure to call this method after `self.map_xbars()`
        '''
        # cast tree number
        cast_num = self.ctg.cast_num

        for sid, (name, root_node, dst_nodes) in enumerate(self.ctg.cast_trees,1):
            root_node = self.map_dict[root_node] # get the mapped node pos
            print(f"starting cast plan {sid}/{cast_num} ....")
            # keep generating the multicast tree until it is valid
            # valid means every node in the multicast tree has no more than 1 in_edge
            if self.cast_method == 'steiner':
                dst_nodes = [self.map_dict[n] for n in dst_nodes]
                base_g = build_mesh(dst_nodes + [root_node])
                g = nx.algorithms.approximation.steiner_tree(base_g, dst_nodes + [root_node])
                g = nx.dfs_tree(g, source=root_node)
            elif self.cast_method == 'dyxy':
                while True:
                    # for each multicast tree
                    # create the simple cast graph where each node represents a cast router
                    g = nx.MultiDiGraph()

                    # complete the simple cast graph by the generated multicast tree
                    paths = []
                    for dst_node in dst_nodes:
                        path = []
                        self._route_dyxy(self.w, self.h,
                                            root_node[0], root_node[1], 
                                            dst_node[0], dst_node[1], path)
                        paths.extend(path)
                    paths = list(set(paths))
                    g.add_edges_from(paths)

                    # verify the validity of the generated multicast tree
                    flag = True
                    for node in g.nodes():
                        if g.in_degree(node) > 1:
                            flag = False
                            break
                    if flag:
                        break
            self.cast_paths[name] = dict()
            self.cast_paths[name]['sid'] = sid
            self.cast_paths[name]['root_node'] = root_node
            self.cast_paths[name]['dst_nodes'] = dst_nodes
            self.cast_paths[name]['path'] = list(g.edges) # add to cast_paths
            self.cast_paths[name]['load_ratio'] = self.ctg.get_attr(name, 'load_ratio')

    def _merge_plan(self) -> None:
        '''
        Planning merge routing paths
        Make sure to call this method after `self.map_xbars()`
        '''
        # merge tree number
        merge_num = self.ctg.merge_num  

        for sid, (name, srcs, root_node) in enumerate(self.ctg.merge_trees, 1):
            root_node = self.map_dict[root_node] # get the mapped node pos
            src_nodes = [self.map_dict[src] for src in srcs ] # get the mapped node pos
            region_nodes = deepcopy(src_nodes)
            region_nodes.append(root_node)
            print(f"starting merge plan {sid}/{merge_num} ....")
            # keep generating the merge tree until it is valid
            # valid means every node in the merge tree has no more than 1 in_edge
            while True:
                # for each merge tree
                # create the simple merge graph where each node represents a merge router
                g = nx.MultiDiGraph()

                # complete the simple merge graph by the generated merge tree
                paths = []
                for src_node in src_nodes:
                    path = []
                    self._route_dyxy(self.w, self.h,
                                        src_node[0], src_node[1], 
                                        root_node[0], root_node[1], path, 
                                        region=region_nodes)
                    paths.extend(path)
                paths = list(set(paths))
                g.add_edges_from(paths)
            
                # verify the validity of the generated merge tree
                flag = True
                for node in g.nodes():
                    if g.out_degree(node) > 1:
                        flag = False
                        break
                if flag:
                    break
            self.merge_paths[name] = dict()
            self.merge_paths[name]['sid'] = sid
            self.merge_paths[name]['path'] = paths # add to merge_paths
            self.merge_paths[name]['load_ratio'] = self.ctg.get_attr(name, 'load_ratio')

    def _gather_plan(self) -> None:
        '''
        Planning gather routing paths
        Make sure to call this method after `self.map_xbars()`
        '''
        # gather pair  number
        gather_num = self.ctg.gather_num
        
        for sid, (name, src_node, dst_node) in enumerate(self.ctg.gather_pairs,1):
            src_node = self.map_dict[src_node]
            dst_node = self.map_dict[dst_node]
            print(f"starting gather plan {sid}/{gather_num} ....")
            # keep generating the gather path until it is valid
            # valid means it has no conflit with existing paths
            path = []
            self._route_dyxy(self.w, self.h, 
                                src_node[0], src_node[1],
                                dst_node[0], dst_node[1], path)
            self.gather_paths[name] = dict()
            self.gather_paths[name]['sid'] = sid
            self.gather_paths[name]['path'] = path
            self.gather_paths[name]['load_ratio'] = self.ctg.get_attr(name, 'load_ratio')

    # @cached_property
    # def contention_coefficient(self) -> float:
    #     '''
    #     This method evaluates the contention coefficient after mapping
    #     The contention coefficient is the average number of streams that each allocated channel supports.
    #     '''
    #     cnt = 0
    #     alloc_chan = 0
    #     for paths in self.cast_config.values():
    #         local_dict = dict()
    #         for path in paths:
    #             if path[1] not in local_dict.keys():
    #                 local_dict[path[1]] = []
    #             local_dict[path[1]].append(path[2])
    #         for v in local_dict.values():
    #             cnt += len(v)
    #             alloc_chan += 1
    #     return cnt / alloc_chan

    # def _plot_routers(self) -> None:
    #     for i in range(self.w):
    #         for j in range(self.h):
    #             plt.plot([0+i*6,0+i*6],[-0-j*6,-4-j*6],color='black',linewidth=1)
    #             plt.plot([0+i*6,3+i*6],[-4-j*6,-4-j*6],color='black',linewidth=1)
    #             plt.plot([3+i*6,4+i*6],[-4-j*6,-3-j*6],color='black',linewidth=1)
    #             plt.plot([4+i*6,4+i*6],[-3-j*6,-0-j*6],color='black',linewidth=1)
    #             plt.plot([4+i*6,0+i*6],[-0-j*6,-0-j*6],color='black',linewidth=1)

    # @staticmethod
    # def _translate(chan_num: int, mode: str) -> str:
    #     if mode == 'i':
    #         if chan_num == 0:
    #             return "cl_i"
    #         elif chan_num == 1:
    #             return "cw_i"
    #         elif chan_num == 2:
    #             return "ce_i"
    #         elif chan_num == 3:
    #             return "cv0_i"
    #         elif chan_num == 4:
    #             return "cv1_i"
        
    #     elif mode == 'o':
    #         if chan_num == 0:
    #             return "cl_o"
    #         elif chan_num == 1:
    #             return "cw_o"
    #         elif chan_num == 2:
    #             return "ce_o"
    #         elif chan_num == 3:
    #             return "cv0_o"
    #         elif chan_num == 4:
    #             return "cv1_o"

    # @staticmethod
    # def _try_add_edge(G: nx.MultiDiGraph, e: Tuple) -> None:
    #     G.add_edge(e[0],e[1])
    #     if G.in_degree(e[0]) == 0 and G.out_degree(e[1]) == 0:
    #         G.remove_edge(e[0],e[1])

    # def _build_cdg(self) -> Tuple[nx.MultiDiGraph, Dict]:
    #     legal_node = ['cw_i','cw_o','ce_i','ce_o','cv0_i','cv1_i','cv1_o','cv0_o','cl_i','cl_o']
    #     legal_xpos = [0,0,4,4,1,2,2,1,3.33+0.5,2.67+0.5]
    #     legal_ypos = [2,1,1,2,0,0,4,4,2.67+0.5,3.33+0.5]
    #     pos = dict()
    #     G=nx.MultiDiGraph()
    #     for i in range(self.w):
    #         for j in range(self.h):
    #             for k in range(len(legal_node)):
    #                 G.add_node(f"{i}_{j}_"+legal_node[k])
    #                 pos[f"{i}_{j}_"+legal_node[k]]=(legal_xpos[k]+6*i,-(legal_ypos[k]+6*j))

    #     # generate cast inner edges according to cast_config
    #     for k,v in self.cast_config.items():
    #         for p in v:
    #             G.add_edge(f"{k[0]}_{k[1]}_"+self._translate(p[0],'i'),f"{k[0]}_{k[1]}_"+self._translate(p[1],'o'))

    #     # generate cast neighbor edges
    #     for i in range(self.w-1):
    #         for j in range(self.h):
    #             self._try_add_edge(G,(f"{i}_{j}_ce_o",f"{i+1}_{j}_cw_i"))
    #             self._try_add_edge(G,(f"{i+1}_{j}_cw_o",f"{i}_{j}_ce_i"))

    #     for i in range(self.w):
    #         for j in range(self.h-1):
    #             self._try_add_edge(G,(f"{i}_{j}_cv0_o",f"{i}_{j+1}_cv0_i"))
    #             self._try_add_edge(G,(f"{i}_{j}_cv1_o",f"{i}_{j+1}_cv1_i"))
    #     return G, pos

    # def plot_map(self) -> None:
    #     plt.figure(figsize=(self.w,self.h))
    #     self._plot_routers()
    #     G,pos = self._build_cdg()
    #     nx.draw(G, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='blue',arrowstyle='-|>')
    #     plt.savefig(self.dir_name + f'/img_map',dpi=400,bbox_inches='tight')
    #     print(f"Finished saving map image")
    #     # plt.show()