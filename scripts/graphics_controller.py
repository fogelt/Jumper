import pygame
from glob import glob
import os
import scripts.graphics_enum as graphics_enum

_files = [f for f in glob('./Graphics/**/*.png', recursive=True)]
_dict = {}

for file in _files:
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]
    _dict[name.lower()] = pygame.image.load(file).convert_alpha()


def load(_type: graphics_enum.Type):
    return _dict[_type.value[0]]


def load_list(_type: graphics_enum.Type):
    _list = []
    for _name in _type.value:
        _list.append(_dict[_name.lower()])
    return _list


def load_dict(names: []):
    d = {}
    for _name in names:
        d[_name] = _dict[_name.lower()]
    return d
