'''
Randomly map the AI model onto the PE array or NoC, then generate cast and merge routing graphs
The procedure of mapping contains 6 steps:
------------------------------------------
1. Reverse-S Projection
2. Adjacent Regions Placement
3. Merge Nodes Selection
4. Cast Targets Placement
5. Communication Plan
6. Cast Routing Plan
7. Merge Routing Plan
------------------------------------------
TODO only for series structure, need to provide support for ResNet structure
TODO need to provide support for random region division
TODO the num_chan_i of the first layer cannot exceed the width of Xbar
#// TODO need to privide support for random merge node selection
'''
import random
import networkx as nx
from matplotlib import pyplot as plt
from typing import List, Dict, Tuple

class NocMapper(object):

    def __init__(self,model:List[List[List[List[Dict]]]],w,h,
                    dir_name="/mnt/c/git/nvcim-comm/network/mapping"):
        '''
            Parameters
            ----------
            model : list[list[list[list[dict]]]]
                model -> layer -> region -> block -> tile
                TileMapper.tile_config
                TODO spec

            w : int
                PE (Tile) array width

            h : int
                PE (Tile) array height

            dir_name : str
                root path to save the map figure
        '''
        self.model = model
        self.__get_pes()
        self.w = w
        self.h = h
        self.dir_name = dir_name

        # intermediate representations
        self.projected_model = []
        self.model_regions = []
        self.merge_nodes = []
        self.cast_targets = []

        # network mapping config info
        self.tile_map = dict()

        # ifinity bandwidth communication config info
        self.cast_comms = list()
        self.merge_comms = list()

        # network routing config info
        self.cast_paths = dict()
        self.merge_paths = []

    def __get_pes(self):
        '''
        get pes_i and pes_o from model
        '''
        self.pes_i = []
        self.pes_o = []
        for layer in self.model:
            self.pes_o.append(len(layer)) # number of regions in each layer
            cnt = 0
            for block in layer[0]: # for each clock in region0
                cnt += len(block)
            self.pes_i.append(cnt) # number of pes in all blocks in each region

    @staticmethod
    def genReverseS(w,h)->List:
        '''
        generate reverse-s path
        '''
        rs_path = []
        for i in range(h):
            for j in range(w):
                if i % 2:
                    rs_path.append((i+1)*w-j-1)
                else:
                    rs_path.append(i*w+j)
        return rs_path

    def ReverseS_Projection(self):
        self.pes = []
        # validity check
        assert len(self.pes_i) == len(self.pes_o), "Model_PEs_I length not match Model_PEs_O"
        assert len(self.pes_i) <= self.w*self.h, "Need larger PE array"
        for i in range(len(self.pes_i)):
            self.pes.append(self.pes_i[i] * self.pes_o[i])
        rs_path = self.genReverseS(self.w,self.h)
        self.projected_model = []
        model_idx = 0
        for pes in self.pes:
            temp = []
            for cnt in range(pes):
                temp.append(rs_path.index(model_idx))
                model_idx += 1
            self.projected_model.append(temp)

    def Adjacent_Regions_Placement(self):
        '''
        Divide the regions following ascending order of the model-indices of the PEs only
        '''
        # dependency check
        assert len(self.projected_model) > 0, "error when adjacent regions placing: projected model not provided"
        self.model_regions = []
        for layer in range(len(self.projected_model)):
            pes = self.projected_model[layer]
            temp = []
            for i in range(self.pes_o[layer]):
                temp.append(pes[i*self.pes_i[layer]:(i+1)*self.pes_i[layer]])
            self.model_regions.append(temp)

    def Merge_Node_Selection(self):
        '''
        #// Select the last node of each region as the merge node
        Select an arbitrate node in each region as the merge node, 
        note that the y-axis coordinate of selected merge node must be the largest among all nodes in the current region
        '''
        # dependency check
        assert len(self.model_regions) > 0, "error when merge node selecting: model regions not provided"
        self.merge_nodes = []
        # for regions in self.model_regions:
        #     temp = []
        #     for pes in regions:
        #         temp.append(pes[-1])
        #     self.merge_nodes.append(temp)
        for regions in self.model_regions:
            temp = []
            for region in regions:
                max_y_pos = 0
                valid_region = []
                for pe in region:
                    y_pos = pe // self.w
                    if y_pos > max_y_pos:
                        max_y_pos = y_pos
                        valid_region.clear()
                    if y_pos == max_y_pos:
                        valid_region.append(pe)
                idx = random.randint(0,len(valid_region)-1)
                temp.append(valid_region[idx])
            self.merge_nodes.append(temp)

    def __first_layer_tile_map(self):
        '''
        the first layer will be neglected when cast targets placement, so it should be mapped separately
        '''
        for j,region in enumerate(self.model[0]):
            pes_pos = self.model_regions[0][j]
            assert len(region) == 1, "the regions in first layer must have only one block, too many input channels in the first layer"
            for h in range(len(region[0])):
                pe_pos = pes_pos[h]
                self.tile_map[(pe_pos % self.w, pe_pos // self.w)] = region[0][h]

    def Cast_Targets_Placement(self):
        '''
        Randomly select cast targets for the merge node in the previous layer
        Generate tile map 
        '''
        # dependency check
        self.__first_layer_tile_map()
        assert len(self.model_regions) > 0, "error when cast targets placing: model regions not provided"
        self.cast_targets = [] 
        for layer in range(len(self.model_regions)-1):
            indices = []
            for region in self.model_regions[layer+1]:
                temp = [h for h in range(len(region))]
                random.shuffle(temp)
                indices.append(temp) # random indices of PEs in each region of each layer
            
            temp1 = []
            for i,region1 in enumerate(self.model[layer]):
                temp2 = []
                for j,region2 in enumerate(self.model[layer+1]):
                    assert len(self.model[layer]) == len(region2), "number of blocks in this layer not equal number of regions in former layer"
                    pes_pos = self.model_regions[layer+1][j] # pe positions in region2
                    block = region2[i] # choose which block
                    base_idx = 0
                    for k in range(i):
                        base_idx += len(region2[k])
                    for h in range(len(block)):
                        idx = indices[j][base_idx + h]
                        pe_pos = pes_pos[idx]
                        temp2.append(pe_pos)
                        self.tile_map[(pe_pos % self.w, pe_pos // self.w)] = block[h] # map the tile config to tile pos
                temp1.append(temp2)
            self.cast_targets.append(temp1)

    def __cast_communication_plan(self):
        # process the cast targets in the first layer
        targets = [] # the cast targets in the first layer
        for region in self.model_regions[0]: # first layer regions
            for pe_pos in region:
                targets.append((pe_pos % self.w, pe_pos // self.w))
        self.cast_comms.append({'src':'chip_in','dst':targets})

        # process the cast targets in the other layers
        for i in range(len(self.merge_nodes)-1):
            roots = self.merge_nodes[i]
            targetss = self.cast_targets[i]
            assert len(roots) == len(targetss), "number of cast srcs not equal number of cast dst zones"
            for j in range(len(roots)):
                root = (roots[j] % self.w, roots[j] // self.w)
                targets = []
                for t in targetss[j]:
                    targets.append((t % self.w, t // self.w))
                self.cast_comms.append({'src':root,'dst':targets})

    def __merge_communication_plan(self):
        for i in range(len(self.merge_nodes)):
            zones = self.model_regions[i]
            roots = self.merge_nodes[i]
            assert len(zones) == len(roots), "number of merge src zones not equal number of merge dst"
            for j in range(len(roots)):
                root = (roots[j] % self.w, roots[j] // self.w)
                sources = []
                for z in zones[j]:
                    if z != root:
                        sources.append((z % self.w, z // self.w))
                self.merge_comms.append({'src':sources,'dst':root})

    def Communication_Plan(self):
        '''
        Generate the communication trees (pairs)
        This info can be used when running infinity bandwidth simulation
        '''
        self.__cast_communication_plan()
        self.__merge_communication_plan()


    @staticmethod
    def routeDyXY(w,h,sx,sy,dx,dy,path:List,region=None)->List:
        if sx == dx and sy == dy:
            return
        if sx != dx and sy != dy:
            randbit = True if random.random() > 0.5 else False
            if randbit:
                nxt_sx = sx
                nxt_sy = sy + (1 if sy < dy else -1)
            else:
                nxt_sy = sy
                nxt_sx = sx + (1 if sx < dx else -1)
        else:
            if sx == dx:
                nxt_sx = sx
                nxt_sy = sy + (1 if sy < dy else -1)
            elif sy == dy:
                nxt_sy = sy
                nxt_sx = sx + (1 if sx < dx else -1)

        # if constrained routing region considered
        if region:
            if (nxt_sx + nxt_sy * w) not in region:
                if sy == nxt_sy:
                    nxt_sx = sx
                    nxt_sy = sy + (1 if sy < dy else -1)
                elif sx == nxt_sx:
                    nxt_sy = sy
                    nxt_sx = sx + (1 if sx < dx else -1)
            assert (nxt_sx + nxt_sy * w) in region, "critical error ecountered at merge path"
        path.append(((sx,sy),(nxt_sx,nxt_sy)))
        NocMapper.routeDyXY(w,h,nxt_sx,nxt_sy,dx,dy,path,region=region)

    @staticmethod
    def getChannel(bias_pos: Tuple, now_pos: Tuple, root_pos: Tuple):
        if bias_pos[0] < now_pos[0]: # west
            return 1
        if bias_pos[0] > now_pos[0]: # east
            return 2
        if now_pos[0] < root_pos[0]: # vert0
            return 3
        return 4 # vert1

    def Cast_Routing_Plan(self):
        # dependency check
        assert len(self.model_regions) > 0, "error when cast routing planning: model regions not provided"
        assert len(self.cast_targets) > 0, "error when cast routing planning: cast targets not provided"
        self.cast_paths = dict() # create the cast dict
        for x in range(self.w):
            for y in range(self.h):
                self.cast_paths[(x,y)] = []
        sid = 0
        for layer in range(len(self.merge_nodes)-1):
            root_nodes = self.merge_nodes[layer]
            for i in range(len(root_nodes)):
                sid += 1
                root_node = root_nodes[i]
                root_node_pos = (root_node % self.w, root_node // self.w)
                dst_nodes = self.cast_targets[layer][i]

                # keep generating the multicast tree until it is valid
                # valid means every node in the multicast tree has no more than 1 in_edge
                while True:
                    # for each multicast tree
                    # create the simple cast graph where each node represents a cast router
                    g = nx.MultiDiGraph()

                    # complete the simple cast graph by the generated multicast tree
                    paths = []
                    for dst_node in dst_nodes:
                        path = []
                        self.routeDyXY(self.w,self.h,
                                            root_node % self.w, root_node // self.w, 
                                            dst_node % self.w, dst_node // self.w, path)
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

                # complete the complex cast graph according to each multicast tree in the simple cast graph
                for node in g.nodes():
                    if node == root_node_pos: # root node
                        assert g.in_degree[node] == 0, "root node in multicast has input path"
                        for de in g.out_edges(node):
                            dst_pos = de[1]
                            dst_chan = self.getChannel(dst_pos,node,root_node_pos)
                            self.cast_paths[node].append((0,dst_chan,sid)) # local
                    
                    else: # not root node
                        if g.out_degree(node) > 0: # routing node
                            src_pos = (list(g.in_edges(node)))[0][0]
                            src_chan = self.getChannel(src_pos,node,root_node_pos)
                            for de in g.out_edges(node):
                                dst_pos = de[1]
                                dst_chan = self.getChannel(dst_pos,node,root_node_pos)
                                self.cast_paths[node].append((src_chan,dst_chan,sid))

                        if (node[0] + node[1] * self.w) in dst_nodes: # target node
                            assert g.in_degree(node) == 1, "target node in multicast tree has multiple input paths"
                            src_pos = (list(g.in_edges(node)))[0][0]
                            src_chan = self.getChannel(src_pos,node,root_node_pos)
                            self.cast_paths[node].append((src_chan,0,sid)) # local


    def Merge_Routing_Plan(self):
        # dependency check
        assert len(self.model_regions) > 0, "error when merge routing planning: model regions not provided"
        assert len(self.cast_targets) > 0, "error when merge routing planning: cast targets not provided"
        self.merge_paths = []
        for layer in range(len(self.merge_nodes)):
            root_nodes = self.merge_nodes[layer]
            for i in range(len(root_nodes)):
                root_node = root_nodes[i]
                region_nodes = self.model_regions[layer][i]

                while True:
                    # for each merge tree
                    # create the simple merge graph where each node represents a merge router
                    g = nx.MultiDiGraph()

                    # complete the simple merge graph by the generated multicast tree
                    paths = []
                    for src_node in region_nodes:
                        if src_node != root_node: # for non-root nodes
                            path = []
                            self.routeDyXY(self.w,self.h,
                                                src_node % self.w, src_node // self.w, 
                                                root_node % self.w, root_node // self.w, path, 
                                                region=region_nodes)
                            paths.extend(path)
                    paths = list(set(paths))
                    g.add_edges_from(paths)
                
                    # verify the validity of the generated multicast tree
                    flag = True
                    for node in g.nodes():
                        if g.out_degree(node) > 1:
                            flag = False
                            break
                    if flag:
                        break
                self.merge_paths.extend(paths)
    
    def Run_Mapping(self):
        self.ReverseS_Projection()
        self.Adjacent_Regions_Placement()
        self.Merge_Node_Selection()
        self.Cast_Targets_Placement()
        self.Communication_Plan()
        self.Cast_Routing_Plan()
        self.Merge_Routing_Plan()

    def Get_Contention_Level(self)->int:
        '''
        This method evaluates the contention level after mapping,
        '''
        cnt = 0
        for paths in self.cast_paths.values():
            local_dict = dict()
            for path in paths:
                if path[1] not in local_dict.keys():
                    local_dict[path[1]] = []
                local_dict[path[1]].append(path[2])
            for v in local_dict.values():
                if len(v) > 1: # there is a channel who has multiple input edges
                    cnt += 1
        return cnt

    def __plot_routers(self):
        for i in range(self.w):
            for j in range(self.h):
                plt.plot([0+i*5,0+i*5],[-0-j*5,-4-j*5],color='black',linewidth=1)
                plt.plot([0+i*5,3+i*5],[-4-j*5,-4-j*5],color='black',linewidth=1)
                plt.plot([3+i*5,4+i*5],[-4-j*5,-3-j*5],color='black',linewidth=1)
                plt.plot([4+i*5,4+i*5],[-3-j*5,-0-j*5],color='black',linewidth=1)
                plt.plot([4+i*5,0+i*5],[-0-j*5,-0-j*5],color='black',linewidth=1)

    @staticmethod
    def translate(chan_num:int,mode:str):
        if mode == 'i':
            if chan_num == 0:
                return "cl_i"
            elif chan_num == 1:
                return "cw_i"
            elif chan_num == 2:
                return "ce_i"
            elif chan_num == 3:
                return "cv0_i"
            elif chan_num == 4:
                return "cv1_i"
        
        elif mode == 'o':
            if chan_num == 0:
                return "cl_o"
            elif chan_num == 1:
                return "cw_o"
            elif chan_num == 2:
                return "ce_o"
            elif chan_num == 3:
                return "cv0_o"
            elif chan_num == 4:
                return "cv1_o"

    @staticmethod
    def try_add_edge(G:nx.MultiDiGraph,e:Tuple):
        G.add_edge(e[0],e[1])
        if G.in_degree(e[0]) == 0 and G.out_degree(e[1]) == 0:
            G.remove_edge(e[0],e[1])

    def __build_cdg(self):
        legal_node = ['cw_i','cw_o','ce_i','ce_o','cv0_i','cv1_i','cv1_o','cv0_o','cl_i','cl_o','mrg']
        legal_xpos = [0,0,4,4,1,2,2,1,3.33+0.5,2.67+0.5,4.5]
        legal_ypos = [2,1,1,2,0,0,4,4,2.67+0.5,3.33+0.5,4.5]
        pos = dict()
        G=nx.MultiDiGraph()
        for i in range(self.w):
            for j in range(self.h):
                for k in range(len(legal_node)):
                    G.add_node(f"{i}_{j}_"+legal_node[k])
                    pos[f"{i}_{j}_"+legal_node[k]]=(legal_xpos[k]+5*i,-(legal_ypos[k]+5*j))

        # generate cast inner edges according to cast_paths
        for k,v in self.cast_paths.items():
            for p in v:
                G.add_edge(f"{k[0]}_{k[1]}_"+NocMapper.translate(p[0],'i'),f"{k[0]}_{k[1]}_"+NocMapper.translate(p[1],'o'))
        
        # generate merge edges according to merge_paths
        for p in self.merge_paths:
            G.add_edge(f"{p[0][0]}_{p[0][1]}_"+'mrg',f"{p[1][0]}_{p[1][1]}_"+'mrg')
        
        # generate cast-merge joint edges
        for i in range(self.w):
            for j in range(self.h):
                if G.out_degree(f"{i}_{j}_mrg") == 0: 
                    if G.in_degree(f"{i}_{j}_cl_o") > 0: # the current node is a caster
                        G.add_edge(f"{i}_{j}_cl_o",f"{i}_{j}_cl_i")
                        G.add_edge(f"{i}_{j}_mrg",f"{i}_{j}_cl_i")
                else: # the current node is not a caster
                    G.add_edge(f"{i}_{j}_cl_o",f"{i}_{j}_mrg")

        # generate cast neighbor edges
        for i in range(self.w-1):
            for j in range(self.h):
                NocMapper.try_add_edge(G,(f"{i}_{j}_ce_o",f"{i+1}_{j}_cw_i"))
                NocMapper.try_add_edge(G,(f"{i+1}_{j}_cw_o",f"{i}_{j}_ce_i"))

        for i in range(self.w):
            for j in range(self.h-1):
                NocMapper.try_add_edge(G,(f"{i}_{j}_cv0_o",f"{i}_{j+1}_cv0_i"))
                NocMapper.try_add_edge(G,(f"{i}_{j}_cv1_o",f"{i}_{j+1}_cv1_i"))
        return G,pos

    def Plot_Map(self):
        plt.figure(figsize=(self.w,self.h))
        self.__plot_routers()
        G,pos = self.__build_cdg()
        nx.draw(G, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='blue',arrowstyle='-|>')
        plt.savefig(self.dir_name + f'/img_map',dpi=400,bbox_inches='tight')
        print(f"Finished saving map image")
