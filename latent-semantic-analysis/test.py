# import numpy as np
#
# S = [0.56914010348699129, 0.5685334517264129, 0.49240595794468056]
# A = np.matrix('1')
# print(A)
# =================================

#  import spacy
# nlp = spacy.load('en')
# =================================

# remove "
# import string
# ignorechars = ''';"'''
# str = '''Anil"kesar?i"ya'''
# new_str = str.replace('"', " ")
# trantab = string.maketrans("", "")
# word = str.lower().translate(trantab, ignorechars)
#
# print new_str
# =================================

# # fill
# t = " k"
# print t.rjust(10,' ')
# #print t
#=================================
ignorechars = ''';"'''
str = '''Anil"kesar;i"ya'''
for c in ignorechars:
    str = str.replace(c, " ")

print(str)