import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

# go to project dir (cwd is src)
head, tail = os.path.split(PROJECT_DIR)
PROJECT_DIR = head


DATA_DIR = PROJECT_DIR+"\\data\\training_data"
MODEL_DIR = PROJECT_DIR+"\\model"

MAIN_DATA_FILE = DATA_DIR+"\\taxonomy_data.xls"
GENSIM_DOC2VEC_MODEL = MODEL_DIR+"\\gensim_doc2vec.doc2vec"
DISTANCE_MATRIX = MODEL_DIR+"\\distance_matrix.xls"
CLUSTER_MATRIX = MODEL_DIR+"\\cluster_matrix.csv"
TAGS_FILE = MODEL_DIR+"\\tags.xls"
OUT_JSON_FILE = MODEL_DIR+"\\clusters.json"