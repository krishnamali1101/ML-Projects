import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

# go to project dir (cwd is src)
head, tail = os.path.split(PROJECT_DIR)
PROJECT_DIR = head


DATA_DIR = PROJECT_DIR+"\\trainingData"
MODEL_DIR = PROJECT_DIR+"\\model"

