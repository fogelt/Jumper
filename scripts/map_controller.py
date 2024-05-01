import pygame
import csv
import scripts.graphics_controller as graphics_controller
import scripts.tile_enum as tile_enum
import scripts.doodad_enum as doodad_enum


class Tile(pygame.sprite.Sprite):
    spawn_x = 0
    spawn_y = 0
    collision = False

    def __init__(self, _image, _x, _y, _collision):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.spawn_x = _x
        self.spawn_y = _y
        self.collision = _collision

    def pos(self, _x, _y):
        self.rect.x = self.spawn_x - _x
        self.rect.y = self.spawn_y - _y


class Doodad(pygame.sprite.Sprite):
    spawn_x = 0
    spawn_y = 0
    collision = False

    def __init__(self, _image, x, y, _collision, _layer_offset):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.collision = _collision
        self.layer_offset = _layer_offset

    def pos(self, _x, _y):
        self.rect.x = self.spawn_x - _x
        self.rect.y = self.spawn_y - _y

    # 0 = above the player
    # 1 = behind the player
    def render_order(self):
        if self.rect.y > self.layer_offset:
            return 0
        else:
            return 1


tile_list = pygame.sprite.Group()
doodad_list = pygame.sprite.Group()

tile_dict = graphics_controller.load_dict([type_.name.lower() for type_ in tile_enum.Type])
doodad_dict = graphics_controller.load_dict([type_.name.lower() for type_ in doodad_enum.Type])

SQUARE_SIZE = 64

_tile_map = []
with open("data/tile_map.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        # Assuming each row contains numeric data, convert them to integers or floats
        numeric_row = [int(value) for value in row]
        _tile_map.append(numeric_row)

for row_index, row in enumerate(_tile_map):
    for col_index, value in enumerate(row):
        image = None
        collision = None

        for tile in tile_enum.Type:
            if tile.value[0] == value:
                image = tile_dict[tile.name.lower()]
                collision = tile.value[1]

        if image is not None:
            tile = Tile(
                image, col_index * SQUARE_SIZE, row_index * SQUARE_SIZE, collision
            )
            tile_list.add(tile)

doodad_map = []
with open("data/doodad_map.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        # Assuming each row contains numeric data, convert them to integers or floats
        numeric_row = [int(value) for value in row]
        doodad_map.append(numeric_row)

for row_index, row in enumerate(doodad_map):
    for col_index, value in enumerate(row):
        image = None
        layerOffset = None
        collision = None
        for doodad in doodad_enum.Type:
            if doodad.value[0] == value:
                image = doodad_dict[doodad.name.lower()]
                layer_offset = doodad.value[1]
                collision = doodad.value[2]

        if image is not None:
            doodad = Doodad(
                image, col_index * SQUARE_SIZE, row_index * SQUARE_SIZE, collision, layer_offset
            )
            doodad_list.add(doodad)
