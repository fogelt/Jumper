import pickle
import os

def save(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)

def load(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return {}