from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph


# Using my DS
class MyNode(object):
    def __init__(self, node_data, parent=None):
        self.node_data = node_data     #string
        self.relation_strength = 0.0    # relation_strength is how tightly node is connected to its parent node,
                                        # range: [0.0, 1.0]; for root node it will be 1.0
        self.children = []              # List of child nodes
        self.parent = parent


# using my DS
class MyTree(object):
    def __init__(self):
        # super(MyTree, self).__init__(node_data, parent)
        self.root = None
        self.node_map = {}  # dict of {nodename: nodeaddress(MyNode)}

    def create_tree(self, nodename="root"):
        # To make a node to a root node, just set 'parent=None'
        self.root = MyNode(nodename)
        # add node mapping
        self.node_map[nodename] = self.root

    def add_child(self, node_name, parent_name):
        # create new node under parent node & add node mapping
        try:
            parent_node = self.node_map[parent_name]
            new_node = MyNode(node_name, parent_node)
            parent_node.children.append(node_name)
            self.node_map[node_name] = new_node
        except:
            print("<", parent_name, "> Parent name doesn't exist")

    def remove_child(self, node_name, parent_name):
        pass

    def renderTree(self):
        # print("Depth & Height of the tree: ", self.root.depth(), self.root.height())
        print("Tree Nodes: ")
        for node_name in self.node_map:
           print(node_name, ":", self.node_map[node_name].children)

    def renderTreeGraph(self):
        # graphic needs to be installed for the next line!
        pass


# using anytree library
class Tree(object):
    def __init__(self):
        self.root = None
        self.node_map = {}      # dict of {nodename: nodeaddress} for anytree

    def create_tree(self, nodename="root"):
        # To make a node to a root node, just set 'parent=None'
        self.root = Node(nodename, parent=None)
        # add node mapping
        self.node_map[nodename] = self.root

    def addChild(self, node_name, parent_name):
        # create new node under parent_name & add node mapping
        try:
            self.node_map[node_name] = Node(node_name, self.node_map[parent_name])
        except:
            print("<", parent_name, "> Parent name doesn't exist")

    def renderTree(self):
        # print("Depth & Height of the tree: ", self.root.depth(), self.root.height())
        print("Tree Nodes: ")
        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))

    def renderTreeGraph(self):
        # graphic needs to be installed for the next line!
        RenderTreeGraph(self.root).to_picture("tree.png")


def test_mytree():
    print("Running Test")
    mytree = MyTree()
    mytree.create_tree("udo")
    mytree.add_child(node_name="marc", parent_name="udo")
    mytree.add_child("lian", "marc")
    mytree.add_child("dan", "udo")
    mytree.add_child("jet", "dan")
    mytree.add_child("jan", "dan")
    mytree.add_child("joe", "dan")

    mytree.renderTree()

    '''
    Running Test
    Tree Nodes:
    jet : []
    dan : ['jet', 'jan', 'joe']
    udo : ['marc', 'dan']
    joe : []
    jan : []
    marc : ['lian']
    lian : []
    '''

def test_tree():
    print("Running Test")
    tree = Tree()
    tree.create_tree("udo")
    tree.addChild(node_name="marc", parent_name="udo")
    tree.addChild("lian", "marc")
    tree.addChild("dan", "udo")
    tree.addChild("jet", "dan")
    tree.addChild("jan", "dan")
    tree.addChild("joe", "dan")

    tree.renderTree()
    '''
    Test1
    udo = Node("Udo")
    marc = Node("Marc", parent=udo)
    lian = Node("Lian", parent=marc)
    dan = Node("Dan", parent=udo)
    jet = Node("Jet", parent=dan)
    jan = Node("Jan", parent=dan)
    joe = Node("Joe", parent=dan)

    print(udo)
    Node('/Udo')
    print(joe)
    Node('/Udo/Dan/Joe')

    for pre, fill, node in RenderTree(udo):
        print("%s%s" % (pre, node.name))
    Udo
    ├── Marc
    │   └── Lian
    └── Dan
        ├── Jet
        ├── Jan
        └── Joe

    print(dan.children)
    (Node('/Udo/Dan/Jet'), Node('/Udo/Dan/Jan'), Node('/Udo/Dan/Joe'))
    '''


# test_tree()
test_mytree()