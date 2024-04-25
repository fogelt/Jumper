import pygame
from glob import glob
import os 

files = [f for f in glob('./Graphics/**/*.png', recursive=True)]
dict = {}

for file in files:
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]
    dict[name] = file

def load(name):
    return pygame.image.load(dict[name]).convert_alpha()

def loadList(names):
    list = []
    for name in names:
        list.append(pygame.image.load(dict[name]).convert_alpha())
    return list
        