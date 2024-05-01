import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font(None, 36)

WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scorch Survival")
clock = pygame.time.Clock()


def get_screen():
    return screen


def get_clock():
    return clock


def get_font():
    return font
