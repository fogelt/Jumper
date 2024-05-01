import pygame
from glob import glob
import os
import random

files = [f for f in glob('./sounds/**/*.*', recursive=True)]
_dict = {}

for file in files:
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]
    _dict[name.lower()] = pygame.mixer.Sound(file)


def play_sound(sound):
    _name = sound.value[0]
    _dict[_name].play()


def play_random_sound(sound):
    _name = random.choice(sound.value)
    _dict[_name].play()
