import pygame
import csv
import Graphics
import TileEnum
import DoodadEnum

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

class Doodad(pygame.sprite.Sprite):
    spawn_x = 0
    spawn_y = 0
    collision = False

    def __init__(self, image, x, y, collision, layerOffset):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.collision = collision
        self.layerOffset = layerOffset

    def pos(self, x, y):
        self.rect.x = self.spawn_x - x
        self.rect.y = self.spawn_y - y

    # 0 = above the player
    # 1 = behind the player
    def render_order(self):
        if self.rect.y > self.layerOffset:
            return 0
        else:
            return 1

tile_list = pygame.sprite.Group()
doodad_list = pygame.sprite.Group()

tile_dict = Graphics.loadDict([type_.name.lower() for type_ in TileEnum.Type])
doodad_dict = Graphics.loadDict([type_.name.lower() for type_ in DoodadEnum.Type])

SQUARE_SIZE = 64

map = []
with open("tileMap.csv", "r") as file:
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

        if image is not None:
            tile = Tile(
                image, col_index * SQUARE_SIZE, row_index * SQUARE_SIZE, collision
            )
            tile_list.add(tile)

doodadMap = []
with open("doodadMap.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        # Assuming each row contains numeric data, convert them to integers or floats
        numeric_row = [int(value) for value in row]
        doodadMap.append(numeric_row)
        
for row_index, row in enumerate(doodadMap):
    for col_index, value in enumerate(row):
        image = None
        layerOffset = None
        collision = None
        for doodad in DoodadEnum.Type:
            if doodad.value[0] == value:
                image = doodad_dict[doodad.name.lower()]
                layerOffset = doodad.value[1]
                collision = doodad.value[2]

        if image is not None:
            doodad = Doodad(
                image, col_index * SQUARE_SIZE, row_index * SQUARE_SIZE, collision, layerOffset
            )
            doodad_list.add(doodad)
