import os
import re

import nltk
from nltk.corpus import wordnet

from src.DataPreprocessing.TextFilter import TextFilter
from src.TrainNLPEngine.BotOperations import BotOperations
from src.TrainNLPEngine.doc2vec_gensim import GensimDoc2Vec

from src import *


class NLPEngine(object):
    def __init__(self):
        # threshold values
        self.similarity_score = 60.0  # in %
        self.confidence_similarity_score = 90.0  # 90%

        # create bot_operation object
        self.bot_operation = BotOperations()

        # create GensimDoc2Vec object
        self.gensim_doc2vec = GensimDoc2Vec()

        # set filters and filter input line
        self.fltr = TextFilter()
        # remove stem filter from all default filters, reason: stem can change the word
        self.fltr.remove_filter(self.fltr.stem_text)

        # create SimilarityModel object
        # self.similarity_model = SimilarityModel()
        # load it when its required, it takes lot of time & memory
        # self.similarity_model.load_google_w2v_model()

    # fetch intents from input sentence
    def fetch_intents(self, filtered_sent):
        filtered_word_list = filtered_sent.split()
        intents = []
        print("Filtered words: ", filtered_word_list)
        pos_tagged_words = nltk.pos_tag(filtered_word_list)
        for tagged_word in pos_tagged_words:
            # append if it is intent(verb) or if it exist in operations or operation-intents
            if re.match(r"VB*", tagged_word[1]) or (tagged_word[0] in self.bot_operation.get_all_operations()) or \
                    self.is_intent_exist(tagged_word[0]):
                intents.append(tagged_word[0])
                '''
                VB	verb, base form	take
                VBD	verb, past tense	took
                VBG	verb, gerund/present participle	taking
                VBN	verb, past participle	taken
                VBP	verb, sing. present, non-3d	take
                VBZ	verb, 3rd person sing. present	takes
                '''
        return intents

    # function to train model (on default sentences) for first time
    def train_model(self):
        # train model
        # filter all sentences of operation_sent_dict
        for opr in self.bot_operation.operation_sent_dict:
            sent_list = self.bot_operation.operation_sent_dict[opr]
            filtered_sent_list = []
            for sent in sent_list:
                filtered_sent_list.append(' '.join(self.fltr.preprocess_string(sent)))

            self.bot_operation.operation_sent_dict[opr] = filtered_sent_list

        # train gensim_word2vec model on some filtered sentences related to default operations
        self.gensim_doc2vec.train_model(self.bot_operation.operation_sent_dict)

        # save default operations_intents dict
        self.bot_operation.save_file(OPERATION_INTENTS_FILE, self.bot_operation.operation_intents_dict)
        # save default, filtered operation_sent_dict
        self.bot_operation.save_file(OPERATION_SENTENCES_FILE, self.bot_operation.operation_sent_dict)
        # save model
        self.gensim_doc2vec.save_model()

    def retrain_model(self):
        operation = input("Enter Operation:(press q for quit)>>> ")
        while operation.lower() != 'q':
            synonyms, antonyms, examples_sentences = self.get_synonyms_antonyms_examples_sentences(operation)
            print("Extracted Intents & sample sentences for operation(you can select intents from it or "
                  "provide your own intents) \n", operation, "\n", set(synonyms), "\n")

            for sent in examples_sentences:
                print(sent)

            intents_list = []
            inpt = input("Enter some intents:(press q for quit)\n>>> ")
            while inpt.lower() != 'q':
                intents_list.append(inpt)
                inpt = input(">>> ")

            sent_list = []
            sent = input("Enter some example sentences:(press q for quit)\n>>> ")
            while sent.lower() != 'q':
                # sentences.append(sent)
                sent = input(">>> ")
                filtered_sent = ' '.join(self.fltr.preprocess_string(sent))
                sent_list.append(filtered_sent)
                # extract intents from sentences
                intents_list += self.fetch_intents(filtered_sent)

            # update opr_sent file & save
            self.bot_operation.update_opr_sentences_dict(operation, sent_list, OPERATION_SENTENCES_FILE)
            # self.bot_operation.operation_sent_dict[operation] = sent_list
            # self.bot_operation.save_file(OPERATION_SENTENCES_FILE, self.bot_operation.operation_sent_dict)

            # add update model & save it
            self.bot_operation.update_opr_intents_dict(operation, intents_list, OPERATION_INTENTS_FILE)
            operation = input("\nEnter Operation:(press q for quit)>>> ")

    def load_model(self):
        # try loading model
        if os.path.exists(BOT_OPERATION_MODEL) and os.path.exists(OPERATION_INTENTS_FILE):
            # load operation_intents map
            self.bot_operation.load_operation_intents_dict(OPERATION_INTENTS_FILE)
            # load gensim_doc2vec model
            self.gensim_doc2vec.load_model()
        else:
            raise ValueError("")

    # check if intent exist in our model (if yes, return operation else return None)
    def is_intent_exist(self, intent):
        for opr in self.bot_operation.get_all_operations():
            if intent in self.bot_operation.get_intents_list(opr):
                return opr

        return None

    def calculate_similarity(self, input_sent_model):
        opr_similarity_map = {}
        # create opr_similarity_map with default similarity 0.0%
        for operation in self.bot_operation.get_all_operations():
            opr_similarity_map[operation] = 0.0

        for operation in opr_similarity_map:
            opr_similarity_map[operation] = input_sent_model.doc_similarity('none', operation)

        return opr_similarity_map

    def get_most_similar_operation(self, opr_similarity_map):
        most_similar_operation = None
        max_val = 0.0

        for operation in opr_similarity_map:
            if opr_similarity_map[operation] > max_val:
                most_similar_operation = operation
                max_val = opr_similarity_map[operation]

        if max_val > self.similarity_score:
            print("similarity score: ", max_val)
            return most_similar_operation
        else:
            return None

    def fetch_operation(self, filtered_sent):
        # extract intents from sentences
        intents = self.fetch_intents(filtered_sent)
        print("Extracted Intents: ", intents)

        # if any of intents contains any operation name/its synonyms, then return that operation directly
        for intent in intents:
            if intent in self.bot_operation.get_all_operations():
                # return operation(in this scenario current intent is operation)
                return intent

            # check intent in operation-intents
            opr = self.is_intent_exist(intent)
            if opr is not None:
                return opr

        # create vector from input sentence
        input_sent_model = GensimDoc2Vec()
        operation_sent_dict = self.bot_operation.operation_sent_dict
        operation_sent_dict['none'] = [filtered_sent]
        # train gensim_word2vec model on input sentence
        # TODO input_sent_model.retrain_model(operation_sent_dict)
        input_sent_model.train_model(operation_sent_dict)

        # TODO add new vector with 'None' operation to trained model and retrain it on that
        # calculate similarity
        opr_similarity_map = self.calculate_similarity(input_sent_model)

        # TODO return best matching operation depending on similarity score & under some threshold,
        # return None, if don't find any operation
        return self.get_most_similar_operation(opr_similarity_map)

    def get_synonyms_antonyms_examples_sentences(self, word):
        synonyms = []
        antonyms = []
        examples_sentences = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
            examples_sentences.append(syn.examples())

        # print("\nSynonyms & antonyms for word ", word)
        # print(set(synonyms))
        # print(set(antonyms))
        return synonyms, antonyms, examples_sentences

    @staticmethod
    def main():
        nlp_engine = NLPEngine()
        # load existing model or train new
        try:
            nlp_engine.load_model()
        except:
            nlp_engine.train_model()

        user_input = input("\nEnter sentence (press q for quit):\n>>> ")
        while user_input.lower() != 'q':
            filtered_word_list = nlp_engine.fltr.preprocess_string(user_input)
            # find best similar operation & call related function
            operation = nlp_engine.fetch_operation(' '.join(filtered_word_list))
            if operation is not None:
                print("Bot Operation: ", operation)
                user_input = input("\n>>> ")
            else:
                print("No operation found, please elaborate it or retrain the model, press 'y' to retrain the model")
                user_input = input("\n>>> ")
                if user_input.lower() == 'y':
                    nlp_engine.retrain_model()
                    user_input = input("\nEnter sentence (press q for quit):\n>>> ")


if __name__ == '__main__':
    NLPEngine.main()
