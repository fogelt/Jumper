import pygame
from glob import glob
import os 
import random

files = [f for f in glob('./sounds/**/*.*', recursive=True)]
dict = {}

for file in files:
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]
    dict[name.lower()] = pygame.mixer.Sound(file)

def play_sound(sound):
    name = sound.value[0]
    dict[name].play()
    
def play_random_sound(sound):
    name = random.choice(sound.value)
    dict[name].play()
