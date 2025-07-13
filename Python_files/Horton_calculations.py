from Python_functions import log_message, log_process
import numpy as np
import pickle
import networkx as nx

def construct_binary_tree_rep(folder):
    '''
    This function constructs a binary tree representation of the community structure of a network. The community structure is obtained from the Girvan-Newman algorithm. The binary tree representation of the community structure is saved in the folder 'Communities_GN' created inside 'folder'.
    Input parameters:
        folder (str): Path to the folder where the community structure data (folder 'Communities_GN') is saved.
    Output:
        B (networkx graph): Binary tree representation of the community structure.
    '''
    with open(f'{folder}/Communities_GN/Community_ordered_dict.pkl', 'rb') as fp:
        D = pickle.load(fp)
    B = nx.Graph()
    N = {}
    for i in range(1,101,1):
        N[i] = 0

    for i in range(int(max(D.keys())), 0, -1): # for each level starting from the bottom till 1st level
        
        log_process(f"-", folder=f'{folder}/Communities_GN')
        Comm_CL = D[i] # community structure at CL
        if i != 1:
            Comm_PL = D[i-1] # community structure at PL
        else: 
            Comm_PL = {0:[sorted(D[i][0][0]+D[i][0][1])]}
        items = Comm_PL.items()  

        for j in list(Comm_CL.keys()): # for each prev level community we have it's sub communities at current level   
            Daughters = Comm_CL[j] 
            Dad = []
            for k in Daughters: 
                for x in k: Dad.append(x)
            Dad.sort() # merged community of the set of communities at CL belonging to father community at PL
            
            for key, value in items:  
                cn = 0
                for val in value:
                    if sorted(val) == sorted(Dad):
                        key_PL = key
                        count_PL = cn
                        break
                    cn += 1

            if len(Comm_CL[j]) == 1: # if the prev level community did not branch out: x: [[X]]
                old = f"{i},{j},0"
                new = f"{i-1},{key_PL},{count_PL}"
                if B.has_node(old):
                    nx.relabel_nodes(B, {old:new}, copy=False)
                else:
                    B.add_node(new, nodetype="leaf")

            elif len(Comm_CL[j]) == 2: # if the prev level community branched out into two sub communities: x = [[X],[Y]]
                c = 0
                root_node = f"{i-1},{key_PL},{count_PL}"
                B.add_node(root_node, nodetype="root")
                for comm in Comm_CL[j]:
                    
                    branch_node = f"{i},{j},{c}"  
                    if not B.has_node(branch_node):
                        if len(comm) == 1:
                            B.add_node(branch_node, nodetype="leaf")    
                        else:
                            B.add_node(branch_node, nodetype="root")

                    B.add_edge(root_node, branch_node)

                    if B.nodes[branch_node]['nodetype'] == "leaf":
                        B.edges[root_node,branch_node]['SHN'] = 1
                        N[1] += 1
                    else:
                        daughters = []
                        for ed in B[branch_node]:
                            if ed != root_node:
                                daughters.append(ed)
                        shn1 = B.edges[branch_node,daughters[0]]['SHN']
                        shn2 = B.edges[branch_node,daughters[1]]['SHN']
                        if shn1 == shn2:
                            B.edges[root_node,branch_node]['SHN'] = shn1+1
                            N[shn1+1] += 1
                        else:
                            B.edges[root_node,branch_node]['SHN'] = max(shn1, shn2)
                    c += 1
            
    # limit to non-zero entries
    a_c = []
    for i in list(N.values()):
        if i>0:
            a_c.append(i)
    
    ancest = []
    log_process(f"-",folder=f'{folder}/Communities_GN')
    for ed in B["0,0,0"]:
        ancest.append(ed)
    shn1 = B.edges["0,0,0",ancest[0]]['SHN']
    shn2 = B.edges["0,0,0",ancest[1]]['SHN']
    if shn1 == shn2:
        N[shn1+1] += 1

    nx.write_gml(B, f"{folder}/Communities_GN/BT_rep.gml")
    return B

