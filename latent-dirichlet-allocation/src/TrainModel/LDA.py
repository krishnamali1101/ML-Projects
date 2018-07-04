import gensim
from gensim import corpora


class LDA(object):
    def __init__(self):
        self.filtered_doc_list = []
    # -------------------------------------------------------------

    def createModel(self):
        # Preparing Document-Term Matrix
        # Creating the term dictionary of our courpus, where every unique term is assigned an index.
        self.dictionary = corpora.Dictionary(self.filtered_doc_list)
        # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
        self.doc_term_matrix = [self.dictionary.doc2bow(doc) for doc in self.filtered_doc_list]

        # Running LDA Model
        # Creating the object for LDA model using gensim library
        Lda = gensim.models.ldamodel.LdaModel

        # Running and Trainign LDA model on the document term matrix.
        self.ldamodel = Lda(self.doc_term_matrix, num_topics=3, id2word= self.dictionary, passes=50)
    # -------------------------------------------------------------

    def printModel(self):
        print("Cleaned Document: ")
        for doc in self.filtered_doc_list:
            print(doc)
        print("")

        print("Dictionary: ")
        print(self.dictionary.values())
        print("")

        print("Doc_term_Matrix: ")
        for row in self.doc_term_matrix:
            print(row)
        print("")
        print("LDA Model: ", self.ldamodel)
    # -------------------------------------------------------------

    def runLDAModel(self):
        #print self.ldamodel.print_topics(num_topics=3, num_words=3)
        #top_topics =  self.ldamodel.top_topics(num_words=3)
        #for topic in top_topics:
        #    print topic

        print("")
        print("Related Topics:")
        for i in range(0, self.ldamodel.num_topics):
            print(self.ldamodel.print_topic(i, 10))
    # -------------------------------------------------------------
