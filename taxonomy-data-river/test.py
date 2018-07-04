'''
doc_labels_dict = {10: 'a', 2: 'z', 3: 'c'}
labels_list = []
doc_list = []
for key, value in doc_labels_dict.items():
    labels_list.append(key)
    doc_list.append(value)

print(labels_list, doc_list)
'''

##===========================================
'''
# doc2vec test
# Import libraries

from gensim.models import doc2vec
from collections import namedtuple

# Load data

doc1 = ["This is a sentence", "This is another sentence"]

# Transform data (you can add more data preprocessing steps)

docs = []
analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
for i, text in enumerate(doc1):
    words = text.lower().split()
    tags = [i]
    docs.append(analyzedDocument(words, tags))

# Train model (set min_count = 1, if you want the model to work with the provided example data set)

model = doc2vec.Doc2Vec(docs, size = 100, window = 300, min_count = 1, workers = 4)

# Get the vectors

print(model.docvecs[0])
print("\n\n")
print(model.docvecs[1])
'''
##===========================================

def test_model(topic,model):
    # print("Most similar to ", topic, "is ", model.most_similar(topic))
    # print(topic, " doesnt_match to ", model.doesnt_match(topic))
    # print("Vector1 for doc ", topic, "is", model[topic])
    # print("Vector2 for doc ", topic, "is", model.syn0)
    # print(model.similarity())
    # print(model.docvecs[0])
    print("\n\n")
    # print("Similarity: \n", model.wv.n_similarity("sentence", "another"))
    # print("Similarity: \n", model.wv.n_similarity("sentence", "sentence"))
    # print(model.docvecs[1])
    # print(model.wv.wmdistance("This is a sentence", "This is another sentence"))    # 0
    # print(model.wv.wmdistance("This is a sentence", "This is a sentence"))  # 0
    # print(model.wv.wmdistance("This is a sentence", "i love exercise"))     # inf
    # print(model.wv.wmdistance("This is a sentence", "sentence"))            # inf
    # print(model.wv.wmdistance("This is a sentence", "this sentence is another"))            # 0
    # print(model.wv.wmdistance("sentence", "this sentence is another"))  # inf
    # print(model.wv.wmdistance("sentence another", "this sentence is another"))  # 0

    print(model.docvecs.most_similar(0))
    # print(model.docvecs.most_similar(model.docvecs[0]))
    docvec1 = model.docvecs[0]
    docvec2 = model.docvecs[1]
    # print(model.wv.n_similarity(docvec1, docvec2))
    print(model.n_similarity(docvec1, docvec2))
    print(model.doc2vec.DocvecsArray)

# Train in epochs
# from gensim.models import doc2vec, Doc2Vec
# import random
# from collections import namedtuple
#
#
# alpha_val = 0.025        # Initial learning rate
# min_alpha_val = 1e-4     # Minimum for linear learning rate decay
# passes = 100              # Number of passes of one document during training
#
# alpha_delta = (alpha_val - min_alpha_val) / (passes - 1)
#
# doc1 = ["This is a sentence", "This is another sentence"]
#
# # Transform data (you can add more data preprocessing steps)
#
# docs = []
# analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
# for i, text in enumerate(doc1):
#     words = text.lower().split()
#     tags = [i]
#     docs.append(analyzedDocument(words, tags))
#
# model = doc2vec.Doc2Vec( size = 100 # Model initialization
#     , window = 300
#     , min_count = 1
#     , workers = 4)
#
# model.build_vocab(docs) # Building vocabulary
#
# for epoch in range(passes):
#     # Shuffling gets better results
#     random.shuffle(docs)
#     # Train
#     model.alpha, model.min_alpha = alpha_val, alpha_val
#     model.train(docs, total_examples = len(docs), epochs=model.iter)
#     # Logs
#     print('Completed pass %i at alpha %f' % (epoch + 1, alpha_val))
#     # Next run alpha
#     alpha_val -= alpha_delta
#
# model.save("model\\my_test_model.doc2vec")
# # model = Doc2Vec.load('model\\my_test_model.doc2vec')
#
# test_model("sentence", model)
# # test_model("another", model)
#


#=======================================================

with open("D:\\Projects\Taxonomy_DataRiver\\model\\investopedia_data_model\\similarity_matrix.xls") as fp:
    print(fp.readline())
    print(fp.readline())
    print(fp.readline())
