#  -*- coding: utf-8 -*-

'''
#as3:/usr/local/lib/python2.7/site-packages# cat sitecustomize.py
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
'''


import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from numpy import zeros
from scipy.linalg import svd
from math import log  #  needed for TFIDF
from numpy import asarray, sum
import pickle   # needed to save & load model(Pickle is the standard way of serializing objects in Python)
import string
import sys
# from enum import Enum
import collections
import os
# from unidecode import unidecode

#  list of categorys (ie. science & Food), each category contains multiple documents
'''
#  cat1: Referencial Confidentiality Provision
#  cat2: Assignment
categories = [
    """Except as otherwise agreed in writing or as required by law, Pinnacle will exercise the highest degree of due diligence and care with respect to keeping confidential all Client information. However, by signing this Agreement, Client authorizes Pinnacle to give a copy of this Agreement to any broker, dealer or other party to a transaction for the account, or Custodian as evidence of Pinnacle’s limited power of attorney and authority to act on Client’s behalf. In addition, Client grants Advisor authority to discuss, disclose and provide confidential Client information to outside attorneys, auditors, consultants and any other professional advisors retained by Pinnacle to assist in the management of this Agreement and Client’s account. It is Pinnacle’s policy to make available Client’s account information to Client’s spouse. A Client may restrict such availability to his/her spouse by notifying Pinnacle in writing.
    The Advisor will collect such personal information from its clients as it deems necessary or advisable in its discretion in order to (i) discharge the Advisor’s obligations under anti-money laundering regulations, (ii) perform a suitability assessment of the Client in compliance with applicable securities laws, and (iii) perform its obligations pursuant to this Agreement. All personal information received by the Advisor will be treated in accordance with the Advisor’s Privacy Policy, reproduced as Schedule D to this Agreement.
    Each party agrees that all non-public confidential information concerning the other party which may become available to such party in connection with services, transactions or relationships contemplated in this Agreement shall at all times be treated in strictest confidence and shall not be disclosed to third persons except as (a) may be required by law or regulatory authority, including but not limited to any subpoena, administrative, regulatory or judicial demand or court order, (b) as otherwise set forth in this Agreement, or (c) upon the prior written approval of the other party to this Agreement. Client authorizes Manager (i) to include Client’s name in a representative or sample client list prepared by Manager, provided Manager shall not disclose Client contact information or any information about Client’s holdings, and (ii) to use Manager’s investment experience with respect to the Account, or the Account’s performance, in composite performance presentations, marketing materials, attribution analyses, statistical compilations, or other similar compilations or presentations, provided such use does not disclose Client’s identity except to the extent permitted by Client.
    The Investment Manager shall retain as strictly confidential all information about SURS, this Agreement, the Fund, and financial transactions regarding the Fund received in performing services contemplated by this Agreement (collectively, “Confidential Information”); provided, however, that such restrictions shall not apply to any disclosure required by regulatory authorities, applicable law or the rules of any securities exchange which may be applicable. The Investment Manager shall inform all of its agents of the confidentiality provisions of this Agreement, and the Investment Manager shall be liable for and shall indemnify SURS for any breaches of such confidentiality provisions of this Agreement by any such agents in accordance with and subject to the limitations in Section 17.1.
    """,

    """This Agreement may not be assigned (within the meaning of the Investment Advisers Act of 1940) by either Client or Pinnacle without the prior consent of the other party. Client acknowledges and agrees that transactions that do not result in a change of actual control or management of Pinnacle shall not be considered an assignment. Should there be a change in control of Pinnacle resulting in an assignment of this Agreement (as that term is defined under the Advisers Act), the successor adviser will notify Client and will continue to provide the services previously provided to the Client by Pinnacle. If the Client continues to accept such services provided by the Successor without written objection during the 60 day period subsequent to receipt of the written notice, the Successor will assume that Client has consented to the assignment and the Successor will become the adviser to Client under the terms and conditions of this Agreement.
    This Agreement shall not be assignable by the Client without the express written consent of the Advisor and shall be assignable by the Advisor with 30 days notice to the Client.
    This Agreement may not be assigned (within the meaning of the Investment Advisers Act of 1940, as amended), in whole or in part, by Manager without the prior written consent of Client. Subject to the preceding sentence, Manager may delegate all or part of its duties under this Agreement to any affiliate.
    No assignment of this Agreement shall be made by the Investment Manager without the written consent of SURS."""
]



categories = [
    """
    Science (from Latin scientia, meaning "knowledge")[1][2]:58 is a systematic enterprise that builds and organizes knowledge in the form of testable explanations and predictions about the universe.[a]
    Contemporary science is typically subdivided into the natural sciences, which study the material universe; the social sciences, which study people and societies; and the formal sciences, which study logic and mathematics.
    The formal sciences are often excluded as they do not depend on empirical observations.[3] Disciplines which use science, like engineering and medicine, may also be considered to be applied sciences.
    """,

    """
    Food is any substance[1] consumed to provide nutritional support for an organism.
    Food is usually of plant or animal origin, and contains essential nutrients, such as carbohydrates, fats, proteins, vitamins, or minerals.
    The substance is ingested by an organism and assimilated by the organism's cells to provide energy, maintain life, or stimulate growth.
    """,

    """
    A game is a structured form of play, usually undertaken for enjoyment and sometimes used as an educational tool. Games are distinct from work, which is usually carried out for remuneration, and from art, 
    which is more often an expression of aesthetic or ideological elements. However, the distinction is not clear-cut, and many games are also considered to be work (such as professional players of spectator sports or games)
     or art (such as jigsaw puzzles or games involving an artistic layout such as Mahjong. games gaming game
    """
]


class categoriesEnum(object):
    SCIENCE = 0
    FOOD = 1
    GAME = 2
'''

