import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

DATA_DIR = ROOT_DIR+"\\data"
MODEL_DIR = ROOT_DIR+"\\model"

MAIN_DATA_FILE = DATA_DIR+"\\main.xls"
GENSIM_DOC2VEC_MODEL = MODEL_DIR+"\\gensim_doc2vec.doc2vec"
DISTANCE_MATRIX = MODEL_DIR+"\\distance_matrix.xls"
CLUSTER_MATRIX = MODEL_DIR+"cluster_matrix.xls"
NODE_MAXSIMILARNODE_LIST = MODEL_DIR+"\\node_maxsimilarnode_list.xls"
TAGS = MODEL_DIR+"\\tags.xls"
OUT_JSON_FILE = MODEL_DIR+"\\clusters.json"