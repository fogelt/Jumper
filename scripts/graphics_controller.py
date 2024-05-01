import pygame
from glob import glob
import os 
import scripts.graphics_enum as graphics_enum

files = [f for f in glob('./Graphics/**/*.png', recursive=True)]
dict = {}

for file in files:
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]
    dict[name.lower()] = pygame.image.load(file).convert_alpha()

def load(type: graphics_enum.Type):
    return dict[type.value[0]]

def load_list(type: graphics_enum.Type):
    list = []
    for name in type.value:
        list.append(dict[name.lower()])
    return list

def load_dict(names: []):
    d = {}
    for name in names:
        d[name] = dict[name.lower()]
    return d
        