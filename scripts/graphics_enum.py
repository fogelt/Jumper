from enum import Enum


class Type(Enum):
    SKELETON = ['skele0', 'skele1', 'skele2', 'skele3']
    PLAYER_IDLE = ['playeridle00', 'playeridle01', 'playeridle02']
    PLAYER_WALK_LEFT = ['playerwalkleft0', 'playerwalkleft1', 'playerwalkleft2', 'playerwalkleft3']
    NOMAD = ['nomad']
    TENT = ['tent1']
    PALM = ['palm']
    MAIN_MENU = ['main_menu2']
