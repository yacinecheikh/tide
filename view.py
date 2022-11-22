import curses

#from interpreter import get, define


class Display:
    def __init__(self, screen):
        self.screen = screen
        self.cache = []

    # TODO: change api use in ast.py

    def add(self, x, y, text, style = None):
        pass

    def addstr(self, y, x, text, style = None):
        call = [x, y, text]
        if style is not None:
            call.append(style)
        self.cache.append(call)

    def update(self):
        calls = self.cache
        self.cache = []
        return self.screen, calls


class Camera:
    def __init__(self, display, x = 0, y = 0):
        self.display = display
        self.x = x
        self.y = y


    def move(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        # text outside the screen will not be displayed
        # to move the camera, clear the screen and render everything once again
        screen, calls = self.display.update()
        w = curses.COLS
        h = curses.LINES
        for args in calls:
            x, y, text, *extra = args
            trim_left = self.x - x
            # TODO: test both left and right
            # TODO: convert x,y to absolute positions
            # instead of using x - camera.x
            if trim_left > 0:
                text = text[trim_left:]
            trim_right = x + len(text) - w
            if trim_right > 0:
                text = text[:-1-trim_right]
            # y can just be checked (ok or not)
            # multiline is done with multiple calls
            if y >= self.y and y < h:
                screen.addstr(y - self.y, x - self.x, text, *extra)




"""
class Editor:
    def __init__(self):
        pass



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

