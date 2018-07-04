# import init
from src import *


# named tuple of doc-tag
def create_similarity_matrix(headers, doc2vec_model, filename=DISTANCE_MATRIX):
    sim_mat = []
    rowno =1
    total_rows = len(headers)
    for rdoc in headers:
        if not (rowno % 100):
            print("Processing RowNo ", rowno, " out-of ", total_rows)
        sim = []
        for cdoc in headers:
            sim.append(doc2vec_model.doc_similarity(rdoc, cdoc))
        rowno += 1

        sim_mat.append(sim)
    # print("\ndistance_matrix created successfully!!")
    # save it & return
    save_distance_matrix(headers, sim_mat, filename)
    return sim_mat


# named tuple of doc-tag
# distance = 100-distance
def create_distance_matrix(headers, doc2vec_model, filename=DISTANCE_MATRIX):
    distance_mat = []
    headers_count = len(headers)
    # create hald matrix
    # copy that values to second half
    for row_no in range(headers_count):
        distance = []
        if not (row_no % 100):
            print("Processing RowNo ", row_no, " out-of ", headers_count)
        for col_no in range(headers_count):
            if row_no == col_no:
                distance.append(0.0)
            elif row_no>col_no:
                distance.append(distance_mat[col_no][row_no])
            else:
                # distance = 100-distance
                distance.append(doc2vec_model.doc_distance(headers[row_no], headers[col_no]))

        distance_mat.append(distance)
    # print("\ndistance_matrix created successfully!!")
    # save it & return
    save_distance_matrix(headers, distance_mat, filename)
    return distance_mat


def print_distance_matrix(headers, sim_mat):
    print("Headers: \n", headers)
    for row in sim_mat:
        for col in row:
            print(col, end=' ')
    print("\n\n")


def save_distance_matrix(headers, sim_mat, filename=DISTANCE_MATRIX):
    # save headers
    print("Saving Headers...")
    with open(TAGS_FILE, 'w') as fp:
        for header in headers:
            fp.write(header+"\n")

    # save distance
    print("Saving sim_mat...")
    with open(filename, 'w') as fp:
        rowno = 1
        total_rows = len(headers)
        for row in sim_mat:
            if not (rowno%100):
                print("Processing RowNo ", rowno, " out-of ", total_rows)
            for cell in row:
                fp.write(str(cell) + "\t")
            fp.write("\n")
            rowno += 1
    # xlsparser.write_xlsx_xlwt(filename, sim_mat)


def load_distance_matrix(filename=DISTANCE_MATRIX):
    try:
        # load headers
        # headers = []
        with open(TAGS_FILE) as fp:
            content = fp.readlines()
            headers = [x.strip() for x in content]  # remove "\n' at the end

        # load distance
        sim_mat = []
        with open(filename, 'r') as fp:
            rowno =1
            total_rows = len(headers)
            for line in fp.readlines():
                if not (rowno % 100):
                    print("Processing RowNo ", rowno, " out-of ", total_rows)
                row = []
                for word in line.strip().split("\t"):
                    row.append(float(word))
                sim_mat.append(row)
                rowno += 1

        # sim_mat = xlsparser.read_xlsx_xlrd(filename)
        return headers, sim_mat
    except:
        print("\nError while loading distance_matrix")
        raise


# try
# mat = [[1,2,3], [4,5,6], [7,8,9]]
# headers = ["A", "B", "C"]
# save_distance_matrix(headers,mat)
# headers, mat = load_distance_matrix()
# print(headers,mat)