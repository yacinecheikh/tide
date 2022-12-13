from curses import LINES, COLS


class Position:
    "generalized position for graphical objects"
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content

    def render(self, screen):
        self.content.render(screen, x, y)




class WindowBase:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def trim(self, x, y, text) -> str:
        if y < 0 or y > self.w:
            return ''
        if x < 0:
            text = text[x:]
            x = 0
        if x + len(text) > self.w:
            text = text[:self.w - len(text) - x]
        return text


class Window(WindowBase):
    "Splittable subwindow. Can be placed with a Position() wrapper"
    def __init__(self, parent, x, y, w, h):
        self.parent = parent
        super().__init__(x, y, w, h)

    def write(self, x, y, text, style=None):
        # TODO: remove checks from parents after confirming subwindows are included in the dimensions of their parent
        # (may reduce perfs later when scaling render calls)
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
        text = self.trim(x, y, text)
        if text:
            if style:
                self.screen.addstr(y, x, text, style)
            else:
                self.screen.addstr(y, x, text)
