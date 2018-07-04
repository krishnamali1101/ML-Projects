from src.DataPreprocessing import read_writeXLFile as xl


class BotOperations(object):
    def __init__(self):
        # default operations
        self.operation_intents_dict = {'create': ['produce', 'make', 'create'],
                                       'update': ['update', 'modify', 'change', 'edit'],
                                       'delete': ['erase', 'cancel', 'delete', 'remove'],
                                       'deploy': ['deploy']
                                       }

        self.operation_sent_dict = {'create': ['i want to create new bot.',
                                               'may i have new bot.',
                                               'make a new bot',
                                               'produce a new bot',
                                               'i want a new bot.'],
                                    'update': ['update bot',
                                               'update this bot',
                                               'change bot name',
                                               'change bot id.',
                                               'modify bot name',
                                               'can you modify bot name',
                                               'edit bot information',
                                               'update bot information'],
                                    'delete': ['erase all existing data',
                                               'delete my bot',
                                               'i want to delete this bot',
                                               'can you delete this bot',
                                               'remove this bot'],
                                    'deploy': ['deploy my bot',
                                               'i want to deploy this bot',
                                               'how can i deploy this bot']
                                    }

    # load operation_intents_dict
    def load_operation_intents_dict(self, filename):
        operations = xl.read_xl(filename)
        if len(operations) > 0:
            self.operation_intents_dict = operations

    def save_file(self, filename, dict):
        xl.write_xl(filename, dict)

    # operation & list of intents to add in existing operation
    def update_opr_intents_dict(self, operation, intents, filename):
        if operation in self.operation_intents_dict:
            # update existing operation intents
            self.operation_intents_dict[operation] += intents
        else:
            # add new operation
            self.operation_intents_dict[operation] = intents

        self.save_file(filename, self.operation_intents_dict)

    # operation & list of intents to add in existing operation
    def update_opr_sentences_dict(self, operation, sentences, filename):
        if operation in self.operation_sent_dict:
            # update existing operation sentences
            self.operation_intents_dict[operation] += sentences
        else:
            # add new operation
            self.operation_intents_dict[operation] = sentences

        self.save_file(filename, self.operation_sent_dict)

    def get_all_operations(self):
        return self.operation_intents_dict.keys()

    # def intents_list of any operations
    def get_intents_list(self, operation):
        return self.operation_intents_dict[operation]

    '''
    Synonyms & antonyms for word  create
    {'produce', 'make', 'create'}
    set()

    Synonyms & antonyms for word  update
    {'update'}
    set()

    Synonyms & antonyms for word  delete
    {'erase', 'blue-pencil', 'cancel', 'edit', 'delete'}
    {'record'}

    Synonyms & antonyms for word  deploy
    {'deploy'}
    set()

    Synonyms & antonyms for word  train
    {'take_aim', 'aim', 'take', 'direct', 'civilise', 'condition', 'discipline', 'trail', 'gear', 
    'train', 'develop', 'railroad_train', 'rail', 'coach', 'caravan', 'civilize', 'school', 'educate', 
    'string', 'power_train', 'geartrain', 'check', 'cultivate', 'gearing', 'groom', 'prepare', 'wagon_train'}
    set()
    '''

