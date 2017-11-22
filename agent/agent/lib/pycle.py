import pickle
from json import dumps
from .exceptions import StateLoadFailed


class State(object):

    def __init__(self, path):
        self.path = path
        try:
            self.file = open(path, 'rb+wb')
        except (OSError, IOError) as e:
            tmp = open(path, 'w').close()
            self.file = open(path, 'rb+wb')
        self.data = {}
        try:
            self.load()
        except EOFError, e:
            self.save()

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

    def get_field(self, key):
        self.load()
        try:
            return self.data[key]
        except KeyError, e:
            return None

    def set_field(self, key, value):
        self.data[key] = value
        self.save()
