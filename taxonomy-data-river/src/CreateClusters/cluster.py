# import scipy
# from scipy.cluster.hierarchy import cophenet
# from scipy.spatial.distance import pdist

# Reference: http://people.revoledu.com/kardi/tutorial/Clustering/Numerical%20Example.htm

import os

import numpy as np
import scipy.cluster.hierarchy as hcl
import scipy.spatial.distance as ssd

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

from src.CreateClusters import clusters_to_json as cl2js
from taxonomy_main import Taxonomy
from src import *


def save_condensed_matrix(condensed_matrix):
    print("saving_condensed_matrix")
    with open(CLUSTER_MATRIX, 'w') as fp:
        r=0
        for row in condensed_matrix:
            if r%100==0:
                print("Processing RowNo ", r, "/", len(condensed_matrix))
            for col in row:
                fp.write(str(col)+"\t")
            fp.write(str("\n"))
            r += 1


def load_condensed_matrix(total_rows):
    print("loading_condensed_matrix")
    condensed_matrix = []
    with open(CLUSTER_MATRIX, 'r') as fp:
        r=0
        for line in fp.readlines():
            if r % 100 == 0:
                print("Processing RowNo ", r, "/", total_rows)
            row =[]
            for word in line.strip().split("\t"):
                row.append(float(word))
            condensed_matrix.append(row)
            r +=1

    # convert to numpy ndarray & return
    return np.array(condensed_matrix)


# create condensed_matrix(clusters)
def create_condensed_matrix(dist_mat):
    print("create_condensed_matrix")
    # convert the redundant n*n square matrix form into a condensed nC2 array
    # distArray[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
    # y
    # y = M[np.triu_indices(n,1)]
    distArray = ssd.squareform(dist_mat)

    '''
    linkage methods like 'single', 'complete', 'average'
     and the different distance metrics like 'euclidean' (default), 'cityblock' aka Manhattan, 'hamming', 'cosine'''
    condensed_matrix = hcl.linkage(distArray, method='single', metric='euclidean')
    # method = single; d(u,v)=min(dist(u[i],v[j]))

    save_condensed_matrix(condensed_matrix)

    return condensed_matrix


# plot Hierarchical clustering Dendrogram
def plot_hcd(headers=None, dist_mat=None):
    if not headers and not dist_mat:
        raise ValueError("dist_mat & headers cant be empty")

    if os.path.exists(CLUSTER_MATRIX):
        condensed_matrix = load_condensed_matrix(len(headers))
    else:
        condensed_matrix = create_condensed_matrix(dist_mat)

    # calculate full dendrogram
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        condensed_matrix,
        leaf_rotation=45,  # rotates the x axis labels
        leaf_font_size=8,  # font size for the x axis labels
        labels=headers,
        orientation='top'   # default
    )
    # plt.show()
    # plt.savefig("model\\scipy-dendrogram.png")

    # cl2js.clusters_to_json(condensed_matrix, headers)

    # dendrogram(
    #     condensed_matrix,
    #     truncate_mode='lastp',  # show only the last p merged clusters
    #     labels=headers[(len(headers) - 13):],
    #     p=12,  # show only the last p merged clusters
    #     show_leaf_counts=False,  # otherwise numbers in brackets are counts
    #     leaf_rotation=90,
    #     leaf_font_size=12,
    #     show_contracted=True,  # to get a distribution impression in truncated branches
    # )
    # plt.show()

def test():
    taxonomy = Taxonomy()
    headers, dist_mat = taxonomy.create_load_distance_matrix()
    plot_hcd(headers, dist_mat)

# test()

'''
scipy.cluster.hierarchy.linkage(y, method='single', metric='euclidean') 
Parameters:	
y : ndarray
    A condensed distance matrix. A condensed distance matrix is a flat array containing the upper triangular of 
    the distance matrix. This is the form that pdist returns. Alternatively, a collection of mm observation 
    vectors in nn dimensions may be passed as an mm by nn array. All elements of the condensed distance matrix must be
    finite, i.e. no NaNs or infs.
method : str, optional
    The linkage algorithm to use. See the Linkage Methods section below for full descriptions.
metric : str or function, optional
    The distance metric to use in the case that y is a collection of observation vectors; ignored otherwise. 
    See the pdist function for a list of valid distance metrics. A custom distance function can also be used.

Returns:	
Z : ndarray
    The hierarchical clustering encoded as a linkage matrix.

https://docs.scipy.org/doc/scipy-0.19.1/reference/generated/scipy.cluster.hierarchy.linkage.html
'''

# hcl.linkage(ssd.squareform(dist_mat))
# print(out_matrix)
'''
[[ 18.          20.          28.63270785   2.        ]
 [ 17.          24.          28.70900394   3.        ]
 [ 10.          25.          29.17791716   4.        ]
 [  7.          16.          29.93885336   2.        ]
 [  8.          27.          30.27082      3.        ]
 [ 11.          12.          30.68464734   2.        ]
 [  1.          28.          31.40298405   4.        ]
 [  4.          21.          31.43284733   2.        ]
 [ 23.          30.          31.59884882   5.        ]
 [  9.          26.          31.60509592   5.        ]
 [  0.          32.          32.41020504   6.        ]
 [  2.          33.          32.62437084   6.        ]
 [ 29.          34.          33.57280177   8.        ]
 [ 35.          36.          33.61457598  14.        ]
 [ 31.          37.          33.86016311  16.        ]
 [ 14.          38.          34.07014104  17.        ]
 [ 19.          39.          34.37222321  18.        ]
 [ 22.          40.          36.75295079  19.        ]
 [  5.          41.          37.75461257  20.        ]
 [ 15.          42.          39.29288628  21.        ]
 [ 13.          43.          39.45631889  22.        ]
 [  6.          44.          39.61061355  23.        ]
 [  3.          45.          41.54958683  24.        ]]
 
array([ 18.          20.          28.63270785   2.        ])
We can see that ach row of the resulting array has the format [idx1, idx2, dist, sample_count].

In its first iteration the linkage algorithm decided to merge the two clusters (original samples here) with indices 
52 and 53, as they only had a distance of 0.04151. This created a cluster with a total of 2 samples.
'''

