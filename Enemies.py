import pygame
import math

class Enemy:
    def __init__(self, rect, target):
        self.rect = rect
        self.target = target
        self.speed = 1

    def move_towards_target(self):
        if self.rect.x < self.target.x:
            self.rect.x += self.speed
        elif self.rect.x > self.target.x:
            self.rect.x -= self.speed

        if self.rect.y < self.target.y:
            self.rect.y += self.speed
        elif self.rect.y > self.target.y:
            self.rect.y -= self.speed

