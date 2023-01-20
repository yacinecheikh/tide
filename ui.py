from curses import COLS, LINES


"""
Window API
Used to split the screen or distinguish areas


windows automatically render on their parent whatever is rendered on them
(the parent can be another window, or the ncurses screen)
(they are not controls, but they are used to place controls using Boxes)
"""

class WindowBase:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # offset/position
        self.ox = 0
        self.oy = 0

        # hook for auto-resizing
        # with the window and the existing sizes,
        # can compute the new sizes for windows

        # can also store (wdw, x, y) to keep proportions
        self.subwindows = []


    # camera/screen scrolling
    def move(self, x, y):
        self.ox += x
        self.oy += y

    def translate(self, x, y):
        return x - self.ox, y - self.oy


    # silent fail when rendering out of window
    def trim(self, x, y, text) -> str:
        if y < 0 or y > self.w:
            return ''
        if x < 0:
            text = text[x:]
            x = 0
        if x + len(text) > self.w:
            text = text[:self.w - len(text) - x]
        return text

    # hook for auto resizing when the screen size changes
    def resize(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Window(WindowBase):
    "Splittable subwindow. Can be placed with a Position() wrapper"
    def __init__(self, parent, x, y, w, h):
        self.parent = parent
        super().__init__(x, y, w, h)

    def write(self, x, y, text, style=None):
        # TODO: remove checks from parents after confirming subwindows are included in the dimensions of their parent
        # (may reduce perfs later when scaling render calls)
        # as it is, as long as the window is included in its parents, trimming always ensures the written text fits in its parent
        # fix: add write_nocheck()

        x, y = self.translate(x, y)
        text = self.trim(x, y, text)
        if text:
            x += self.x
            y += self.y
            self.parent.write(x, y, text, style)


class ScreenWindow(WindowBase):
    "compatibility layer between curses screen and sub Window API"
    def __init__(self, screen):
        self.screen = screen
        super().__init__(0, 0, COLS, LINES)

    def write(self, x, y, text, style=None):
        x, y = self.translate(x, y)
        text = self.trim(x, y, text)
        if text:
            if style:
                self.screen.addstr(y, x, text, style)
            else:
                self.screen.addstr(y, x, text)



"""
Control Base API

Controls can be rendered on displays (windows) and updated over time
Box(control, display, x, y) allows passive management by the Activity

"""
class Control:
    def render(self, display, x, y):
        pass

    def update(self, dt):
        pass


class Box:
    def __init__(self, display, x, y, control):
        # avoid using __setattr__ before attributes exist
        # oher solutions: https://stackoverflow.com/questions/17020115/how-to-use-setattr-correctly-avoiding-infinite-recursion
        self.__dict__['content'] = control
        self.__dict__['display'] = display
        self.__dict__['x'] = x
        self.__dict__['y'] = y

    def update(self, dt):
        self.content.update(dt)

    def render(self):
        self.content.render(self.display, self.x, self.y)


    # TODO: test
    # used for easier scripting API
    # redirect properties to the boxed Control

    def __getattr__(self, key):
        if key in self.__dict__:
            return super().__getattr__(key)
        return self.content.__getattr__(key)

    def __setattr__(self, key, val):
        # TODO: see if Box init constructor is redirected too
        if key in self.__dict__:
            return super().__setattr__(key, val)
        return self.content.__setattr__(key, val)

