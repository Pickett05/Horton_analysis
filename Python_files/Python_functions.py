import networkx as nx
import datetime
from datetime import datetime
import shutil
import os

def log_message(message, folder):
    '''
    This function logs the given message to the logfile in a given folder, while also printing in the standard output.
    Input parameters:
        message (str): Message to be logged
        folder (str): Path to the folder where the logfile is to be created/situated
    Output:
        Prints and appends the message to the logfile in the given folder.
    '''
    print(message)
    log_file = open(f"{folder}/logfile.txt", "a")
    log_file.write(f"{message} \n")
    log_file.close()

def log_process(message, folder):
    '''
    This function logs a simulation/process to the logfile in a given folder, while also printing in the standard output.
    Input parameters:
        message (str): Message to be logged
        folder (str): Path to the folder where the logfile is to be created/situated
    Output:
        Prints and appends the loading to the logfile in the given folder.
    '''
    print(message, end='')
    log_file = open(f"{folder}/logfile.txt", "a")
    log_file.write(f"{message}")
    log_file.close()

def empty_directory(directory_path):
    '''
    This function deletes all files and subdirectories in the given directory.
    Input parameters:
        directory_path (str): Path to the directory to be emptied
    Output:
        Deletes all files and subdirectories in the given directory.
    '''
    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_file():
                    os.unlink(entry.path)
                else:
                    shutil.rmtree(entry.path)
        print("All files and subdirectories deleted successfully.")
    except OSError:
        print("Error occurred while deleting files and subdirectories.")


from Community_detection_codes import Girvan_Newman_community_detection, community_detection_data, print_community_detection_data
from Horton_calculations import construct_binary_tree_rep, calculate_Horton_attributes, find_branches, calculate_Horton_branch_attributes


def run_community_detection(folder):
    ''' 
    This function runs the community detection algorithm on the network graph in the given folder.
    Input parameters:
        folder (str): Path to the folder where the network graph ('network.gml') is located
    Output:
        Creates a new folder for community detection results (Communities_GN) and saves the data in appropriate format.
    '''
    new_folder = f'{folder}/Communities_GN'
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    empty_directory(new_folder)    
    current_time1 = datetime.now()
    log_message(f'Running commuity detection. Start time: {current_time1}', new_folder)
    Girvan_Newman_community_detection(nx.read_gml(f'{folder}/network.gml'),folder)
    current_time2 = datetime.now()
    log_message(f'Community detection done. End time: {current_time2}', new_folder)
    log_message(f'Total time taken = {current_time2 - current_time1}', new_folder)
    log_message('\nConstructing data structure (dictionary) to save the communities detected.', new_folder)
    s = community_detection_data(folder)
    # Uncomment the following two lines to print the community detection data for first few levels
    # print("\nPrinting the community detection data for first few levels.")
    # print_community_detection_data(s,5)
    log_message(f"Exiting the code. End time: {datetime.now()}", new_folder)

def run_binary_tree_rep_construction(folder):
    '''
    This function constructs a binary tree representation of the community structure in the given folder.
    Input parameters:
        folder (str): Path to the folder where the network graph ('network.gml') is located. This function should be run only after running the community detection algorithm via the 'run_community_detection' function.
    Output:
        Saves the binary tree representation in appropriate format in 'Communities_GN' folder.
    '''
    new_folder = f'{folder}/Communities_GN'
    current_time1 = datetime.now()
    log_message(f'\nConstructing binary tree representation of the community structure. Start time: {current_time1}', new_folder)   
    s = construct_binary_tree_rep(folder)
    log_message('\nDone.', new_folder)
    current_time2 = datetime.now()
    log_message(f'Exiting the code. End time: {current_time2}', new_folder)
    log_message(f'Total time taken = {current_time2 - current_time1} \n', new_folder)

def run_Horton_analysis(folder):
    '''
    This function runs the Horton analysis on the community structure in the given folder.
    Input parameters:
        folder (str): Path to the folder where the network graph ('network.gml') is located. This function should be run only after obtaining the binary tree representation using the function 'run_binary_tree_rep_construction'.
    Output:
        Saves the Horton analysis results in appropriate format in 'Communities_GN' folder.
    '''
    new_folder = f'{folder}/Communities_GN'
    current_time1 = datetime.now()
    log_message(f'\nFinding all the measures for community nodes. Start time: {current_time1}', new_folder)   
    s = calculate_Horton_attributes(folder)
    log_message('Done.', new_folder)
    log_message('\nFinding all the measures for branches in the tree.',new_folder)
    disconnected_G = find_branches(folder)
    t = calculate_Horton_branch_attributes(folder, disconnected_G)
    log_message('Done.', new_folder)
    current_time2 = datetime.now()
    log_message(f'Exiting the code. End time: {current_time2}', new_folder)
    log_message(f'Total time taken = {current_time2 - current_time1} \n', new_folder)