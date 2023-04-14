import os
import networkx as nx
from copy import deepcopy
from matplotlib import pyplot as plt
from typing import Dict, List, Any, Optional, Tuple
from maptools.core import ROOT_DIR

__all__ = ['MapPlotter']

class MapPlotter(object):

    def __init__(
        self, 
        w: int, 
        h: int, 
        cast_paths: Dict[str, Dict[str, Any]],
        merge_paths: Dict[str, Dict[str, Any]],
        gather_paths: Dict[str, Dict[str, Any]],
        show_path: Optional[bool] = False,
        **kwargs: Any
    ) -> None:
        '''
        Plot the NoC-Mapped results

        Parameters
        ----------
        w : int
            network width
        
        h : int
            network height
        
        cast_paths : Dict[str, Dict[str, Any]]
            cast paths generated from `NocMapper`

        merge_paths : Dict[str, Dict[str, Any]]
            merge paths generated from `NocMapper`

        gather_paths : Dict[str, Dict[str, Any]]
            gather paths generated from `NocMapper`

        kwargs : Dict
            mapname : str = 'newmap'
                Map name
        '''
        self.w = w
        self.h = h
        self.cast_paths = cast_paths
        self.merge_paths = merge_paths
        self.gather_paths = gather_paths
        self.mapname = 'newmap'
        self.__dict__.update(kwargs)

        self.cast_graph = nx.MultiDiGraph()
        self.merge_graph = nx.MultiDiGraph()
        self.gather_graph = nx.MultiDiGraph()

        self.cast_links = dict()
        self.merge_links = dict()
        self.gather_links = dict()

        self.show_path = show_path
        if self.show_path:
            self.link_len = 5.5
            self.node_size = 20
            self.arrow_size = 10
            self.dpi = 500
        else:
            self.link_len = 10
            self.node_size = 0
            self.arrow_size = 5
            self.label_size = 7
            self.dpi = 680

    @staticmethod
    def _route_channel(now_node: Tuple, desire_node: Tuple, mode: str) -> str:
        if desire_node[0] < now_node[0]: # go west
            return 'w_o' if mode == 'o' else 'e_i'
        if desire_node[0] > now_node[0]: # go east
            return 'e_o' if mode == 'o' else 'w_i'
        if desire_node[1] > now_node[1]: # go south
            return 's_o' if mode == 'o' else 'n_i'
        else: # go north
            return 'n_o' if mode == 'o' else 's_i'
    
    @staticmethod
    def _get_link(edge: Tuple) -> Optional[Tuple]:
        sn = edge[0]
        dn = edge[1]
        if dn[0] > sn[0]:
            return ((sn[0], sn[1], 'e_o'), (dn[0], dn[1], 'w_i'))
        if dn[0] < sn[0]:
            return ((sn[0], sn[1], 'w_o'), (dn[0], dn[1], 'e_i'))
        if dn[1] > sn[1]:
            return ((sn[0], sn[1], 's_o'), (dn[0], dn[1], 'n_i'))
        if dn[1] < sn[1]:
            return ((sn[0], sn[1], 'n_o'), (dn[0], dn[1], 's_i'))

    def _update_cast_links(self, link: Tuple, ratio: float) -> None:
        if link not in self.cast_links:
            self.cast_links[link] = 0
            self.cast_graph.add_edge(link[0], link[1])
        self.cast_links[link] += ratio
    
    def _update_merge_links(self, link: Tuple) -> None:
        if link not in self.merge_links:
            self.merge_links[link] = 0
            self.merge_graph.add_edge(link[0], link[1])

    def _update_gather_links(self, link: Tuple, ratio: float) -> None:
        if link not in self.gather_links:
            self.gather_links[link] = 0
            self.gather_graph.add_edge(link[0], link[1])
        self.gather_links[link] += ratio

    def _cast_plan(self):
        for connect in self.cast_paths.values():
            g = nx.MultiDiGraph()
            g.add_edges_from(connect['path'])
            dst_nodes = connect['dst']
            ratio = connect['load_ratio']
            if self.show_path:
                for node in g.nodes: # add intra-router paths
                    if g.in_degree(node) == 0: # root node
                        src_chan = (node[0], node[1], 'l_i')
                        for dst_pos in g.successors(node):
                            out_chan = self._route_channel(node, dst_pos, 'o')
                            out_chan = (node[0], node[1], out_chan)
                            self.cast_graph.add_edge(src_chan, out_chan)

                    else: # not root node
                        if g.out_degree(node) > 0: # routing node
                            src_pos = list(g.predecessors(node))[0]
                            src_chan = self._route_channel(src_pos, node, 'i')
                            src_chan = (node[0], node[1], src_chan)
                            for dst_pos in g.successors(node):
                                dst_chan = self._route_channel(node, dst_pos, 'o')
                                dst_chan = (node[0], node[1], dst_chan)
                                self.cast_graph.add_edge(src_chan, dst_chan)

                        if node in dst_nodes: # target node
                            src_pos = list(g.predecessors(node))[0]
                            src_chan = self._route_channel(src_pos, node, 'i')
                            src_chan = (node[0], node[1], src_chan)
                            dst_chan = (node[0], node[1], 'l_o')
                            self.cast_graph.add_edge(src_chan, dst_chan)

            for edge in g.edges: # add inter-router paths
                link = self._get_link(edge)
                self._update_cast_links(link, 0 if self.show_path else round(ratio, 2))

    def _merge_plan(self):
        for connect in self.merge_paths.values():
            g = nx.MultiDiGraph()
            g.add_edges_from(connect['path'])
            if self.show_path:
                for node in g.nodes: # add intra-router paths
                    if g.out_degree(node) == 0: # root node
                        dst_chan = (node[0], node[1], 'l_o')
                        for src_pos in g.predecessors(node):
                            in_chan = self._route_channel(src_pos, node, 'i')
                            in_chan = (node[0], node[1], in_chan)
                            self.merge_graph.add_edge(in_chan, dst_chan)

                    else: # not root node, must be source node
                        dst_pos = list(g.successors(node))[0]
                        dst_chan = self._route_channel(node, dst_pos, 'o')
                        dst_chan = (node[0], node[1], dst_chan)
                        src_chan = (node[0], node[1], 'l_i')
                        self.merge_graph.add_edge(src_chan, dst_chan)
                        for src_pos in g.predecessors(node):
                            src_chan = self._route_channel(src_pos, node, 'i')
                            src_chan = (node[0], node[1], src_chan)
                            self.merge_graph.add_edge(src_chan, dst_chan)

            for edge in g.edges: # add inter-router paths
                link = self._get_link(edge)
                self._update_merge_links(link)

    def _gather_plan(self):
        for connect in self.gather_paths.values():
            g = nx.MultiDiGraph()
            g.add_edges_from(connect['path'])
            ratio = connect['load_ratio']
            if self.show_path:
                for node in g.nodes: # add intra-router paths
                    if g.in_degree(node) == 0: # start node
                        src_chan = (node[0], node[1], 'l_i')
                        for dst_pos in g.successors(node):
                            out_chan = self._route_channel(node, dst_pos, 'o')
                            out_chan = (node[0], node[1], out_chan)
                            self.gather_graph.add_edge(src_chan, out_chan)

                    elif g.out_degree(node) == 0: # dst node
                        src_pos = list(g.predecessors(node))[0]
                        src_chan = self._route_channel(src_pos, node, 'i')
                        src_chan = (node[0], node[1], src_chan)
                        dst_chan = (node[0], node[1], 'l_o')
                        self.gather_graph.add_edge(src_chan, dst_chan)

                    else: # routing node
                        if g.out_degree(node) > 0: # routing node
                            src_pos = list(g.predecessors(node))[0]
                            src_chan = self._route_channel(src_pos, node, 'i')
                            src_chan = (node[0], node[1], src_chan)
                            for dst_pos in g.successors(node):
                                dst_chan = self._route_channel(node, dst_pos, 'o')
                                dst_chan = (node[0], node[1], dst_chan)
                                self.gather_graph.add_edge(src_chan, dst_chan)

            for edge in g.edges: # add inter-router paths
                link = self._get_link(edge)
                self._update_gather_links(link, 0 if self.show_path else round(ratio, 2))

    def _plot_routers(self) -> None:
        if self.show_path:
            for i in range(self.w):
                for j in range(self.h):
                    plt.plot(
                        [0+i*self.link_len,0+i*self.link_len],
                        [-0-j*self.link_len,-4-j*self.link_len],
                        color='black',
                        linewidth=1
                    )
                    plt.plot(
                        [0+i*self.link_len,3+i*self.link_len],
                        [-4-j*self.link_len,-4-j*self.link_len],
                        color='black',
                        linewidth=1
                    )
                    plt.plot(
                        [3+i*self.link_len,4+i*self.link_len],
                        [-4-j*self.link_len,-3-j*self.link_len],
                        color='black',
                        linewidth=1
                    )
                    plt.plot(
                        [4+i*self.link_len,4+i*self.link_len],
                        [-3-j*self.link_len,-0-j*self.link_len],
                        color='black',
                        linewidth=1
                    )
                    plt.plot(
                        [4+i*self.link_len,0+i*self.link_len],
                        [-0-j*self.link_len,-0-j*self.link_len],
                        color='black',
                        linewidth=1
                    )
        else:
            for i in range(self.w):
                for j in range(self.h):
                    plt.plot(
                        [0+i*self.link_len,0+i*self.link_len],
                        [-0-j*self.link_len,-4-j*self.link_len],
                        color='black',
                        linewidth=1
                    )
                    plt.plot(
                        [0+i*self.link_len,4+i*self.link_len],
                        [-4-j*self.link_len,-4-j*self.link_len],
                        color='black',
                        linewidth=1
                    )
                    plt.plot(
                        [4+i*self.link_len,4+i*self.link_len],
                        [-4-j*self.link_len,-0-j*self.link_len],
                        color='black',
                        linewidth=1
                    )
                    plt.plot(
                        [4+i*self.link_len,0+i*self.link_len],
                        [-0-j*self.link_len,-0-j*self.link_len],
                        color='black',
                        linewidth=1
                    )

    def _build_graph(self) -> Tuple[nx.MultiDiGraph, Dict[Tuple, Tuple]]:
        graph = nx.MultiDiGraph()
        if self.show_path:
            legal_node = ['w_i','w_o','e_i','e_o','n_i','n_o','s_i','s_o','l_i','l_o']
            legal_xpos = [0,0,4,4,1,2,2,1,3.33+0.5,2.67+0.5]
            legal_ypos = [2,1,1,2,0,0,4,4,2.67+0.5,3.33+0.5]
        else:
            legal_node = ['w_i','w_o','e_i','e_o','n_i','n_o','s_i','s_o']
            legal_xpos = [0,0,4,4,1,3,3,1]
            legal_ypos = [3,1,1,3,0,0,4,4]
        pos = dict()
        for i in range(self.w):
            for j in range(self.h):
                for k in range(len(legal_node)):
                    graph.add_node((i, j, legal_node[k]))
                    pos[(i, j, legal_node[k])] = (
                        legal_xpos[k]+self.link_len*i,
                        -(legal_ypos[k]+self.link_len*j)
                    )
        return graph, pos

    def _get_dir(self, file_name: str) -> str:
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'nocpath')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        return os.path.join(save_dir, file_name+'.png')

    def plot_cast_map(self, file_name: str = 'cast_path'):
        plt.figure(figsize=(self.w,self.h))
        self._plot_routers()
        self.cast_graph, pos = self._build_graph()
        self._cast_plan()
        nx.draw(
            self.cast_graph, 
            pos, 
            node_size=self.node_size, 
            width=1, 
            arrowsize=self.arrow_size, 
            node_color='black',
            edge_color='red',
            arrowstyle='-|>'
        )
        if not self.show_path:
            nx.draw_networkx_edge_labels(
                self.cast_graph, 
                pos, 
                edge_labels=self.cast_links, 
                font_size=self.label_size, 
                label_pos=0.5
            )
        file_dir = self._get_dir(file_name)
        plt.savefig(
            file_dir,
            dpi=self.dpi, 
            bbox_inches='tight'
        )
        print(f"image saved to {file_dir}")

    def plot_merge_map(self, file_name: str = 'merge_path'):
        plt.figure(figsize=(self.w,self.h))
        self._plot_routers()
        self.merge_graph, pos = self._build_graph()
        self._merge_plan()
        nx.draw(
            self.merge_graph, 
            pos, 
            node_size=self.node_size, 
            width=1, 
            arrowsize=self.arrow_size, 
            node_color='black',
            edge_color='blue',
            arrowstyle='-|>'
        )
        file_dir = self._get_dir(file_name)
        plt.savefig(
            file_dir,
            dpi=self.dpi, 
            bbox_inches='tight'
        )
        print(f"image saved to {file_dir}")

    def plot_gather_map(self, file_name: str = 'gather_path'):
        plt.figure(figsize=(self.w,self.h))
        self._plot_routers()
        self.gather_graph, pos = self._build_graph()
        self._gather_plan()
        nx.draw(
            self.gather_graph, 
            pos, 
            node_size=self.node_size, 
            width=1, 
            arrowsize=self.arrow_size, 
            node_color='black',
            edge_color='purple',
            arrowstyle='-|>'
        )
        if not self.show_path:
            nx.draw_networkx_edge_labels(
                self.gather_graph, 
                pos, 
                edge_labels=self.gather_links, 
                font_size=self.label_size, 
                label_pos=0.5
            )
        file_dir = self._get_dir(file_name)
        plt.savefig(
            file_dir,
            dpi=self.dpi, 
            bbox_inches='tight'
        )
        print(f"image saved to {file_dir}")

    def plot_cast_gather_map(self, file_name: str = 'cast_gather_map'):
        plt.figure(figsize=(self.w,self.h))
        self._plot_routers()
        self.cast_graph, pos = self._build_graph()
        self._cast_plan()
        self.gather_graph, pos = self._build_graph()
        self._gather_plan()

        new_graph = deepcopy(self.cast_graph)
        new_graph.add_edges_from(self.gather_graph.edges)

        new_links = deepcopy(self.cast_links)
        for link in self.gather_links:
            if link not in new_links:
                new_links[link] = 0
            new_links[link] += self.gather_links[link]

        for k, v in new_links.items():
            new_links[k] = round(v, 2)

        nx.draw(
            new_graph, 
            pos, 
            node_size=self.node_size, 
            width=1, 
            arrowsize=self.arrow_size, 
            node_color='black',
            edge_color='blue',
            arrowstyle='-|>'
        )
        if not self.show_path:
            nx.draw_networkx_edge_labels(
                new_graph, 
                pos, 
                edge_labels=new_links, 
                font_size=self.label_size, 
                label_pos=0.5
            )
        file_dir = self._get_dir(file_name)
        plt.savefig(
            file_dir,
            dpi=self.dpi, 
            bbox_inches='tight'
        )
        print(f"image saved to {file_dir}")
