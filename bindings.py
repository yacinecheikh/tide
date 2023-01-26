from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER

from actions import *


base = {
    'q': quit_app,


    # test forms
    'd': {
        'p': default, # default action
    },

    'dd': default,
}

editor = { **base,
    'ic': insert_comment,
}

scroll = {
    **base,
    KEY_UP: slide_up,
    KEY_DOWN: slide_down,
    KEY_LEFT: slide_left,
    KEY_RIGHT: slide_right,
}

menu = {
    **base,
    KEY_UP: menunav_up,
    KEY_DOWN: menunav_down,
    KEY_ENTER: menunav_select,
}
