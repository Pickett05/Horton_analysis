import numpy as np
import os
import pickle
from networkx.algorithms import community
import itertools
from datetime import datetime

def Girvan_Newman_community_detection(G,destination_folder):
    '''
    Input parameters:
        G (networkx graph): Graph whose community structure needs to be obtained
        destination_folder (str): Path to the folder where the results will be saved
    Output:
        Saves the community detection results, mainly, Community_Nodelist (list: contains lists of nodes constituting communities at a given level), actual_NC (list: number of communities at a level), l (list: level of community detection); in the folder 'Communities_GN' created inside 'destination folder'.
    '''
    level = 1
    N = G.number_of_nodes()
    # initializing the arrays and dictionaries
    l = [0]
    nodelist = {0:[list(G.nodes())]}
    actual_NC = [1]
    comp = community.girvan_newman(G)
    limited = itertools.takewhile(lambda c: len(c) <= N, comp)
    for communities in limited:
        current_time = datetime.now()
        print(f'Level = {level} at time {current_time}')
        log_file = open(f"{destination_folder}/Communities_GN/logfile.txt", "a")
        log_file.write(f"Level = {level} at time {current_time} \n")
        log_file.close()
        actual_NC.append(len(communities))
        l.append(level)
        nodelist[level] = list(sorted(c) for c in communities)
        level = level+1
    folder = f'{destination_folder}/Communities_GN'
    np.savetxt(f'{folder}/actual_NC.txt',actual_NC)
    np.savetxt(f'{folder}/l.txt',l)
    with open(f'{folder}/Community_Nodelist.pkl', 'wb') as fp:
        pickle.dump(nodelist, fp)

def common_member(a, b): 
    '''
    Input parameters:
        a = list
        b = list
    Output:
        Boolean value: whether a and b have anything in common
    '''  
    a_set = set(a)
    b_set = set(b)    
    # check length
    if len(a_set.intersection(b_set)) > 0:
        return(True)
    else:
        return(False)

def reorder_level(C_list_prev, C_list_current):
    '''
    Input parameters:
        C_list_prev = list of lists of communities at prev level
        C_list_current = list of lists of communities at current level
    Output:
        Community_ordered_dict: Dictionary where keys are previous communities and values are list of lists of current communities branched out from the previous one
    '''  
    Community_ordered_dict = {}
    ind = 0
    for j in C_list_prev:    
        Community_ordered_dict[ind] = []
        for i in C_list_current:
            
            if common_member(i,j):
                Community_ordered_dict[ind].append(i)
        ind = ind+1    
    return Community_ordered_dict

def community_detection_data(f1):
    '''
    Input parameters:
        f1 (str): path to community data
    Output:
        Community_ordered_dict (dict): Dictionary (keys are levels) of dictionaries (where keys are previous communities and values are list of lists of current communities branched out from the previous one)
    '''
    actual_NC = np.loadtxt(f'{f1}/Communities_GN/actual_NC.txt')
    l = np.loadtxt(f'{f1}/Communities_GN/l.txt')
    with open(f'{f1}/Communities_GN/Community_Nodelist.pkl', 'rb') as fp:
        Community_nodelist = pickle.load(fp)
    levels = l.size
    Community_ordered_dict = {}
    for i in range(1,levels):
        # previous level community partition
        if i == 1:
            C_list_prev = [list(Community_nodelist[0][0])]
        else:
            C_list_prev = []
            for j in Community_ordered_dict[i-1].values():
                for k in j:
                    C_list_prev.append(k)
        C_list_current = []
        # current level community partition
        for j in range(0,int(actual_NC[i])):  
            x = Community_nodelist[i][j]
            if np.ndim(x) == 0:
                C_list_current.append([x.tolist()])   
            else:
                C_list_current.append(list(x)) 
        Community_ordered_dict[i] = reorder_level(C_list_prev, C_list_current)
    # save dictionary to Community_ordered_dict.pkl file
    with open(f'{f1}/Communities_GN/Community_ordered_dict.pkl', 'wb') as fp:
        pickle.dump(Community_ordered_dict, fp)
        print('Saved the data.')                
    return Community_ordered_dict

def print_community_detection_data(D, levels):
    '''
    Input parameters:
        D (dict): Dictionary containing community detection data ('Community_ordered_dict')
        levels (int): Number of levels to print
    Output:
        Prints the community detection data for the first few levels.
    '''
    for i in range(1,levels):
        print(f'Level = {i}')
        for j in list(D[i].keys()):
            print(f'C{j} of L{i-1} has:')
            for k in D[i][j]:
                print(f'C = {k} with size = {len(k)}')
        print()