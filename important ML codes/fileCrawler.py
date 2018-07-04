#  -*- coding: utf-8 -*-

import os
from os.path import join, getsize

categories = []

trainingDataPath  = ".\..\LSA(Latent Semantic Analysis)\LSA\\trainingdata"
categoriesList = []
#categoriesList = os.listdir(trainingDataPath)
#fileType = {"*.txt"} #set of file types to crawle

if os.path.exists(trainingDataPath):
    for root, dirs, docs in os.walk(trainingDataPath):
        #print root, dirs, files
        docList = []
        if not len(docs) == 0:
            categoriesList.append(root)
        for doc in docs:
            if doc.endswith('.txt'):
                #print os.path.join(root, file)
                doc = os.path.join(root,doc)
                doc = open(doc,"r")
                docList.append(doc.read())
        categories.append(''.join(docList))
else:
    print("Training Directory not found")


for cat in categories:
    print(cat)
    print("====================================================")

print(len(categories))
print(categoriesList)
'''
for root, dirs, files in os.walk('.\..\LSA(Latent Semantic Analysis)\LSA\data'):
    print root, "consumes",
    print sum(getsize(join(root, name)) for name in files),
    print "bytes in", len(files), "non-directory files"
    if 'CVS' in dirs:
        dirs.remove('CVS')  # don't visit CVS directories




for root, directories, filenames in os.walk('/tmp/'):
     for directory in directories:
             print os.path.join(root, directory)
     for filename in filenames:
             print os.path.join(root,filename)


print os.listdir('/tmp/')

if os.path.exists(path):
    print path

import os
from fnmatch import fnmatch

root = '/some/directory'
pattern = "*.py"

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            print os.path.join(path, name)

'''