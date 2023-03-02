import os
import networkx as nx
from matplotlib import pyplot as plt
from copy import deepcopy

class DeadlockKiller(object):

    def __init__(self,w,h,merge_nodes,cast_targets,cast_paths,
                    sloops,cloops,dir_name="/mnt/c/git/nvcim-comm/behavior_model/test_auto"):
        self.w = w
        self.h = h
        self.merge_nodes = merge_nodes
        self.cast_targets = cast_targets
        self.cast_paths = cast_paths
        self.sloops = sloops
        self.cloops = cloops
        self.dir_name = dir_name

    def Run_Contention_Analysis(self):
        '''
        This method evaluates the contention level after mapping,
        and finds all the destination nodes that is to be E2E-FCed.
        This method can be used to generate E2E-FC info.
        After this analysis, all simple loops are eliminated.
        '''
        self.e2e_dict = dict()
        merge_nodes_plain = []
        cast_targets_plain = []
        for tar in self.cast_targets:
            cast_targets_plain += tar
        for mer in self.merge_nodes:
            merge_nodes_plain += mer
        cnt = 0
        for paths in self.cast_paths.values():
            local_dict = dict()
            for path in paths:
                if path[1] not in local_dict.keys():
                    local_dict[path[1]] = []
                local_dict[path[1]].append(path[2])
            for v in local_dict.values():
                if len(v) > 1: # there is a channel who has multiple input edges
                    for sid in v:
                        self.e2e_dict[merge_nodes_plain[sid-1]] = cast_targets_plain[sid-1]
                    cnt += 1
        self.contention_level = cnt

    def __filter_loops(self):
        '''
        Filter out all the loops that cannot be broken by E2E-FC.
        Always call this method after self.Run_Contention_Analysis().
        '''
        self.e2e_nodes = []
        self.remain_loops = []
        for v in self.e2e_dict.values():
            self.e2e_nodes += v
        for loop in self.cloops:
            for node in self.e2e_nodes:
                exist_chan = False
                x = node % self.w
                y = node // self.w
                dst_chan = f"{x}_{y}_cl_o"
                for i,edge in enumerate(loop[:-1]):
                    if edge[1] == dst_chan and loop[i+1][0] == dst_chan: # the loop can be broken by E2E-FC
                        exist_chan = True
                        break
                if exist_chan:
                    break
            if not exist_chan:
                self.remain_loops.append(deepcopy(loop))

    def __collect_candidate_ubm_nodes(self):
        '''
        Collect candidate UBM nodes (channels) from self.remain_loops.
        The candidate UBM node should be a multicast source node.
        Always call this method after self.__filter_loops().
        '''
        self.candidate_nodes = []
        if len(self.remain_loops) == 0:
            return
        for loop in self.remain_loops:
            local_list = []
            graph = nx.MultiDiGraph()
            graph.add_edges_from(loop[:-1])
            for node in graph.nodes():
                if graph.out_degree(node) > 1: # is a multicast node
                    local_list.append(node)
            self.candidate_nodes.append(local_list)

    @staticmethod
    def greedy_SCP(U:set,S:list,accum_U:set,ret:list):
        '''
        Greedy algorithm to solve set cover problem

        Parameters
        ----------
        U : set(ele1,ele2, .... ,elen)
            A set that contains all elements

        S : list[tupe(id1,set(eles)),tupe(id2,set(eles)),tupe(id3,set(eles)),...]
            A list that contains all match pairs,
            a match pair is a tuple, whose first elements is the id of a set,
            and second elements is the set itself.
        '''
        assert len(S) > 0, "fatal error when greedy_SCP"
        if accum_U == U:
            return 

        remain_U = U - accum_U
        cnt_list = []
        for mp in S:
            cnt = 0
            for ele in mp[1]:
                if ele in remain_U:
                    cnt += 1
            cnt_list.append(cnt)
        idx = cnt_list.index(max(cnt_list))
        ret.append(S[idx][0])
        accum_U |= (S.pop(idx))[1]
        DeadlockKiller.greedy_SCP(U,S,accum_U,ret)

    def __get_ubm_nodes(self):
        '''
        Get the UBM channels through greedy SCP
        Remove an arbitary dependency in each reamin_loop
        The UBM selection problem can be tranferred to cover problem:

        node       loop_set
        ------------------------------------------
        node1 ---> {loop1, loop2, loop3, ....}
        node2 ---> {loop3, loop4, ....}
        node3 ---> {loop5, loop6, loop2, ....}
        node4 ---> {loop1, loop7, ....}
        ....

        Then:
        node_list = [node1, node2, node3, node4, ....]
        loop_union = {loop1, loop2, loop3, loop4, loop5, loop6, loop7, ....}
        match_list = [(node1,loop_set1), (node2,loop_set2), (node3,loop_set3), (node4,loop_set4), ....]
        '''
        # get node list
        if len(self.candidate_nodes) == 0:
            return
        node_list = []
        self.ubm_nodes = []
        for loop in self.candidate_nodes:
            for node in loop:
                node_list.append(node)
        node_list = list(set(node_list))

        # get match list
        match_list = []
        for node in node_list:
            loop_set = []
            for i,loop in enumerate(self.candidate_nodes):
                if node in loop:
                    loop_set.append(i) # only record the id of the loop
            match_list.append((node,set(loop_set)))
        
        # get loop union
        loop_union = set(range(len(self.candidate_nodes)))

        print("node_list:",node_list)
        print("match_list:",match_list)
        ret = []
        DeadlockKiller.greedy_SCP(loop_union,match_list,set(),ret)
        print("ubm_nodes:",ret)
        self.ubm_nodes = ret

    def Run_UBM_Analysis(self):
        self.__filter_loops()
        if len(self.remain_loops) == 0: # if there is no remain loops, omit this step
            self.ubm_nodes = []
            return
        self.__collect_candidate_ubm_nodes()
        self.__get_ubm_nodes()

    def Run_Killing(self):
        self.Run_Contention_Analysis()
        self.Run_UBM_Analysis()

    # methods below are all for test
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

    def Plot_Remain_Loops(self):
        os.chdir(self.dir_name)
        os.system("rm -rf remain_loop_img")
        os.system("mkdir remain_loop_img")

        cnt = 0
        for cl in self.remain_loops:
            cnt += 1
            plt.figure(figsize=(self.w,self.h))
            self.__plot_routers()
            pcdg,pos,el = self.__build_pcdg(cl)
            nx.draw(pcdg, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='red',arrowstyle='-|>')
            nx.draw_networkx_edge_labels(pcdg,pos,edge_labels=el,font_size=7,font_color='blue',bbox=dict(alpha=0))
            plt.savefig(self.dir_name + f'/remain_loop_img/img_'+str(cnt),
                dpi=400,bbox_inches='tight')
            print(f"Finished saving {cnt} remain loop image")

if __name__ == "__main__":
    from noc_mapper import NocMapper
    from deadlock_analyzer import DeadlockAnalyzer
    while True:
        maper = NocMapper(5,11,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
        maper.Run_Mapping()
        dla = DeadlockAnalyzer(5,11,maper.cast_paths,maper.merge_paths,log=None)
        dla.Run_Analyzing()
        dlk = DeadlockKiller(5,11,maper.merge_nodes,maper.cast_targets,maper.cast_paths,dla.sloops,dla.cloops)
        dlk.Run_Killing()
        print("remain_loops:",len(dlk.remain_loops))
        if len(dlk.remain_loops) > 0:
            print("Exception!!!remain_loops")
            break