def assign_Horton_index(G):
    '''
    Input parameters:
        G (networkx graph): A binary tree that could represent the community structure of a network. However, this function can work on any general binary tree.
    Output:
        G (networkx graph): Binary tree with Horton index assigned to each node (as node attribute 'node_ind').
        N (1D ndarray): Array containing the number of branches at a Horton index.
    '''
    N = np.zeros(50) # an arbitrarily large number that should be larger than maximum Horton-Strahler index
    leaf_nodes = []
    branch_nodes = []
    for node in G.nodes():
        if G.degree(node) == 1:
            nx.set_node_attributes(G, {node:1}, "node_ind")
            leaf_nodes.append(node)
            N[1] += 1
        else:
            nx.set_node_attributes(G, {node:0}, "node_ind")
            branch_nodes.append(node)
    
    while len(branch_nodes) > 0:
        for b_node in branch_nodes:
            b_edges = list(G.edges(b_node))
            sum_node_ind = 0
            b_kids = []
            for i in b_edges:
                if G.nodes[i[1]]["node_ind"]>0:
                    b_kids.append(i[1])
                    sum_node_ind += 1
            if sum_node_ind == 2:
                if G.nodes[b_kids[0]]["node_ind"] != G.nodes[b_kids[1]]["node_ind"]:
                    G.nodes[b_node]["node_ind"] = max(G.nodes[b_kids[0]]["node_ind"],G.nodes[b_kids[1]]["node_ind"])
                else:
                    G.nodes[b_node]["node_ind"] = G.nodes[b_kids[0]]["node_ind"] + 1
                    N[G.nodes[b_node]["node_ind"]] += 1
                branch_nodes.remove(b_node)
    N = np.trim_zeros(N,'fb')
    
    return G, N

def n_score(Nodelist, G):
    '''
    This function calculates the relative link density of a community in a network.
    Input parameters:
        Nodelist (list): List of nodes in the community detected in a network
        G (networkx graph): Network whose community structure is being analyzed
    Output:
        nsc (float): The value of relative link density of the community
    '''
    AdjMat = nx.to_numpy_array(G)
    # initialization
    nsc = 0
    nc = len(Nodelist)  # number of nodes in the community
    k_in = {}
    k_out = {}
    k_in_frac = {}
    k_out_frac = {}
    global_nodelist = list(np.array((G.nodes), dtype=int))
    
    # calculating the degrees
    Nodelist = list(np.array(Nodelist, dtype=int))
    for i in Nodelist:
        k_in[i] = 0
        k_out[i] = 0
        c = 0
        for j in global_nodelist:
            if AdjMat[global_nodelist.index(i)][global_nodelist.index(j)] == 1:
                c += 1
                if j in Nodelist:
                    k_in[i] += 1
                else:
                    k_out[i] += 1
        k_in_frac[i] = k_in[i]/c
        k_out_frac[i] = k_out[i]/c

    # calulating n score
    r = nx.density(nx.from_numpy_array(AdjMat))
    if nc==1:
        rc = 0
    else:
        rc = (sum(k_in.values())/2)/(nc*(nc-1)/2)
    nsc = rc/r

    return nsc

def calculate_Horton_attributes(folder):
    ''' 
    Input parameters:
        folder (str): Path to the folder where the community structure data (folder 'Communities_GN') is saved.
    Output:
        BT_Dict (dict): Dictionary containing the Horton-Strahler index, eta, size, and depth of each community in the network. This data structure is explained in detail in the documentation.
    '''
    B = nx.read_gml(f"{folder}/Communities_GN/BT_rep.gml")
    G = nx.read_gml(f"{folder}/network.gml")
    with open(f'{folder}/Communities_GN/Community_ordered_dict.pkl', 'rb') as fp:
        D = pickle.load(fp)
    sh_B, N_i_sm = assign_Horton_index(B)
    
    BT_Dict = {'0,0,0':{'eta':1,'size':G.number_of_nodes(),'hsi':len(N_i_sm),'depth':nx.shortest_path_length(B, source='0,0,0', target='0,0,0')}}
    log_message("Community:  0,0,0", folder=f'{folder}/Communities_GN')
    C_list = list(B.nodes())
    C_list.remove('0,0,0')
    for community_node in C_list:
        # print("Community: ",community_node)
        [a, b, c] = [int(i) for i in community_node.split(',')]
        i = B.nodes[community_node]["node_ind"]
        if len(D[a][b][c]) > 0:
            log_message(f"Community: {community_node}", folder=f'{folder}/Communities_GN')
            BT_Dict[community_node]={}
            BT_Dict[community_node]['eta'] = n_score(D[a][b][c], G)
            BT_Dict[community_node]['size'] = len(D[a][b][c])
            BT_Dict[community_node]['hsi'] = i
            BT_Dict[community_node]['depth'] = nx.shortest_path_length(B, source='0,0,0', target=community_node)        
    
    nx.write_gml(sh_B, f"{folder}/Communities_GN/BT_rep.gml")
    with open(f'{folder}/Communities_GN/BT_Dict.pkl', 'wb') as fp:
        pickle.dump(BT_Dict, fp)
    # Order: key, hsi, eta, depth, size_C
    BT_Mat_nodes = []
    BT_Mat = [[],[],[],[]]
    for key in BT_Dict.keys():
        BT_Mat_nodes.append(key)
        BT_Mat[0].append(BT_Dict[key]['hsi'])
        BT_Mat[1].append(BT_Dict[key]['eta'])
        BT_Mat[2].append(BT_Dict[key]['depth'])
        BT_Mat[3].append(BT_Dict[key]['size'])
    
    np.savetxt(f'{folder}/Communities_GN/BT_Mat.txt',BT_Mat)
    np.savetxt(f'{folder}/Communities_GN/BT_Mat_names.txt',BT_Mat_nodes, fmt="%s")

    return BT_Dict

