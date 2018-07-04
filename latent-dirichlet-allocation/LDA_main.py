from src import *
from src.TrainModel.LDA import LDA
from src.DataPreprocessing import parse_data as parser


def main():
    mylda = LDA()
    mylda.filtered_doc_list = parser.read_data_files(DATA_DIR)
    # Cleaning and Preprocessing
    mylda.createModel()
    mylda.printModel()
    mylda.runLDAModel()


###############################################################
if __name__ == '__main__':
    main()
