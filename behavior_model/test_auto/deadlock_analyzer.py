import os
import networkx as nx
from matplotlib import pyplot as plt
from copy import deepcopy
from typing import List, Dict, Tuple

class DeadlockAnalyzer(object):

    def __init__(self,w,h,cast_paths:dict,merge_paths:list,
                    ubm_channels:list=[],log=None,
                    dir_name="/mnt/c/git/nvcim-comm/behavior_model/test_auto"):
        self.w = w
        self.h = h
        self.cast_paths = cast_paths # generated from mapper
        self.merge_paths = merge_paths # generated form mapper
        self.ubm_channels = ubm_channels # specify the channels where ubm is adopted
        self.__build_CDG()
        self.raw_loops = [] # raw loops
        self.cloops = [] # complex loops
        self.sloops = [] # simple loops
        self.log = log
        self.dir_name = dir_name

    def __build_CDG(self):
        self.cdg = nx.MultiDiGraph()
        self.sid = dict() # store the stream id of each edge in CDG
        self.is_ctt = dict() # store whether each is a contention node, V type dependency only happens on contentions node
        self.is_ubm = dict() # store whether a node is a unicast-based multicast node, the unicast-based multicast is used to break out deadlock loops
        cast_nodes = ['cw_i','cw_o','ce_i','ce_o','cv0_i','cv0_o','cv1_i','cv1_o','cl_i','cl_o'] 

        # generate cast nodes
        for i in range(self.w):
            for j in range(self.h):
                for n in cast_nodes:
                    self.cdg.add_node(f"{i}_{j}_"+n)
                    self.is_ubm[f"{i}_{j}_"+n] = False
                    if n[-1] == "o":
                        self.is_ctt[f"{i}_{j}_"+n] = True
                    else:
                        self.is_ctt[f"{i}_{j}_"+n] = False

        # generate cast transfer edges according to cast_paths
        for k in self.cast_paths.keys():
            x = k[0]
            y = k[1]
            for path in self.cast_paths[k]:
                i_chan_name = self.translate(path[0],'i')
                o_chan_name = self.translate(path[1],'o')
                sn = f"{x}_{y}_"+i_chan_name
                dn = f"{x}_{y}_"+o_chan_name
                self.cdg.add_edge(sn,dn)
                if (sn,dn) not in self.sid.keys():
                    self.sid[(sn,dn)] = []
                self.sid[(sn,dn)].append(path[2])

        # generate cast neighbor edges
        # horizontal links
        for i in range(self.w-1):
            for j in range(self.h):
                self.cdg.add_edge(f"{i}_{j}_ce_o",f"{i+1}_{j}_cw_i")
                self.cdg.add_edge(f"{i+1}_{j}_cw_o",f"{i}_{j}_ce_i")

        # vertical links
        # for i in range(W):
        #     for j in range(H-1):
        #         CDG.add_edge(f"{i}_{j}_cv0_o",f"{i}_{j+1}_cv0_i")
        #         CDG.add_edge(f"{i}_{j}_cv1_o",f"{i}_{j+1}_cv1_i")

        # generate merge nodes
        for i in range(self.w):
            for j in range(self.h):
                self.cdg.add_node(f"{i}_{j}_mrg")
                self.is_ubm[f"{i}_{j}_mrg"] = False
                self.is_ctt[f"{i}_{j}_mrg"] = False

        # generate merge edges according to merge_paths
        for path in self.merge_paths:
            sx = path[0][0]
            sy = path[0][1]
            dx = path[1][0]
            dy = path[1][1]
            if sx != dx: # filter out all vertical links
                self.cdg.add_edge(f"{sx}_{sy}_mrg",f"{dx}_{dy}_mrg")

        # generate cast-merge joint edges
        for i in range(self.w):
            for j in range(self.h):
                if self.cdg.out_degree(f"{i}_{j}_mrg") == 0 and self.cdg.in_degree(f"{i}_{j}_mrg") == 0: # is an island merge node
                    pass
                elif self.cdg.out_degree(f"{i}_{j}_mrg") == 0: #the current node is a caster
                    self.cdg.add_edge(f"{i}_{j}_cl_o",f"{i}_{j}_cl_i")
                    self.cdg.add_edge(f"{i}_{j}_mrg",f"{i}_{j}_cl_i")
                else: # the current node is not a caster
                    self.cdg.add_edge(f"{i}_{j}_cl_o",f"{i}_{j}_mrg")

        # pick out unicast-based multicast node
        for node in self.ubm_channels:
            assert node in self.cdg.nodes(), f"the user defined unicast node {node} is invalid"
            self.is_ubm[node] = True

    @staticmethod
    def translate(chan_num:int,mode:str)->str:
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
    def popp(lst:list):
        lst.pop()
        return lst

    def __log_out(self,dep_chain:list,ocp:dict):
        self.f.write("find a complex loop:"+str(dep_chain)+"\n")
        occupied_list = []
        for k in ocp.keys():
            if ocp[k]:
                occupied_list.append(ocp[k])
        self.f.write("occupation:"+str(occupied_list)+"\n")

    def __DFS(self,start_edge,cur_edge,dep_chain:list,ocp:dict,last_dep="M"):
        if cur_edge == start_edge:
            self.raw_loops.append(deepcopy(dep_chain))
            if not self.log is None:
                self.__log_out(dep_chain,ocp)
            return
        
        elif cur_edge in self.popp(dep_chain):
            dep_chain.append(cur_edge)
            return
        dep_chain.append(cur_edge)

        # find M type dependency
        if last_dep != "M" and not self.is_ubm[cur_edge[0]]:
            if self.cdg.out_degree(cur_edge[0]) > 1:
                for e in self.cdg.out_edges(cur_edge[0]):
                    assert len(self.sid[cur_edge]) > 0, "error: current multicast edge has no stream id"
                    for id in self.sid[cur_edge]:
                        if e != cur_edge and (id in self.sid[e]): # for every other multicast edge with the same stream id
                            dep_chain.append(e)
                            self.__DFS(start_edge,e,dep_chain,ocp,last_dep="M")
                            dep_chain.pop()

        # find C type dependency
        if last_dep != "C" and self.is_ctt[cur_edge[1]]:
            if self.cdg.in_degree(cur_edge[1]) > 1:
                if ocp[cur_edge[1]] == False: # not occupied
                    for e in self.cdg.in_edges(cur_edge[1]):
                        if e != cur_edge: # for every other content edge
                            ocp[cur_edge[1]] = e # occupy
                            dep_chain.append(e)
                            self.__DFS(start_edge,e,dep_chain,ocp,last_dep="C")
                            ocp[cur_edge[1]] = False # release
                            dep_chain.pop()
                else: #occupied
                    dep_chain.append(ocp[cur_edge[1]])
                    self.__DFS(start_edge,ocp[cur_edge[1]],dep_chain,ocp,last_dep="C")
                    dep_chain.pop()

        # find S type dependency
        if self.cdg.out_degree(cur_edge[1]) > 0:
            for e in self.cdg.out_edges(cur_edge[1]):
                dep_chain.append(e)
                self.__DFS(start_edge,e,dep_chain,ocp,last_dep="S")
                dep_chain.pop()
        return

    @staticmethod
    def valid_dep(pe,ae)->bool:
        if pe[0] == ae[0]: # multicast dependency
            return True
        elif pe[1] == ae[1]: # contention dependency
            return True
        elif pe[1] == ae[0]: # serial dependency
            return True
        return False

    def __simplify_loops(self):
        '''
        simplify loops by removing additional edges in each loop and removing repetitious loops.
        '''
        for i,rloop in enumerate(self.raw_loops):
            temp_loop = []
            for j,e in enumerate(rloop[:-1]):
                if j == 0:
                    pe = rloop[-2]
                else:
                    pe = rloop[j-1]
                if j == len(rloop)-2:
                    ae = rloop[0]
                else:
                    ae = rloop[j+1]
                if self.valid_dep(pe,ae):
                    continue
                temp_loop.append(deepcopy(e))
            temp_loop.append(temp_loop[0])
            self.raw_loops[i] = tuple(temp_loop)
        self.raw_loops = list(set(self.raw_loops))

    def __classify_loops(self):
        for rloop in self.raw_loops:
            graph = nx.MultiDiGraph()
            graph.add_edges_from(rloop[:-1])
            for n in graph.nodes():
                is_simple = True
                if graph.out_degree(n) > 1: 
                        is_simple = False
                        break
            if is_simple:
                self.sloops.append(rloop) # add to simple loops
            else:
                self.cloops.append(rloop) # add to complex loops

    def Run_Analyzing(self):
        if not self.log is None:
            self.f = open(self.log,'w')

        # MCS search algorithm
        ocp = dict()
        for n in self.cdg.nodes():
            ocp[n] = False
        for n in self.cdg.nodes():
            if self.cdg.in_degree(n) > 1 and self.is_ctt[n]: # contention node
                for de in self.cdg.in_edges(n):
                    for se in self.cdg.in_edges(n):
                        ocp[n] = se
                        if de != se:
                            self.__DFS(se,de,[se,de],ocp,last_dep="C")
                        ocp[n] = False

        # self.sloops = [*nx.simple_cycles(self.cdg)]
        self.__simplify_loops()
        self.__classify_loops()

        if not self.log is None:
            for sloop in self.sloops:
                self.f.write("find a simple loop:"+str(sloop)+"\n")

        if not self.log is None:
            self.f.flush()
            self.f.close()
        
        print(f"find {len(self.cloops)} complex loop(s)")
        print(f"find {len(self.sloops)} simple loop(s)")

    def __plot_routers(self):
        for i in range(self.w):
            for j in range(self.h):
                plt.plot([0+i*5,0+i*5],[-0-j*5,-4-j*5],color='black',linewidth=1)
                plt.plot([0+i*5,3+i*5],[-4-j*5,-4-j*5],color='black',linewidth=1)
                plt.plot([3+i*5,4+i*5],[-4-j*5,-3-j*5],color='black',linewidth=1)
                plt.plot([4+i*5,4+i*5],[-3-j*5,-0-j*5],color='black',linewidth=1)
                plt.plot([4+i*5,0+i*5],[-0-j*5,-0-j*5],color='black',linewidth=1)

    def __build_pcdg(self,loop):
        legal_node = ['cw_i','cw_o','ce_i','ce_o','cv0_i','cv1_i','cv1_o','cv0_o','cl_i','cl_o','mrg']
        legal_xpos = [0,0,4,4,1,2,2,1,3.33+0.5,2.67+0.5,4.5]
        legal_ypos = [2,1,1,2,0,0,4,4,2.67+0.5,3.33+0.5,4.5]
        pos = dict()
        edge_label = dict()
        pcdg=nx.MultiDiGraph()
        for i in range(self.w):
            for j in range(self.h):
                for k in range(len(legal_node)):
                    pcdg.add_node(f"{i}_{j}_"+legal_node[k])
                    pos[f"{i}_{j}_"+legal_node[k]]=(legal_xpos[k]+5*i,-(legal_ypos[k]+5*j))

        pcdg.add_edges_from(loop)
        for i in range(len(loop)-1):
            edge_label[loop[i]] = i
        return pcdg,pos,edge_label

    def Plot_Loops(self):
        '''
        Plot all the complex and simple loops and save the figures to self.dir_name/c(s)loop_img/
        Always call this method after calling self.Run_Analyzing()
        '''
        os.chdir(self.dir_name)
        os.system("rm -rf cloop_img")
        os.system("rm -rf sloop_img")
        os.system("mkdir cloop_img")
        os.system("mkdir sloop_img")

        # save complex loop figures
        cnt = 0
        for cl in self.cloops:
            cnt += 1
            plt.figure(figsize=(self.w,self.h))
            self.__plot_routers()
            pcdg,pos,el = self.__build_pcdg(cl)
            nx.draw(pcdg, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='red',arrowstyle='-|>')
            nx.draw_networkx_edge_labels(pcdg,pos,edge_labels=el,font_size=7,font_color='blue',bbox=dict(alpha=0))
            plt.savefig(self.dir_name + f'/cloop_img/img_'+str(cnt),
                dpi=400,bbox_inches='tight')
            print(f"Finished saving {cnt} complex loop image")

        # save simple loop figures
        cnt = 0
        for sl in self.sloops:
            cnt += 1
            plt.figure(figsize=(self.w,self.h))
            self.__plot_routers()
            pcdg,pos,el = self.__build_pcdg(sl)
            nx.draw(pcdg, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='red',arrowstyle='-|>')
            nx.draw_networkx_edge_labels(pcdg,pos,edge_labels=el,font_size=7,font_color='blue',bbox=dict(alpha=0))
            plt.savefig(self.dir_name + f'/sloop_img/img_'+str(cnt),
                dpi=400,bbox_inches='tight')
            print(f"Finished saving {cnt} simple loop image")

if __name__ == "__main__":
    from noc_mapper import NocMapper
    maper = NocMapper(5,11,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
    maper.Run_Mapping()
    dla = DeadlockAnalyzer(5,11,maper.cast_paths,maper.merge_paths,log=None)
    dla.Run_Analyzing()
    dla.Plot_Loops()
