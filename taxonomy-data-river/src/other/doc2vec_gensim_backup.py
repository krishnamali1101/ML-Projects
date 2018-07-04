import gensim
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from collections import namedtuple


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

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            # yield LabeledSentence(words=doc.split(), labels=[self.labels_list[idx]])
            analyzedDocument = namedtuple('TaggedDocument', 'words tags')
            # yield TaggedDocument(analyzedDocument(doc.split(), [self.labels_list[idx]]))
            self.docs.append(analyzedDocument(doc.split(), [self.labels_list[idx]]))



class GensimDoc2Vec(object):
    def __init__(self, doc_labels_dict):
        self.sentences = LabeledLineSentence(doc_labels_dict)
        self.total_examples = len(doc_labels_dict)
        self.model = None

    def train_model(self):
        """
            # The input to Doc2Vec is an iterator of LabeledSentence objects.Each such object represents a single sentence,
              and consists of two simple lists: a list of words and a list of labels.
            # The algorithm then runs through the sentences iterator twice: once to build the vocab,
              and once to train the model on the input data, learning a vector representation
              for each word and for each label in the dataset.
        """
        # create model blueprint
        self.model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11, alpha=0.025,
                                      min_alpha=0.025)  # use fixed learning rate
        # build vocab
        self.model.build_vocab(self.sentences)

        # train model
        for epoch in range(10):
            self.model.train(self.sentences, total_examples = self.total_examples)
            self.model.alpha -= 0.002  # decrease the learning rate
            self.model.min_alpha = self.model.alpha  # fix the learning rate, no deca
            self.model.train(self.sentences)

        self.save_model()

    def save_model(self):
        self.model.save("model\\my_model.doc2vec")

    def load_model(self):
        try:
            self.model = Doc2Vec.load('\\model\\my_model.doc2vec')
        except Exception:
            print("Error in loading model")

    # topic: documentFileNameInYourDataFolder
    def test_model(self, topic):
        print("Most similar to ", topic, "is ", self.model.most_similar(topic))
        print(topic, " doesnt_match to ", self.model.doesnt_match(topic))
        print("Vector1 for doc ", topic, "is", self.model[topic])
        print("Vector2 for doc ", topic, "is", self.model.syn0)
        print(self.model.similarity())


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