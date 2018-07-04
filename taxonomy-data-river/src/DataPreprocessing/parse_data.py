from src import *
from src.DataPreprocessing import xls_csv_parser as xlparser

from src.DataPreprocessing.TextFilter import TextFilter


def read_data_files(dir_path):
    fltr = TextFilter()
    topic_description_map = {}
    if not os.path.exists(dir_path):
        print(dir_path+ "doesn't exist")
        return topic_description_map

    for root, dirs, docs in os.walk(dir_path):
        # print root, dirs, files
        for doc in docs:
            if doc.endswith('.tsv') or doc.endswith('.csv') or doc.endswith('.txt') or doc.endswith('.xls'):
                print("\nProcessing: ", os.path.join(root, doc))
                doc = os.path.join(root, doc)
                temp_dict = xlparser.csv2dict(doc)

                # filter data and append to topic_description_map
                for key in temp_dict:
                    topic = ' '.join(fltr.preprocess_string(key))
                    description = ' '.join(fltr.preprocess_string(temp_dict[key]))
                    topic_description_map[topic] = description

    # save data to xls file
    xlparser.dict2csv(topic_description_map, MAIN_DATA_FILE)
    print("\nTotal missed Lines in all files: ", xlparser.total_missed_lines, "/", xlparser.total_lines)
    return topic_description_map


def read_main_csv(filename):
    topic_description_map = {}
    values = xlparser.read_xlsx_xlrd(filename)
    # skip first row (its heading)
    for row in values[1:]:
        # filtering short keys(ie len<=1)
        if len(row[0]) > 1:
            topic_description_map[row[0]] = row[1]

    return topic_description_map


# read headers/ topics
def read_headers(filename):
    headers = []
    values = xlparser.read_xlsx_xlrd(filename)
    # skip first row (its heading)
    for row in values[1:]:
        # filtering short keys(ie len<=1)
        if len(row[0]) > 1:
            headers.append(row[0])

    return headers