import gensim
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec, doc2vec
from gensim.models.doc2vec import DocvecsArray
from collections import namedtuple
import random

from src import *

class LabeledLineSentence(object):
    def __init__(self, doc_labels_dict):
        # create labels & docs lists out of doc_labels_dict
        # assuming data is already preprocessed/filtered
        self.labels_list = []
        self.doc_list = []
        self.docs = []  # named tuple of doc-tag
        for key, value in doc_labels_dict.items():
            self.labels_list.append(key)
            self.doc_list.append(value)
            analyzedDocument = namedtuple('TaggedDocument', 'words tags')
            # yield TaggedDocument(analyzedDocument(doc.split(), [self.labels_list[idx]]))
            self.docs.append(analyzedDocument(value.split(), [key]))

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            # yield LabeledSentence(words=doc.split(), labels=[self.labels_list[idx]])
            analyzedDocument = namedtuple('TaggedDocument', 'words tags')
            # yield TaggedDocument(analyzedDocument(doc.split(), [self.labels_list[idx]]))
            self.docs.append(analyzedDocument(doc.split(), [self.labels_list[idx]]))


class GensimDoc2Vec(object):
    def __init__(self):
        self.model = None
        self.docs = []  # named tuple of doc-tag

    def create_document(self, doc_labels_dict):
        for key, value in doc_labels_dict.items():
            analyzedDocument = namedtuple('TaggedDocument', 'words tags')
            # yield TaggedDocument(analyzedDocument(doc.split(), [self.labels_list[idx]]))
            doc = ' '.join(value)
            self.docs.append(analyzedDocument(doc, [key]))

        # for doc in self.docs:
        #    print(doc, "\n\n")

    def train_model(self, doc_labels_dict):
        self.create_document(doc_labels_dict)
        """
            # The input to Doc2Vec is an iterator of LabeledSentence objects.Each such object represents a single sentence,
              and consists of two simple lists: a list of words and a list of labels.
            # The algorithm then runs through the sentences iterator twice: once to build the vocab,
              and once to train the model on the input data, learning a vector representation
              for each word and for each label in the dataset.
        """
        alpha_val = 0.025  # Initial learning rate
        min_alpha_val = 1e-4  # Minimum for linear learning rate decay
        passes = 100  # Number of passes of one document during training

        alpha_delta = (alpha_val - min_alpha_val) / (passes - 1)

        # Model initialization
        self.model = doc2vec.Doc2Vec(size=100, window=30, min_count=1, workers=4)
        # Building vocabulary
        self.model.build_vocab(self.docs)

        for epoch in range(passes):
            # Shuffling gets better results
            random.shuffle(self.docs)
            # Train
            self.model.alpha, self.model.min_alpha = alpha_val, alpha_val
            self.model.train(self.docs, total_examples=len(self.docs), epochs=self.model.iter)
            # Logs
            # print('Completed pass %i at alpha %f' % (epoch + 1, alpha_val))
            # Next run alpha
            alpha_val -= alpha_delta

        # Doc2Vec.delete_temporary_training_data()
        # self.save_model()

    # TODO
    def retrain_model(self, doc_labels_dict):
        pass

    def save_model(self, path=BOT_OPERATION_MODEL):
        self.model.save(path)

    def load_model(self, path=BOT_OPERATION_MODEL):
        try:
            # TODO self.create_document(doc_labels_dict)
            self.model = Doc2Vec.load(path)
        except Exception:
            print("Error in loading model!!")
            raise

    def doc_similarity(self, tag1, tag2):
        if len(tag1) < 2 or len(tag2) < 2:
            return 0
        # print(self.model.docvecs.similarity(tag1, tag2)*100, tag1, tag2)
        # print("Similarity ", tag2, tag1, self.model.docvecs.similarity(tag2, tag1))
        return self.model.docvecs.similarity(tag1, tag2)*100    # return similarity in percentage

    # return similarity in percentage
    def doc_distance(self, tag1, tag2):
        return (1 - self.model.docvecs.similarity(tag1, tag2))*100

    # topic: documentFileNameInYourDataFolder
    def test_model(self, topic):
        # print("Most similar to ", topic, "is ", self.model.most_similar(topic))
        # print(topic, " doesnt_match to ", self.model.doesnt_match(topic))
        # print("Vector1 for doc ", topic, "is", self.model[topic])
        # print("Vector2 for doc ", topic, "is", self.model.syn0)
        # print(self.model.similarity())

        # print(self.model.docvecs[0])
        # print(self.model.docvecs.most_similar(0))
        # print("\n\n")
        # print(self.model.docvecs[20])
        # print(self.model.docvecs.most_similar(20))
        # print("\n\n")
        # print(self.model.docvecs[1])
        # print(self.model.docvecs.most_similar(1))
        # print("\n\n")
        # print(self.model.docvecs[2])
        # print(self.model.docvecs.most_similar(2))
        # print("\n\n")
        # print(self.model.docvecs[3])
        # print(self.model.docvecs.most_similar(3))
        # print("\n\n")
        # print(self.model.docvecs[4])
        # print(self.model.docvecs.most_similar(4))

        # print(self.model.docvecs.most_similar(0))
        # print(self.model.docvecs.n_similarity(self.model.docvecs[4], self.model.docvecs[1]))
        # print(self.model.docvecs.similarity(self.model.docvecs[4], self.model.docvecs[1]))
        # print("\n Food, Game", self.model.docvecs.similarity("Food", "Game"))

        # self.doc_similarity("Food", "Game")

        # print(self.model.docvecs.n_similarity(1, 2))
        # print(self.model.docvecs.similarity("food", "game"))
        pass



'''
class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences
'''