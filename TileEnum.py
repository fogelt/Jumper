from enum import Enum

# class syntax
class Type(Enum):
    GRASS = 1000, False
    WATER = 1001, True
    GRASS_BOT = 1002, False
    GRASS_TOP = 1003, False
    GRASS_LEFT = 1004, False
    GRASS_RIGHT = 1005, False
    GRASS_BOTL = 1006, False
    GRASS_BOTR = 1007, False
    GRASS_TOPL = 1008, False
    GRASS_TOPR = 1009, False
    TREE = 1010, True
    GRASS0 = 1011, False
    GRASS1 = 1012, False
    colgrass = 2000, True
