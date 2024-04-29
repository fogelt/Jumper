import pygame
from glob import glob
import os 

files = [f for f in glob('./Graphics/**/*.png', recursive=True)]
dict = {}

for file in files:
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]
    dict[name.lower()] = pygame.image.load(file).convert_alpha()

def load(name):
    return dict[name]

def loadList(names):
    list = []
    for name in names:
        list.append(dict[name.lower()])
    return list

def loadDict(names):
    d = {}
    for name in names:
        d[name] = dict[name.lower()]
    return d
        