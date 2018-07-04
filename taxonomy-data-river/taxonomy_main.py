
from src.DataPreprocessing.TextFilter import TextFilter
from src.TrainModel import distance_matrix as dist_mat
from src.TrainModel.doc2vec_gensim import GensimDoc2Vec
from src.CreateClusters import cluster as cl
from src.DataPreprocessing import parse_data as parser
from src.CreateClusters import clusters_to_json as cl2js

from src import *


class Taxonomy(object):
    def __init__(self):
        self.topic_description_map = {}

        # set filters and filter input line
        self.fltr = TextFilter()
        # remove stem filter from all default filters, reason: stem can change the word
        self.fltr.set_filters([lambda x: x.lower(), self.fltr.strip_tags, self.fltr.strip_punctuation,
                               self.fltr.strip_multiple_whitespaces])

        self.gensimdoc2vec_obj = GensimDoc2Vec()
        # list of topics
        self.headers = []    # headers / topics

    # distance should be minimum
    def create_node_maxsimilarnode_list(self, headers, matrix):
        node_maxsimilarnode_list = []
        print("Creating new node_maxsimilarnode_list.xls...")
        r=0
        for row in matrix:
            if not (r % 100):
                print("Processing RowNo ", r, " out-of ", len(headers))
            c =0
            min = 100.0
            similar_nodes = []
            for col in row:
                col = round(col, 3)
                if r==c:    # ignore diagonal elements
                    c += 1
                    continue
                # add all ele having same distance
                if min>col:
                    min = col
                    similar_nodes.clear()
                    similar_nodes.append(headers[c])
                elif min==col:
                    # append for same distance
                    similar_nodes.append(headers[c])

                c += 1

            inner_list = []
            inner_list.append(headers[r])
            inner_list.append(str(min))
            inner_list += similar_nodes
            node_maxsimilarnode_list.append(inner_list)
            r += 1

        # write it to file
        with open(MODEL_DIR+"\\node_maxsimilarnode_list.csv", "w") as fp:
            for line in node_maxsimilarnode_list:
                fp.write("\t".join(line)+"\n")
        print("Created & Saved Successfully!!\n")
        return node_maxsimilarnode_list

    def print_node_maxsimilarnode_list(self, node_maxsimilarnode_list):
        for lst in node_maxsimilarnode_list:
            print(lst)

    @staticmethod
    def main():
        taxonomy = Taxonomy()

        try:
            # read & filter data
            print("Reading data files...  ")
            taxonomy.topic_description_map = parser.read_data_files(DATA_DIR)
            if len(taxonomy.topic_description_map)<1:
                raise ValueError("Exception in reading data")
            print("Loaded Successfully!!\n")
        except:
            raise ValueError("Exception in reading data")

        # train gensim doc2vec model
        try:
            print("Training new doc2vec model...")
            taxonomy.gensimdoc2vec_obj.train_model(taxonomy.topic_description_map)
            print("Successfully Trained!!\n")
        except:
            raise ValueError("Exception in training gensim doc2vec model")

        # create distance_matrix
        try:
            print("Creating new distance_matrix.xls...")
            taxonomy.headers = parser.read_headers(MAIN_DATA_FILE)

            taxonomy.dist_matrix = dist_mat.create_distance_matrix(taxonomy.headers, taxonomy.gensimdoc2vec_obj, DISTANCE_MATRIX)
            print("Created & Saved Successfully!!\n")
        except:
            raise ValueError("Exception in create_distance_matrix")

        # create clusters
        try:
            condensed_matrix = cl.create_condensed_matrix(taxonomy.dist_matrix)
            cl2js.clusters_to_json(condensed_matrix, taxonomy.headers)
        except:
            raise ValueError("Exception in creating clusters")

        # render_json_on_browser
        cl2js.render_json_on_browser()

        ## create node_maxsimilarnode_list
        node_maxsimilarnode_list = taxonomy.create_node_maxsimilarnode_list(taxonomy.headers, taxonomy.dist_matrix)
        taxonomy.print_node_maxsimilarnode_list(node_maxsimilarnode_list)


if __name__ == '__main__':
    Taxonomy.main()

