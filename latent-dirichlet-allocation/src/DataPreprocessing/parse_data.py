from src import *
from src.DataPreprocessing.TextFilter import TextFilter


def read_data_files(dir_path):
    fltr = TextFilter()
    fltr.remove_filter(fltr.stem_text)
    filtered_doc_list = []
    if not os.path.exists(dir_path):
        print(dir_path+ "doesn't exist")
        return filtered_doc_list

    for root, dirs, docs in os.walk(dir_path):
        # print root, dirs, files
        for doc in docs:
            if doc.endswith('.tsv') or doc.endswith('.csv') or doc.endswith('.txt') or doc.endswith('.xls'):
                print("\nProcessing: ", os.path.join(root, doc))
                doc = os.path.join(root, doc)

                # filter data and append to filtered_doc_list
                with open(doc, 'r') as fp:
                    filtered_doc_list.append(fltr.preprocess_string(fp.read()))

    return filtered_doc_list
# -------------------------------------------------------------

#
# # read headers/ topics
# def read_headers(filename):
#     headers = []
#     values = xlparser.read_xlsx_xlrd(filename)
#     # skip first row (its heading)
#     for row in values[1:]:
#         # filtering short keys(ie len<=1)
#         if len(row[0]) > 1:
#             headers.append(row[0])
#
#     return headers