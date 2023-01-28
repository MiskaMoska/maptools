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
'''
import random

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
                assert len(region2) % src_node_num == 0, "regions illegal divided"
                unit = len(region2) // src_node_num
                for k in range(unit):
                    idx = indices[j][i * unit + k]
                    temp2.append(region2[idx])
                j += 1
            i += 1
            temp1.append(temp2)
        cast_targets.append(temp1)
    return cast_targets



if __name__ == "__main__":
    projected_model = ReverseS_Projection(PE_Array_Width,PE_Array_Height,Model_PEs_I,Model_PEs_O)
    model_regions = Adjacent_Regions_Placement(PE_Array_Width,PE_Array_Height,projected_model,Model_PEs_I,Model_PEs_O)
    merge_nodes = Merge_Node_Selection(model_regions)
    cast_targets =  Cast_Targets_Placement(model_regions)

    # generate cast communication pairs
    for i in range(len(merge_nodes)-1):
        nodes = merge_nodes[i]
        for j in range(len(nodes)):
            node = nodes[j]
            targets = cast_targets[i][j]
            print(f"{node}->{targets}")
