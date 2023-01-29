'''
Randomly map the AI model onto the PE array and generate cast and merge routing graphs
The procedure of mapping contains 6 steps:
------------------------------------------
1. Reverse-S Projection
2. Adjacent Regions Placement
3. Merge Nodes Selection
4. Cast Targets Placement
5. Cast Routing Plan
6. Merge Routing Plan
------------------------------------------
TODO only for series structure, need to provide support for ResNet structure
TODO need to provide support for random region division
'''
import random
import networkx as nx

# PE array width
PE_Array_Width = 7

# PE array height
PE_Array_Height = 8

# occupied PEs by input channels of each layer of the AI model
Model_PEs_I = [1,1,1,1,1,2,2,2,4,4,4,4,4] # VGG 16

# occupied PEs by output channels of each layer of the AI model
Model_PEs_O = [1,1,1,1,1,1,1,2,2,2,2,2,2] # VGG 16

def Generate_ReverseS(w,h)->list:
    rs_path = []
    for i in range(h):
        for j in range(w):
            if i % 2:
                rs_path.append((i+1)*w-j-1)
            else:
                rs_path.append(i*w+j)
    return rs_path

def ReverseS_Projection(w,h,pes_i:list,pes_o:list)->list:
    model_pes = []
    assert len(pes_i) == len(pes_o), "Model_PEs_I length not match Model_PEs_O"
    assert len(pes_i) <= w*h, "Need larger PE array"
    for i in range(len(pes_i)):
        model_pes.append(pes_i[i] * pes_o[i])
    rs_path = Generate_ReverseS(w,h)
    projected_model = []
    model_idx = 0
    for pes in model_pes:
        temp = []
        for cnt in range(pes):
            temp.append(rs_path.index(model_idx))
            model_idx += 1
        projected_model.append(temp)
    return projected_model

def Adjacent_Regions_Placement(w,h,projected_model:list,pes_i:list,pes_o:list)->list:
    '''
    Cut the regions following ascending order of the model-indices of the PEs only
    '''
    model_regions = []
    for layer in range(len(projected_model)):
        pes = projected_model[layer]
        temp = []
        for i in range(pes_o[layer]):
            temp.append(pes[i*pes_i[layer]:(i+1)*pes_i[layer]])
        model_regions.append(temp)
    return model_regions

def Merge_Node_Selection(model_regions)->list:
    '''
    Select the last node of each region as the merge node
    '''
    merge_nodes = []
    for regions in model_regions:
        temp = []
        for pes in regions:
            temp.append(pes[-1])
        merge_nodes.append(temp)
    return merge_nodes

def Cast_Targets_Placement(model_regions:list)->list:
    '''
    Randomly select cast targets for the merge node in the previous layer
    '''
    cast_targets = [] # 
    for layer in range(len(model_regions)-1):
        indices = []
        for region in model_regions[layer+1]:
            temp = [h for h in range(len(region))]
            random.shuffle(temp)
            indices.append(temp)
            
        temp1 = []
        i = 0
        src_node_num = len(model_regions[layer])
        for region1 in model_regions[layer]:
            temp2 = []
            j = 0
            for region2 in model_regions[layer+1]:
                assert len(region2) % src_node_num == 0, "regions illegally divided"
                unit = len(region2) // src_node_num
                for k in range(unit):
                    idx = indices[j][i * unit + k]
                    temp2.append(region2[idx])
                j += 1
            i += 1
            temp1.append(temp2)
        cast_targets.append(temp1)
    return cast_targets

def Route_DyXY(w,h,sx,sy,dx,dy,path:list,region=None)->list:
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
    Route_DyXY(w,h,nxt_sx,nxt_sy,dx,dy,path,region=region)

def Get_Channel_From_Edge(bias_pos:tuple,now_pos:tuple,root_pos:tuple):
    if bias_pos[0] < now_pos[0]: # west
        return 1
    if bias_pos[0] > now_pos[0]: # east
        return 2
    if now_pos[0] < root_pos[0]: # vert0
        return 3
    return 4 # vert1

def Cast_Routing_Plan(w,h,merge_nodes,cast_targets):
    path_dict = dict() # create the cast dict
    for x in range(w):
        for y in range(h):
            path_dict[(x,y)] = []
    sid = 0
    for layer in range(len(merge_nodes)-1):
        src_nodes = merge_nodes[layer]
        for i in range(len(src_nodes)):
            sid += 1
            src_node = src_nodes[i]
            src_node_pos = (src_node % w, src_node // w)
            dst_nodes = cast_targets[layer][i]

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
                    Route_DyXY(w,h,src_node % w, src_node // w, dst_node % w, dst_node // w, path)
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
                if g.in_degree(node) > 0 and g.out_degree(node) > 0: # inter node
                    src_pos = (list(g.in_edges(node)))[0][0]
                    src_chan = Get_Channel_From_Edge(src_pos,node,src_node_pos)
                    for de in g.out_edges(node):
                        dst_pos = de[1]
                        dst_chan = Get_Channel_From_Edge(dst_pos,node,src_node_pos)
                        path_dict[node].append((src_chan,dst_chan,sid))
    return path_dict

def Merge_Routing_Plan(w,h,merge_nodes:list,model_regions:list):
    merge_paths = []
    for layer in range(len(merge_nodes)):
        root_nodes = merge_nodes[layer]
        for i in range(len(root_nodes)):
            root_node = root_nodes[i]
            region_nodes = model_regions[layer][i]

            while True:
                # for each merge tree
                # create the simple merge graph where each node represents a merge router
                g = nx.MultiDiGraph()

                # complete the simple merge graph by the generated multicast tree
                paths = []
                for src_node in region_nodes:
                    if src_node != root_node: # for non-root nodes
                        path = []
                        Route_DyXY(w,h,src_node % w, src_node // w, root_node % w, root_node // w, path, region=region_nodes)
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

            merge_paths.extend(paths)
    return merge_paths



if __name__ == "__main__":
    projected_model = ReverseS_Projection(PE_Array_Width,PE_Array_Height,Model_PEs_I,Model_PEs_O)
    model_regions = Adjacent_Regions_Placement(PE_Array_Width,PE_Array_Height,projected_model,Model_PEs_I,Model_PEs_O)
    merge_nodes = Merge_Node_Selection(model_regions)
    cast_targets =  Cast_Targets_Placement(model_regions)
    cast_paths = Cast_Routing_Plan(PE_Array_Width,PE_Array_Height,merge_nodes,cast_targets)
    print("\ncast_paths:")
    for k,v in cast_paths.items():
        print(k,v)
    merge_paths = Merge_Routing_Plan(PE_Array_Width,PE_Array_Height,merge_nodes,model_regions)
    print("\nmerge_paths:")
    for i in merge_paths:
        print(i)
    # # generate cast communication pairs
    # for i in range(len(merge_nodes)-1):
    #     nodes = merge_nodes[i]
    #     for j in range(len(nodes)):
    #         node = nodes[j]
    #         targets = cast_targets[i][j]
    #         print(f"{node}->{targets}")
