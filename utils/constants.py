from enum import Enum

INIT_THEME    = 'dark'

COLOR_THEME   = 'dark-blue'

MAIN_FONT     = 'arial black'

COIN_DIAMETER = 60

COLORS        = {
    0 : ('black' , 'white'),
    1 : ('white' , 'black'),
    2 : ('red'   , 'white'),
    3 : ('green' , 'black'),
    4 : ('blue'  , 'white'),
    5 : ('gold'  , 'black')
                }

RANKS         = {
    0 : '#86C6F4',
    1 : '#80EF80',
    2 : '#FFCC31'
                }

class Mode(Enum):
    IDLE         = 0
    GET_COINS    = 1
    GET_CARD     = 2
    RESERVE_CARD = 3
    END_OF_TURN  = 4
    GAME_ENDED   = 5

FACES         = [
    [0, 0, 4, 4, 0],
    [4, 0, 4, 0, 0],
    [3, 0, 3, 3, 0],
    [0, 0, 3, 3, 3],
    [0, 0, 0, 4, 4],
    [0, 3, 0, 3, 3],
    [0, 4, 0, 0, 4],
    [3, 3, 3, 0, 0],
    [4, 4, 0, 0, 0],
    [3, 3, 0, 0, 3]
                ]