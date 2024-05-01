import pygame

def play():
    pygame.mixer.music.load('Sounds/caravan.ogg.ogg')
    pygame.mixer.music.play(loops=-1)

def pause():
    pygame.mixer.music.stop()