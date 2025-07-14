# Repository for Horton analysis

This repository contains the codes required for:
1. Finding the community structure of a given network using Girvan-Newman's community detection algorithm and storing the data in an appropriate data structure that preserves the hierarchical organization of communities.

1. Representing the hierarchical organization of communities in the form of a binary tree.

1. Evaluating different Horton's laws for the binary tree representation of the network.

Please cite the following authors if using this repository:

>Tandon, S.\*, Sonwane, N. D.\*, Braun, T., Marwan, N., Kurths, J., and Sujith, R. I. (2025). Universal self-similarity of hierarchical
communities formed through a general self-organizing principle (these authors contributed equally).

## Function/class files

This repository has two folders: `Python_files` and `MATLAB_files` containing several files serving different purposes. **Note that these codes only work on unweighted, undirected, connected networks with nodes having integer labels.**

### `Python_files`

This folder contains files for detecting communities in a given network, representing the hierarchical community structure in the form of a binary tree and calculating different attributes of communities that would be eventually needed for evaluating the Horton's laws. Ensure that this folder is added in your path in order to be able to use all the modules. The files are:

* `Community_detection_codes.py` performs community detection and efficient storage of community structure data. 
* `Horton_calculations.py` contains functions for representing the topology of communities in the form of a binary tree, assignment of Horton-Strahler indices to nodes in a tree and calculation of different attributes of communities detected.
* `Python_functions.py` contains functions for running different functions in the above files and other miscellaneous functions for logging the process.

### `MATLAB_files`

This folder contains files for generating the Horton's laws for a tree representing the community structure of a given network, and hence unravelling the topological self-similarity in that network after all the calculations have been made using the Python codes described above. Ensure that this folder is added in your MATLAB path in order to be able to run the main code.


## Example usage

Consider a folder `sample_1` containing some sample network to be analysed. Note that this network must be named and saved in the format `network.gml`. Please check the sample file `Example.ipynb` that characterizes the community structure of a given network and evaluates different attributes of the community required for finding the Horton's laws. Run this file for the above folder to find the output stored in a new folder named `Communities_GN` that will be automatically created in the given folder. This folder will contain all our community structure related data. It has the following files of interest:

* `Community_ordered_dict.pkl` is a pickle file when loaded in Python represents a `dictionary` that stores the hierarchical community structure of the network. The dictionary has elements whose
    * `key` represents level of community detection (`int`)
    * `value` contains the communities at that level represented by another `dictionary` whose elements contain:
        * `key` represents ID of community at the previous level, i.e., parent community (`int`)
        * `value` represents the communities within the parent community (`list`). This list contains lists of communities each having the set of nodes constituting that community (thus, every element is a node label/ID).
* `BT_rep.gml` encodes the binary tree representation of the network in GML format. Each node has an attribute named `node_ind` storing its Horton-Strahler index.
* `BT_dict.pkl`, `BT_Mat.txt` and `BT_Mat_names.txt` store different attributes of the community-nodes of the binary tree representation in different formats. These will be used by our MATLAB codes to generate the plots showing the Horton's laws. `BT_dict.pkl` when loaded in Python represents a dictionary containing the information regarding the community-nodes present in the binary tree representation. This dictionary has:
    * `key` representing ID of a community-node. Every community-node has an ID in the following format:
    '$a,b,c$' where $a$, $b$ and $c$ are integers such that:
        * $a$ - level at which the community has been detected
        * $b$ - list index of the parent community in a list of communities detected at the previous level.
        * $c$ - list index of the community in the list of communities that are children of the parent community. Since at any level, a community will split into atmost 2 sub-communities, the list containing these sub-communities will have a size of atmost 2. Thus, $c$ can take values from the set $\{0,1\}$.
    
        Note: the entire network as a single community is exceptionally named as '$0,0,0$'.
    * `value` containing another `dictionary` containing different attributes of that community. In particular, this dictionary will have 4 keys, namely 'eta', 'size', 'hsi', 'depth' with the respective numerical values for relative link density, size (number of nodes), Horton-Strahler index, hierarchical depth of the community under consideration.

    We save the same data in text files `BT_Mat.txt` and `BT_Mat_names.txt`. Each row of `BT_Mat_names.txt` contains the community-node ID. The corresponding attributes of the community are stored in `BT_Mat.txt` each line representing Horton-Strahler order, relative link density, hierarchical depth, size of the community. The values for all these communities are separated by spaces, i.e., for a given community-node, if its ID is in the $x^{th}$ row of `BT_Mat_names.txt`, the attributes are present in the $x^{th}$ column of `BT_Mat.txt`.
* `BL_dict.pkl`, `BL_Mat.txt` and `BL_Mat_names.txt` store different attributes of the branches of the binary tree representation in different formats. The format is similar to how data is stored for community-nodes present in the tree representation. These will be used by our MATLAB codes to generate the plots showing the Horton's laws.

Next, run the file `Example.m` to generate the plot showing the Horton's laws. Refer to the paper for more details on the details of all the laws and the terminologies used in this repository.

## External dependencies

In order to run the codes in this repository, the following Python modules are needed, please ensure that they are installed.
* networkx
* numpy
* itertools
* pickle
* datetime
* shutil
* os
* sys