def find_branches(folder):
    '''
    This function identifies the branches in a binary tree whose nodes are indexed using the Horton-Strahler indexing scheme.
    Input parameters:
        folder (str): Path to the folder where the community structure data (folder 'Communities_GN') is saved.
    Output:
        disconnected_G (networkx graph): A graph containing the branches of the binary tree isolated as individual connected components.
    '''
    G = nx.read_gml(f"{folder}/Communities_GN/BT_rep.gml")
    disconnected_G = G
    for edge in G.edges():
        if G.nodes[edge[0]]["node_ind"] != G.nodes[edge[1]]["node_ind"]:
            disconnected_G.remove_edge(edge[0],edge[1])
    return disconnected_G

def calculate_Horton_branch_attributes(folder, disconnected_G):
    '''                 
    Input parameters:
        folder (str): Path to the folder where the community structure data (folder 'Communities_GN') is saved.
        disconnected_G (networkx graph): A graph containing the branches of the binary tree isolated as individual connected components.
    Output:
        new_dict (dict): Dictionary containing the Horton-Strahler index, eta, size, and depth of each branch in the network.
    '''
    with open(f'{folder}/Communities_GN/BT_Dict.pkl', 'rb') as fp:
        BT_Dict = pickle.load(fp)
    new_dict = {}
    for branch in sorted(nx.connected_components(disconnected_G), key=len, reverse=True):

        branch_nodes = list(disconnected_G.subgraph(branch).nodes())
        branch_key = ''
        for node in branch_nodes: branch_key += node+' '
        l = len(branch_nodes)

        new_dict[branch_key]={}
        new_dict[branch_key]['eta'] = 0
        new_dict[branch_key]['size'] = 0
        new_dict[branch_key]['hsi'] = 0
        new_dict[branch_key]['depth'] = 0
        dep = []
        new_dict[branch_key]['length'] = l

        for community_node in branch_nodes:
            new_dict[branch_key]['eta'] += BT_Dict[community_node]['eta']
            new_dict[branch_key]['size'] += BT_Dict[community_node]['size']
            new_dict[branch_key]['hsi'] += BT_Dict[community_node]['hsi']
            new_dict[branch_key]['depth'] += BT_Dict[community_node]['depth']
        
        new_dict[branch_key]['eta'] = new_dict[branch_key]['eta']/l
        new_dict[branch_key]['size'] = new_dict[branch_key]['size']/l
        new_dict[branch_key]['hsi'] = new_dict[branch_key]['hsi']/l
        new_dict[branch_key]['depth'] = new_dict[branch_key]['depth']/l

    with open(f'{folder}/Communities_GN/BL_Dict.pkl', 'wb') as fp:
        pickle.dump(new_dict, fp)
    # Order: key, hsi, eta, depth, size_C
    BL_Mat_nodes = []
    BL_Mat = [[],[],[],[]]
    for key in new_dict.keys():
        BL_Mat_nodes.append(key)
        BL_Mat[0].append(new_dict[key]['hsi'])
        BL_Mat[1].append(new_dict[key]['eta'])
        BL_Mat[2].append(new_dict[key]['depth'])
        BL_Mat[3].append(new_dict[key]['size'])
    np.savetxt(f'{folder}/Communities_GN/BL_Mat.txt',BL_Mat)
    np.savetxt(f'{folder}/Communities_GN/BL_Mat_names.txt',BL_Mat_nodes, fmt="%s")
    return new_dict