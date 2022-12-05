import curses

#from interpreter import get, define


class Display:
    "virtual infinite screen"
    def __init__(self, screen):
        self.screen = screen
        #self.element = element
        self.cache = []

    def add(self, x, y, text, style = None):
        if style is not None:
            self.cache.append((x, y, text, style))
        else:
            self.cache.append((x, y, text))

    # TODO: deprecate
    def addstr(self, y, x, text, style = None):
        "mock for curses screen"
        call = [x, y, text]
        if style is not None:
            call.append(style)
        self.cache.append(call)

    def reset(self):
        "return rendering calls"
        calls = self.cache
        self.cache = []
        return calls

    #def clear(self):


class Camera:
    "view on display which renders text on screen"
    def __init__(self, display, x = 0, y = 0):
        self.display = display
        self.x = x
        self.y = y


    def move(self, x, y):
        self.x += x
        self.y += y

    def update(self):
        # text outside the screen will not be displayed
        # to move the camera, clear the screen and render everything once again
        screen = self.display.screen
        calls = self.display.reset()

        w = curses.COLS
        h = curses.LINES
        for args in calls:
            # tested for x < 0, x > w, y < 0
            # y > 0 is hard to test on mobile
            x, y, text, *extra = args
            trim_left = self.x - x
            trim_right = (x + len(text)) - (w + self.x)

            if trim_left > 0:
                x += trim_left
                text = text[x:]

            if trim_right > 0:
                text = text[:-trim_right]
            # y can just be checked (ok or not)
            # screen coordinates
            x -= self.x
            y -= self.y
            if y >= 0 and y < h:
                screen.addstr(y, x, text, *extra)

        screen.refresh()




"""
class Screen:
    def __init__(self):
        self.bindings = {}
        define(self.bindings, 't', lambda: print('test'))

    def inline(s):
        pass

    def update(self, key):
        if key is not None:
            self.keys.append(key)
            reset, callback = get(self.bindings, self.keys
"""

