import json
import scipy.cluster.hierarchy as hcl
from functools import reduce
import sys

from src import *


# Create a nested dictionary from the ClusterNode's returned by SciPy
def add_node(node, parent):
    # First create the new node and append it to its parent's children
    newnode = dict(node_id=node.id, children=[])
    parent["children"].append(newnode)

    # Recursively add the current node's children
    if node.left:
        add_node(node.left, newnode)
    if node.right:
        add_node(node.right, newnode)


# Label each node with the names of each leaf in its subtree
def label_tree(n, id2name, leafNames_list):
    # If the node is a leaf, then we have its name
    if len(n["children"]) == 0:
        leafNames = [id2name[n["node_id"]]]
        leafNames_list.append(leafNames)

    # If not, flatten all the leaves in the node's subtree
    else:
        reduced_value = reduce(lambda ls, c: ls + label_tree(c, id2name, leafNames_list), n["children"], [])
        leafNames = [len(leafNames_list)]
        leafNames_list.append(reduced_value)

    # Delete the node id since we don't need it anymore and
    # it makes for cleaner JSON
    del n["node_id"]

    # Labeling convention: "-"-separated leaf names
    n["name"] = name = "-".join(sorted(map(str, leafNames)))

    return leafNames


# clusters : condensed_matrix & labels(list): headers
def clusters_to_json(clusters, labels):
    T = hcl.to_tree(clusters, rd=False)
    # Create dictionary for labeling nodes by their IDs
    id2name = dict(zip(range(len(labels)), labels))

    # Initialize nested dictionary for d3, then recursively iterate through tree
    d3Dendro = dict(children=[], name="Root1")
    add_node(T, d3Dendro)

    leafNames_list = []
    sys.setrecursionlimit(15000)
    label_tree(d3Dendro["children"][0], id2name, leafNames_list)

    # Output to JSON
    json.dump(d3Dendro, open(OUT_JSON_FILE, "w"), sort_keys=True, indent=4)

    with open(MODEL_DIR+"\\leafNames_list.txt", 'w') as fp:
        indx = 0
        for line in leafNames_list:

            def join_list(line_list, joined_list):

                for word in line_list:
                    if type(word) == int:
                        # find word
                        join_list(leafNames_list[word], joined_list)
                    else:
                        joined_list.append(str(word))

            joined_list = []
            join_list(line, joined_list)
            fp.write(str(indx)+"\t"+'--'.join(joined_list)+"\n")
            # fp.write(str(indx) + "\t" + "--".join(str(x) for x in line) + "\n")
            indx += 1


def render_json_on_browser():
    # import webbrowser
    # webbrowser.get("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe").open(url)

    from subprocess import call
    url = "http://localhost:63342/Taxonomy_DataRiver/web/show_json.html"
    call(["C:\\Program Files (x86)\\Google\Chrome\\Application\\chrome.exe", "-new-tab", url])


# show()