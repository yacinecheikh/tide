import curses


next_color = 0
max_color = curses.COLORS  # 256 on termux
def color(r, g, b):
    global next_color
    i = next_color
    curses.init_color(i, r, g, b)
    next_color += 1
    return i

next_pair = 1
max_pair = curses.COLOR_PAIRS  # 65k or termux
def pair(text, bg):
    global next_pair
    i = next_pair
    curses.init_pair(i, text, bg)
    next_pair += 1
    return curses.color_pair(i)  # no need for index anyway

"""
default colors:
black
blue
cyan
green
magenta
red
white
yellow
"""
black = color(0, 0, 0)
blue = color(0, 0, 1000)
red = color(1000, 0, 0)
green = color(0, 1000, 0)
white = color(1000, 1000, 1000)
grey = color(500, 500, 500)
lightgrey = color(200, 200, 200)
