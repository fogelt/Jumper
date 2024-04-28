import pygame

pygame.mixer.init()

def play():
    pygame.mixer.music.load("Sounds/backgroundmusic.ogg")
    pygame.mixer.music.play(loops=-1)

def pause():
    pygame.mixer.music.stop()