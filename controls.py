import styles
import settings


from ui import Window, Control

#from color import pair, grey, lightgrey, black, white
#import color as c


"""
Core rendering primitives
Nodes are used for DOM-like structured data
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
        # w, h rendering
        height = 0
        width = 0
        for item in self.children:
            w, h = item.render(screen, x + self.indent, y + height)
            height += h
            width = max(w, width)
        return width, height
        """ # line-only rendering
        c = 0
        for item in self.children:
            c += item.render(screen, x + self.indent, y + c)
        return c
        """


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

            # width
            return x

    # TODO: constructor styles
    # Text()
    # Text(style = style)
    # Text(multiline)
    # Text((str1, style), (str2, style),...)


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
            self.lines.append(Text.Line(line))

    def add(self, content, line='append'):
        if line == 'append':
            line = len(self.lines)

        while line >= len(self.lines):
            self.lines.append(Text.Line())

        # content is str, (str, style) or (None, length)
        self.lines[line].add(content)


    def render(self, display, x, y):
        width = 0
        height = 0
        for line in self.lines:
            w = line.render(display, x, y, self.style)
            width = max(width, w)
            height += 1
        return width, height


"""

higher level controls (rely on Node, Text and Window)

"""


class ItemList(Node):
    def __init__(self):
        super().__init__(indent = 0)
    

class Menu(ItemList):
    "chosable items"
    def __init__(self):
        super().__init__()
        self.callbacks = []
        self.cursor = 0
        self.cursor_text = Text(' <-')

        self.text = None

    def gentext(self):
        # cursor after first line
        # pb: elements cannot be converted to Text
        # (especially if they change over time)
        pass

    def render(self, screen, x, y):
        # w, h rendering
        height = 0
        width = 0
        for i in range(len(self.children)):
            item = self.children[i]
            w, h = item.render(screen, x + self.indent, y + height)
            if self.cursor == i:
                self.cursor_text.render(screen, x + w + self.indent, y + height)
            height += h
            width = max(w, width)
        return width, height

    def select(self):
        pass
    def up(self):
        pass
    def down(self):
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
