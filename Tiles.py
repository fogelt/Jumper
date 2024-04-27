import pygame
import csv
import Graphics

class Tile(pygame.sprite.Sprite):
    spawn_x = 0
    spawn_y = 0
    collision = False
    def __init__(self, image, x, y, collision):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.collision = collision

    def pos(self, x, y):
        self.rect.x = self.spawn_x - x
        self.rect.y = self.spawn_y - y


tiles = pygame.sprite.Group()
grass_image = Graphics.load("grass")
water_image = pygame.image.load("Graphics/water.png")
grass_bot = pygame.image.load("Graphics/grass_bot.png")
grass_top = pygame.image.load("Graphics/grass_top.png")
grass_left = pygame.image.load("Graphics/grass_left.png")
grass_right = pygame.image.load("Graphics/grass_right.png")
grass_botl = pygame.image.load("Graphics/grass_botl.png")
grass_botr = pygame.image.load("Graphics/grass_botr.png")
grass_topl = pygame.image.load("Graphics/grass_topl.png")
grass_topr = pygame.image.load("Graphics/grass_topr.png")
tree = pygame.image.load("Graphics/tree.png")



SQUARE_SIZE = 64 

map = []
with open("map.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        # Assuming each row contains numeric data, convert them to integers or floats
        numeric_row = [int(value) for value in row]
        map.append(numeric_row)

for row_index, row in enumerate(map):
    for col_index, value in enumerate(row):
        if value == 1000:
            image = grass_image
            collision = False
        elif value == 1001:
            image = water_image
            collision = True
        elif value == 1002:
            image = grass_bot
            collision = False
        elif value == 1003:
            image = grass_top
            collision = False
        elif value == 1004:
            image = grass_left
            collision = False
        elif value == 1005:
            image = grass_right
            collision = False
        elif value == 1006:
            image = grass_botl
            collision = False
        elif value == 1007:
            image = grass_botr
            collision = False
        elif value == 1008:
            image = grass_topl
            collision = False
        elif value == 1009:
            image = grass_topr
            collision = False
        elif value == 1010:
            image = tree
            collision = False

        tile = Tile(image, col_index * SQUARE_SIZE, row_index * SQUARE_SIZE, collision)
        tiles.add(tile)
