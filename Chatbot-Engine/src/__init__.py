import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

# go to project dir (cwd is src)
head, tail = os.path.split(PROJECT_DIR)
PROJECT_DIR = head

DATA_DIR = PROJECT_DIR + "\\data"
MODEL_DIR = PROJECT_DIR + "\\model"

BOT_OPERATION_MODEL = MODEL_DIR+"\\bot_operation_model.doc2vec"
OPERATION_INTENTS_FILE = MODEL_DIR+"\\operation_intents.xlsx"
OPERATION_SENTENCES_FILE = MODEL_DIR+"\\operation_sentences.xlsx"
