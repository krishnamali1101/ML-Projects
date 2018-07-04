#!/usr/bin/env python
 
from math import*
from decimal import Decimal


class Similarity(object):
    def __init__(self):
        pass

    """ Five similarity measures function """
    def euclidean_distance(self, x, y):
        """ return euclidean distance between two lists """
        return sqrt(sum(pow(a-b, 2) for a, b in zip(x, y)))
 
    def manhattan_distance(self, x, y):
        """ return manhattan distance between two lists """
        return sum(abs(a-b) for a, b in zip(x, y))
 
    def minkowski_distance(self, x, y, p_value):
        """ return minkowski distance between two lists """
        return self.nth_root(sum(pow(abs(a-b), p_value) for a, b in zip(x, y)), p_value)
 
    def nth_root(self, value, n_root):
        """ returns the n_root of an value """
        root_value = 1/float(n_root)
        return round (Decimal(value) ** Decimal(root_value), 3)
 
    def cosine_similarity(self, x, y):
        """ return cosine similarity between two lists """
        numerator = sum(a*b for a, b in zip(x, y))
        denominator = self.square_rooted(x)*self.square_rooted(y)
        return round(numerator/float(denominator), 3)
 
    def square_rooted(self, x):
        """ return 3 rounded square rooted value """
        return round(sqrt(sum([a*a for a in x])), 3)

    def jaccard_similarity(self, x, y):
        """ returns the jaccard similarity between two lists """
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality/float(union_cardinality)
 

def main():
    """ the main function to create Similarity class instance and get used to it """
    vec1 = [0, 3, 4, 5]
    vec2 = [7, 6, 3, -1]
    vec3 = [0, 1, 2, 5, 6]
    vec4 = [0, 2, 3, 5, 7, 9]

    measures = Similarity()
    # various distance between vec1 & vec2
    print("Vectors(vec1&vec2): ", vec1, vec2)
    print("euclidean_distance: ", measures.euclidean_distance(vec1, vec2))
    print("manhattan_distance: ", measures.manhattan_distance(vec1, vec2))
    print("minkowski_distance: ", measures.minkowski_distance(vec1, vec2, 3))
    print("cosine_similarity : ", measures.cosine_similarity(vec1, vec2))
    print("jaccard_similarity: ", measures.jaccard_similarity(vec1, vec2))

    # various distance between vec3 & vec4
    print("\n\nVectors(vec3&vec4): ", vec3, vec4)
    print("euclidean_distance: ", measures.euclidean_distance(vec3, vec4))
    print("manhattan_distance: ", measures.manhattan_distance(vec3, vec4))
    print("minkowski_distance: ", measures.minkowski_distance(vec3, vec4, 3))
    print("cosine_similarity : ", measures.cosine_similarity(vec3, vec4))
    print("jaccard_similarity: ", measures.jaccard_similarity(vec3, vec4))

if __name__ == "__main__":
    main()

# ==================================================


# OUTPUT:
''''
Vectors(vec1&vec2):  [0, 3, 4, 5] [7, 6, 3, -1]
euclidean_distance:  9.746794344808963
manhattan_distance:  17
minkowski_distance:  8.373
cosine_similarity :  0.363
jaccard_similarity:  0.14285714285714285


Vectors(vec3&vec4):  [0, 1, 2, 5, 6] [0, 2, 3, 5, 7, 9]
euclidean_distance:  1.7320508075688772
manhattan_distance:  3
minkowski_distance:  1.442
cosine_similarity :  0.712
jaccard_similarity:  0.375
'''