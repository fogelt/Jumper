import pygame
from pygame.locals import*

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.display.set_caption("Scorch Survival")

WIDTH, HEIGHT = 1280, 720

_screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
_font = pygame.font.Font(None, 36)
_clock = pygame.time.Clock()


def get_screen():
    return _screen


def get_clock():
    return _clock


def get_font():
    return _font
