import gensim
import logging
import sys


class SimilarityModel(object):
    def __init__(self):
        self.w2v_model = None
        self.model_name = "GoogleNews-vectors-negative300.bin"

    # load GoogleNews model
    def load_google_w2v_model(self):
        model_path = ".//model//" + self.model_name

        # Logging code
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        # Load Google's pre-trained Word2Vec model.
        try:
            self.w2v_model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
        except Exception as e:
            print(e)
            print("load word2vec model failed, make sure model path <<", model_path, ">> is correct")
            sys.exit()

    def similarity(self, w1, w2):
        if not self.w2v_model:
            print("No similarity model loaded, exiting process...")
            sys.exit()

        try:
            if self.model_name is "GoogleNews-vectors-negative300.bin":
                sim = self.w2v_model.wv.similarity(w1, w2)
                return sim*100
        except Exception as e:
            print(e)
            # print("Word not found in the vocabulary")
            return 0

    def train(self, sentences):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        # sentences = word2vec.Text8Corpus('text8')
        model = gensim.models.Word2Vec(sentences, size=200)
        model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
        model.most_similar(positive=['woman', 'king'], negative=['man'], topn=2)
        model.most_similar(['man'])
        model.save('text8.model')
        model.save_word2vec_format('text.model.bin', binary=True)
        model1 = gensim.models.KeyedVectors.load_word2vec_format('text.model.bin', binary=True)
        model1.most_similar(['girl', 'father'], ['boy'], topn=3)

    def similarity_test(self):
        while True:
            w1 = input(">>> ")
            w2 = input(">>> ")
            try:
                sim = self.similarity(w1, w2)
                print(sim, "%")
            except Exception as e:
                print(e)

# w2v = Word2Vec()
# w2v.similarity_test()