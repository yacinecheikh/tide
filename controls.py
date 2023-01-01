#import curses
from curses import COLS, LINES


import styles
import settings

#from color import pair, grey, lightgrey, black, white
#import color as c


# this interface is also implemented by Text
class Control:
    "any graphical element which can be updated over time and rendered on a screen at coordinates (x,y)"
    def update(self, dt):
        pass

    def render(self, display, x, y):
        pass


"""
Window API
Used to split the screen or distinguish areas
"""


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


"""
Core rendering primitives
Nodes are used to make DOM-like structured data rendering
Texts contain formatted string rendering data, and are used to implement graphical descriptions of rendered objects
"""

# can be extended for usage in AST, file navigation menus,...
# inherited control should manage their own indent
class Node(Control):
    """
    Generic purpose Node tree
    (element of an objet oriented linked tree)

    Nodes only manage the indentation of their children
    (they don't have their own rendering)

    To manage style and other properties, go through a node tree to process non-Node children
    """
    def __init__(self, indent = settings.indent):
        # DOM-like tree
        self.parent = None
        # name ideas instead of children
        """
        self.contents = []
        self.items = []
        self.data = []
        """
        self.children = []

        # default setting
        self.indent = indent


    def add(self, child):
        child.parent = self
        self.children.append(child)


    def update(self, dt):
        for item in self.children:
            item.update(dt)


    def render(self, screen, x = 0, y = 0):
        c = 0
        for item in self.children:
            c += item.render(screen, x + self.indent, y + c)
        return c


class Text(Control):
    """
    Kitchen sink, multipart text

    style: common style for all text parts without a dedicated style (can be modified after creation)
    lines: split lines for quick block indenting and/or line iteration

    Lines are renderable objects. Can contain subparts with a dedicated style, and use the parent text style as default

    this format allows both simple, multiline text
    and the usage of complex animated, non-ascii
    or transparent parts
    """


    class Line:
        def __init__(self, *parts):
            #self.style = default_style
            self.contents = []
            for elt in parts:
                self.add(elt)

        def add(self, element):
            # auto-format str to (str, style)
            if isinstance(element, str):
                element = (element, 'default')
            # item is (str, style) or (None, length)
            self.contents.append(element)

        def render(self, screen, x, y, default_style):
            for elt in self.contents:
                text, param = elt
                if text is None:
                    # transparency (blank spaces)
                    x += param
                else:
                    # override default style
                    if param == 'default':
                        style = default_style
                    else:
                        style = param
                    screen.write(x, y, text, style)
                    x += len(text)


    def __init__(self, text: str, style=None):
        self.style = style or styles.default
        # line contents are str, (str, style),
        # or (None, length) for transparent parts


        # TODO(maybe):
        # the constructor only takes a single string
        # could change later
        # for now, Line is internal
        self.lines = []
        for line in text.split('\n'):
            self.lines.append(Line(line))

    def add(self, content, line='append'):
        if line == 'append':
            line = len(self.lines)

        while line >= len(self.lines):
            self.lines.append(Line())

        # content is str, (str, style) or (None, length)
        self.lines[line].add(content)


    def render(self, screen, x, y):
        for line in self.lines:
            line.render(screen, x, y, self.style)
            y += 1


"""

"""


# TODO: rename to Container ?
class Positioned:
    def __init__(self, control, x, y):
        self.content = control

    def render(self, screen):
        self.content.render(screen, x, y)


"""

higher level controls (rely on Node, Text and Window)

"""


class Menu(Node):
    def __init__(self):
        super().__init__(indent=0)

    def add(self, control):
        super().add(control)
    
    def render(self):
        pass



class FileNav:
    pass


class Notification(Control):
    # use a dedicated subwindow to delimit borders
    def __init__(self, window):
        self.window = window
        self.queue = []

    def add(self, control):
        pass



def Notifications(Widget):
    # TODO: when the camera moves, keep the notificatioss on the same spot ?
    # (ex: in a menu on the right
    # requires having a Display which does not fill the screen
    def __init__(self):
        super().__init__(self)
        self.rendering = []
        self.height = 2  # elements
        # cannot predict an element will be too long
        # any element could be 10 lines long and fill the screen
        # 
        self.lines = 3  # max lines before stopping
        self.duration = 3  # seconds

    def add(self, widget):
        self.queue.append({
            'time': 0,
            'element': widget,
        })

    def update(self, dt):
        for x in self.queue[:self.height][::-1]:
            # display the 3 first (lowest) nodes, from the top
            x['time'] += dt
            if x['time'] > 3:
                self.rendering.remove(x)
        # move from queue 
        while len(self.rendering) < 1 and len(self.queue):
            self.rendering.append({
                'time': 0,
                'element': self.queue.pop(0)
            })


    def render(self, screen, x, y):
        # x, y is for custom rendering
        # ignore when None ?
        pass
