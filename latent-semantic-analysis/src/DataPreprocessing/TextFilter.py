#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import string
import glob

from gensim import utils
from gensim.parsing.porter import PorterStemmer
from nltk.corpus import stopwords


class TextFilter(object):
    def __init__(self):

        # self.stopwords = """for a of the and to in"""
        # self.stopwords = frozenset(w for w in self.stopwords.split() if w)
        self.stopwords = set(stopwords.words('english'))

        self.RE_PUNCT = re.compile('([%s])+' % re.escape(string.punctuation), re.UNICODE)
        self.RE_TAGS = re.compile(r"<([^>]+)>", re.UNICODE)
        self.RE_NUMERIC = re.compile(r"[0-9]+", re.UNICODE)

        self.RE_NONALPHA = re.compile(r"\W", re.UNICODE)
        self.RE_WHITESPACE = re.compile(r"(\s)+", re.UNICODE)

        self.RE_AL_NUM = re.compile(r"([a-z]+)([0-9]+)", flags=re.UNICODE)
        self.RE_NUM_AL = re.compile(r"([0-9]+)([a-z]+)", flags=re.UNICODE)

        self.stem = self.stem_text

        self.DEFAULT_FILTERS = [
            lambda x: x.lower(), self.strip_tags, self.strip_punctuation,
            self.strip_multiple_whitespaces, self.strip_numeric,
            self.remove_stopwords, self.strip_short, self.stem_text
        ]

    # ==================== Filters =========================
    def remove_stopwords(self, s):
        s = utils.to_unicode(s)
        return " ".join(w for w in s.split() if w not in self.stopwords)

    # remove all punctuation(,./""; etc)
    def strip_punctuation(self, s):
        s = utils.to_unicode(s)
        return self.RE_PUNCT.sub(" ", s)

    # unicode.translate cannot delete characters like str can
    # strip_punctuation2 = strip_punctuation
    # def strip_punctuation2(s):
    #     s = utils.to_unicode(s)
    #     return s.translate(None, string.punctuation)

    # remove tags
    def strip_tags(self, s):
        s = utils.to_unicode(s)
        return self.RE_TAGS.sub("", s)

    # remove short words
    def strip_short(self, s, minsize=3):
        s = utils.to_unicode(s)
        return " ".join(e for e in s.split() if len(e) >= minsize)

    # remove numeric values (0-9)
    def strip_numeric(self, s):
        s = utils.to_unicode(s)
        return self.RE_NUMERIC.sub("", s)

    # matches any non-alphanumeric character; this is equivalent to the set [^a-zA-Z0-9_]
    def strip_non_alphanum(self, s):
        s = utils.to_unicode(s)
        return self.RE_NONALPHA.sub(" ", s)

    # it matches any whitespace character, this is equivalent to the set [ \t\n\r\f\v]
    def strip_multiple_whitespaces(self, s):
        s = utils.to_unicode(s)
        return self.RE_WHITESPACE.sub(" ", s)

    def split_alphanum(self, s):
        s = utils.to_unicode(s)
        s = self.RE_AL_NUM.sub(r"\1 \2", s)
        return self.RE_NUM_AL.sub(r"\1 \2", s)

    # Return lowercase and (porter-)stemmed version of string `text`.
    def stem_text(self, text):
        text = utils.to_unicode(text)
        p = PorterStemmer()
        return ' '.join(p.stem(word) for word in text.split())
    # =========================================================================

    def set_stopwords(self, stops):
        self.stopwords += stops

    def set_filters(self, filters):
        if len(filters) > 0:
            self.DEFAULT_FILTERS = filters

    def add_filter(self, filter):
        self.DEFAULT_FILTERS.append(filter)

    def remove_filter(self, filter):
        self.DEFAULT_FILTERS.remove(filter)

    def preprocess_string(self, s):
        s = utils.to_unicode(s)
        for f in self.DEFAULT_FILTERS:
            s = f(s)
        return s.split()

    # docs: list of strings
    def preprocess_documents(self, docs):
        return [self.preprocess_string(d) for d in docs]

    def read_file(self, path):
        with utils.smart_open(path) as fin:
            return fin.read()

    def read_files(self, pattern):
        return [self.read_file(fname) for fname in glob.glob(pattern)]

# ob = TextFilter()
# print(ob.stopwords)