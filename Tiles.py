import pygame
import csv
import Graphics
import TileEnum


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
tile_dict = Graphics.loadDict([type_.name.lower() for type_ in TileEnum.Type])

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
        image = None
        collision = None

        for tile in TileEnum.Type:
            if tile.value[0] == value:
                image = tile_dict[tile.name.lower()]
                collision = tile.value[1]

        if image is not None and collision is not None:
            tile = Tile(
                image, col_index * SQUARE_SIZE, row_index * SQUARE_SIZE, collision
            )
            tiles.add(tile)