categories = []
trainingDataPath = ".\\trainingData"

#  catEnum = [categoriesEnum.SCIENCE, categoriesEnum.FOOD]

#categoriesList = ["SCIENCE", "FOOD", "GAME"]
categoriesList = []
#  categoriesList = ["ReferencialConfidentialityProvision", "Assignment"]

#  set of stopwords
setofstopwords = {'a','and', 'for', 'in', 'of', 'the', 'to', 'not', 'or', 'as', 'by'}
unionsetofstopwords = set(stopwords.words('english')).union(setofstopwords)

#  nltkStopWords = set(stopwords.words('english'))
#  unionsetofstopwords = setofstopwords.union(nltkStopWords)

# string of ignore chars
ignorechars = '''?,":'’!.)([]{}�'''


##########################################################################
class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {} # key:words, value:list of doc number
        self.category_count = 0
    #  -------------------------------------------------------------


    #  filterWord(Remove ignorechars, steaming, lemmatize)
    def filterWord(self,word):
        #TODO ignore char not working
        # Remove ignorechars
        trantab = string.maketrans("", "")
        word = word.lower().translate(trantab, self.ignorechars)
        # space = ""
        # trantab = string.maketrans(self.ignorechars, space.rjust(self.ignorechars, " "))
        # word = word.replace()


        # steaming
        # ps = PorterStemmer()
        # word = ps.stem(word)

        # lemmatize
        # TODO use pos tag
        lmtzr = WordNetLemmatizer()
        word = lmtzr.lemmatize(word)

        return word
        #  -------------------------------------------------------------

    # TODO: filterLine
    def filterLine(self, line):
        # replace ignore chars with space
        for ic in self.ignorechars:
            line = line.replace(ic, " ")

        #remove stopwords
        # http://www.geeksforgeeks.org/removing-stop-words-nltk-python/
        # stopwords.words('english')

        # postagging
        # return nouns & verbs


        '''
        replace ignore char with space
        remove stopwords
        split by space
        traverse words:
            lama word
        '''
        pass
    #  -------------------------------------------------------------


    #  filter documents & create wdict
    def parse(self, doc):
        # TODO: use nltk tokenizer
        # TODO replace nltk lib with spaCy lib
        words = doc.split()
        for w in words:
            #print w
            #TODO filterWord taking lot of time, filter line by line or doc by dod
            try:
                w = self.filterWord(w)
            except:
                continue

            if (w in unionsetofstopwords) or (w in string.whitespace) or (len(w) < 2):
                continue

            if w in self.wdict:
                self.wdict[w].append(self.category_count)
            else:
                self.wdict[w] = [self.category_count]
        self.category_count += 1
        print(self.wdict, self.category_count)
    #  -------------------------------------------------------------


    # parse input query (remove stopwords, ignorechars & create word_freq_dict)
    def parseQuery(self, query):
        words = query.split()
        word_freq_dict  = {}
        for w in words:
            w = self.filterWord(w)
            if (w in unionsetofstopwords) or (w in string.whitespace):
                continue

            if w not in word_freq_dict:
                word_freq_dict[w] = 1
            else:
                word_freq_dict[w] += 1


        return word_freq_dict
    #  -------------------------------------------------------------

    def readTrainingData(self):
        if not os.path.exists(trainingDataPath):
            return False

        for root, dirs, docs in os.walk(trainingDataPath):
            # print root, dirs, files
            docList = []
            for doc in docs:
                if doc.endswith('.txt'):
                    # print os.path.join(root, file)
                    doc = os.path.join(root, doc)

                    #with io.open(doc, "r", encoding="utf-8") as my_file:
                        #docList.append(my_file.read())

                    # TODO read & process line by line and process
                    with open(doc, 'r') as doc:
                        docList.append(doc.read())
                        # docList.append(unidecode(doc.read()))
                        #docList.append(unicode(doc.read(), encoding = "utf-8"))
                        #docList.append(doc.read().encode('ascii', errors='ignore'))

            if not len(docs) == 0:
                _, folder = os.path.split(root)
                categoriesList.append(folder)
                categories.append(''.join(docList))
        return True



    #  rows -> keywords (occur more than twice), cols -> documentID
    #  building count matrix(Category/Document-Term Matrix)
    def build(self):
        # # TODO parse all documents
        if not self.readTrainingData():
            print("Training Directory not found")
            exit()

        for docs in categories:
            self.parse(docs)

        # print("\n\n",self.wdict)

        #  fatch all words(keys), repeted atleast twise(combind all doc)
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        # print "Model vocabulary: ",self.keys

        # TODO remove keys from member variable

        #  createing count matrix
        self.countMat = zeros([len(self.keys), self.category_count])
        self.wordsDict = {}     # wordsDict(hash map) to store all words and its enum value(row number) so that retrival will be in O(1)

        for rno, word in enumerate(self.keys):   # [0:w1; 1:w2; ...]
            self.wordsDict[word] = rno
            for d in self.wdict[word]:
                self.countMat[rno, d] += 1
    #  -------------------------------------------------------------


    #  SVD
    def calc_SVD(self):
        # Using scipy
        #  self.U, self.S, self.Vt = svd(self.countMat)

        # using numpy
        self.U, Stemp, self.Vt = np.linalg.svd(self.countMat, full_matrices=False)

        # build proper singular matrix from Stemp list
        self.K = len(Stemp)
        self.S = [[0 for x in range(self.K)] for y in range(self.K)]
        for i in range(self.K):
            self.S[i][i] = Stemp[i]

    '''
        Here is the complete 3 dimensional Singular Value Decomposition of our matrix.
        U matrix:  It gives us the coordinates of each word on our “concept” space,
                   Each word has 3 numbers associated with it, one for each dimension.
                   The first number tends to correspond to the number of times that word appears in all titles and is not as informative as the second and third dimensions.
        Vt matrix: It gives us the coordinates of each document in our “concept” space,
                    Each title also has 3 numbers associated with it, one for each dimension.
                    Once again, the first dimension is not very interesting because it tends to correspond to the number of words in the title.
        S matrix:  singular values gives us a clue as to how many dimensions or “concepts” we need to include.
    '''
    #  -------------------------------------------------------------


    #  apply TFIDF
    def TFIDF(self):
        WordsPerDoc = sum(self.countMat, axis=0)
        DocsPerWord = sum(asarray(self.countMat > 0, 'i'), axis=1)
        # rows, cols = self.countMat.shapeo
        rows, cols = self.countMat.shape
        for i in range(rows):
            for j in range(cols):
                self.countMat[i, j] = (self.countMat[i, j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

    '''
        TFIDF(i,j) = ( N(i,j) / N(*,j) ) * log( D / D(i) ) where

        N(i,j) = the number of times word i appears in document j (the original cell count).
        N(*,j) = the number of total words in document j (just add the counts in column j).
        D = the number of documents (the number of columns).
        D(i) = the number of documents in which word i appears (the number of non-zero columns in row i).
    '''
    #  -------------------------------------------------------------


    # Create Model from existing categories & documents
    def createModel(self):
        self.build()
        self.matPrint("Count", self.countMat)
        self.TFIDF()
        # self.matPrint("CountMat_TFIDF", self.countMat)
        self.calc_SVD()

        #  TODO: Ignore first row and first column
        # self.matPrint("CountMat", self.countMat)
        # self.matPrint("U", self.U)
        # self.matPrint("S", self.S)
        # self.matPrint("Vt", self.Vt)

        self.US = np.matmul(self.U, self.S)                 # in US(Term-concept) matrics each row represents a word
        self.SVt = np.matmul(self.S, self.Vt)               # in SVt(concept-Category) matrics each column represents a category
    #  -------------------------------------------------------------


    # calculate Centroid of all word vectors in vectorList
    def calculateCentroid(self, vectorList):
        if len(vectorList) == 0:
            return 0
        # r,c = np.shape(vectorList[0])
        r = len(vectorList[0])
        c=1
        sumMat = zeros(shape=(c,r))
        # centroid = []
        for mat in vectorList:
            sumMat +=mat

        return sumMat[0]/len(vectorList)

    '''
        centroid = (V1+V2+....+Vn) / n;
    '''
    #  -------------------------------------------------------------


    #  Takes 2 vectors U, V and returns the cosine similarity according to the definition of the dot product
    def cosignDistance(self, U, V):
        dot_product = np.dot(U, V)
        norm_u = np.linalg.norm(U)
        norm_v = np.linalg.norm(V)
        if norm_u and norm_v:
            ret = dot_product / (norm_u * norm_v)
            return ret
        else:
            return 2

    '''
    cosign distance is between [0,1]
    https://en.wikipedia.org/wiki/Cosine_similarity
                    U·V
    cos(thita) =   -----
                   |U||V|
    '''
    #  -------------------------------------------------------------


    #  fatch word vectors for all words in input query
    def fatchTermVectors(self, queryWordList):
        wordVectorList = []
        for word in queryWordList:
            if word in self.wordsDict:
                rowNo = self.wordsDict[word]
                # A = self.US[rowNo]
                # AT = np.transpose(self.US[rowNo])
                row = list(self.US[rowNo])
                wordVectorList.append(row)

        return wordVectorList
    #  -------------------------------------------------------------


    # fatch Resultset for input query
    def fatchResultset(self, query):
        word_freq_dict = self.parseQuery(query)
        queryWordList = list(word_freq_dict.keys())

        print("Model vocabulary: ", self.keys)
        print("Query vocabulary: ", queryWordList)
        print("")

        # TODO: use frequency of words to increase word wattage in document search
        vectorList = self.fatchTermVectors(queryWordList)
        centroid = self.calculateCentroid(vectorList)

        resultSetDect = {}  # distance-vector map
        # resultSetDect = collections.OrderedDict()
        tempResultSetDect = {}
        #  calculate cosign distance of centroid from all available category vectors
        row, col = np.shape(self.SVt)
        for c in range(col):
            category = self.SVt[:,c]
            distance = self.cosignDistance(centroid, category)
            tempResultSetDect[round(distance,4)] = categoriesList[c]

        totalDistance = sum(tempResultSetDect.keys())
        for i in tempResultSetDect:
            percentage = round( ( (i )*100)/ totalDistance, 1)
            # if percentage > 36:
            resultSetDect[percentage] = tempResultSetDect[i]

        return resultSetDect

        # TODO: pass empty list if no related doc found

        '''
            # parse input query(tokenize string, remove stopwords, ignorecase, remove ignore char)
            # fatch related term vectors for our query
            # calculate centroid of all fatched term vectors
            # calculate cosign distance of centroid from all document vectors
            # return sorted(descending) list of related docs
            # if no related document found(all cosign distance are less then perticular amount then return empty list.
        '''
    #  -------------------------------------------------------------


    # print any matrix
    def matPrint(self, matrixName, matrix):
        # print(matrixName, "Matrix \n", matrix,"\n")
        print(matrixName+" Matrix ")
        print(matrix)
        print("")
    #  -------------------------------------------------------------


    # print all model matrix
    def printModel(self):
        # self.matPrint("Count", self.countMat)
        self.matPrint("TFIDF_Count", self.countMat)
        self.matPrint("Term(U)", self.U)
        self.matPrint("Singular(S)", self.S)
        self.matPrint("Category(Vt)", self.Vt)
        self.matPrint("Words vectors(US)", self.US)
        self.matPrint("Category vectors(SVt)", self.SVt)
    #  -------------------------------------------------------------


    # if model exists, load the model from disk
    def loadModel(self):
        # TODO loadModel
        '''
        if ModelExist:
            load it
            return True

        loaded_model = pickle.load(open(filename, 'rb'))
        result = loaded_model.score(X_test, Y_test)
        '''
        return False
    #  -------------------------------------------------------------


    def saveModel(self):
        #  TODO saveModel
        '''
        # https: // machinelearningmastery.com / save - load - machine - learning - models - python - scikit - learn /
        pickle.dump(mylsa<model>, open(<filename>, 'wb'))
        '''
        pass
    #  -------------------------------------------------------------


    @staticmethod
    def main():
        #  Create model
        # TODO use intent and entity only to create model and also in query rply
        mylsa = LSA(stopwords, ignorechars)

        # if pre trained model exist, load that model and use it directly else create new model and save it
        if not mylsa.loadModel():
            mylsa.createModel()
            mylsa.saveModel()

        mylsa.printModel()

        #  Respond to query
        # query = input("Enter query: ")
        query = input("Enter query(or quit): ")


        while query.lower() != "quit":
            print("=====================================================================================================")
            resultset = mylsa.fatchResultset(query)  #  ordered(descending) list of all related docs to input query

            # print "============================="

            if len(resultset) > 0:
                print("Related Categories: ")        # TODO: (ordered, most related to least): "
                # for i in resultset:
                for i, cat in sorted(resultset.items(), reverse=True):
                    print(i, "%   ", cat)
            else:
                print("No related Categories found")

            # print "============================="
            print("=====================================================================================================")
            query = input("Enter query(or quit): ")


##########################################################################
if __name__ == '__main__':
    LSA.main()
