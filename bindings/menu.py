from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER

from actions import *

bindings = {
    KEY_UP: menunav_up,
    KEY_DOWN: menunav_down,
    '\n': menunav_select,
}

