import pickle
from json import dumps

class State(object):

    def __init__(self, path):
        self.path = path
        self.file = open(path, 'rb+wb')
        self.data = {}
        try:
            self.load()
        except EOFError, e:
            pass

    def load(self):
        self.file.seek(0)
        self.data = pickle.load(self.file)

    def save(self):
        self.file.seek(0)
        self.file.truncate()
        pickle.dump(self.data, self.file)

    def dump(self):
        self.load()
        return dumps(self.data)

    def update(self, data):
        for key, value in data.iteritems():
            self.data[key] = value
        self.save()
